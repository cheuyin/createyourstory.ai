from sqlmodel import SQLModel, Field, DateTime
import datetime


class StoryJob(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    job_id: str = Field(index=True, unique=True)
    session_id: str = Field(index=True)
    theme: str
    status: str
    story_id: int | None
    error: str | None
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now)
    completed_job: datetime.datetime | None
