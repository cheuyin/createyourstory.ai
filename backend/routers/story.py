from typing import Annotated
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, Cookie, Response, BackgroundTasks, status
from sqlmodel import Session, select
import json

from routers.auth import get_user_from_token
from models.auth import User
from core.image_generator import generate_image
from exceptions.exceptions import *
from models.story import CompleteStoryNodePublic, Story, StoryNode, StoryCreate, CompleteStoryPublic
from models.job import StoryJob, StoryJobPublic
from db.database import get_db
from core.story_generator import StoryGenerator

router = APIRouter(
    prefix="/stories",
    tags=["stories"]
)

SessionDep = Annotated[Session, Depends(get_db)]

VALID_AI_MODELS = [
    "gemini-3.5-flash",
    "gemini-3.1-pro-preview",
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-pro"
]


def get_session_id(session_id: str | None = Cookie(None)):
    if session_id is None:
        session_id = str(uuid.uuid4())
    return str(session_id)


@router.post("/create", response_model=StoryJobPublic)
def create_story(
    request: StoryCreate,
    background_tasks: BackgroundTasks,
    response: Response,
    db: SessionDep,
    user: User = Depends(get_user_from_token),
    session_id: str = Depends(get_session_id),
):
    assert user.id

    if request.ai_model not in VALID_AI_MODELS:
        raise UnsupportedAIModelError()

    response.set_cookie(key="session_id", value=session_id, httponly=True)
    job_id = str(uuid.uuid4())

    job = StoryJob(job_id=job_id, session_id=session_id,
                   theme=request.theme, status="pending", user_id=user.id)

    db.add(job)
    db.commit()
    db.refresh(job)

    background_tasks.add_task(
        generate_story_task,
        job_id,
        request.theme,
        session_id,
        request.ai_model,
        user.id
    )

    job_public = StoryJobPublic(
        story_id=None,
        job_id=job_id,
        username=user.username,
        status="pending",
        created_at=job.created_at,
        completed_at=None,
        error=None
    )

    return job_public


@router.delete("/{story_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_story(story_id: int, db: SessionDep, user: Annotated[User, Depends(get_user_from_token)]):
    statement = select(Story).where(Story.id == story_id)
    story = db.exec(statement).first()
    if not story:
        raise StoryNotFoundError()
    if story.user_id != user.id:
        raise AuthorizationError(
            message="You cannot delete stories you did not create")
    db.delete(story)
    db.commit()
    return


def generate_story_task(job_id: str, theme: str, session_id: str, ai_model: str, user_id: int):
    db = next(get_db())
    statement = select(StoryJob).where(StoryJob.job_id == job_id)
    results = db.exec(statement)
    job = results.first()
    if not job:
        raise JobNotFoundError()
    try:
        job.status = "processing"
        db.commit()
        story = StoryGenerator.generate_story(
            db, session_id,  ai_model, user_id=user_id, theme=theme)
        job.story_id = story.id
        generate_story_stats(story)
        job.status = "completed"
        job.completed_at = datetime.now()
        db.commit()
        db.refresh(story)
        generate_image_task(story, db)
    except CreateYourStoryError as e:
        story = None
        job.status = "failed"
        job.completed_at = datetime.now()
        job.error = str(e)
        db.commit()


def generate_image_task(story: Story, db: Session):
    generate_image(story)
    db.commit()


@router.get("/{story_id}", response_model=CompleteStoryPublic)
def get_complete_story(story_id: int, db: SessionDep):
    statement = select(Story).where(Story.id == story_id)
    story = db.exec(statement).first()
    if not story:
        raise StoryNotFoundError()
    complete_story = build_complete_story_tree(db, story=story)
    return complete_story


@router.get("/", response_model=list[CompleteStoryPublic])
def get_all_stories(db: SessionDep):
    query = select(Story)
    stories = db.exec(statement=query).all()

    def func(story: Story):
        return build_complete_story_tree(db, story)

    stories = map(func, stories)
    return stories


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
    assert user
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
        image_base_64=story.image_base_64,
        username=user.username
    )


def generate_story_stats(story: Story):
    # 1. Calculate and save total word count
    total_words = 0
    for node in story.nodes:
        total_words += len(node.content.split())
    story.num_words = total_words

    num_endings = 0
    num_winning_endings = 0

    # 2. Calculate number of endings and winning endings
    for node in story.nodes:
        if node.is_ending:
            num_endings += 1
        if node.is_winning_ending:
            num_winning_endings += 1

    story.num_endings = num_endings
    story.num_winning_endings = num_winning_endings
