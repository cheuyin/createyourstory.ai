from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, FileResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from pathlib import Path
from routers import auth
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


@app.exception_handler(ImageGenerationException)
def image_generation_error_handler(_: Request, exc: ImageGenerationException):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"error": exc.name,
                 "message": exc.message})


@app.exception_handler(InsufficientCreditsError)
def insufficient_credits_error_handler(_: Request, exc: InsufficientCreditsError):
    return JSONResponse(
        status_code=status.HTTP_402_PAYMENT_REQUIRED,
        content={"error": exc.name,
                 "message": exc.message})


@app.exception_handler(AuthenticationError)
def authentication_error_handler(_: Request, exc: AuthenticationError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": exc.name,
                 "message": exc.message},
        headers={
            "WWW-Authenticate": "Bearer"
        })


@app.exception_handler(AuthorizationError)
def authorization_error_handler(_: Request, exc: AuthorizationError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"error": exc.name,
                 "message": exc.message},
    )


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


app.include_router(story.router, prefix=settings.API_PREFIX)
app.include_router(job.router, prefix=settings.API_PREFIX)
app.include_router(auth.router, prefix=settings.API_PREFIX)


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"

if FRONTEND_DIR.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIR /
              "assets"), name="assets")

    @app.get("/{catchall:path}")
    async def serve_frontend(catchall: str):
        if catchall.startswith("api") or catchall.startswith("docs") or catchall.startswith("redoc") or catchall.startswith("openapi.json"):
            return JSONResponse(status_code=404, content={"error": "Not found", "message": "Page not found"})
        file_path = FRONTEND_DIR / catchall
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIR / "index.html")
else:
    @app.get("/")
    def hello():
        return {"error": "Frontend not found", "message": "Hello! Frontend build not found. Run frontend dev server or build frontend."}
