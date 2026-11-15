import os
from dotenv import load_dotenv
from google import genai
from config import MODEL_NAME


load_dotenv()


class GeminiClient:
    """
    Handles all communication with Gemini.
    """

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in .env"
            )

        self.client = genai.Client(api_key=api_key)

    def generate_response(self, prompt: str) -> str:
        """
        Send prompt to Gemini.
        """

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        return response.text.strip()