from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class Story(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    title: str = Field(index=True)
    session_id: str = Field(index=True)
    ai_model: str
    nodes: list["StoryNode"] = Relationship(back_populates="story")
    created_at: datetime = Field(
        default_factory=datetime.now)


class StoryNode(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    story_id: int = Field(foreign_key="story.id", index=True)
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
    session_id: str | None
    created_at: datetime
    root_node: CompleteStoryNodePublic
    all_nodes: dict[int, CompleteStoryNodePublic]
