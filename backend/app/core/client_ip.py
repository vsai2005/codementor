"""Client IP resolution for rate limiting.

A forwarded client address is honored ONLY when its source is authenticated; otherwise the
TCP socket peer is used (it cannot be spoofed). Two trusted sources are supported:

1. Proxy attestation (production: Vercel -> Render).
   The Next.js middleware on Vercel copies the client IP that Vercel itself writes (Vercel
   overwrites X-Forwarded-For / x-real-ip, so browsers cannot set it) into
   X-CodeMentor-Client-IP and adds X-CodeMentor-Proxy-Auth = PROXY_SHARED_SECRET. The
   backend honors the IP only if the secret matches (constant-time). The Render URL is
   public and Render's proxy addresses are not published, so neither a hop count nor a
   CIDR list can distinguish Vercel from an attacker calling Render directly; the secret
   can.

2. Trusted reverse proxies by CIDR (generic deployments, e.g. nginx on a private network).
   If the socket peer is inside TRUSTED_PROXY_CIDRS, X-Forwarded-For is walked from the
   right, skipping trusted hops; the first untrusted address is the client. Entries left of
   it are client-controlled and never read. A malformed entry before a client is found
   invalidates the chain and the socket peer is used.

Addresses are normalized (IPv4-mapped IPv6 -> IPv4, zone ids and ports stripped, canonical
text) and IPv6 clients are keyed by their /64, so one host cannot evade limits by rotating
through its own prefix.
"""

from __future__ import annotations

import hmac
import ipaddress
from typing import Iterable, Sequence

from starlette.requests import Request

IPAddress = ipaddress.IPv4Address | ipaddress.IPv6Address
IPNetwork = ipaddress.IPv4Network | ipaddress.IPv6Network

CLIENT_IP_HEADER = "x-codementor-client-ip"
PROXY_AUTH_HEADER = "x-codementor-proxy-auth"
_MAX_HEADER_ENTRIES = 32
_MAX_ENTRY_LEN = 64


def parse_ip(value: str | None) -> IPAddress | None:
    """Parses one address as found in headers or ASGI scope; None if malformed.

    Accepts "1.2.3.4", "1.2.3.4:5678", "2001:db8::1", "[2001:db8::1]:443", "fe80::1%eth0",
    and IPv4-mapped IPv6 (returned as IPv4).
    """
    if not value:
        return None
    text = value.strip().strip('"')
    if not text or len(text) > _MAX_ENTRY_LEN:
        return None
    if text.startswith("["):
        end = text.find("]")
        if end == -1:
            return None
        text = text[1:end]
    elif text.count(":") == 1:  # IPv4 with port
        text = text.split(":", 1)[0]
    text = text.split("%", 1)[0]  # IPv6 zone id
    try:
        addr = ipaddress.ip_address(text)
    except ValueError:
        return None
    if isinstance(addr, ipaddress.IPv6Address) and addr.ipv4_mapped is not None:
        return addr.ipv4_mapped
    return addr


def rate_limit_key(addr: IPAddress) -> str:
    """Canonical bucket id: the IPv4 address, or the IPv6 /64 prefix."""
    if isinstance(addr, ipaddress.IPv6Address):
        return str(ipaddress.IPv6Network((addr, 64), strict=False))
    return str(addr)


def parse_cidrs(spec: str | Iterable[str]) -> list[IPNetwork]:
    """Parses a comma-separated (or iterable) CIDR list; raises ValueError on bad input."""
    items = spec.split(",") if isinstance(spec, str) else list(spec)
    return [ipaddress.ip_network(item.strip(), strict=False) for item in items if item.strip()]


def _in_any(addr: IPAddress, networks: Sequence[IPNetwork]) -> bool:
    return any(addr.version == net.version and addr in net for net in networks)


def _forwarded_chain(request: Request) -> list[str]:
    entries: list[str] = []
    for raw in request.headers.getlist("x-forwarded-for"):
        entries.extend(part.strip() for part in raw.split(","))
    return entries[-_MAX_HEADER_ENTRIES:]


def resolve_client_ip(
    request: Request,
    *,
    proxy_secret: str | None,
    trusted_proxies: Sequence[IPNetwork],
) -> tuple[str, str]:
    """Returns (rate-limit key, source) where source is attested|forwarded|peer."""
    peer_raw = request.client.host if request.client else ""
    peer = parse_ip(peer_raw)
    peer_key = rate_limit_key(peer) if peer else (peer_raw or "unknown")

    presented = request.headers.get(PROXY_AUTH_HEADER)
    if proxy_secret and presented is not None:
        if hmac.compare_digest(presented.encode("utf-8"), proxy_secret.encode("utf-8")):
            attested = parse_ip(request.headers.get(CLIENT_IP_HEADER))
            if attested is not None:
                return rate_limit_key(attested), "attested"
        return peer_key, "peer"

    if trusted_proxies and peer is not None and _in_any(peer, trusted_proxies):
        chain = _forwarded_chain(request)
        for entry in reversed(chain):
            addr = parse_ip(entry)
            if addr is None:
                return peer_key, "peer"  # unverifiable chain: never guess
            if not _in_any(addr, trusted_proxies):
                return rate_limit_key(addr), "forwarded"
        leftmost = parse_ip(chain[0]) if chain else None
        if leftmost is not None:
            return rate_limit_key(leftmost), "forwarded"  # every hop is trusted infrastructure

    return peer_key, "peer"
