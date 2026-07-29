"""
Smoke test — a quick sanity check that the test harness itself works.

If this passes, pytest is installed, the app imports cleanly, and TestClient
can talk to FastAPI. Later chunks will add real business-logic tests.
"""


def test_app_starts(client):
    # `client` is injected by pytest from conftest.py (the `client` fixture).
    # /docs is FastAPI's built-in Swagger UI page — no database required.
    response = client.get("/docs")

    assert response.status_code == 200
