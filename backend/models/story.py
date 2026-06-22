from sqlmodel import SQLModel, Column, Field, String, ForeignKey, Boolean, Relationship, JSON
from datetime import datetime


class Story(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    title: str = Field(index=True)
    session_id: str = Field(index=True)

    nodes: list["StoryNode"] = Relationship(back_populates="story")


class StoryNode(SQLModel):
    id: int | None = Field(primary_key=True, index=True)
    story_id: int = Field(default=None, foreign_key="story.id", index=True)
    content: str
    is_root: bool = False
    is_ending: bool = False
    is_winning_ending = False
    options: JSON
    story = Relationship(back_populates="nodes")


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
