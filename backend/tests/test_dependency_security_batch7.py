"""Request parsing and body-limit coverage for patched ASGI dependencies."""

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.core.request_limits import BODY_LIMITS, BodySizeLimitMiddleware, MAX_REJECTION_DRAIN_BYTES
from app.main import app


@pytest.mark.parametrize(
    "path,category",
    [
        ("/api/auth/login", "auth"),
        ("/api/problems/generate", "generation"),
        ("/api/tutor/chat", "tutor"),
        ("/api/coach/debrief", "coach"),
        ("/api/submissions", "code_execution"),
        ("/api/sap/execution/validate", "sap_execution"),
        ("/api/progress", "default"),
    ],
)
def test_multipart_bodies_cannot_bypass_route_size_limits(path, category):
    # Multipart framing itself is below a KiB. The file makes the raw body
    # exceed the selected route's cap, even where the endpoint expects JSON.
    with TestClient(app) as client:
        response = client.post(
            path,
            files={"upload": ("sample.txt", b"x" * BODY_LIMITS[category])},
        )
    assert response.status_code == 413
    assert str(BODY_LIMITS[category]) in response.json()["detail"]


def test_patched_form_parsers_replay_bounded_requests():
    # Current product routes accept JSON, but the pinned parser is part of the
    # FastAPI/Starlette stack. Exercise both encodings behind our ASGI guard.
    probe = FastAPI()
    probe.add_middleware(BodySizeLimitMiddleware)

    @probe.post("/form")
    async def read_form(request: Request):
        form = await request.form()
        return {"field": form["field"]}

    with TestClient(probe) as client:
        urlencoded = client.post(
            "/form", content=b"field=one%3Btwo", headers={"content-type": "application/x-www-form-urlencoded"}
        )
        multipart = client.post("/form", files={"field": (None, "one;two")})
        oversized = client.post("/form", files={"field": (None, "x" * BODY_LIMITS["default"])})

    assert urlencoded.status_code == 200
    assert multipart.status_code == 200
    assert urlencoded.json() == multipart.json() == {"field": "one;two"}
    assert oversized.status_code == 413


def test_real_json_auth_route_does_not_accept_small_form_body():
    with TestClient(app) as client:
        response = client.post(
            "/api/auth/login",
            content=b"identifier=someone&password=secret",
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
    assert response.status_code == 422


def test_oversized_response_does_not_force_connection_close():
    # A streaming reverse proxy must be able to forward the structured 413
    # after this middleware discards a modest declared oversize body.
    with TestClient(app) as client:
        response = client.post(
            "/api/auth/login", json={"identifier": "x" * BODY_LIMITS["auth"], "password": "p"}
        )
    assert response.status_code == 413
    assert response.headers.get("connection") != "close"


@pytest.mark.asyncio
async def test_modest_declared_oversize_is_discarded_without_reaching_route():
    reads = 0
    sent = []
    reached_route = False

    async def receive():
        nonlocal reads
        reads += 1
        return {"type": "http.request", "body": b"x" * 5000, "more_body": reads == 1}

    async def send(message):
        sent.append(message)

    async def route(_scope, _receive, _send):
        nonlocal reached_route
        reached_route = True

    scope = {
        "type": "http", "path": "/api/auth/login",
        "headers": [(b"content-length", b"10000")],
    }
    await BodySizeLimitMiddleware(route)(scope, receive, send)
    assert reads == 2
    assert not reached_route
    assert sent[0]["status"] == 413


@pytest.mark.asyncio
async def test_misdeclared_oversize_discard_has_a_byte_bound():
    reads = 0
    sent = []

    async def receive():
        nonlocal reads
        reads += 1
        return {"type": "http.request", "body": b"x" * (MAX_REJECTION_DRAIN_BYTES + 1), "more_body": True}

    async def send(message):
        sent.append(message)

    scope = {
        "type": "http", "path": "/api/auth/login",
        "headers": [(b"content-length", b"10000")],
    }
    await BodySizeLimitMiddleware(None)(scope, receive, send)
    assert reads == 1
    assert sent[0]["status"] == 413
