import json
from langchain_protocol import ImageContentBlock
from sqlmodel import select
from models.story import Story
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from db.database import get_db
from exceptions.exceptions import *

load_dotenv()


image_model = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite-image",
    max_tokens=None,
    timeout=None,
    max_retries=1,
)


def generate_image(story: Story):
    story_transcript = ""
    for node in story.nodes:
        story_transcript += node.content + "\n"
    response = image_model.invoke(
        f"The following is the full transcript of a choose your adventure game. Generate an image for this story. It should be an image of an important moment of the story that captures what the story is about: ${story_transcript}")
    content = response.content_blocks[0]
    if content["type"] != "image" or "base64" not in content:
        raise Exception("Image model returned invalid response")
    story.image_base_64 = content["base64"]
