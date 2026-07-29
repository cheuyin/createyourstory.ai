"""
Auth API tests — signup, login, and JWT-protected routes.

These hit real HTTP endpoints through TestClient (no mocking). They prove the
auth flow works end-to-end: password hashing, token issuance, and Bearer auth.
"""

SIGNUP_JSON = {
    "username": "carol",
    "full_name": "Carol",
    "password": "secret123",
}


def test_signup_returns_token_and_me_works(client):
    # Sign up a new user; the API returns a JWT access token.
    signup_response = client.post("/api/auth/signup", json=SIGNUP_JSON)

    assert signup_response.status_code == 201
    body = signup_response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"

    # Use that token to fetch the current user's profile.
    me_response = client.get(
        "/api/auth/users/me",
        headers={"Authorization": f"Bearer {body['access_token']}"},
    )

    assert me_response.status_code == 200
    assert me_response.json() == {
        "username": "carol",
        "full_name": "Carol",
    }


def test_login_with_wrong_password_returns_401(client):
    client.post("/api/auth/signup", json=SIGNUP_JSON)

    # Login uses OAuth2 "password" flow — form fields, not JSON.
    login_response = client.post(
        "/api/auth/login",
        data={"username": "carol", "password": "wrong-password"},
    )

    assert login_response.status_code == 401
    body = login_response.json()
    assert "error" in body
    assert "message" in body


def test_duplicate_signup_returns_400(client):
    first = client.post("/api/auth/signup", json=SIGNUP_JSON)
    assert first.status_code == 201

    second = client.post("/api/auth/signup", json=SIGNUP_JSON)

    assert second.status_code == 400
    body = second.json()
    assert "error" in body
    assert "message" in body
