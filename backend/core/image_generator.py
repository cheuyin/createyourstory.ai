import requests
import os


class ImageGenerator:

    @classmethod
    def generate_image(cls, prompt: str) -> str:
        """
        Input: prompt as a string
        Output: image data as a base64 string
        Throws: ImageGenerationException if someone goes wrong
        """
        URL = "https://openrouter.ai/api/v1/images"
        BODY = {
            "model": "x-ai/grok-imagine-image-quality",
            "prompt": prompt,
        }
        HEADERS = {
            "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
            "Content-Type": "application/json",
        }

        response = requests.post(URL, json=BODY, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data["data"][0]["b64_json"]
