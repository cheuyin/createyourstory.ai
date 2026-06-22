from sqlmodel import SQLModel
from datetime import datetime


class StoryOptions(SQLModel):
    text: str
    node_id: int | None = None


class CompleteStoryNodePublic(SQLModel):
    id: int
    options: list[StoryOptions]
    content: str
    is_ending: bool = False
    is_winning_ending: bool = False


class StoryCreate(SQLModel):
    theme: str


class CompleteStoryPublic(SQLModel):
    id: int
    title: str
    session_id: str | None
    created_at: datetime
    root_node: CompleteStoryNodePublic
    all_nodes: dict[int, CompleteStoryNodePublic]
