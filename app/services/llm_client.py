from google import genai
from google.genai import types
from pydantic import BaseModel

from app.config import settings
from app.utils.exceptions import LLMServiceError

_client = genai.Client(api_key=settings.gemini_api_key)

DEFAULT_MODEL = "gemini-3.5-flash-lite"


def generate_structured(prompt: str, response_schema: type[BaseModel], model: str = DEFAULT_MODEL) -> BaseModel:
    try:
        response = _client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=response_schema,
                temperature=0.1,  
            ),
        )
    except Exception as e:
        raise LLMServiceError(f"Gemini API call failed: {e}")

    if response.parsed is None:
        raise LLMServiceError("Gemini returned output that could not be parsed into the expected structure.")

    return response.parsed