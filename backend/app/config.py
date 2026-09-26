"""Settings — env vars only, never secrets in code (PRD 6)."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Literal
from urllib.parse import urlparse

from pydantic import AliasChoices, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self

FORBIDDEN_PRODUCTION_SECRETS: frozenset[str] = frozenset({
    "change-me-in-production",
    "replace-with-a-long-random-string",
    "secret",
    "admin",
    "password",
    "jwt_secret",
})


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "CodeMentor AI"
    environment: str = "development"

    database_url: str = "postgresql+psycopg://codementor:codementor@localhost:5433/codementor"

    jwt_secret: str = Field(
        default="change-me-in-production",
        validation_alias=AliasChoices("JWT_SECRET", "jwt_secret"),
    )
    jwt_algorithm: str = "HS256"
    jwt_expiry_hours: int = 24

    redis_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("REDIS_URL", "redis_url"),
    )

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

    run_rate_limit: int = 30
    run_rate_window_s: int = 60

    tutor_rate_limit: int = 20
    tutor_rate_window_s: int = 300

    coach_rate_limit: int = 20
    coach_rate_window_s: int = 300

    generate_rate_limit: int = 10
    generate_rate_window_s: int = 300

    # Authentication rate limits (attempts per window). Every attempt counts, successful or
    # not, and account buckets exist for unknown identifiers too, so the limiter never
    # reveals whether an account exists. Per-IP limits are deliberately roomier than
    # per-account ones: classrooms and campuses share one NAT address.
    auth_login_ip_limit: int = 100
    auth_login_ip_window_s: int = 900
    auth_login_account_limit: int = 10
    auth_login_account_window_s: int = 900
    auth_register_ip_limit: int = 20
    auth_register_ip_window_s: int = 3600
    auth_google_ip_limit: int = 100
    auth_google_ip_window_s: int = 900
    auth_google_identity_limit: int = 10
    auth_google_identity_window_s: int = 900

    # Client-IP trust for per-IP rate limits (see app/core/client_ip.py). Unset = use the
    # socket peer, which is correct for direct connections and local development.
    # PROXY_SHARED_SECRET: shared with the Vercel frontend; requests carrying it may state
    # the client IP (production path Vercel -> Render). Must be >= 32 characters.
    proxy_shared_secret: str | None = None
    # TRUSTED_PROXY_CIDRS: comma-separated networks of reverse proxies whose
    # X-Forwarded-For entries are trusted (generic deployments). Empty = trust none.
    trusted_proxy_cidrs: str = ""

    @model_validator(mode="after")
    def validate_production_config(self) -> Self:
        # Normalize database_url prefix for SQLAlchemy 2.0 / psycopg3
        url = self.database_url
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+psycopg://", 1)
        elif url.startswith("postgresql://") and not url.startswith("postgresql+"):
            url = url.replace("postgresql://", "postgresql+psycopg://", 1)
        self.database_url = url

        # Client-IP trust configuration (all environments): fail on malformed values.
        if self.proxy_shared_secret is not None:
            self.proxy_shared_secret = self.proxy_shared_secret.strip() or None
        if self.proxy_shared_secret is not None and len(self.proxy_shared_secret) < 32:
            raise ValueError(
                "PROXY_SHARED_SECRET must be at least 32 characters (generate with "
                "`python -c \"import secrets; print(secrets.token_urlsafe(48))\"`)."
            )
        from app.core.client_ip import parse_cidrs  # local import: avoids import cycles
        try:
            parse_cidrs(self.trusted_proxy_cidrs)
        except ValueError as exc:
            raise ValueError(f"TRUSTED_PROXY_CIDRS is invalid: {exc}") from exc

        if self.is_production:
            # 1. JWT Secret Validation
            secret = (self.jwt_secret or "").strip()
            if not secret or secret.lower() in FORBIDDEN_PRODUCTION_SECRETS:
                raise ValueError(
                    "Production misconfiguration: Running with ENVIRONMENT=production requires a secure "
                    f"JWT_SECRET. Default placeholder '{self.jwt_secret}' is strictly prohibited."
                )
            if len(secret) < 32:
                raise ValueError(
                    f"Production misconfiguration: JWT_SECRET is too short ({len(secret)} characters). "
                    "Production JWT_SECRET must be at least 32 characters long."
                )

            # 2. Database URL Validation
            if not url:
                raise ValueError(
                    "Production misconfiguration: DATABASE_URL must be set in production."
                )
            parsed = urlparse(url)
            hostname = (parsed.hostname or "").lower()
            if hostname in ("localhost", "127.0.0.1", "::1") or "localhost" in url.lower():
                raise ValueError(
                    f"Production misconfiguration: DATABASE_URL cannot point to localhost/loopback in production ({url})."
                )

            # 3. Redis URL Validation
            redis_str = (self.redis_url or "").strip()
            if not redis_str:
                raise ValueError(
                    "Production misconfiguration: REDIS_URL must be configured in production for distributed rate limiting."
                )
            parsed_redis = urlparse(redis_str)
            if parsed_redis.scheme not in ("redis", "rediss"):
                raise ValueError(
                    f"Production misconfiguration: REDIS_URL must have scheme 'redis://' or 'rediss://' (got '{parsed_redis.scheme}')."
                )
            redis_host = (parsed_redis.hostname or "").lower()
            if redis_host in ("localhost", "127.0.0.1", "::1") or "localhost" in redis_str.lower():
                raise ValueError(
                    f"Production misconfiguration: REDIS_URL cannot point to localhost/loopback in production ({redis_str})."
                )

        return self

    @property
    def client_ip_trust_source(self) -> str:
        """How per-IP rate limits identify clients: attested, trusted-cidrs, or socket-peer."""
        if self.proxy_shared_secret:
            return "attested"
        if self.trusted_proxy_cidrs.strip():
            return "trusted-cidrs"
        return "socket-peer"

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

