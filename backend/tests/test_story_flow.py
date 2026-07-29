"""
End-to-end story creation — HTTP create → background generation → fetch result.

AI is mocked at the service boundary (no OpenRouter). We call run_story_generation
directly instead of waiting on FastAPI BackgroundTasks.

run_story_generation opens its own Session(db.database.engine), so we patch that
engine to the in-memory test engine — otherwise the job row would not be found.
"""

from models.job import StoryJob
from services.story import run_story_generation
from sqlmodel import select

AI_MODEL = "google/gemini-2.5-flash"
THEME = "A hero stands at a crossroads in a dark forest."


def test_create_story_flow_with_mocked_ai(
    client,
    db_session,
    engine,
    sample_llm_response,
    mocker,
):
    mocker.patch(
        "services.story.generate_story_response",
        return_value=sample_llm_response,
    )
    mocker.patch(
        "core.image_generator.ImageGenerator.generate_image",
        return_value="base64fake",
    )
    # Background worker uses db.database.engine, not the TestClient override.
    mocker.patch("services.story.engine", engine)
    mocker.patch("services.job.engine", engine)

    create_response = client.post(
        "/api/stories/create",
        json={"theme": THEME, "ai_model": AI_MODEL},
    )
    assert create_response.status_code == 200
    job_id = create_response.json()["job_id"]

    job_row = db_session.exec(
        select(StoryJob).where(StoryJob.job_id == job_id)
    ).first()
    assert job_row is not None
    assert job_row.id is not None

    run_story_generation(job_row.id)

    job_response = client.get(f"/api/jobs/stories/{job_id}")
    assert job_response.status_code == 200
    job_body = job_response.json()
    assert job_body["status"] == "completed"
    assert job_body["story_id"] is not None

    story_response = client.get(f"/api/stories/{job_body['story_id']}")
    assert story_response.status_code == 200
    story_body = story_response.json()
    assert story_body["title"] == "The Fork in the Road"
    assert len(story_body["all_nodes"]) == 3
