import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlmodel import Session, select

from models.story import Story, StoryNode, StoryCreate, CompleteStoryPublic
from models.job import StoryJob, StoryJobPublic
from db.database import get_db

router = APIRouter(
    prefix="/stories",
    tags=["stories"]
)


def get_session_id(session_id: str | None = Cookie(None)):
    if session_id is None:
        session_id = str(uuid.uuid4())
    return session_id


@router.post("/create", response_model=StoryJobPublic)
def create_story(
    request: StoryCreate,
    background_tasks: BackgroundTasks,
    response: Response,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    job_id = str(uuid.uuid4())

    # TODO: add background tasks to generate a story

    job = StoryJob(job_id=job_id, session_id=session_id,
                   theme=request.theme, status="pending")

    db.add(job)
    db.commit()

    return job


def generate_story_task(job_id: str, theme: str, session_id: str, db: Session = Depends(get_db)):
    statement = select(StoryJob).where(StoryJob.job_id == job_id)
    results = db.exec(statement)
    job = results.first()
    if not job:
        return
    try:
        job.status = "processing"
        db.commit()
        story = {}  # TODO: Generate story
        job.story_id = 1  # TODO: update story ID
        job.status = "completed"
        job.completed_at = datetime.now()
        db.commit()
    except Exception as e:
        job.status = "failed"
        job.completed_at = datetime.now()
        job.error = str(e)
        db.commit()


@router.get("/{story_id}/complete", response_model=CompleteStoryPublic)
def get_complete_story(story_id: int, db: Session = Depends(get_db)):
    statement = select(Story).where(Story.id == story_id)
    story = db.exec(statement).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    complete_story = build_complete_story_tree(db, story=story)
    return complete_story


def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryPublic:
    pass
