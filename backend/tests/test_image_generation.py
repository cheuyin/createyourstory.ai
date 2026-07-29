from unittest.mock import MagicMock, patch

import pytest
from sqlmodel import select

from core.image_generator import IMAGE_MODEL, ImageGenerator
from core.prompts import MAX_IMAGE_PROMPT_BYTES, generate_story_image_prompt
from exceptions.exceptions import ImageGenerationException
from models.job import ImageJob
from models.story import Story, StoryNode
from services.job import get_image_job_status, run_image_generation


def test_generate_image_returns_b64_json_on_success():
    mock_response = MagicMock()
    mock_response.ok = True
    mock_response.json.return_value = {"data": [{"b64_json": "abc123"}]}

    with patch(
        "core.image_generator.requests.post", return_value=mock_response
    ) as post:
        result = ImageGenerator.generate_image("A quiet forest path")

    assert result == "abc123"
    post.assert_called_once()
    assert post.call_args.kwargs["json"]["model"] == IMAGE_MODEL
    assert post.call_args.kwargs["json"]["output_format"] == "jpeg"


def test_generate_image_includes_openrouter_error_body():
    mock_response = MagicMock()
    mock_response.ok = False
    mock_response.status_code = 400
    mock_response.text = '{"error":{"message":"Prompt length exceeds the maximum allowed length of 8000"}}'

    with patch("core.image_generator.requests.post", return_value=mock_response):
        with pytest.raises(ImageGenerationException) as exc_info:
            ImageGenerator.generate_image("too long")

    message = exc_info.value.message
    assert message.startswith("OpenRouter 400:")
    assert "Prompt length exceeds the maximum allowed length of 8000" in message


def test_generate_story_image_prompt_keeps_short_stories_intact():
    story = Story(
        title="Short",
        session_id="session",
        ai_model="google/gemini-2.5-flash",
        nodes=[StoryNode(content="Once upon a time.", story_id=1)],
    )

    prompt = generate_story_image_prompt(story)

    assert len(prompt.encode("utf-8")) <= MAX_IMAGE_PROMPT_BYTES
    assert "Once upon a time." in prompt
    assert "[transcript truncated]" not in prompt


def test_generate_story_image_prompt_caps_long_transcripts():
    story = Story(
        title="Long",
        session_id="session",
        ai_model="google/gemini-2.5-flash",
        nodes=[StoryNode(content="x" * 20_000, story_id=1)],
    )

    prompt = generate_story_image_prompt(story)

    assert len(prompt.encode("utf-8")) <= MAX_IMAGE_PROMPT_BYTES
    assert "[transcript truncated]" in prompt
    assert prompt.startswith("\nYou are given the complete transcript")


def test_generate_story_image_prompt_respects_utf8_byte_limit_for_ascii_transcript():
    story = Story(
        title="Long ASCII",
        session_id="session",
        ai_model="google/gemini-2.5-flash",
        nodes=[StoryNode(content="a" * 20_000, story_id=1)],
    )

    prompt = generate_story_image_prompt(story)

    assert len(prompt.encode("utf-8")) <= MAX_IMAGE_PROMPT_BYTES
    assert len(prompt.encode("utf-8")) == MAX_IMAGE_PROMPT_BYTES


def test_run_image_generation_persists_openrouter_error(db_session, engine, mocker):
    mocker.patch("services.job.engine", engine)

    story = Story(
        title="Test Story",
        session_id="session",
        ai_model="google/gemini-2.5-flash",
    )
    db_session.add(story)
    db_session.commit()
    db_session.refresh(story)

    image_job = ImageJob(
        job_id="image-job-1",
        theme="A dark forest",
        status="processing",
        image_model=IMAGE_MODEL,
        story_id=story.id,
    )
    db_session.add(image_job)
    db_session.commit()

    error_message = (
        'OpenRouter 400: {"error":{"message":"Prompt length exceeds the maximum '
        'allowed length of 8000"}}'
    )
    mocker.patch(
        "services.job.ImageGenerator.generate_image",
        side_effect=ImageGenerationException(message=error_message),
    )

    run_image_generation(image_job.job_id)

    db_session.expire_all()
    failed_job = db_session.exec(
        select(ImageJob).where(ImageJob.job_id == image_job.job_id)
    ).first()
    assert failed_job is not None
    assert failed_job.status == "failed"
    assert failed_job.error == error_message

    with pytest.raises(ImageGenerationException) as exc_info:
        get_image_job_status(db_session, image_job.job_id)

    assert exc_info.value.message == error_message
