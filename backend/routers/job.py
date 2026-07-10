from datetime import datetime

from models.story import Story
from core.prompts import generate_story_image_prompt
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi import BackgroundTasks
import uuid

from fastapi import APIRouter
from models.auth import User
from models.job import ImageJob, ImageJobPublic, StoryJobPublic, StoryJob
from sqlmodel import select, Session
from db.database import SessionDep, engine
from exceptions.exceptions import *

load_dotenv()

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)


@router.get("/stories/{job_id}", response_model=StoryJobPublic)
def get_job_status(job_id: str, background_tasks: BackgroundTasks, db: SessionDep):
    statement = select(StoryJob).where(StoryJob.job_id == job_id)
    job = db.exec(statement).first()
    if not job:
        raise JobNotFoundError()
    if job.status == "failed":
        raise StoryGenerationError()
    user = db.get(User, job.user_id)

    image_job_id = None
    if job.status == "completed":
        image_job_id = str(uuid.uuid4())
        assert job.story_id
        image_job = ImageJob(story_id=job.story_id, job_id=image_job_id, image_model="gemini-3.1-flash-image",
                             theme=job.theme, status="processing", user_id=job.user_id if job.user_id else None)

        job.image_job_id = image_job_id

        db.add(image_job)
        db.commit()

        background_tasks.add_task(generate_image_task, image_job_id)

    job_public = StoryJobPublic(
        job_id=job.job_id,
        username=user.username if user else None,
        ai_model=job.ai_model,
        status=job.status,
        image_job_id=image_job_id or None,
        created_at=job.created_at,
        story_id=job.story_id,
        completed_at=job.completed_at,
        error=job.error
    )

    return job_public


@router.get("/images/{job_id}", response_model=ImageJobPublic)
def get_image_job_status(job_id: str, db: SessionDep):
    statement = select(ImageJob).where(ImageJob.job_id == job_id)
    job = db.exec(statement).first()
    if not job:
        raise JobNotFoundError(message="Image job not found")
    if job.status == "failed":
        raise CreateYourStoryError(
            name="Image generation failed", message=job.error or "Something failed during image generation")
    user = db.get(User, job.user_id)
    return ImageJobPublic(
        job_id=job_id,
        theme=job.theme,
        status=job.status,
        image_model=job.image_model,
        story_id=job.story_id,
        error=job.error,
        username=user.username if user else None,
        created_at=job.created_at,
        completed_at=job.completed_at
    )


image_model = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-image",
    image_config={
        "aspect_ratio": "4:3",
        "image_size": "1K"
    },
)


def generate_image_task(job_id: str):
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
            response = image_model.invoke(
                generate_story_image_prompt(story))
            content = response.content_blocks[0]
            if content["type"] != "image" or "base64" not in content:
                raise CreateYourStoryError(
                    message="Image model returned invalid response", name="Image generation error")
            story.image_base_64 = content["base64"]

            image_job.status = "completed"
            image_job.completed_at = datetime.now()

        except Exception as e:
            image_job.status = "failed"
            image_job.error = str(e)
            image_job.completed_at = datetime.now()

        db.commit()
