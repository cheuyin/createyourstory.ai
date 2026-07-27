import json
import uuid
from datetime import datetime

from sqlmodel import Session, select

from core.story_generator import StoryGenerator
from db.database import engine
from exceptions.exceptions import (
    AuthorizationError,
    StoryNotFoundError,
    StoryRootNotFoundError,
    UnsupportedAIModelError,
)
from models.auth import User
from models.job import StoryJob, StoryJobPublic
from models.story import (
    CompleteStoryNodePublic,
    CompleteStoryPublic,
    Story,
    StoryCreate,
    StoryNode,
)

VALID_AI_MODELS = [
    "google/gemini-3.5-flash",
    "google/gemini-3.1-pro-preview",
    "google/gemini-3.1-flash-lite",
    "google/gemini-2.5-flash",
    "google/gemini-2.5-pro",
    "anthropic/claude-sonnet-4.5",
    "x-ai/grok-4.5",
]


def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryPublic:
    statement = select(StoryNode).where(StoryNode.story_id == story.id)
    nodes = db.exec(statement).all()
    node_map = {}
    for node in nodes:
        assert node.id
        node_response = CompleteStoryNodePublic(
            id=node.id,
            content=node.content,
            is_ending=node.is_ending,
            is_winning_ending=node.is_winning_ending,
            options=json.loads(
                node.options_raw_json_str) if node.options_raw_json_str else [])
        node_map[node.id] = node_response
    root_node = next((node for node in nodes if node.is_root), None)
    if not root_node:
        raise StoryRootNotFoundError()
    assert story.id
    user_query = select(User).where(User.id == story.user_id)
    user = db.exec(user_query).first()
    return CompleteStoryPublic(
        id=story.id,
        title=story.title,
        session_id=story.session_id,
        root_node=node_map[root_node.id],
        ai_model=story.ai_model,
        all_nodes=node_map,
        num_endings=story.num_endings or -1,
        num_winning_endings=story.num_winning_endings or -1,
        num_words=story.num_words or -1,
        created_at=story.created_at,
        image_job_id=story.image_job.job_id if story.image_job else None,
        image_base_64=story.image_base_64,
        username=user.username if user else None,
    )


def generate_story_stats(story: Story) -> None:
    total_words = 0
    for node in story.nodes:
        total_words += len(node.content.split())
    story.num_words = total_words

    num_endings = 0
    num_winning_endings = 0

    for node in story.nodes:
        if node.is_ending:
            num_endings += 1
        if node.is_winning_ending:
            num_winning_endings += 1

    story.num_endings = num_endings
    story.num_winning_endings = num_winning_endings


def _get_story_by_id(db: Session, story_id: int) -> Story:
    story = db.exec(select(Story).where(Story.id == story_id)).first()
    if not story:
        raise StoryNotFoundError()
    return story


def get_story(db: Session, story_id: int, user: User | None) -> CompleteStoryPublic:
    story = _get_story_by_id(db, story_id)
    if story.user_id is not None:
        if not user:
            raise AuthorizationError(
                message="You cannot view other users' stories as a guest")
        if story.user_id != user.id:
            raise AuthorizationError(
                message="You are not authorized to view this story")
    return build_complete_story_tree(db, story)


def list_stories(db: Session, user: User) -> list[CompleteStoryPublic]:
    stories = db.exec(select(Story).where(Story.user_id == user.id)).all()
    return [build_complete_story_tree(db, story) for story in stories]


def delete_story(db: Session, story_id: int, user: User) -> None:
    story = _get_story_by_id(db, story_id)
    if story.user_id != user.id:
        raise AuthorizationError(
            message="You cannot delete stories you did not create")
    db.delete(story)
    db.commit()


def create_story_job(
    db: Session,
    request: StoryCreate,
    user: User | None,
    session_id: str,
) -> tuple[StoryJobPublic, int]:
    if request.ai_model not in VALID_AI_MODELS:
        raise UnsupportedAIModelError()

    job_id = str(uuid.uuid4())
    job = StoryJob(
        job_id=job_id,
        session_id=session_id,
        ai_model=request.ai_model,
        theme=request.theme,
        status="pending",
        user_id=user.id if user else None,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    assert job.id

    job_public = StoryJobPublic(
        story_id=None,
        job_id=job_id,
        username=user.username if user else None,
        status="pending",
        created_at=job.created_at,
        completed_at=None,
        ai_model=request.ai_model,
        error=None,
    )
    return job_public, job.id


def run_story_generation(job_id: int) -> None:
    with Session(engine) as db:
        job = None
        try:
            job = db.get(StoryJob, job_id)
            assert job
            job.status = "processing"
            db.commit()
            db.refresh(job)
            story = StoryGenerator.generate_story(
                db,
                job.session_id,
                job.ai_model,
                user_id=job.user_id if job.user_id else None,
                theme=job.theme,
            )
            job.story_id = story.id
            generate_story_stats(story)
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()
        except Exception as e:
            if job:
                job.status = "failed"
                job.completed_at = datetime.now()
                job.error = str(e)
                db.commit()
