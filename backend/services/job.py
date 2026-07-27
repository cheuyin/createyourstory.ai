import uuid
from datetime import datetime

from sqlmodel import Session, select

from core.image_generator import ImageGenerator
from core.prompts import generate_story_image_prompt
from db.database import engine
from exceptions.exceptions import (
    ImageGenerationException,
    JobNotFoundError,
    StoryGenerationError,
    StoryNotFoundError,
)
from models.auth import User
from models.job import ImageJob, ImageJobPublic, StoryJob, StoryJobPublic
from models.story import Story

IMAGE_MODEL = "gemini-3.1-flash-image"


def create_image_job_for_story_job(db: Session, job: StoryJob) -> str:
    assert job.story_id
    image_job_id = str(uuid.uuid4())
    image_job = ImageJob(
        story_id=job.story_id,
        job_id=image_job_id,
        image_model=IMAGE_MODEL,
        theme=job.theme,
        status="processing",
        user_id=job.user_id,
    )
    job.image_job_id = image_job_id
    db.add(image_job)
    return image_job_id


def get_story_job_status(db: Session, job_id: str) -> StoryJobPublic:
    statement = select(StoryJob).where(StoryJob.job_id == job_id)
    job = db.exec(statement).first()
    if not job:
        raise JobNotFoundError()
    if job.status == "failed":
        raise StoryGenerationError(
            message=job.error or "Error occured during story generation")

    user = db.get(User, job.user_id) if job.user_id else None

    return StoryJobPublic(
        job_id=job.job_id,
        username=user.username if user else None,
        ai_model=job.ai_model,
        status=job.status,
        image_job_id=job.image_job_id,
        created_at=job.created_at,
        story_id=job.story_id,
        completed_at=job.completed_at,
        error=job.error,
    )


def get_image_job_status(db: Session, job_id: str) -> ImageJobPublic:
    statement = select(ImageJob).where(ImageJob.job_id == job_id)
    job = db.exec(statement).first()
    if not job:
        raise JobNotFoundError(message="Image job not found")
    if job.status == "failed":
        raise ImageGenerationException(
            message=job.error or "Something went wrong during image generation")
    user = db.get(User, job.user_id) if job.user_id else None
    return ImageJobPublic(
        job_id=job_id,
        theme=job.theme,
        status=job.status,
        image_model=job.image_model,
        story_id=job.story_id,
        error=job.error,
        username=user.username if user else None,
        created_at=job.created_at,
        completed_at=job.completed_at,
    )


def run_image_generation(job_id: str) -> None:
    with Session(engine) as db:
        statement = select(ImageJob).where(ImageJob.job_id == job_id)
        image_job = db.exec(statement).first()
        if not image_job:
            raise JobNotFoundError(
                message=f"Image job with ID {job_id} not found")
        story = db.get(Story, image_job.story_id)
        if not story:
            raise StoryNotFoundError()
        try:
            prompt = generate_story_image_prompt(story)
            image_data = ImageGenerator.generate_image(prompt)
            story.image_base_64 = image_data
            story.image_job = image_job
            image_job.status = "completed"
            image_job.completed_at = datetime.now()
        except ImageGenerationException as e:
            image_job.status = "failed"
            image_job.error = e.message
            image_job.completed_at = datetime.now()
        except Exception as e:
            image_job.status = "failed"
            image_job.error = str(e)
            image_job.completed_at = datetime.now()

        db.commit()
