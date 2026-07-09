from sqlmodel import SQLModel, Field
from datetime import datetime


class StoryJob(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    job_id: str = Field(index=True, unique=True)
    session_id: str = Field(index=True)
    theme: str
    status: str
    ai_model: str
    story_id: int | None = None
    error: str | None = None
    user_id: int | None = Field(foreign_key="user.id",
                                index=True, nullable=True)
    created_at: datetime = Field(
        default_factory=datetime.now)
    completed_at: datetime | None = None


class StoryJobPublic(SQLModel):
    job_id: str
    username: str | None
    status: str
    ai_model: str
    created_at: datetime
    story_id: int | None
    completed_at: datetime | None
    error: str | None
