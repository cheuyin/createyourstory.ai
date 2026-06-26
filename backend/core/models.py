from pydantic import BaseModel, Field


class StoryNodeLLM(BaseModel):
    id: int = Field(description="Id of this node")
    optionText: str | None = Field(
        default=None, description="Text of the option shown to the user that this node pertains to")
    options: list[int] = Field(
        description="Options for this node as a list of node ids")
    content: str = Field(description="The main content of the story node")
    isWinningEnding: bool = Field(
        description="Whether this node is the winning choice. Should only be one per story.")


class StoryResponseLLM(BaseModel):
    title: str = Field(description="Title of the story")
    rootNodeId: int = Field(description="Id of the root node of the story")
    allNodes: dict[int, StoryNodeLLM] = Field(
        description="All the nodes in the story in a dictionary with their key as the id")
