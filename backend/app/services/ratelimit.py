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

        return RateLimitVerdict(True, self._limit - count - 1, 0)

    def reset(self, key: str | None = None) -> None:
        if key is None:
            for k in self._redis.scan_iter("ratelimit:*"):
                self._redis.delete(k)
        else:
            self._redis.delete(f"ratelimit:{key}")


_default: BaseRateLimiter | None = None


def get_rate_limiter() -> BaseRateLimiter:
    global _default
    if _default is None:
        from app.config import get_settings

        settings = get_settings()
        redis_url = os.getenv("REDIS_URL")

        if redis_url:
            try:
                import redis
                client = redis.from_url(redis_url)
                _default = RedisRateLimiter(
                    client, settings.submission_rate_limit, settings.submission_rate_window_s
                )
                return _default
            except Exception:
                pass

        _default = InMemoryRateLimiter(
            settings.submission_rate_limit, settings.submission_rate_window_s
        )
    return _default
