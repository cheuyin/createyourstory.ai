from fastapi import APIRouter

from db.database import SessionDep
from models.job import ImageJobPublic, StoryJobPublic
from services import job as job_service

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)


@router.get("/stories/{job_id}", response_model=StoryJobPublic)
def get_job_status(job_id: str, db: SessionDep):
    return job_service.get_story_job_status(db, job_id)


@router.get("/images/{job_id}", response_model=ImageJobPublic)
def get_image_job_status(job_id: str, db: SessionDep):
    return job_service.get_image_job_status(db, job_id)
