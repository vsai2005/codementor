"""Rate limiting for LLM-backed endpoints (Phase 3).

Provides:
  - BaseRateLimiter (ABC)
  - RedisRateLimiter (atomic sliding window via pipeline)
  - InMemoryRateLimiter (thread-safe sliding window with cleanup)
"""

from __future__ import annotations

import os
import threading
import time
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from dataclasses import dataclass


class RateLimiterUnavailable(RuntimeError):
    """The rate-limit backend could not be consulted.

    Policy (matches the production boot rule that Redis is mandatory): fail closed. The API
    answers 503 with a generic message; the backend error is logged, never returned.
    """


@dataclass(frozen=True)
class RateLimitVerdict:
    allowed: bool
    remaining: int
    retry_after_s: int


class BaseRateLimiter(ABC):
    @abstractmethod
    def check(self, key: str) -> RateLimitVerdict:
        """Evaluate whether an action under `key` is permitted."""

    @abstractmethod
    def reset(self, key: str | None = None) -> None:
        """Reset rate-limit state for key (or all keys if None)."""


class InMemoryRateLimiter(BaseRateLimiter):
    """Thread-safe in-memory sliding window limiter for local testing."""

    def __init__(self, limit: int = 10, window_s: int = 300) -> None:
        self._limit = limit
        self._window = window_s
        self._hits: dict[str, deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def check(self, key: str) -> RateLimitVerdict:
        now = time.monotonic()
        with self._lock:
            window = self._hits[key]
            while window and now - window[0] > self._window:
                window.popleft()

            if len(window) >= self._limit:
                retry = int(self._window - (now - window[0])) + 1
                return RateLimitVerdict(False, 0, max(1, retry))

            window.append(now)
            return RateLimitVerdict(True, self._limit - len(window), 0)

    def reset(self, key: str | None = None) -> None:
        with self._lock:
            if key is None:
                self._hits.clear()
            else:
                self._hits.pop(key, None)


class RedisRateLimiter(BaseRateLimiter):
    """Distributed sliding window in Redis using an atomic pipeline."""

    def __init__(self, redis_client, limit: int = 10, window_s: int = 300) -> None:
        self._redis = redis_client
        self._limit = limit
        self._window = window_s

    def check(self, key: str) -> RateLimitVerdict:
        import uuid

        now = time.time()
        redis_key = f"ratelimit:{key}"
        cutoff = now - self._window

        try:
            pipe = self._redis.pipeline()
            pipe.zremrangebyscore(redis_key, 0, cutoff)
            pipe.zcard(redis_key)
            pipe.zadd(redis_key, {str(uuid.uuid4()): now})
            pipe.expire(redis_key, self._window + 10)
            _, count, _, _ = pipe.execute()

            if count >= self._limit:
                self._redis.zremrangebyrank(redis_key, -1, -1)  # undo our own add
                oldest = self._redis.zrange(redis_key, 0, 0, withscores=True)
                retry = int(self._window - (now - oldest[0][1])) + 1 if oldest else self._window
                return RateLimitVerdict(False, 0, max(1, retry))
        except Exception as exc:  # redis.RedisError, socket errors, timeouts
            raise RateLimiterUnavailable("rate limiter backend unavailable") from exc

        return RateLimitVerdict(True, self._limit - count - 1, 0)

    def reset(self, key: str | None = None) -> None:
        if key is None:
            for k in self._redis.scan_iter("ratelimit:*"):
                self._redis.delete(k)
        else:
            self._redis.delete(f"ratelimit:{key}")


_default: BaseRateLimiter | None = None
_tutor_limiter: BaseRateLimiter | None = None
_run_limiter: BaseRateLimiter | None = None
_coach_limiter: BaseRateLimiter | None = None
_generate_limiter: BaseRateLimiter | None = None
_sap_execution_limiter: BaseRateLimiter | None = None


def _get_redis_client():
    from app.config import get_settings

    settings = get_settings()
    redis_url = settings.redis_url or os.getenv("REDIS_URL")

    if settings.is_production:
        if not redis_url:
            raise RuntimeError(
                "Production misconfiguration: REDIS_URL must be configured in production."
            )
        try:
            import redis
            client = redis.from_url(redis_url)
            client.ping()
            return client
        except Exception as exc:
            raise RuntimeError(
                f"Production misconfiguration: Failed to connect to Redis at {redis_url}: {exc}"
            ) from exc

    if redis_url:
        try:
            import redis
            client = redis.from_url(redis_url)
            client.ping()
            return client
        except Exception:
            return None

    return None


def get_rate_limiter() -> BaseRateLimiter:
    global _default
    if _default is None:
        from app.config import get_settings

        settings = get_settings()
        client = _get_redis_client()

        if client is not None:
            _default = RedisRateLimiter(
                client, settings.submission_rate_limit, settings.submission_rate_window_s
            )
        else:
            _default = InMemoryRateLimiter(
                settings.submission_rate_limit, settings.submission_rate_window_s
            )
    return _default


def get_tutor_rate_limiter() -> BaseRateLimiter:
    global _tutor_limiter
    if _tutor_limiter is None:
        from app.config import get_settings

        settings = get_settings()
        client = _get_redis_client()
        limit = int(os.getenv("TUTOR_RATE_LIMIT", str(settings.tutor_rate_limit)))
        window = int(os.getenv("TUTOR_RATE_WINDOW_S", str(settings.tutor_rate_window_s)))
        if client is not None:
            _tutor_limiter = RedisRateLimiter(client, limit, window)
        else:
            _tutor_limiter = InMemoryRateLimiter(limit, window)
    return _tutor_limiter


def get_coach_rate_limiter() -> BaseRateLimiter:
    global _coach_limiter
    if _coach_limiter is None:
        from app.config import get_settings

        settings = get_settings()
        client = _get_redis_client()
        limit = int(os.getenv("COACH_RATE_LIMIT", str(settings.coach_rate_limit)))
        window = int(os.getenv("COACH_RATE_WINDOW_S", str(settings.coach_rate_window_s)))
        if client is not None:
            _coach_limiter = RedisRateLimiter(client, limit, window)
        else:
            _coach_limiter = InMemoryRateLimiter(limit, window)
    return _coach_limiter


def get_run_rate_limiter() -> BaseRateLimiter:
    global _run_limiter
    if _run_limiter is None:
        from app.config import get_settings

        settings = get_settings()
        client = _get_redis_client()
        limit = settings.run_rate_limit
        window = settings.run_rate_window_s
        if client is not None:
            _run_limiter = RedisRateLimiter(client, limit, window)
        else:
            _run_limiter = InMemoryRateLimiter(limit, window)
    return _run_limiter


def get_generate_rate_limiter() -> BaseRateLimiter:
    global _generate_limiter
    if _generate_limiter is None:
        from app.config import get_settings

        settings = get_settings()
        client = _get_redis_client()
        limit = int(os.getenv("GENERATE_RATE_LIMIT", str(settings.generate_rate_limit)))
        window = int(os.getenv("GENERATE_RATE_WINDOW_S", str(settings.generate_rate_window_s)))
        if client is not None:
            _generate_limiter = RedisRateLimiter(client, limit, window)
        else:
            _generate_limiter = InMemoryRateLimiter(limit, window)
    return _generate_limiter


def get_sap_execution_rate_limiter() -> BaseRateLimiter:
    global _sap_execution_limiter
    if _sap_execution_limiter is None:
        from app.config import get_settings

        settings = get_settings()
        client = _get_redis_client()
        limit = int(os.getenv("SAP_EXECUTION_RATE_LIMIT", "30"))
        window = int(os.getenv("SAP_EXECUTION_RATE_WINDOW_S", "60"))
        if client is not None:
            _sap_execution_limiter = RedisRateLimiter(client, limit, window)
        else:
            _sap_execution_limiter = InMemoryRateLimiter(limit, window)
    return _sap_execution_limiter


# =============================================================================
# Authentication rate-limit policies
# =============================================================================

# policy name -> (Settings attribute for the limit, Settings attribute for the window)
AUTH_RATE_LIMIT_POLICIES: dict[str, tuple[str, str]] = {
    "auth_login_ip": ("auth_login_ip_limit", "auth_login_ip_window_s"),
    "auth_login_account": ("auth_login_account_limit", "auth_login_account_window_s"),
    "auth_register_ip": ("auth_register_ip_limit", "auth_register_ip_window_s"),
    "auth_google_ip": ("auth_google_ip_limit", "auth_google_ip_window_s"),
    "auth_google_identity": ("auth_google_identity_limit", "auth_google_identity_window_s"),
}

_policy_limiters: dict[str, BaseRateLimiter] = {}
_policy_lock = threading.Lock()


def get_policy_rate_limiter(policy: str) -> BaseRateLimiter:
    """Limiter for a named policy; Redis-backed when available, same fallback as the rest."""
    with _policy_lock:
        limiter = _policy_limiters.get(policy)
        if limiter is None:
            from app.config import get_settings

            settings = get_settings()
            limit_attr, window_attr = AUTH_RATE_LIMIT_POLICIES[policy]
            limit, window = getattr(settings, limit_attr), getattr(settings, window_attr)
            client = _get_redis_client()
            limiter = (
                RedisRateLimiter(client, limit, window) if client is not None
                else InMemoryRateLimiter(limit, window)
            )
            _policy_limiters[policy] = limiter
        return limiter


def reset_policy_rate_limiters() -> None:
    """Empty and drop all policy limiters (tests / settings reload); rebuilt on next use."""
    with _policy_lock:
        for policy, limiter in _policy_limiters.items():
            try:
                limiter.reset(None)
            except Exception:
                pass
        _policy_limiters.clear()
