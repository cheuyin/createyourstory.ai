"""
Error contract tests — make sure the API returns consistent JSON on failures.

Every error response should look like: {"error": "...", "message": "..."}
These tests lock that shape in so we notice if it ever changes.
"""


def test_story_not_found_returns_404_with_error_body(client):
    response = client.get("/api/stories/99999")

    assert response.status_code == 404
    body = response.json()
    assert body["error"] == "Not found"
    assert body["message"] == "Story not found"


def test_invalid_create_body_returns_400(client):
    # StoryCreate requires theme and ai_model — an empty body should fail validation.
    response = client.post("/api/stories/create", json={})

    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "Validation error"
    assert body["message"] == "The request was poorly formatted"
