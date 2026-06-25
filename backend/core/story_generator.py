from langchain.agents import create_agent
from sqlmodel import Session
from models.story import Story, StoryNode, StoryOption
from core.models import StoryLLMResponse, StoryNodeLLM
from core.prompts import STORY_PROMPT
from dotenv import load_dotenv
import json

load_dotenv()


class StoryGenerator:
    @classmethod
    def _get_agent(cls):
        return create_agent(
            model="google_genai:gemini-3.1-flash-lite",
            response_format=StoryLLMResponse,
        )

    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy"):
        try:
            agent = cls._get_agent()
            response = agent.invoke({
                "messages": [
                    {
                        "role": "system",
                        "content": STORY_PROMPT
                    },
                    {
                        "role": "user",
                        "content": f"Create a story with this theme: {theme}"
                    }
                ]
            })
            response = StoryLLMResponse.model_validate(
                response["structured_response"])
            story = Story(title=response.title, session_id=session_id)
            db.add(story)
            db.flush()
            assert story.id

            cls._process_story_node(
                db, story.id, response.rootNode, is_root=True)

            db.commit()
            return story
        except Exception as e:
            raise e

    @classmethod
    def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False) -> StoryNode:
        node = StoryNode(
            story_id=story_id,
            content=node_data.content,
            is_root=is_root,
            is_ending=node_data.isEnding,
            is_winning_ending=node_data.isWinningEnding,
        )
        db.add(node)
        db.flush()

        if not node.is_ending and hasattr(node_data, "options") and node_data.options:
            options_raw_json_str_list: list[dict] = []
            for option_data in node_data.options:
                next_node = StoryNodeLLM.model_validate(option_data.nextNode)
                child_node = cls._process_story_node(
                    db, story_id, next_node, False)
                options_raw_json_str_list.append(StoryOption(**{
                    "text": option_data.text,
                    "node_id": child_node.id
                }).model_dump(mode="json"))
            node.options_raw_json_str = json.dumps(options_raw_json_str_list)

        db.flush()
        return node
