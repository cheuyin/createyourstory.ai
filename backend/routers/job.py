from fastapi import APIRouter, Depends
from models.auth import User
from models.job import StoryJobPublic, StoryJob
from sqlmodel import Session, select
from db.database import get_db
from exceptions.exceptions import *

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)


@router.get("/stories/{job_id}", response_model=StoryJobPublic)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    statement = select(StoryJob).where(StoryJob.job_id == job_id)
    job = db.exec(statement).first()
    if not job:
        raise JobNotFoundError()
    if job.status == "failed":
        raise StoryGenerationError()
    user = db.exec(statement=select(User).where(
        User.id == job.user_id)).first()
    job_public = StoryJobPublic(
        job_id=job.job_id,
        username=user.username if user else None,
        ai_model=job.ai_model,
        status=job.status,
        created_at=job.created_at,
        story_id=job.story_id,
        completed_at=job.completed_at,
        error=job.error
    )
    return job_public


@router.get("/images/{job_id}")
def get_image_job_status(job_id: str, db: Session = Depends(get_db)):
    pass
