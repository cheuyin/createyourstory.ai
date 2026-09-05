from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from core.config import settings


def _normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


def _create_db_engine():
    db_url = _normalize_database_url(settings.DATABASE_URL)
    connect_args = {}
    engine_kwargs = {}

    if db_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    elif db_url:
        engine_kwargs["pool_pre_ping"] = True
        engine_kwargs["pool_recycle"] = 300

    return create_engine(db_url, connect_args=connect_args, **engine_kwargs)


engine = _create_db_engine()


def get_db():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


SessionDep = Annotated[Session, Depends(get_db)]
