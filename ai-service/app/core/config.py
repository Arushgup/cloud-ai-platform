from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    SERVICE_NAME: str = "ai-service"
    ENVIRONMENT: str  = Field(default="development")

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = Field(default="localhost:9092")
    KAFKA_RESUME_TOPIC: str      = Field(default="resume-uploaded")
    KAFKA_DLQ_TOPIC: str         = Field(default="resume-dlq")
    KAFKA_GROUP_ID: str          = Field(default="ai-service-group")

    # Groq
    GROQ_API_KEY: str  = Field(...)
    GROQ_MODEL: str    = Field(default="llama-3.3-70b-versatile")

    # Chroma
    CHROMA_PERSIST_PATH: str    = Field(default="./chroma_data")
    CHROMA_COLLECTION_NAME: str = Field(default="resumes")

    # Embeddings
    EMBEDDING_MODEL: str = Field(default="all-MiniLM-L6-v2")

    # Mock mode
    MOCK_LLM: bool = Field(default=False)


settings = Settings()