from typing import TYPE_CHECKING

from sqlmodel import Column, SQLModel, Field, Relationship, Text
from datetime import datetime

if TYPE_CHECKING:
    from models.auth import User


class Story(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    title: str = Field(index=True)
    session_id: str = Field(index=True)
    ai_model: str
    nodes: list["StoryNode"] = Relationship(
        back_populates="story", cascade_delete=True)
    # ===== Stats =====
    num_endings: int | None = Field(default=None)
    num_winning_endings: int | None = Field(default=None)
    num_words: int | None = Field(default=None)
    image_base_64: str | None = Field(default=None, sa_column=Column(Text))
    # ==== User =====
    user_id: int | None = Field(foreign_key="user.id",
                                index=True, ondelete="CASCADE", nullable=True)
    user: "User" = Relationship(back_populates="stories")
    created_at: datetime = Field(
        default_factory=datetime.now)


class StoryNode(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    story_id: int = Field(foreign_key="story.id",
                          index=True, ondelete="CASCADE")
    content: str
    is_root: bool = False
    is_ending: bool = False
    is_winning_ending: bool = False
    # Serialized JSON string of a list of StoryOptions
    options_raw_json_str: str | None = None
    story: Story = Relationship(back_populates="nodes")


class StoryOption(SQLModel):
    text: str
    node_id: int


class CompleteStoryNodePublic(SQLModel):
    id: int
    content: str
    is_ending: bool = False
    is_winning_ending: bool = False
    options: list[StoryOption]


class StoryCreate(SQLModel):
    theme: str
    ai_model: str


class CompleteStoryPublic(SQLModel):
    id: int
    title: str
    ai_model: str
    username: str | None
    session_id: str | None
    created_at: datetime
    root_node: CompleteStoryNodePublic
    all_nodes: dict[int, CompleteStoryNodePublic]
    num_endings: int
    num_winning_endings: int
    num_words: int
    image_base_64: str | None
