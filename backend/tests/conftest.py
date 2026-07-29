"""
Shared pytest setup for the backend test suite.

pytest automatically loads this file before running any test. Fixtures defined
here can be used in any test file without importing them manually.

Run tests from the backend folder:
    uv sync --group dev
    uv run pytest -v
"""

import os

# ---------------------------------------------------------------------------
# Step 1: Set fake config BEFORE importing the app
# ---------------------------------------------------------------------------
# main.py and db/database.py read settings when they are first imported.
# If we imported the app first, it might connect to your real database.db
# file or fail because JWT_SECRET_KEY is missing. Setting these env vars
# first keeps tests isolated and predictable.
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-tests-only-32b")
os.environ.setdefault("OPENROUTER_API_KEY", "test-key-not-used-in-tests")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from core.llm_schemas import StoryNodeLLM, StoryResponseLLM
from db.database import get_db
from main import app
from models.auth import User, UserCreate
from services import auth as auth_service


# ---------------------------------------------------------------------------
# Fixture: engine
# ---------------------------------------------------------------------------
# A "fixture" is reusable test setup that pytest injects into test functions.
# This one creates a fresh in-memory SQLite database for each test that needs it.
#
# ":memory:" means the database lives only in RAM. SQLite gives each connection
# its own empty :memory: DB by default — StaticPool forces one shared connection
# so tables we create here are visible to every request in the test.
@pytest.fixture
def engine():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create all tables (user, story, storynode, storyjob, imagejob, etc.)
    # SQLModel needs the model classes to be imported first; importing `app`
    # above already pulled them in via the routers and services.
    SQLModel.metadata.create_all(test_engine)

    yield test_engine  # Tests run here

    test_engine.dispose()  # Cleanup after the test finishes


# ---------------------------------------------------------------------------
# Fixture: db_session
# ---------------------------------------------------------------------------
# Gives tests a single database session bound to the in-memory engine.
# Think of it as "open a connection, run the test, close the connection."
@pytest.fixture
def db_session(engine):
    with Session(engine) as session:
        yield session


# ---------------------------------------------------------------------------
# Fixture: client
# ---------------------------------------------------------------------------
# TestClient lets us call API routes (GET, POST, etc.) without starting
# uvicorn or making real HTTP requests over the network.
#
# We override `get_db` so every route handler uses OUR test database
# instead of the one created at app startup in db/database.py.
@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Always undo the override so later tests are not affected.
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Fixture: sample_llm_response
# ---------------------------------------------------------------------------
# A fake "AI output" we can use instead of calling OpenRouter.
# Shape matches StoryResponseLLM — a tiny decision tree:
#   root (id 0) → two endings (id 1 loses, id 2 wins).
# Persistence and flow tests will reuse this so we never hit the real API.
@pytest.fixture
def sample_llm_response() -> StoryResponseLLM:
    return StoryResponseLLM(
        title="The Fork in the Road",
        rootNodeId=0,
        allNodes={
            0: StoryNodeLLM(
                id=0,
                optionText=None,
                options=[1, 2],
                content="You stand at a crossroads.",
                isWinningEnding=False,
            ),
            1: StoryNodeLLM(
                id=1,
                optionText="Go left",
                options=[],
                content="A wolf appears. You lose.",
                isWinningEnding=False,
            ),
            2: StoryNodeLLM(
                id=2,
                optionText="Go right",
                options=[],
                content="You find treasure. You win.",
                isWinningEnding=True,
            ),
        },
    )


# ---------------------------------------------------------------------------
# Helper: create_user
# ---------------------------------------------------------------------------
# Not a fixture — call this when a test needs a User row in the database
# without going through HTTP (e.g. story ownership tests in later chunks).
def create_user(
    db_session: Session,
    *,
    username: str,
    password: str = "secret123",
    full_name: str | None = None,
) -> User:
    auth_service.signup_user(
        db_session,
        UserCreate(
            username=username,
            full_name=full_name or username.title(),
            password=password,
        ),
    )
    user = auth_service.get_user_by_username(db_session, username)
    assert user is not None
    return user


# ---------------------------------------------------------------------------
# Fixture: auth_headers
# ---------------------------------------------------------------------------
# Signs up "alice" via the API and returns headers you pass to authenticated
# requests: {"Authorization": "Bearer <token>"}.
@pytest.fixture
def auth_headers(client) -> dict[str, str]:
    response = client.post(
        "/api/auth/signup",
        json={
            "username": "alice",
            "full_name": "Alice",
            "password": "secret123",
        },
    )
    assert response.status_code == 201
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Fixture: second_user_headers
# ---------------------------------------------------------------------------
# Same as auth_headers but for a second user ("bob"). Used when we need to
# prove user A cannot access user B's stories (authorization matrix tests).
@pytest.fixture
def second_user_headers(client) -> dict[str, str]:
    response = client.post(
        "/api/auth/signup",
        json={
            "username": "bob",
            "full_name": "Bob",
            "password": "secret123",
        },
    )
    assert response.status_code == 201
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
