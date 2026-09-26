"""Batch 4: auth rate limiting, Google username safety, request body-size limits."""

from __future__ import annotations

import json
import threading
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.config import get_settings
from app.core.request_limits import BODY_LIMITS, BodySizeLimitMiddleware, body_limit_for
from app.database import get_db
from app.main import app
from app.models.models import User
from app.services import google_accounts, ratelimit
from app.services.google_accounts import resolve_google_user, username_base
from app.services.ratelimit import RedisRateLimiter

PASSWORD = "CorrectHorse9!"


# =============================================================================
# Fixtures & helpers
# =============================================================================

@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def limits(monkeypatch):
    """Override auth limits for a test (limiters are rebuilt from settings on first use)."""
    settings = get_settings()

    def _set(**values):
        for key, value in values.items():
            monkeypatch.setattr(settings, key, value)
        ratelimit.reset_policy_rate_limiters()

    return _set


@pytest.fixture
def per_ip(monkeypatch):
    """Trust one proxy hop so tests can present distinct client IPs via X-Forwarded-For."""
    monkeypatch.setattr(get_settings(), "trusted_proxy_hops", 1)
    return lambda ip: {"X-Forwarded-For": ip}


def register(client, username, headers=None, **extra):
    return client.post("/api/auth/register", headers=headers or {},
                       json={"username": username, "password": PASSWORD, **extra})


def login(client, identifier, password=PASSWORD, headers=None):
    return client.post("/api/auth/login", headers=headers or {},
                       json={"identifier": identifier, "password": password})


def user_count(db) -> int:
    db.expire_all()
    return db.execute(select(func.count()).select_from(User)).scalar_one()


def uname(prefix="u") -> str:
    return f"{prefix}{uuid.uuid4().hex[:10]}"


def assert_429(res):
    assert res.status_code == 429, res.text
    assert int(res.headers["retry-after"]) >= 1
    assert "set-cookie" not in res.headers
    assert res.json()["detail"] == "Too many attempts. Please wait before trying again."


# =============================================================================
# 1. Authentication rate limiting
# =============================================================================

def test_repeated_failed_login_is_throttled_per_account(client, db, limits):
    limits(auth_login_account_limit=5, auth_login_ip_limit=100)
    name = uname()
    assert register(client, name).status_code == 200
    for _ in range(5):
        assert login(client, name, "wrong-password").status_code == 401
    # Even the correct password is refused once the bucket is exhausted: no session.
    assert_429(login(client, name))


def test_repeated_successful_login_is_also_throttled(client, db, limits):
    limits(auth_login_account_limit=3, auth_login_ip_limit=100)
    name = uname()
    register(client, name)
    for _ in range(3):
        assert login(client, name).status_code == 200
    assert_429(login(client, name))


def test_limit_behaviour_does_not_reveal_account_existence(client, db, limits):
    limits(auth_login_account_limit=4, auth_login_ip_limit=100)
    real = uname()
    register(client, real)
    ghost = uname("ghost")  # never registered
    real_codes = [login(client, real, "wrong").status_code for _ in range(6)]
    ghost_codes = [login(client, ghost, "wrong").status_code for _ in range(6)]
    assert real_codes == ghost_codes == [401] * 4 + [429] * 2


def test_identifier_is_normalized_for_the_account_bucket(client, db, limits):
    limits(auth_login_account_limit=2, auth_login_ip_limit=100)
    name = uname()
    register(client, name)
    login(client, name.upper(), "x")
    login(client, f"  {name}  ", "x")
    assert_429(login(client, name))


def test_per_user_isolation(client, db, limits):
    limits(auth_login_account_limit=3, auth_login_ip_limit=100)
    alice, bob = uname("alice"), uname("bob")
    register(client, alice)
    register(client, bob)
    for _ in range(3):
        login(client, alice, "wrong")
    assert_429(login(client, alice))
    assert login(client, bob).status_code == 200  # same IP, different account


def test_per_ip_isolation_and_spoof_resistance(client, db, limits, per_ip):
    limits(auth_login_ip_limit=3, auth_login_account_limit=100)
    name = uname()
    register(client, name, headers=per_ip("198.51.100.9"))
    for _ in range(3):
        login(client, uname("x"), "x", headers=per_ip("203.0.113.1"))
    assert_429(login(client, name, headers=per_ip("203.0.113.1")))
    assert login(client, name, headers=per_ip("203.0.113.2")).status_code == 200
    # A client-supplied left-most entry cannot choose the bucket: the trusted hop wins.
    spoofed = {"X-Forwarded-For": "10.9.9.9, 203.0.113.1"}
    assert_429(login(client, name, headers=spoofed))


def test_without_trusted_proxies_forwarded_header_is_ignored(client, db, limits):
    limits(auth_login_ip_limit=2, auth_login_account_limit=100)
    for i in range(2):
        login(client, uname(), "x", headers={"X-Forwarded-For": f"192.0.2.{i}"})
    assert_429(login(client, uname(), "x", headers={"X-Forwarded-For": "192.0.2.99"}))


def test_registration_abuse_is_throttled_per_ip_with_no_account_created(client, db, limits, per_ip):
    limits(auth_register_ip_limit=3)
    for _ in range(3):
        assert register(client, uname(), headers=per_ip("203.0.113.5")).status_code == 200
    before = user_count(db)
    blocked = uname()
    assert_429(register(client, blocked, headers=per_ip("203.0.113.5")))
    assert user_count(db) == before
    assert db.execute(select(User).where(User.username == blocked)).first() is None
    assert register(client, uname(), headers=per_ip("203.0.113.6")).status_code == 200


def test_window_expiry_restores_access(client, db, limits, monkeypatch):
    limits(auth_login_account_limit=2, auth_login_account_window_s=60, auth_login_ip_limit=100)
    clock = {"t": 1_000.0}
    monkeypatch.setattr(ratelimit.time, "monotonic", lambda: clock["t"])
    name = uname()
    register(client, name)
    login(client, name, "x")
    login(client, name, "x")
    res = login(client, name)
    assert_429(res)
    assert int(res.headers["retry-after"]) <= 61
    clock["t"] += 61
    assert login(client, name).status_code == 200


class _BrokenRedis:
    """A Redis client whose every operation fails like a dropped connection."""

    def pipeline(self):
        raise ConnectionError("Error 10061 connecting to redis-internal.svc:6379. Connection refused.")

    def __getattr__(self, name):
        def fail(*a, **k):
            raise ConnectionError("redis down")
        return fail


@pytest.mark.parametrize("policy,call", [
    ("auth_login_ip", lambda c: login(c, "someone", "x")),
    ("auth_register_ip", lambda c: register(c, uname())),
])
def test_redis_unavailable_fails_closed_without_leaking_details(client, db, policy, call):
    ratelimit.get_policy_rate_limiter(policy)  # build, then swap in a broken backend
    ratelimit._policy_limiters[policy] = RedisRateLimiter(_BrokenRedis(), 5, 60)
    before = user_count(db)
    res = call(client)
    assert res.status_code == 503
    assert res.headers["retry-after"] == "5"
    assert "redis" not in res.text.lower() and "6379" not in res.text
    assert "set-cookie" not in res.headers
    assert user_count(db) == before


def test_auth_policies_work_against_live_redis(client, db):
    """The same policies run on the shared Redis backend (namespaced keys)."""
    import redis

    live = redis.from_url("redis://localhost:6379/0")
    live.ping()  # the verification stack includes Redis: fail, don't skip, if absent
    limiter = RedisRateLimiter(live, 2, 60)
    ratelimit._policy_limiters["auth_register_ip"] = limiter
    try:
        assert register(client, uname()).status_code == 200
        assert register(client, uname()).status_code == 200
        assert_429(register(client, uname()))
        assert any(k.startswith(b"ratelimit:auth_register_ip:") for k in live.scan_iter("ratelimit:auth_register_ip:*"))
    finally:
        for k in live.scan_iter("ratelimit:auth_register_ip:*"):
            live.delete(k)


# =============================================================================
# 2. Google sign-in: rate limits and username safety
# =============================================================================

def google_claims(email, sub=None, name="Alex"):
    return {"email": email, "sub": sub or f"sub-{uuid.uuid4().hex}", "name": name,
            "email_verified": True, "iss": "accounts.google.com"}


@pytest.fixture
def google_as(monkeypatch):
    """Makes /api/auth/google accept a fake token whose claims the test chooses."""
    state = {}

    def fake_verify(token):
        from app.core.security import AuthError
        if token == "bad":
            raise AuthError("invalid Google ID token: Wrong number of segments in token: b'bad'")
        return state[token]

    monkeypatch.setattr("app.api.routes.auth.verify_google_id_token", fake_verify)

    def _register(token, claims):
        state[token] = claims
        return token
    return _register


def google_login(client, token, headers=None):
    return client.post("/api/auth/google", json={"id_token": token}, headers=headers or {})


def test_google_abuse_is_throttled_per_ip_before_token_verification(client, db, limits, per_ip, monkeypatch):
    limits(auth_google_ip_limit=3)
    calls = []
    from app.core.security import AuthError

    def verify(token):
        calls.append(token)
        raise AuthError("bad")
    monkeypatch.setattr("app.api.routes.auth.verify_google_id_token", verify)
    for _ in range(3):
        assert google_login(client, "x", per_ip("203.0.113.7")).status_code == 401
    assert_429(google_login(client, "x", per_ip("203.0.113.7")))
    assert len(calls) == 3  # the throttled request never reached verification
    assert google_login(client, "x", per_ip("203.0.113.8")).status_code == 401


def test_google_identity_is_throttled_across_ips(client, db, limits, per_ip, google_as):
    limits(auth_google_identity_limit=2, auth_google_ip_limit=100)
    tok = google_as("t", google_claims(f"{uname()}@gmail.com"))
    assert google_login(client, tok, per_ip("203.0.113.10")).status_code == 200
    assert google_login(client, tok, per_ip("203.0.113.11")).status_code == 200
    assert_429(google_login(client, tok, per_ip("203.0.113.12")))


def test_same_local_part_different_domains_get_distinct_accounts(client, db, google_as):
    local = uname("alex")
    a = google_login(client, google_as("a", google_claims(f"{local}@gmail.com", "sub-a"))).json()["user"]
    b = google_login(client, google_as("b", google_claims(f"{local}@outlook.com", "sub-b"))).json()["user"]
    assert a["id"] != b["id"]
    assert a["username"] == local
    assert b["username"].startswith(f"{local}-") and b["username"] != local
    assert a["email"] == f"{local}@gmail.com" and b["email"] == f"{local}@outlook.com"


def test_collision_with_password_account_never_touches_it(client, db, google_as):
    local = uname("sam")
    assert register(client, local, email=f"{local}@corp.example").status_code == 200
    owner = db.execute(select(User).where(User.username == local)).scalar_one()
    snapshot = (owner.email, owner.pwd_hash, owner.salt, owner.google_sub, owner.name)

    res = google_login(client, google_as("g", google_claims(f"{local}@gmail.com", "sub-sam")))
    assert res.status_code == 200
    assert res.json()["user"]["id"] != str(owner.id)
    assert res.json()["user"]["username"] != local
    db.refresh(owner)
    assert (owner.email, owner.pwd_hash, owner.salt, owner.google_sub, owner.name) == snapshot
    assert login(client, local).status_code == 200  # password owner still signs in


def test_multiple_sequential_collisions_are_deterministic(db):
    local = uname("kim")
    sub = "sub-kim-4"
    import hashlib
    digest = hashlib.sha256(sub.encode()).hexdigest()
    for taken in (local, f"{local}-{digest[:4]}", f"{local}-{digest[:6]}"):
        db.add(User(email=f"{taken}@other.example", username=taken, name="x"))
    db.commit()
    user = resolve_google_user(db, google_claims(f"{local}@gmail.com", sub))
    assert user.username == f"{local}-{digest[:8]}"


def test_existing_google_user_keeps_account_and_username(client, db, google_as):
    local = uname("lee")
    tok = google_as("l", google_claims(f"{local}@gmail.com", "sub-lee"))
    first = google_login(client, tok).json()["user"]
    # A colliding newcomer arrives in between.
    google_login(client, google_as("n", google_claims(f"{local}@yahoo.com", "sub-new")))
    again = google_login(client, tok).json()["user"]
    assert again["id"] == first["id"] and again["username"] == first["username"] == local


def test_invalid_google_payloads_create_nothing(client, db, google_as):
    before = user_count(db)
    res = google_login(client, "bad")
    assert res.status_code == 401
    assert res.json()["detail"] == "Google sign-in failed. Please try again."
    assert "segments" not in res.text
    for claims in ({"sub": "s1"}, {"email": "x@gmail.com"}, {"email": "no-at-sign", "sub": "s2"},
                   {"email": "", "sub": ""}):
        assert google_login(client, google_as(f"c{len(claims)}{claims.get('sub','')}", claims)).status_code == 401
    assert user_count(db) == before


def test_email_bound_to_another_google_identity_is_not_merged(client, db, google_as):
    email = f"{uname('pat')}@gmail.com"
    first = google_login(client, google_as("p1", google_claims(email, "sub-original"))).json()["user"]
    res = google_login(client, google_as("p2", google_claims(email, "sub-intruder")))
    assert res.status_code == 409
    owner = db.execute(select(User).where(User.id == uuid.UUID(first["id"]))).scalar_one()
    assert owner.google_sub == "sub-original"


def test_username_base_sanitizes_local_parts():
    assert username_base("Alex.Smith+tag@gmail.com") == "alex.smithtag"
    assert username_base("jo@x.com") == "jo-user"
    assert username_base("é@x.com") == "user"
    assert len(username_base("a" * 80 + "@x.com")) <= 17


# ---- PostgreSQL concurrency ----------------------------------------------------

@pytest.fixture
def committed_cleanup(engine, migrated):
    emails: list[str] = []
    yield emails
    with Session(engine) as s:
        s.execute(User.__table__.delete().where(User.email.in_(emails)))
        s.commit()


def _race_signups(engine, claims_list, monkeypatch):
    """Runs resolve_google_user concurrently; both threads reach their first INSERT together."""
    barrier = threading.Barrier(len(claims_list))
    local = threading.local()
    original = Session.begin_nested

    def synced_begin_nested(self, *a, **k):
        if not getattr(local, "synced", False):
            local.synced = True
            barrier.wait(timeout=30)
        return original(self, *a, **k)

    monkeypatch.setattr(Session, "begin_nested", synced_begin_nested)
    results: list = [None] * len(claims_list)

    def worker(i):
        with Session(engine) as s:
            try:
                u = resolve_google_user(s, claims_list[i])
                results[i] = (str(u.id), u.username, u.email)
            except Exception as exc:  # surfaced below
                results[i] = exc

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(len(claims_list))]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=60)
    return results


def test_concurrent_colliding_signups_get_distinct_usernames(engine, committed_cleanup, monkeypatch):
    local = uname("race")
    claims = [google_claims(f"{local}@gmail.com", f"sub-{local}-1"),
              google_claims(f"{local}@outlook.com", f"sub-{local}-2")]
    committed_cleanup.extend(c["email"] for c in claims)
    results = _race_signups(engine, claims, monkeypatch)
    assert not [r for r in results if isinstance(r, Exception)], results
    ids, names = {r[0] for r in results}, {r[1] for r in results}
    assert len(ids) == 2 and len(names) == 2 and local in names


def test_concurrent_same_identity_signups_resolve_to_one_account(engine, committed_cleanup, monkeypatch):
    local = uname("twin")
    claims = google_claims(f"{local}@gmail.com", f"sub-{local}")
    committed_cleanup.append(claims["email"])
    results = _race_signups(engine, [claims, dict(claims)], monkeypatch)
    assert not [r for r in results if isinstance(r, Exception)], results
    assert results[0] == results[1]
    with Session(engine) as s:
        assert s.execute(select(func.count()).select_from(User).where(User.email == claims["email"])).scalar_one() == 1


# =============================================================================
# 3. Request body-size limits
# =============================================================================

def test_route_categories_are_explicit():
    expected = {
        "/api/auth/login": "auth", "/api/auth/register": "auth", "/api/auth/google": "auth",
        "/api/tutor/chat": "tutor", "/api/learning/tutor/chat": "tutor",
        "/api/learning/tutor/quick-action": "tutor", "/api/coach/debrief": "coach",
        "/api/problems/generate": "generation", "/api/problems/recommend": "generation",
        "/api/submissions": "code_execution", "/api/submissions/run": "code_execution",
        "/api/submissions/run-custom": "code_execution", "/api/learning/run": "code_execution",
        "/api/sap/execution/validate": "sap_execution", "/api/sap/placement/submit": "default",
    }
    assert {p: body_limit_for(p).category for p in expected} == expected
    assert BODY_LIMITS["auth"] < BODY_LIMITS["tutor"] < BODY_LIMITS["coach"]


def _padded_json(fields: dict, pad_key: str, total_bytes: int) -> bytes:
    """A valid JSON object of exactly total_bytes by padding one string field."""
    doc = dict(fields, **{pad_key: ""})
    base = len(json.dumps(doc).encode())
    doc[pad_key] = "a" * (total_bytes - base)
    raw = json.dumps(doc).encode()
    assert len(raw) == total_bytes
    return raw


class Sentinel:
    def __init__(self):
        self.calls = 0

    def __call__(self, *a, **k):
        self.calls += 1
        raise AssertionError("expensive downstream work was reached")


@pytest.fixture
def expensive(monkeypatch):
    """Sentinels on every expensive step behind the size limit."""
    s = {name: Sentinel() for name in ("hash", "verify", "google", "llm", "generate", "sandbox", "rate")}
    monkeypatch.setattr("app.api.routes.auth.hash_password", s["hash"])
    monkeypatch.setattr("app.api.routes.auth.verify_password", s["verify"])
    monkeypatch.setattr("app.api.routes.auth.verify_google_id_token", s["google"])
    monkeypatch.setattr("app.api.routes.tutor.get_llm_client", s["llm"])
    monkeypatch.setattr("app.services.problem_generator.generate_and_validate_problem", s["generate"])
    monkeypatch.setattr("app.api.routes.submissions.svc.execute_async", s["sandbox"])
    monkeypatch.setattr("app.api.rate_limit.get_policy_rate_limiter", s["rate"])
    return s


FIVE_MB = 5 * 1024 * 1024


@pytest.mark.parametrize("path,payload", [
    ("/api/auth/login", {"identifier": "x" * FIVE_MB, "password": "p"}),
    ("/api/auth/register", {"username": "u" * FIVE_MB, "password": "p" * 10}),
    ("/api/auth/google", {"id_token": "t" * FIVE_MB}),
    ("/api/tutor/chat", {"message": "hi", "problem_id": None, "context": [{"x": ["y" * 1024] * 200}]}),
    ("/api/learning/tutor/chat", {"message": "hi", "history": [{"role": "user", "content": "z" * 4096}] * 64,
                                  "step_context": {"nested": [{"deep": "q" * 2048}] * 64}}),
    ("/api/learning/tutor/quick-action", {"action": "hint", "step_context": {"k": "v" * 200_000}}),
    ("/api/coach/debrief", {"problem_id": "p", "code": "c" * 600_000}),
    ("/api/problems/generate", {"topic": "t" * 10_000}),
    ("/api/submissions", {"problem_id": str(uuid.uuid4()), "code": "x" * 300_000}),
    ("/api/submissions/run-custom", {"problem_id": "p", "code": "x", "args": ["a" * 300_000]}),
    ("/api/sap/execution/validate", {"provider_type": "simulation", "code_or_payload": "x" * 200_000}),
])
def test_oversized_bodies_rejected_before_any_expensive_work(client, db, expensive, path, payload):
    """Unauthenticated on purpose: 413 (not 401) proves the check runs before auth/DB."""
    before = user_count(db)
    res = client.post(path, json=payload)
    assert res.status_code == 413, (path, res.status_code, res.text[:200])
    assert "too large" in res.json()["detail"]
    assert all(s.calls == 0 for s in expensive.values()), {k: v.calls for k, v in expensive.items()}
    assert user_count(db) == before


def test_positive_control_sentinels_do_fire_for_normal_requests(client, db, expensive):
    """Guards the test above against being vacuous."""
    with pytest.raises(AssertionError, match="expensive downstream work"):
        client.post("/api/auth/register", json={"username": uname(), "password": "p" * 10})
    assert expensive["rate"].calls == 1


def test_exactly_at_limit_passes_and_one_byte_over_is_rejected(client, db):
    limit = BODY_LIMITS["auth"]
    at = _padded_json({"password": "x"}, "identifier", limit)
    over = _padded_json({"password": "x"}, "identifier", limit + 1)
    headers = {"content-type": "application/json"}
    assert client.post("/api/auth/login", content=at, headers=headers).status_code == 401
    assert client.post("/api/auth/login", content=over, headers=headers).status_code == 413


def test_limits_are_bytes_not_characters(client, db):
    limit = BODY_LIMITS["auth"]
    emoji = "😀"  # 1 character, 4 UTF-8 bytes
    chars = limit // 3  # well under the limit in characters, ~1.3x over in bytes
    body = json.dumps({"identifier": "u", "password": emoji * chars}, ensure_ascii=False).encode()
    assert len(emoji * chars) < limit < len(body)
    res = client.post("/api/auth/login", content=body, headers={"content-type": "application/json"})
    assert res.status_code == 413
    ok_body = json.dumps({"identifier": "ü" * 100, "password": "密码" * 200}, ensure_ascii=False).encode()
    assert len(ok_body) < limit
    assert client.post("/api/auth/login", content=ok_body,
                       headers={"content-type": "application/json"}).status_code == 401


def test_missing_content_length_is_still_counted(client, db):
    def chunks(total, size=4096):
        sent = 0
        yield b'{"identifier": "'
        while sent < total:
            yield b"a" * size
            sent += size
        yield b'", "password": "x"}'

    headers = {"content-type": "application/json"}
    res = client.post("/api/auth/login", content=chunks(64 * 1024), headers=headers)
    assert res.status_code == 413
    small = client.post("/api/auth/login", content=chunks(1024), headers=headers)
    assert small.status_code == 401


def test_forged_content_length_is_not_trusted(client, db):
    big = _padded_json({"password": "x"}, "identifier", BODY_LIMITS["auth"] + 5000)
    res = client.post("/api/auth/login", content=big,
                      headers={"content-type": "application/json", "content-length": "10"})
    assert res.status_code == 413
    small = _padded_json({"password": "x"}, "identifier", 200)
    res = client.post("/api/auth/login", content=small,
                      headers={"content-type": "application/json", "content-length": "10"})
    assert res.status_code == 400


# ---- ASGI-level checks: declared length is rejected without reading the body -----

async def _asgi_call(path, headers, body_chunks, read_guard=False):
    reads = {"n": 0}
    sent: list[dict] = []
    chunks = list(body_chunks)

    async def receive():
        reads["n"] += 1
        if read_guard:
            raise AssertionError("body was read")
        if chunks:
            chunk = chunks.pop(0)
            return {"type": "http.request", "body": chunk, "more_body": bool(chunks)}
        return {"type": "http.disconnect"}

    async def send(message):
        sent.append(message)

    async def downstream(scope, receive_, send_):
        msg = await receive_()
        await send_({"type": "http.response.start", "status": 200, "headers": []})
        await send_({"type": "http.response.body", "body": str(len(msg["body"])).encode()})

    mw = BodySizeLimitMiddleware(downstream)
    scope = {"type": "http", "method": "POST", "path": path, "headers": headers}
    await mw(scope, receive, send)
    return sent[0]["status"], sent[1]["body"], reads["n"]


@pytest.mark.anyio
async def test_declared_oversize_is_rejected_without_reading_the_body():
    status, _, reads = await _asgi_call(
        "/api/auth/login", [(b"content-length", str(FIVE_MB).encode())], [], read_guard=True)
    assert status == 413 and reads == 0


@pytest.mark.anyio
@pytest.mark.parametrize("value", [b"abc", b"-5", b"1e3"])
async def test_malformed_content_length_is_rejected(value):
    status, _, reads = await _asgi_call("/api/auth/login", [(b"content-length", value)], [], read_guard=True)
    assert status == 400 and reads == 0


@pytest.mark.anyio
async def test_body_is_read_once_and_replayed_whole():
    chunks = [b"a" * 1000, b"b" * 1000, b"c" * 500]
    status, body, reads = await _asgi_call("/api/auth/login", [], chunks)
    assert status == 200 and body == b"2500" and reads == 3


@pytest.fixture
def anyio_backend():
    return "asyncio"
