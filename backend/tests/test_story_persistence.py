"""
Story persistence tests — persist_story_from_llm without HTTP or AI.

These call the service layer directly to verify the decision tree is stored
correctly, and that a bad LLM-shaped graph rolls back without leaving rows.
"""

import json

import pytest
from core.llm_schemas import StoryNodeLLM, StoryResponseLLM
from models.story import Story, StoryNode
from services.story import persist_story_from_llm
from sqlmodel import select

AI_MODEL = "google/gemini-2.5-flash"


def test_persist_story_from_llm_creates_correct_tree(db_session, sample_llm_response):
    story = persist_story_from_llm(
        db_session,
        sample_llm_response,
        session_id="persist-sess",
        ai_model=AI_MODEL,
        user_id=None,
    )

    assert story.title == "The Fork in the Road"
    assert story.session_id == "persist-sess"
    assert story.ai_model == AI_MODEL

    nodes = db_session.exec(
        select(StoryNode).where(StoryNode.story_id == story.id)
    ).all()

    assert len(nodes) == 3
    assert sum(1 for node in nodes if node.is_root) == 1
    assert sum(1 for node in nodes if node.is_ending) == 2
    assert sum(1 for node in nodes if node.is_winning_ending) == 1

    root = next(node for node in nodes if node.is_root)
    assert root.options_raw_json_str is not None

    options = json.loads(root.options_raw_json_str)
    assert len(options) == 2
    for option in options:
        assert "text" in option
        assert "node_id" in option

    option_texts = {option["text"] for option in options}
    assert option_texts == {"Go left", "Go right"}


def test_persist_story_from_llm_rolls_back_on_invalid_graph(db_session):
    # rootNodeId points to a node that is not in allNodes — persistence must fail.
    invalid_response = StoryResponseLLM(
        title="Broken Tree",
        rootNodeId=99,
        allNodes={
            0: StoryNodeLLM(
                id=0,
                optionText=None,
                options=[],
                content="Orphan root that will never be reached.",
                isWinningEnding=False,
            ),
        },
    )

    with pytest.raises(KeyError):
        persist_story_from_llm(
            db_session,
            invalid_response,
            session_id="rollback-sess",
            ai_model=AI_MODEL,
            user_id=None,
        )

    stories = db_session.exec(select(Story)).all()
    nodes = db_session.exec(select(StoryNode)).all()
    assert len(stories) == 0
    assert len(nodes) == 0
