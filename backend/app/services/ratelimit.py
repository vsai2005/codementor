"""Rate limiting for LLM-backed endpoints (PRD 5.4 step 1, PRD 6).

This requirement appears in the PRD but in none of the build prompts, so it
would have been silently dropped. 10 submissions / 5 min / user.

Implementation is a sliding window. The in-memory backend is correct for a
single process; on more than one worker each process keeps its own window, so
the effective limit multiplies by the worker count. Redis is the fix and the
interface is the same — do not deploy multi-worker on the in-memory backend
and assume the limit holds.
"""

from __future__ import annotations

import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class RateLimitVerdict:
    allowed: bool
    remaining: int
    retry_after_s: int


class RateLimiter(Protocol):
    def check(self, key: str) -> RateLimitVerdict: ...


class InMemoryRateLimiter:
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


class RedisRateLimiter:
    """Sliding window in Redis — correct across workers and restarts."""

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


_default: RateLimiter | None = None


def get_rate_limiter() -> RateLimiter:
    global _default
    if _default is None:
        from app.config import get_settings

        settings = get_settings()
        _default = InMemoryRateLimiter(
            settings.submission_rate_limit, settings.submission_rate_window_s
        )
    return _default
