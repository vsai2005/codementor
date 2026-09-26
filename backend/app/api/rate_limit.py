"""Request-level rate-limit helpers shared by routes.

Keys are namespaced per policy ("<policy>:<subject>") so buckets never collide across
policies, and account identifiers are hashed so raw emails/usernames never reach Redis.
"""

from __future__ import annotations

import hashlib
from functools import lru_cache

from fastapi import HTTPException, Request, status

from app.config import get_settings
from app.core.client_ip import parse_cidrs, resolve_client_ip
from app.services.ratelimit import get_policy_rate_limiter


@lru_cache(maxsize=8)
def _trusted_networks(spec: str):
    return tuple(parse_cidrs(spec))


def client_ip(request: Request) -> str:
    """Rate-limit key for the caller's IP (see app.core.client_ip for the trust model).

    Forwarded addresses are honored only from an authenticated proxy (shared secret) or a
    trusted proxy network; otherwise the socket peer is used.
    """
    settings = get_settings()
    key, _source = resolve_client_ip(
        request,
        proxy_secret=settings.proxy_shared_secret,
        trusted_proxies=_trusted_networks(settings.trusted_proxy_cidrs),
    )
    return key


def account_subject(identifier: str) -> str:
    """Stable, non-reversible bucket id for a normalized account identifier."""
    return hashlib.sha256(identifier.strip().lower().encode("utf-8")).hexdigest()[:32]


def enforce_rate_limit(policy: str, subject: str) -> None:
    """Consumes one attempt from the policy bucket, or raises 429 with Retry-After.

    RateLimiterUnavailable (backend down) propagates to the app-level 503 handler.
    """
    verdict = get_policy_rate_limiter(policy).check(f"{policy}:{subject}")
    if not verdict.allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many attempts. Please wait before trying again.",
            headers={"Retry-After": str(verdict.retry_after_s)},
        )
