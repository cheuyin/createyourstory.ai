from sqlmodel import SQLModel, Column, Field, String, ForeignKey, Boolean, Relationship, JSON


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

