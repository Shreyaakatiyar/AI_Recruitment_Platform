from app.services.gemini_client import client
from app.utils.exceptions import EmbeddingServiceError

EMBEDDING_MODEL = "gemini-embedding-001"


def get_embedding(text: str) -> list[float]:
    if not text or not text.strip():
        raise EmbeddingServiceError("Cannot generate an embedding for empty text.")

    try:
        response = client.models.embed_content(model=EMBEDDING_MODEL, contents=text)
    except Exception as e:
        raise EmbeddingServiceError(f"Gemini embedding call failed: {e}")

    if not response.embeddings:
        raise EmbeddingServiceError("Gemini returned no embedding for the given text.")

    return response.embeddings[0].values