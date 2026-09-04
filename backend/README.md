# CreateYourStory.ai — Backend

FastAPI REST API for story generation, jobs, and auth. See the [root README](../README.md) for full project setup (`.env`, OpenRouter key, running the server).

## Prerequisites

- You need Python 3.13 or newer installed locally.
- The project uses `uv` for package and virtual environment management.
- You need a Supabase connection string to connect to the PostgreSQL database.

## Database Configuration

The application uses PostgreSQL as its primary database.

- Both local development and production deployments connect to Supabase PostgreSQL using the transaction pooler URI.
- The database engine automatically enables connection pre-pinging and recycles stale connections.
- Missing tables are created automatically on application startup.
- Automated tests continue to use an in-memory SQLite database for speed and isolation.

## Running tests

From this directory:

```bash
uv sync --group dev
uv run ruff check .
uv run ruff format --check .
uv run pytest -v
```

Running `ruff format .` without `--check` automatically formats python files. The `--group dev` flag installs pytest, pytest-mock, httpx2, and ruff.

### What the suite does

- The test suite covers authentication, database persistence, error contracts, and story flows.
- Tests run against an isolated in-memory SQLite database so they never touch your live data.
- Language model and image generation APIs are mocked to prevent external network calls.
- In-memory database settings are injected before the application loads so no `.env` file is required for testing.

### CI

Pull requests that change `backend/**` run the same commands on GitHub Actions (workflow: `.github/workflows/backend-test.yml`).
