"""Request-level rate-limit helpers shared by routes.

Keys are namespaced per policy ("<policy>:<subject>") so buckets never collide across
policies, and account identifiers are hashed so raw emails/usernames never reach Redis.
"""

from __future__ import annotations

import hashlib

from fastapi import HTTPException, Request, status

from app.config import get_settings
from app.services.ratelimit import get_policy_rate_limiter


def client_ip(request: Request) -> str:
    """The caller's IP.

    With trusted_proxy_hops = N > 0, the address N entries from the right of
    X-Forwarded-For is used (each trusted proxy appends the address it received the
    request from, so entries further left can be forged by the client). Otherwise, or when
    the header is shorter than expected, the socket peer address is used.
    """
    hops = get_settings().trusted_proxy_hops
    if hops > 0:
        forwarded = [p.strip() for p in request.headers.get("x-forwarded-for", "").split(",") if p.strip()]
        if len(forwarded) >= hops:
            return forwarded[-hops]
    return request.client.host if request.client else "unknown"


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
