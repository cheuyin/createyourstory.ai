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
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-tests-only")
os.environ.setdefault("OPENROUTER_API_KEY", "test-key-not-used-in-tests")

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from db.database import get_db
from main import app

# ---------------------------------------------------------------------------
# Fixture: engine
# ---------------------------------------------------------------------------
# A "fixture" is reusable test setup that pytest injects into test functions.
# This one creates a fresh in-memory SQLite database for each test that needs it.
#
# ":memory:" means the database lives only in RAM and disappears when the
# connection closes — perfect for fast, isolated tests.
@pytest.fixture
def engine():
    # SQLite normally allows only one thread per connection. FastAPI's
    # TestClient can use multiple threads, so we relax that rule here.
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
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
