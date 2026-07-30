"""Rate limiter tests (PRD 5.4 step 1)."""

import time

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
