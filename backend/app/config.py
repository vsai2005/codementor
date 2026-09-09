"""Settings — env vars only, never secrets in code (PRD 6)."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Literal

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

    llm_provider: str = "nvidia"
    llm_model: str = "nvidia/nemotron-3-ultra-550b-a55b"
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"
    nvidia_tutor_api_keys: str = ""
    nvidia_practice_api_keys: str = ""
    nvidia_api_key: str = ""
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    llm_timeout_s: float = 8.0
    llm_retry_timeout_s: float = 4.0

    embedding_provider: str = "openai"
    embedding_model: str = "text-embedding-3-small"

    # CORS configuration: ALLOWED_ORIGINS takes precedence if set
    allowed_origins: str | None = None
    cors_origins: str = "http://localhost:3000"

    # HttpOnly Cookie parameters
    cookie_samesite: Literal["lax", "strict", "none"] = "lax"
    cookie_secure: bool | None = None
    cookie_domain: str | None = None
    cookie_max_age: int = 86400  # 24 hours

    submission_rate_limit: int = 10
    submission_rate_window_s: int = 300

    @property
    def is_production(self) -> bool:
        return self.environment.lower() in ("production", "prod")

    @property
    def secure_cookies(self) -> bool:
        if self.cookie_secure is not None:
            return self.cookie_secure
        return self.is_production

    @property
    def cors_origin_list(self) -> list[str]:
        raw = os.getenv("ALLOWED_ORIGINS") or self.allowed_origins or self.cors_origins
        return [o.strip() for o in raw.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
