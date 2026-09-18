"""Rate limiter tests (PRD 5.4 step 1)."""

import time
import pytest

from app.services.ratelimit import InMemoryRateLimiter


def test_allows_up_to_the_limit_then_blocks():
    rl = InMemoryRateLimiter(limit=3, window_s=60)
    verdicts = [rl.check("alice") for _ in range(4)]

    assert [v.allowed for v in verdicts] == [True, True, True, False]
    assert verdicts[2].remaining == 0
    assert verdicts[3].retry_after_s > 0


def test_users_have_independent_windows():
    rl = InMemoryRateLimiter(limit=2, window_s=60)
    rl.check("alice"); rl.check("alice")

    assert rl.check("alice").allowed is False
    assert rl.check("bob").allowed is True


def test_window_slides_and_frees_capacity():
    rl = InMemoryRateLimiter(limit=2, window_s=1)
    rl.check("alice"); rl.check("alice")
    assert rl.check("alice").allowed is False

    time.sleep(1.1)
    assert rl.check("alice").allowed is True


def test_retry_after_is_bounded_by_the_window():
    rl = InMemoryRateLimiter(limit=1, window_s=300)
    rl.check("alice")
    v = rl.check("alice")
    assert 0 < v.retry_after_s <= 301


def test_concurrent_checks_do_not_exceed_the_limit():
    import threading

    rl = InMemoryRateLimiter(limit=10, window_s=60)
    allowed = []
    lock = threading.Lock()

    def hammer():
        v = rl.check("alice")
        with lock:
            allowed.append(v.allowed)

    threads = [threading.Thread(target=hammer) for _ in range(50)]
    for t in threads: t.start()
    for t in threads: t.join()

    assert sum(allowed) == 10, "limit leaked under concurrency"


def test_redis_rate_limiter_live():
    """Verify distributed rate limiting against the local Docker Redis container."""
    import redis
    from app.services.ratelimit import RedisRateLimiter

    try:
        client = redis.from_url("redis://localhost:6379/0")
        client.ping()
    except Exception as exc:
        pytest.skip(f"Live Redis not reachable: {exc}")

    rl = RedisRateLimiter(client, limit=3, window_s=60)
    rl.reset("test_user_redis")

    verdicts = [rl.check("test_user_redis") for _ in range(4)]
    assert [v.allowed for v in verdicts] == [True, True, True, False]
    assert verdicts[2].remaining == 0
    assert verdicts[3].retry_after_s > 0

    rl.reset("test_user_redis")
    assert rl.check("test_user_redis").allowed is True


def test_production_rate_limiter_fails_fast_without_redis(monkeypatch):
    """In production, missing REDIS_URL or connection failure must raise RuntimeError."""
    from app.config import Settings
    from app.services import ratelimit

    monkeypatch.setattr(ratelimit, "_default", None)

    fake_prod_settings = Settings(
        environment="production",
        jwt_secret="a" * 32,
        database_url="postgresql+psycopg://codementor:pass@remote-db.render.com:5432/codementor",
        redis_url="redis://invalid-host-cannot-connect:6379/0",
    )

    with monkeypatch.context() as m:
        m.setattr("app.config.get_settings", lambda: fake_prod_settings)
        with pytest.raises(RuntimeError) as exc_info:
            ratelimit.get_rate_limiter()
        assert "Production misconfiguration" in str(exc_info.value)

