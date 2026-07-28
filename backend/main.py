from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
from routers import auth
from exceptions.handlers import register_exception_handlers
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

register_exception_handlers(app)


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
