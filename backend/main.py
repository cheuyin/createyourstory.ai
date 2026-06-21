from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings

app = FastAPI(
    title="Choose Your Own Adventure Game API",
    description="API to generate cool stories",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# A security thing - for dev purposes, allow any origin, but change it for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def main():
    print("Hello from backend!")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
