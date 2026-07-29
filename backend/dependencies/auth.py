from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from core.config import settings
from db.database import SessionDep
from exceptions.exceptions import AuthenticationError
from models.auth import User
from services import auth as auth_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login", auto_error=False)


def _decode_token_username(token: str) -> str:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise AuthenticationError()
        return username
    except jwt.InvalidTokenError:
        raise AuthenticationError()


def get_user_from_token(
    db: SessionDep,
    token: Annotated[str | None, Depends(oauth2_scheme)],
) -> User:
    if not token:
        raise AuthenticationError()
    username = _decode_token_username(token)
    user = auth_service.get_user_by_username(db, username)
    if user is None:
        raise AuthenticationError()
    return user


def get_optional_user_from_token(
    db: SessionDep,
    token: Annotated[str | None, Depends(oauth2_scheme)],
) -> User | None:
    if not token:
        return None
    username = _decode_token_username(token)
    user = auth_service.get_user_by_username(db, username)
    if user is None:
        raise AuthenticationError()
    return user
