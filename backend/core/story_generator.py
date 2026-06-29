from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import ValidationError
from sqlmodel import Session
from exceptions.exceptions import StoryResponseValidationError
from models.story import Story, StoryNode, StoryOption
from core.models import StoryResponseLLM, StoryNodeLLM
from core.prompts import STORY_PROMPT
from dotenv import load_dotenv
import json

load_dotenv()


class StoryGenerator:
    @classmethod
    def _get_model(cls):
        model = ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite",
            max_tokens=None,
            timeout=None,
            max_retries=2,
        ).with_structured_output(schema=StoryResponseLLM.model_json_schema(), method="json_schema")
        return model

    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy"):
        try:
            model = cls._get_model()
            response = model.invoke([
                {
                    "role": "system",
                    "content": STORY_PROMPT,
                },
                {
                    "role": "user",
                    "content": f"Create a story with this theme: {theme}"
                }
            ]
            )
            print("RESPONSE: ", response)
            response = StoryResponseLLM.model_validate(response)
            story = Story(title=response.title, session_id=session_id)
            db.add(story)
            db.flush()
            assert story.id

            cls._process_story_node(
                db, story.id, response, response.rootNodeId, is_root=True)

            db.commit()
            return story
        except ValidationError:
            raise StoryResponseValidationError()

    @classmethod
    def _process_story_node(cls, db: Session, story_id: int, story: StoryResponseLLM, curr_node_id: int, is_root: bool = False) -> StoryNode:
        curr_node = story.allNodes[curr_node_id]
        node = StoryNode(
            story_id=story_id,
            content=curr_node.content,
            is_root=is_root,
            is_ending=len(curr_node.options) == 0,
            is_winning_ending=curr_node.isWinningEnding,
        )
        db.add(node)
        db.flush()

        if not node.is_ending:
            options_raw_json_str_list: list[dict] = []
            for option_id in curr_node.options:
                next_node = StoryNodeLLM.model_validate(
                    story.allNodes[option_id])
                added_child = cls._process_story_node(
                    db, story_id, story, next_node.id, False)
                options_raw_json_str_list.append(StoryOption(**{
                    "text": story.allNodes[option_id].optionText,
                    "node_id": added_child.id
                }).model_dump(mode="json"))
            node.options_raw_json_str = json.dumps(options_raw_json_str_list)

        db.flush()
        return node
