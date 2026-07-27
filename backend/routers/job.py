from fastapi import APIRouter, BackgroundTasks

from db.database import SessionDep
from models.job import ImageJobPublic, StoryJobPublic
from services import job as job_service

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)


@router.get("/stories/{job_id}", response_model=StoryJobPublic)
def get_job_status(job_id: str, background_tasks: BackgroundTasks, db: SessionDep):
    job_public, image_job_id = job_service.get_story_job_status(db, job_id)
    if image_job_id:
        background_tasks.add_task(job_service.run_image_generation, image_job_id)
    return job_public


@router.get("/images/{job_id}", response_model=ImageJobPublic)
def get_image_job_status(job_id: str, db: SessionDep):
    return job_service.get_image_job_status(db, job_id)
