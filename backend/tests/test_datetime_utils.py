import json
from datetime import UTC, datetime

from core.datetime_utils import utc_now
from models.story import CompleteStoryNodePublic, CompleteStoryPublic


def test_utc_now_is_naive_utc():
    now = utc_now()
    assert now.tzinfo is None
    assert abs((now - datetime.now(UTC).replace(tzinfo=None)).total_seconds()) < 2


def test_api_serializes_created_at_with_z():
    node = CompleteStoryNodePublic(
        id=1,
        content="test",
        is_ending=True,
        is_winning_ending=False,
        options=[],
    )
    story = CompleteStoryPublic(
        id=1,
        title="Test",
        ai_model="test",
        username=None,
        session_id="sess",
        created_at=utc_now(),
        root_node=node,
        all_nodes={1: node},
        num_endings=1,
        num_winning_endings=0,
        num_words=1,
        image_job_id=None,
        image_base_64=None,
    )
    created_at = json.loads(story.model_dump_json())["created_at"]
    assert created_at.endswith("Z")
