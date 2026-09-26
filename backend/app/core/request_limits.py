"""Central request-body size limits.

Every limit is in BYTES of the raw request body (so multi-byte UTF-8 counts fully) and is
enforced by BodySizeLimitMiddleware before routing: oversized requests never reach JSON
parsing, auth lookups, password hashing, DB writes, LLM calls, or the sandbox.

Enforcement does not trust Content-Length: a declared length over the limit is rejected
without reading, and the actual streamed bytes are always counted (chunked, missing, or
understated lengths included). The body is read once, capped at limit + 1 bytes, and
replayed to the app, so the app never re-reads it.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

KiB = 1024

# Category -> maximum body size in bytes.
BODY_LIMITS: dict[str, int] = {
    # Credentials and Google ID tokens (~1-2 KiB). Tiny on purpose.
    "auth": 8 * KiB,
    # Problem generation / recommendation takes a topic and tier only.
    "generation": 4 * KiB,
    # Tutor messages (<= 4000 chars), user code (<= 20000 chars), last-10 history, step context.
    "tutor": 128 * KiB,
    # Coach debrief echoes code plus the full test report (stdout/stderr per case).
    "coach": 512 * KiB,
    # Submissions / runs: code <= 50000 chars (up to 4 bytes each in UTF-8) plus arguments.
    "code_execution": 256 * KiB,
    # SAP validation: route allows 64 KiB code + 16 KiB context after JSON decoding.
    "sap_execution": 160 * KiB,
    # Every other endpoint (small JSON commands: progress, SAP learning, missions, ...).
    "default": 64 * KiB,
}

# (path prefix, category). The longest matching prefix wins.
ROUTE_CATEGORIES: tuple[tuple[str, str], ...] = (
    ("/api/auth/", "auth"),
    ("/api/problems/generate", "generation"),
    ("/api/problems/recommend", "generation"),
    ("/api/tutor/", "tutor"),
    ("/api/learning/tutor/", "tutor"),
    ("/api/coach/", "coach"),
    ("/api/submissions", "code_execution"),
    ("/api/learning/run", "code_execution"),
    ("/api/sap/execution/", "sap_execution"),
)


@dataclass(frozen=True)
class BodyLimit:
    category: str
    max_bytes: int


def body_limit_for(path: str) -> BodyLimit:
    matches = [(prefix, cat) for prefix, cat in ROUTE_CATEGORIES if path.startswith(prefix)]
    category = max(matches, key=lambda m: len(m[0]))[1] if matches else "default"
    return BodyLimit(category, BODY_LIMITS[category])


def _json_response(status: int, detail: str) -> tuple[dict, dict]:
    body = json.dumps({"detail": detail}).encode("utf-8")
    start = {
        "type": "http.response.start",
        "status": status,
        "headers": [
            (b"content-type", b"application/json"),
            (b"content-length", str(len(body)).encode("ascii")),
            (b"connection", b"close"),
        ],
    }
    return start, {"type": "http.response.body", "body": body, "more_body": False}


class BodySizeLimitMiddleware:
    """Pure ASGI middleware enforcing BODY_LIMITS per route category."""

    def __init__(self, app) -> None:
        self.app = app

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        limit = body_limit_for(scope.get("path", ""))

        declared: int | None = None
        raw_lengths = [v for k, v in scope.get("headers", []) if k.lower() == b"content-length"]
        if raw_lengths:
            try:
                values = {int(v.decode("latin-1").strip()) for v in raw_lengths}
            except ValueError:
                await self._reject(send, 400, "Malformed Content-Length header.")
                return
            if len(values) != 1 or min(values) < 0:
                await self._reject(send, 400, "Malformed Content-Length header.")
                return
            declared = values.pop()
            if declared > limit.max_bytes:
                await self._reject_too_large(send, limit)
                return

        # Read the body once, counting real bytes, never buffering past limit + 1.
        chunks: list[bytes] = []
        received = 0
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            chunk = message.get("body", b"")
            received += len(chunk)
            if received > limit.max_bytes:
                await self._reject_too_large(send, limit)
                return
            chunks.append(chunk)
            if not message.get("more_body", False):
                break

        if declared is not None and received != declared:
            await self._reject(send, 400, "Request body does not match Content-Length.")
            return

        body = b"".join(chunks)
        replayed = False

        async def replay_receive():
            nonlocal replayed
            if not replayed:
                replayed = True
                return {"type": "http.request", "body": body, "more_body": False}
            return await receive()

        await self.app(scope, replay_receive, send)

    @staticmethod
    async def _reject(send, status: int, detail: str) -> None:
        start, body = _json_response(status, detail)
        await send(start)
        await send(body)

    async def _reject_too_large(self, send, limit: BodyLimit) -> None:
        await self._reject(
            send, 413,
            f"Request body too large: this endpoint accepts at most {limit.max_bytes} bytes.",
        )
