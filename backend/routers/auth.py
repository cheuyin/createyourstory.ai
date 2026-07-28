from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from db.database import SessionDep
from dependencies.auth import get_user_from_token
from models.auth import Token, User, UserCreate, UserPublic
from services import auth as auth_service

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: SessionDep,
):
    return auth_service.login_user(db, form_data.username, form_data.password)


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(data: UserCreate, db: SessionDep):
    return auth_service.signup_user(db, data)


@router.get("/users/me", response_model=UserPublic)
def read_users_me(current_user: Annotated[User, Depends(get_user_from_token)]):
    return UserPublic(
        username=current_user.username, full_name=current_user.full_name)
