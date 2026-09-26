"""Client-IP resolution for rate limiting: trust model and spoofing resistance."""

from __future__ import annotations

import uuid

import pytest
from fastapi.testclient import TestClient
from starlette.requests import Request

from app.api.deps import get_db
from app.config import Settings, get_settings
from app.core.client_ip import parse_cidrs, parse_ip, rate_limit_key, resolve_client_ip
from app.main import app
from app.services import ratelimit

SECRET = "s" * 48
RENDER_PEER = "10.201.4.7"          # an internal platform proxy address
TRUSTED = parse_cidrs("10.0.0.0/8, fd00::/8")


def req(peer: str | None, headers: dict[str, str] | list[tuple[str, str]] | None = None) -> Request:
    items = headers.items() if isinstance(headers, dict) else (headers or [])
    scope = {
        "type": "http", "method": "POST", "path": "/api/auth/login",
        "headers": [(k.lower().encode(), v.encode()) for k, v in items],
        "client": (peer, 5555) if peer is not None else None,
    }
    return Request(scope)


def resolve(peer, headers=None, *, secret=None, trusted=()):
    return resolve_client_ip(req(peer, headers), proxy_secret=secret, trusted_proxies=list(trusted))


def attest(ip, secret=SECRET, extra=None):
    return {"X-CodeMentor-Client-IP": ip, "X-CodeMentor-Proxy-Auth": secret, **(extra or {})}


# =============================================================================
# Parsing & normalization
# =============================================================================

@pytest.mark.parametrize("raw,expected", [
    ("203.0.113.9", "203.0.113.9"),
    (" 203.0.113.9 ", "203.0.113.9"),
    ("203.0.113.9:4431", "203.0.113.9"),
    ("::ffff:203.0.113.9", "203.0.113.9"),          # IPv4-mapped IPv6 == the IPv4 address
    ("2001:DB8::0:1", "2001:db8::/64"),             # canonical text, /64 bucket
    ("[2001:db8::1]:443", "2001:db8::/64"),
    ("fe80::1%eth0", "fe80::/64"),
    ('"198.51.100.1"', "198.51.100.1"),
])
def test_equivalent_addresses_normalize_to_one_key(raw, expected):
    assert rate_limit_key(parse_ip(raw)) == expected


@pytest.mark.parametrize("raw", [
    "", "unknown", "256.1.1.1", "1.2.3", "2001:db8::zz", "[2001:db8::1", "a" * 100,
    "1.2.3.4, 5.6.7.8", "<script>", "localhost",
])
def test_malformed_values_do_not_parse(raw):
    assert parse_ip(raw) is None


def test_ipv6_hosts_in_one_slash64_share_a_bucket_but_not_across_prefixes():
    a, b, c = (rate_limit_key(parse_ip(x)) for x in ("2001:db8:1:2::1", "2001:db8:1:2:ffff::9", "2001:db8:1:3::1"))
    assert a == b != c


# =============================================================================
# Trust algorithm
# =============================================================================

def test_direct_client_without_forwarding_headers_uses_socket_peer():
    assert resolve("198.51.100.20") == ("198.51.100.20", "peer")
    assert resolve("2001:db8:5::7") == ("2001:db8:5::/64", "peer")


def test_forwarding_headers_from_an_untrusted_peer_are_ignored():
    headers = {"X-Forwarded-For": "1.1.1.1", "X-Real-IP": "2.2.2.2", "CF-Connecting-IP": "3.3.3.3",
               "True-Client-IP": "4.4.4.4", "Forwarded": "for=5.5.5.5"}
    assert resolve("198.51.100.20", headers, trusted=TRUSTED) == ("198.51.100.20", "peer")


def test_attested_client_ip_is_used_only_with_the_correct_secret():
    assert resolve(RENDER_PEER, attest("203.0.113.50"), secret=SECRET) == ("203.0.113.50", "attested")
    assert resolve(RENDER_PEER, attest("203.0.113.50", secret="wrong"), secret=SECRET) == (RENDER_PEER, "peer")
    assert resolve(RENDER_PEER, attest("203.0.113.50", secret=SECRET[:-1]), secret=SECRET) == (RENDER_PEER, "peer")
    # Backend without a configured secret never trusts the header.
    assert resolve(RENDER_PEER, attest("203.0.113.50"), secret=None) == (RENDER_PEER, "peer")


def test_attested_ipv6_client():
    assert resolve(RENDER_PEER, attest("2001:db8:aa:bb::5"), secret=SECRET) == ("2001:db8:aa:bb::/64", "attested")


def test_attested_but_malformed_ip_falls_back_to_peer():
    for bad in ("not-an-ip", "", "1.2.3.4, 5.6.7.8"):
        assert resolve(RENDER_PEER, attest(bad), secret=SECRET) == (RENDER_PEER, "peer")


def test_a_wrong_secret_does_not_fall_through_to_forwarded_headers():
    headers = attest("203.0.113.50", secret="wrong", extra={"X-Forwarded-For": "203.0.113.60"})
    assert resolve(RENDER_PEER, headers, secret=SECRET, trusted=TRUSTED) == (RENDER_PEER, "peer")


def test_legitimate_trusted_proxy_chain():
    # client -> proxy A (10.0.0.2) -> proxy B (peer 10.0.0.3)
    assert resolve("10.0.0.3", {"X-Forwarded-For": "198.51.100.77, 10.0.0.2"}, trusted=TRUSTED) \
        == ("198.51.100.77", "forwarded")


def test_multiple_trusted_hops_including_ipv6():
    headers = {"X-Forwarded-For": "2001:db8:9::1, 10.1.1.1, fd00::5, 10.2.2.2"}
    assert resolve("10.3.3.3", headers, trusted=TRUSTED) == ("2001:db8:9::/64", "forwarded")


def test_attacker_prepended_entries_are_never_read():
    # Attacker sends "X-Forwarded-For: 1.1.1.1, 2.2.2.2"; the trusted proxy appends the real IP.
    headers = {"X-Forwarded-For": "1.1.1.1, 2.2.2.2, 198.51.100.88"}
    assert resolve("10.0.0.3", headers, trusted=TRUSTED) == ("198.51.100.88", "forwarded")
    # Attacker also prepends an address inside the trusted range: still ignored.
    headers = {"X-Forwarded-For": "10.9.9.9, 198.51.100.88"}
    assert resolve("10.0.0.3", headers, trusted=TRUSTED) == ("198.51.100.88", "forwarded")


def test_repeated_forwarded_headers_are_read_as_one_chain():
    headers = [("X-Forwarded-For", "1.1.1.1"), ("X-Forwarded-For", "198.51.100.3, 10.0.0.2")]
    assert resolve("10.0.0.3", headers, trusted=TRUSTED) == ("198.51.100.3", "forwarded")


@pytest.mark.parametrize("chain", ["198.51.100.1, garbage", "198.51.100.1, , 10.0.0.2", "999.1.1.1"])
def test_malformed_chain_falls_back_to_socket_peer(chain):
    assert resolve("10.0.0.3", {"X-Forwarded-For": chain}, trusted=TRUSTED) == ("10.0.0.3", "peer")


def test_trusted_peer_without_forwarded_header_is_the_peer():
    assert resolve("10.0.0.3", {}, trusted=TRUSTED) == ("10.0.0.3", "peer")


def test_non_ip_socket_peer_is_kept_verbatim():
    assert resolve("testclient") == ("testclient", "peer")
    assert resolve(None) == ("unknown", "peer")


# =============================================================================
# Configuration
# =============================================================================

def test_short_secret_and_bad_cidrs_are_rejected():
    with pytest.raises(ValueError, match="PROXY_SHARED_SECRET"):
        Settings(proxy_shared_secret="too-short")
    with pytest.raises(ValueError, match="TRUSTED_PROXY_CIDRS"):
        Settings(trusted_proxy_cidrs="10.0.0.0/8, not-a-cidr")
    assert Settings(proxy_shared_secret="   ").proxy_shared_secret is None


def _production(**overrides):
    base = dict(environment="production", jwt_secret="j" * 40,
                database_url="postgresql+psycopg://u:p@db.internal:5432/app",
                redis_url="redis://redis.internal:6379/0", cors_origins="https://app.example")
    base.update(overrides)
    return Settings(**base)


def test_trust_source_reflects_configuration():
    assert _production().client_ip_trust_source == "socket-peer"
    assert _production(proxy_shared_secret=SECRET).client_ip_trust_source == "attested"
    assert _production(trusted_proxy_cidrs="10.0.0.0/8").client_ip_trust_source == "trusted-cidrs"


def test_production_without_trust_source_boots_but_logs_an_error(monkeypatch, caplog):
    """Not fatal (a missing secret must not become an outage) but impossible to miss."""
    import asyncio
    import logging

    import app.main as main

    monkeypatch.setattr(main, "settings", _production())
    monkeypatch.setattr(main.engine, "connect", lambda: _NoopConn())
    with caplog.at_level(logging.ERROR):
        async def run():
            async with main.lifespan(main.app):
                pass
        asyncio.run(run())
    assert any("PROXY_SHARED_SECRET" in r.getMessage() for r in caplog.records)

    caplog.clear()
    monkeypatch.setattr(main, "settings", _production(proxy_shared_secret=SECRET))
    with caplog.at_level(logging.ERROR):
        asyncio.run(run())
    assert not any("PROXY_SHARED_SECRET" in r.getMessage() for r in caplog.records)


class _NoopConn:
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def execute(self, *a, **k):
        return None


def test_development_needs_no_proxy_configuration():
    s = Settings(environment="development")
    assert s.proxy_shared_secret is None and s.trusted_proxy_cidrs == ""


# =============================================================================
# End to end through the auth rate limiter
# =============================================================================

@pytest.fixture
def client(db, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "proxy_shared_secret", SECRET)
    monkeypatch.setattr(settings, "auth_login_ip_limit", 3)
    monkeypatch.setattr(settings, "auth_login_account_limit", 1000)
    ratelimit.reset_policy_rate_limiters()
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def _login(client, headers):
    return client.post("/api/auth/login", headers=headers,
                       json={"identifier": f"nobody-{uuid.uuid4().hex[:8]}", "password": "x"}).status_code


def test_two_real_users_behind_the_production_proxy_get_separate_buckets(client):
    alice, bob = attest("203.0.113.10"), attest("2001:db8:77::10")
    assert [_login(client, alice) for _ in range(4)] == [401, 401, 401, 429]
    assert _login(client, bob) == 401  # unaffected by Alice's exhaustion


def test_same_user_cannot_evade_throttling_with_spoofed_headers(client):
    me = attest("203.0.113.20")
    assert [_login(client, me) for _ in range(3)] == [401, 401, 401]
    evasions = [
        {**me, "X-Forwarded-For": "198.51.100.1"},                    # extra XFF
        {**me, "X-Real-IP": "198.51.100.2", "CF-Connecting-IP": "198.51.100.3"},
        attest("::ffff:203.0.113.20"),                                 # IPv4-mapped form
        attest(" 203.0.113.20:9999 "),                                 # port / whitespace
    ]
    assert [_login(client, h) for h in evasions] == [429] * 4
    # Forging the attestation without the secret lands in the peer bucket, not a fresh one.
    forged = attest("198.51.100.99", secret="guess")
    assert [_login(client, forged) for _ in range(4)] == [401, 401, 401, 429]


def test_ipv6_user_cannot_evade_by_rotating_within_their_slash64(client):
    codes = [_login(client, attest(f"2001:db8:5:6::{i:x}")) for i in range(1, 5)]
    assert codes == [401, 401, 401, 429]
