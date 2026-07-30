"""Settings — env vars only, never secrets in code (PRD 6)."""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "CodeMentor AI"
    environment: str = "development"

    database_url: str = "postgresql+psycopg://codementor:codementor@localhost:5432/codementor"

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiry_hours: int = 24

    google_client_id: str = ""

    llm_provider: str = "anthropic"
    llm_model: str = "claude-sonnet-4-6"
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    llm_timeout_s: float = 6.0
    llm_retry_timeout_s: float = 4.0

    embedding_provider: str = "openai"
    embedding_model: str = "text-embedding-3-small"

    cors_origins: str = "http://localhost:3000"

    submission_rate_limit: int = 10
    submission_rate_window_s: int = 300

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
