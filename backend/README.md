# CreateYourStory.ai — Backend

FastAPI REST API for story generation, jobs, and auth. See the [root README](../README.md) for full project setup (`.env`, OpenRouter key, running the server).

## Prerequisites

- Python 3.13 or newer
- [`uv`](https://docs.astral.sh/uv/)

## Running tests

From this directory:

```bash
uv sync --group dev
uv run pytest -v
```

`--group dev` installs pytest, pytest-mock, and httpx2 (for FastAPI’s `TestClient`).

### What the suite does

- **13 tests** under `tests/` — auth, error contracts, story authorization, persistence, and one end-to-end create flow.
- **In-memory SQLite** — each test gets a fresh database (`conftest.py`); your local `database.db` is not touched.
- **Mocked AI** — OpenRouter is never called. `generate_story_response` and `ImageGenerator.generate_image` are patched in tests that need them.
- **No `.env` required for tests** — `conftest.py` sets safe defaults (`DATABASE_URL`, `JWT_SECRET_KEY`, `OPENROUTER_API_KEY`) before the app loads.

### CI

Pull requests that change `backend/**` run the same commands on GitHub Actions (workflow: `.github/workflows/backend-test.yml`).
