import logging
import chromadb
from chromadb.config import Settings as ChromaSettings
from app.core.config import settings
from typing import Optional

logger = logging.getLogger(__name__)

_client: Optional[chromadb.PersistentClient] = None
_collection = None


def get_chroma_client() -> chromadb.PersistentClient:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_PATH,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        logger.info("ChromaDB client ready at: %s", settings.CHROMA_PERSIST_PATH)
    return _client


def get_collection():
    global _collection
    if _collection is None:
        client = get_chroma_client()
        _collection = client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            # cosine similarity: measures angle between vectors
            # better than euclidean distance for text similarity
            metadata={"hnsw:space": "cosine"},
        )
        logger.info("Chroma collection ready: %s", settings.CHROMA_COLLECTION_NAME)
    return _collection


def upsert_resume(
        resume_id: str,
        text: str,
        embedding: list[float],
        metadata: dict,
) -> None:
    """
    Upsert = INSERT if not exists, UPDATE if exists.
    This means reprocessing a resume never creates duplicates.
    """
    collection = get_collection()
    collection.upsert(
        ids=[resume_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata],
    )
    logger.info("Upserted resume into ChromaDB resume_id=%s", resume_id)


def query_similar(
        query_embedding: list[float],
        n_results: int = 10,
        where: dict | None = None,
) -> dict:
    """
    Find the n most similar resumes to a query embedding.
    Used in Phase 3 — Job Matching Agent.
    """
    collection = get_collection()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=where,
        include=["documents", "metadatas", "distances"],
    )
    return results