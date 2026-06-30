from typing import Annotated
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, Cookie, Response, BackgroundTasks
from sqlmodel import Session, select
import json

from exceptions.exceptions import CreateYourStoryError, JobNotFoundError, StoryNotFoundError, StoryResponseValidationError, StoryRootNotFoundError
from models.story import CompleteStoryNodePublic, Story, StoryNode, StoryCreate, CompleteStoryPublic
from models.job import StoryJob, StoryJobPublic
from db.database import get_db
from core.story_generator import StoryGenerator

router = APIRouter(
    prefix="/stories",
    tags=["stories"]
)

SessionDep = Annotated[Session, Depends(get_db)]


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
    session_id: str = Depends(get_session_id),
):
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    job_id = str(uuid.uuid4())

    job = StoryJob(job_id=job_id, session_id=session_id,
                   theme=request.theme, status="pending")

    db.add(job)
    db.commit()

    background_tasks.add_task(
        generate_story_task,
        job_id,
        request.theme,
        session_id
    )

    return job


def generate_story_task(job_id: str, theme: str, session_id: str):
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
            db, session_id, theme=theme)
        job.story_id = story.id
        job.status = "completed"
        job.completed_at = datetime.now()
        db.commit()
    except CreateYourStoryError as e:
        job.status = "failed"
        job.completed_at = datetime.now()
        job.error = str(e)
        db.commit()


@router.get("/{story_id}/complete", response_model=CompleteStoryPublic)
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
    return CompleteStoryPublic(
        id=story.id,
        title=story.title,
        session_id=story.session_id,
        root_node=node_map[root_node.id],
        all_nodes=node_map,
        created_at=story.created_at
    )
