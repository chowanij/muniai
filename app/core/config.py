"""
Konfiguracja aplikacji - ładuje zmienne z .env
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # APP
    app_name: str = "MuniAI"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: Literal["development", "staging", "production"] = "development"

    # DATABASE
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/muniai"
    db_pool_size: int = 5
    db_max_overflow: int = 10

    # REDIS
    redis_url: str = "redis://localhost:6379/0"

    # QDRANT
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "documents"

    # LLM
    openai_api_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()