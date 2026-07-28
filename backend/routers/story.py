from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, Cookie, Response, BackgroundTasks, status

from dependencies.auth import get_user_from_token, get_optional_user_from_token
from models.auth import User
from models.story import StoryCreate, CompleteStoryPublic
from models.job import StoryJobPublic
from db.database import SessionDep
from services import story as story_service

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
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    job_public, job_db_id = story_service.create_story_job(
        db, request, user, session_id)
    background_tasks.add_task(story_service.run_story_generation, job_db_id)
    return job_public


@router.delete("/{story_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_story(story_id: int, db: SessionDep, user: Annotated[User, Depends(get_user_from_token)]):
    story_service.delete_story(db, story_id, user)


@router.get("/{story_id}", response_model=CompleteStoryPublic)
def get_complete_story(story_id: int, db: SessionDep, user: Annotated[User | None, Depends(get_optional_user_from_token)]):
    return story_service.get_story(db, story_id, user)


@router.get("", response_model=list[CompleteStoryPublic])
def get_all_stories(db: SessionDep, user: Annotated[User, Depends(get_user_from_token)]):
    return story_service.list_stories(db, user)
