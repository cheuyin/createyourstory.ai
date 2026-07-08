from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.story import Story


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    username: str = Field(unique=True)
    full_name: str
    hashed_password: str
    stories: list["Story"] = Relationship(
        back_populates="user", cascade_delete=True)


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None


class UserCreate(SQLModel):
    username: str
    full_name: str
    password: str
