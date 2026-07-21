from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # Environment
    environment: Literal["development", "production"] = "development"

    # LLM
    DEFAULT_PROVIDER: str


    PORTKEY_API_KEY: str

    # Search
    tavily_api_key: str

    # Embeddings
    embedding_model: str
    EMBEDDING_DIMENSION: int = 384

    # Vector Database
    QDRANT_URL: str
    QDRANT_API_KEY: str
    QDRANT_COLLECTION: str = "knowledge"

    # Observability
    logfire_token: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()