from typing import Annotated

from fastapi import Depends

from core.config import settings
from sqlmodel import create_engine, Session, SQLModel

engine = create_engine(settings.DATABASE_URL)


def get_db():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


SessionDep = Annotated[Session, Depends(get_db)]
