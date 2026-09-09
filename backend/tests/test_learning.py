"""Unit & regression tests for /api/learning/run execution endpoint."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_learning_run_success():
    payload = {
        "code": "x = 10\ny = 20\nprint(f'sum: {x + y}')",
        "day_number": 1,
    }
    response = client.post("/api/learning/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "sum: 30" in data["stdout"]
    assert data["stderr"] == ""


def test_learning_run_memory_diagnostic():
    payload = {
        "code": (
            "daily_coding_hours = 3.5\n"
            "initial_id = id(daily_coding_hours)\n"
            "daily_coding_hours = daily_coding_hours + 1\n"
            "new_id = id(daily_coding_hours)\n"
            "print(f'rebound: {initial_id != new_id}')"
        ),
        "day_number": 1,
    }
    response = client.post("/api/learning/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "rebound: True" in data["stdout"]


def test_learning_run_syntax_error():
    payload = {
        "code": "x = 10\nif x = 10:\n    print(x)",
        "day_number": 1,
    }
    response = client.post("/api/learning/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert "SyntaxError" in data["stderr"]


def test_learning_run_runtime_exception():
    payload = {
        "code": "x = 10 / 0\nprint(x)",
        "day_number": 1,
    }
    response = client.post("/api/learning/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert "ZeroDivisionError" in data["stderr"]


def test_learning_run_blocked_operation():
    payload = {
        "code": "import os\nos.system('echo dangerous')",
        "day_number": 1,
    }
    response = client.post("/api/learning/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert "blocked" in data["stderr"].lower() or "permission" in data["stderr"].lower()
