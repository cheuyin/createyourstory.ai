from fastapi import APIRouter, Depends, HTTPException
from models.job import StoryJobPublic, StoryJob
from sqlmodel import Session, select
from db.database import get_db
from exceptions.exceptions import *

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)


@router.get("/{job_id}", response_model=StoryJobPublic)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    statement = select(StoryJob).where(StoryJob.job_id == job_id)
    job = db.exec(statement).first()
    if not job:
        raise JobNotFoundError()
    if job.status == "failed":
        raise StoryGenerationError()
    return job
