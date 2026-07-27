from typing import Annotated
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, Cookie, Response, BackgroundTasks, status
from sqlmodel import Session, select

from dependencies.auth import get_user_from_token, get_optional_user_from_token
from models.auth import User
from exceptions.exceptions import *
from models.story import Story, StoryCreate, CompleteStoryPublic
from models.job import StoryJob, StoryJobPublic
from db.database import SessionDep, engine
from core.story_generator import StoryGenerator
from services.story import (
    VALID_AI_MODELS,
    build_complete_story_tree,
    generate_story_stats,
)

router = APIRouter(
    prefix="/stories",
    tags=["stories"]
)


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
    user: User | None = Depends(get_optional_user_from_token),
    session_id: str = Depends(get_session_id),
):
    if request.ai_model not in VALID_AI_MODELS:
        raise UnsupportedAIModelError()

    response.set_cookie(key="session_id", value=session_id, httponly=True)
    job_id = str(uuid.uuid4())

    job = StoryJob(job_id=job_id, session_id=session_id, ai_model=request.ai_model,
                   theme=request.theme, status="pending", user_id=user.id if user else None)

    db.add(job)
    db.commit()
    db.refresh(job)

    assert job.id

    background_tasks.add_task(
        generate_story_task,
        job.id
    )

    job_public = StoryJobPublic(
        story_id=None,
        job_id=job_id,
        username=user.username if user else None,
        status="pending",
        created_at=job.created_at,
        completed_at=None,
        ai_model=request.ai_model,
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


def generate_story_task(job_id: int):
    with Session(engine) as db:
        job = None
        try:
            job = db.get(StoryJob, job_id)
            assert job
            job.status = "processing"
            db.commit()
            db.refresh(job)
            story = StoryGenerator.generate_story(
                db, job.session_id,  job.ai_model, user_id=job.user_id if job.user_id else None, theme=job.theme)
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


@router.get("/{story_id}", response_model=CompleteStoryPublic)
def get_complete_story(story_id: int, db: SessionDep, user: Annotated[User | None, Depends(get_optional_user_from_token)]):
    statement = select(Story).where(Story.id == story_id)
    story = db.exec(statement).first()
    if not story:
        raise StoryNotFoundError()
    if story.user_id is not None:
        if not user:
            raise AuthorizationError(
                message="You cannot view other users' stories as a guest")
        if story.user_id != user.id:
            raise AuthorizationError(
                message="You are not authorized to view this story")
    return build_complete_story_tree(db, story=story)


@router.get("", response_model=list[CompleteStoryPublic])
def get_all_stories(db: SessionDep, user: Annotated[User, Depends(get_user_from_token)]):
    query = select(Story).where(Story.user_id == user.id)
    stories = db.exec(statement=query).all()
    return [build_complete_story_tree(db, story) for story in stories]
