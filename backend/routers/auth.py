from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from core.config import settings
from db.database import SessionDep, get_db
from exceptions.exceptions import *
from models.auth import TokenData, User, UserCreate, UserPublic
from services import auth as auth_service

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/auth/login", auto_error=False)

ALGORITHM = "HS256"


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: SessionDep,
):
    return auth_service.login_user(db, form_data.username, form_data.password)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(data: UserCreate, db: SessionDep):
    access_token = auth_service.signup_user(db, data)
    return {"access_token": access_token}


def get_user(username: str):
    gen = get_db()
    db = next(gen)
    try:
        return auth_service.get_user_by_username(db, username)
    finally:
        next(gen, None)


def get_user_from_token(token: Annotated[str | None, Depends(oauth2_scheme)]) -> User:
    if not token:
        raise AuthenticationError()
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY,
                             algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise AuthenticationError()
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise AuthenticationError()
    assert token_data.username
    user = get_user(username=token_data.username)
    if user is None:
        raise AuthenticationError()
    return user


def get_optional_user_from_token(token: Annotated[str | None, Depends(oauth2_scheme)]) -> User | None:
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY,
                             algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise AuthenticationError()
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise AuthenticationError()
    assert token_data.username
    user = get_user(username=token_data.username)
    if user is None:
        raise AuthenticationError()
    return user


@router.get("/users/me", response_model=UserPublic)
def read_users_me(current_user: Annotated[User, Depends(get_user_from_token)]):
    return UserPublic(
        username=current_user.username, full_name=current_user.full_name)
