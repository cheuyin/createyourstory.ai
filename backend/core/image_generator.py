import json
from langchain_protocol import ImageContentBlock
from sqlmodel import select
from models.story import Story
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from db.database import get_db
from exceptions.exceptions import *
from core.prompts import generate_story_image_prompt

load_dotenv()


image_model = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-image",
    image_config={
        "aspect_ratio": "4:3",
        "image_size": "1K"
    },
)


def generate_image(story: Story):
    response = image_model.invoke(generate_story_image_prompt(story))
    content = response.content_blocks[0]
    if content["type"] != "image" or "base64" not in content:
        raise Exception("Image model returned invalid response")
    story.image_base_64 = content["base64"]
