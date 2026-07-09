from typing import Annotated

from fastapi import Depends, FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from routers import auth
from routers.auth import get_user_from_token
from models.auth import User
from exceptions.exceptions import *
from core.config import settings
from routers import story, job
from db.database import create_db_and_tables

create_db_and_tables()

app = FastAPI(
    title="ChooseYourStory.ai API",
    description="Generate any story!",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(AuthenticationError)
def authentication_error_handler(_: Request, exc: AuthenticationError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": exc.name,
                 "message": exc.message},
        headers={
            "WWW-Authenticate": "Bearer"
        })


@app.exception_handler(UnsupportedAIModelError)
def unsupported_ai_model_error_handler(_: Request, exc: UnsupportedAIModelError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": exc.name,
                 "message": exc.message})


@app.exception_handler(StoryGenerationError)
def story_generation_error_handler(_: Request, exc: StoryGenerationError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": exc.name,
                 "message": exc.message})


@app.exception_handler(StoryResponseValidationError)
def story_response_validation_handler(_: Request, exc: StoryResponseValidationError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": exc.name,
                 "message": exc.message})


@app.exception_handler(StoryRootNotFoundError)
def story_root_not_found_handler(_: Request, exc: StoryRootNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": exc.name,
                 "message": exc.message})


@app.exception_handler(StoryNotFoundError)
def story_not_found_handler(_: Request, exc: StoryNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": exc.name,
                 "message": exc.message})


@app.exception_handler(JobNotFoundError)
def job_not_found_handler(_: Request, exc: JobNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": exc.name,
                 "message": exc.message})


@app.exception_handler(CreateYourStoryError)
def base_exception_handler(_: Request, exc: CreateYourStoryError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": exc.name,
                 "message": exc.message})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Validation error",
                 "message": "The request was poorly formatted"})


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail,
                 "message": "Something went wrong"})


@app.get("/")
def hello():
    return {"message": "Hello!"}


app.include_router(story.router, prefix=settings.API_PREFIX)
app.include_router(job.router, prefix=settings.API_PREFIX)
app.include_router(auth.router, prefix=settings.API_PREFIX)
