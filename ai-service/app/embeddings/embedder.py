import logging
from sentence_transformers import SentenceTransformer
from app.core.config import settings
from typing import Optional
logger = logging.getLogger(__name__)

# Loaded once when the module is first imported — expensive operation
# Subsequent calls reuse the same loaded model
_model: Optional[SentenceTransformer] = None


def get_embedding_model() -> SentenceTransformer:
    global _model
    if _model is None:
        logger.info("Loading embedding model: %s", settings.EMBEDDING_MODEL)
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
        logger.info("Embedding model loaded successfully")
    return _model


def generate_embedding(text: str) -> list[float]:
    """
    Convert text into a vector of floats.

    Example:
        "Python developer with 5 years experience"
        → [0.123, -0.456, 0.789, ...]  (384 numbers for MiniLM)

    Two similar texts produce vectors that are close together.
    This is how semantic search works.
    """
    if not text or not text.strip():
        raise ValueError("Cannot generate embedding for empty text")

    model = get_embedding_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()