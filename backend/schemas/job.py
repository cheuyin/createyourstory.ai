from sqlmodel import SQLModel
from datetime import datetime


class StoryJobPublic(SQLModel):
    job_id: int
    status: str
    created_at: datetime
    story_id: int | None
    completed_at: datetime | None
    error: str | None


class StoryJobCreate(SQLModel):
    theme: str
