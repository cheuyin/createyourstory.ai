from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from pwdlib import PasswordHash
from sqlmodel import Session, select
from db.database import get_db
from models.auth import Token, TokenData, User, UserCreate, UserPublic
from exceptions.exceptions import *
from core.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SessionDep = Annotated[Session, Depends(get_db)]


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/auth/login", auto_error=False)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(username=form_data.username,
                             password=form_data.password)

    if not user:
        raise AuthenticationError()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(data: UserCreate, db: SessionDep):
    statement = select(User).where(User.username == data.username)
    result = db.exec(statement).first()
    if result:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User already exists")
    user = User(username=data.username, full_name=data.full_name,
                hashed_password=password_hash.hash(data.password))
    db.add(user)
    db.commit()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
    }


def get_user(username: str):
    gen = get_db()
    db = next(gen)
    try:
        user = db.exec(statement=select(
            User).where(User.username == username)).first()
        if user:
            return user
        else:
            return None
    finally:
        next(gen, None)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


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
    user_public = UserPublic(
        username=current_user.username, full_name=current_user.full_name)
    return user_public
