"""
Story authorization tests — who can read GET /api/stories/{id}.

Rules (from services/story.py → get_story):
  - Guest stories (user_id is None): anyone can read, no login required.
  - Owned stories: caller must be logged in AND must be the owner.

We seed stories directly via persist_story_from_llm (no AI, no HTTP create).
"""

import pytest

from services import auth as auth_service
from services.story import persist_story_from_llm
from tests.conftest import create_user

AI_MODEL = "google/gemini-2.5-flash"


@pytest.mark.parametrize(
    "owner,headers_fixture,expected_status",
    [
        ("guest", None, 200),
        ("alice", "auth_headers", 200),
        ("alice", None, 403),
        ("alice", "second_user_headers", 403),
    ],
    ids=[
        "guest-no-auth",
        "owner-as-owner",
        "owner-as-guest",
        "owner-as-other-user",
    ],
)
def test_get_story_authorization(
    client,
    db_session,
    sample_llm_response,
    owner,
    headers_fixture,
    expected_status,
    request,
):
    # Resolve auth headers first — some fixtures sign up users via the API.
    headers: dict[str, str] = {}
    if headers_fixture is not None:
        headers = request.getfixturevalue(headers_fixture)

    # Seed a story in the DB without calling OpenRouter.
    if owner == "guest":
        user_id = None
        session_id = "guest-sess"
    else:
        alice = auth_service.get_user_by_username(db_session, "alice")
        if alice is None:
            alice = create_user(db_session, username="alice")
        user_id = alice.id
        session_id = "owned-sess"

    story = persist_story_from_llm(
        db_session,
        sample_llm_response,
        session_id=session_id,
        ai_model=AI_MODEL,
        user_id=user_id,
    )

    response = client.get(f"/api/stories/{story.id}", headers=headers)

    assert response.status_code == expected_status

    if expected_status == 403:
        body = response.json()
        assert body["error"] == "Not authorized"
        assert "message" in body
    else:
        assert response.json()["title"] == "The Fork in the Road"
