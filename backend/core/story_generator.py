from langchain_openrouter import ChatOpenRouter
from pydantic import ValidationError

from core.models import StoryResponseLLM
from core.prompts import STORY_PROMPT
from exceptions.exceptions import InsufficientCreditsError, StoryResponseValidationError


def _get_model(ai_model: str):
    return ChatOpenRouter(
        model=ai_model,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        reasoning={
            "effort": "medium"
        },
    ).with_structured_output(
        schema=StoryResponseLLM.model_json_schema(), method="json_schema")


def generate_story_response(theme: str, ai_model: str) -> StoryResponseLLM:
    try:
        model = _get_model(ai_model)
        response = model.invoke([
            {
                "role": "system",
                "content": STORY_PROMPT,
            },
            {
                "role": "user",
                "content": f"Create a story with this theme: {theme}",
            },
        ])
        return StoryResponseLLM.model_validate(response)
    except ValidationError:
        raise StoryResponseValidationError()
    except Exception as e:
        if "429" in str(e):
            raise InsufficientCreditsError()
        raise
