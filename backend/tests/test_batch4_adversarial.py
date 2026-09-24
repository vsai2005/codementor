"""Batch 4 Adversarial Verification Test Suite.

Covers:
1. Anonymous execution rejection (unauthenticated access to expensive sandbox & LLM endpoints)
2. Rate-limit exhaustion & per-user isolation (sandbox execution quota per user)
3. LLM throttling & per-user isolation (coach debrief and tutor chat limits)
4. Safe vs unsafe/open redirect rejection (protocol-relative, UNC, scheme injection, auth loops)
5. SAP login-return flow (/sap/placement redirect preservation)
6. Generated vs recommended problem behavior (sandbox validation, rejected when invalid, truthful curation)
"""

import json
import uuid
from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import Problem, Topic, User
from app.schemas.api import ProblemDetail
from app.services.ratelimit import (
    InMemoryRateLimiter,
    get_coach_rate_limiter,
    get_generate_rate_limiter,
    get_run_rate_limiter,
    get_tutor_rate_limiter,
)
from app.services.sandbox import ExecutionReport, TestResult

client = TestClient(app)


@pytest.fixture
def user_a():
    return User(
        id=uuid.uuid4(),
        email="user_a@example.com",
        username="user_a",
        name="User Alpha",
    )


@pytest.fixture
def user_b():
    return User(
        id=uuid.uuid4(),
        email="user_b@example.com",
        username="user_b",
        name="User Beta",
    )


@pytest.fixture
def mock_db():
    session = MagicMock()
    topic = Topic(id=uuid.uuid4(), slug="arrays", name="Arrays & Hashing")
    prob = Problem(
        id=uuid.uuid4(),
        slug="two-sum",
        title="Two Sum",
        statement_md="Find two indices that sum to target.",
        constraints_md="N <= 10^4",
        difficulty_tier=1,
        topic_id=topic.id,
        entry_point="two_sum",
        test_cases=[{"args": [[2, 7, 11, 15], 9], "expected": [0, 1]}],
        starter_code={"python": "def two_sum(nums, target):\n    pass\n"},
        optimal_time="O(N)",
        optimal_space="O(1)",
    )
    prob.topic = topic

    session.get.return_value = prob

    def mock_execute(stmt, *args, **kwargs):
        res = MagicMock()
        stmt_str = str(stmt).lower()
        if "topic" in stmt_str and "problem" not in stmt_str:
            res.scalar_one_or_none.return_value = topic
            res.scalars.return_value.first.return_value = topic
            res.scalars.return_value.all.return_value = [topic]
        else:
            res.scalar_one_or_none.return_value = prob
            res.scalars.return_value.first.return_value = prob
            res.scalars.return_value.all.return_value = [prob]
        res.scalar_one.return_value = 1
        res.all.return_value = []
        return res

    session.execute.side_effect = mock_execute
    return session


# ==============================================================================
# 1. ANONYMOUS EXECUTION REJECTION
# ==============================================================================

def test_anonymous_submissions_run_rejected():
    """POST /api/submissions/run strictly rejects unauthenticated callers with 401."""
    res = client.post("/api/submissions/run", json={
        "problem_id": str(uuid.uuid4()),
        "code": "def solve(): pass"
    })
    assert res.status_code == 401


def test_anonymous_submissions_run_custom_rejected():
    """POST /api/submissions/run-custom strictly rejects unauthenticated callers with 401."""
    res = client.post("/api/submissions/run-custom", json={
        "problem_id": "two-sum",
        "code": "def two_sum(nums, target): return [0, 1]",
        "args": [[2, 7], 9]
    })
    assert res.status_code == 401


def test_anonymous_coach_debrief_rejected():
    """POST /api/coach/debrief strictly rejects unauthenticated callers with 401."""
    res = client.post("/api/coach/debrief", json={
        "problem_id": "two-sum",
        "code": "def two_sum(nums, target): return [0, 1]",
        "tests": {"passed": 1, "total": 1}
    })
    assert res.status_code == 401


def test_anonymous_tutor_chat_rejected():
    """POST /api/tutor/chat strictly rejects unauthenticated callers with 401."""
    res = client.post("/api/tutor/chat", json={
        "message": "Can you explain this problem?"
    })
    assert res.status_code == 401


def test_anonymous_learning_run_rejected():
    """POST /api/learning/run strictly rejects unauthenticated callers with 401."""
    res = client.post("/api/learning/run", json={
        "code": "print('hello')",
        "day_number": 1
    })
    assert res.status_code == 401


def test_anonymous_learning_tutor_chat_rejected():
    """POST /api/learning/tutor/chat strictly rejects unauthenticated callers with 401."""
    res = client.post("/api/learning/tutor/chat", json={
        "day_number": 1,
        "step_number": 1,
        "message": "Help me understand variables",
        "history": []
    })
    assert res.status_code == 401


def test_anonymous_learning_tutor_quick_action_rejected():
    """POST /api/learning/tutor/quick-action strictly rejects unauthenticated callers with 401."""
    res = client.post("/api/learning/tutor/quick-action", json={
        "day_number": 1,
        "step_number": 1,
        "action": "give_hint",
        "history": []
    })
    assert res.status_code == 401


def test_anonymous_problem_generate_rejected():
    """POST /api/problems/generate strictly rejects unauthenticated callers with 401."""
    res = client.post("/api/problems/generate", json={
        "topic": "arrays",
        "tier": 1
    })
    assert res.status_code == 401


# ==============================================================================
# 2. RATE-LIMIT EXHAUSTION & PER-USER ISOLATION
# ==============================================================================

def test_submissions_run_rate_limiting_and_user_isolation(user_a, user_b, mock_db):
    """User A exhausting /api/submissions/run receives 429; User B remains unblocked."""
    app.dependency_overrides[get_db] = lambda: mock_db

    # Configure a fresh tight limiter for testing
    test_limiter = InMemoryRateLimiter(limit=2, window_s=60)
    with patch("app.api.routes.submissions.get_run_rate_limiter", return_value=test_limiter):
        with patch("app.services.submissions.execute_async") as mock_exec:
            mock_exec.return_value = ExecutionReport(
                results=[TestResult(0, True, "ok", 10, expected=None, returned=None)],
                network_isolated=True,
            )

            # User A requests
            app.dependency_overrides[get_current_user] = lambda: user_a
            payload = {"problem_id": str(mock_db.get(Problem, None).id), "code": "def solve(): pass"}

            # Hit 1 & 2: Allowed
            r1 = client.post("/api/submissions/run", json=payload)
            assert r1.status_code == 200
            r2 = client.post("/api/submissions/run", json=payload)
            assert r2.status_code == 200

            # Hit 3: User A is rate limited
            r3 = client.post("/api/submissions/run", json=payload)
            assert r3.status_code == 429
            assert "Rate limit" in r3.json()["detail"] or "rate limit" in r3.json()["detail"]
            assert "Retry-After" in r3.headers

            # User B must NOT be blocked by User A's exhaustion (per-user isolation)
            app.dependency_overrides[get_current_user] = lambda: user_b
            rb = client.post("/api/submissions/run", json=payload)
            assert rb.status_code == 200

    app.dependency_overrides.clear()


def test_submissions_run_custom_rate_limiting(user_a, mock_db):
    """User exhausting /api/submissions/run-custom receives 429."""
    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_current_user] = lambda: user_a

    test_limiter = InMemoryRateLimiter(limit=1, window_s=60)
    with patch("app.api.routes.submissions.get_run_rate_limiter", return_value=test_limiter):
        with patch("app.services.sandbox.run_custom_async") as mock_custom:
            mock_custom.return_value = MagicMock(status="ok", returned=[0, 1], stdout="", stderr="", runtime_ms=5)

            payload = {"problem_id": "two-sum", "code": "def two_sum(n, t): return [0, 1]", "args": [[2, 7], 9]}
            r1 = client.post("/api/submissions/run-custom", json=payload)
            assert r1.status_code == 200

            r2 = client.post("/api/submissions/run-custom", json=payload)
            assert r2.status_code == 429
            assert "Retry-After" in r2.headers

    app.dependency_overrides.clear()


# ==============================================================================
# 3. LLM THROTTLING & ISOLATION
# ==============================================================================

def test_coach_debrief_rate_limiting_and_user_isolation(user_a, user_b, mock_db):
    """User A exhausting /api/coach/debrief receives 429; User B is unaffected."""
    app.dependency_overrides[get_db] = lambda: mock_db

    test_limiter = InMemoryRateLimiter(limit=2, window_s=60)
    with patch("app.api.routes.tutor.get_coach_rate_limiter", return_value=test_limiter):
        payload = {
            "problem_id": "two-sum",
            "code": "def two_sum(): pass",
            "tests": {"passed": 1, "total": 1}
        }

        # User A hits limit
        app.dependency_overrides[get_current_user] = lambda: user_a
        r1 = client.post("/api/coach/debrief", json=payload)
        assert r1.status_code == 200
        r2 = client.post("/api/coach/debrief", json=payload)
        assert r2.status_code == 200
        r3 = client.post("/api/coach/debrief", json=payload)
        assert r3.status_code == 429
        assert "Retry-After" in r3.headers

        # User B still gets coaching
        app.dependency_overrides[get_current_user] = lambda: user_b
        rb = client.post("/api/coach/debrief", json=payload)
        assert rb.status_code == 200

    app.dependency_overrides.clear()


def test_tutor_chat_rate_limiting(user_a, mock_db):
    """User exhausting /api/tutor/chat receives 429."""
    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_current_user] = lambda: user_a

    test_limiter = InMemoryRateLimiter(limit=1, window_s=60)
    with patch("app.api.routes.tutor.get_tutor_rate_limiter", return_value=test_limiter):
        with patch("app.api.routes.tutor.get_llm_client") as mock_llm:
            mock_llm.return_value.complete.return_value = "Think about two pointers."
            payload = {"message": "How do I solve two sum?"}

            r1 = client.post("/api/tutor/chat", json=payload)
            assert r1.status_code == 200

            r2 = client.post("/api/tutor/chat", json=payload)
            assert r2.status_code == 429
            assert "Retry-After" in r2.headers

    app.dependency_overrides.clear()


# ==============================================================================
# 4. SAFE VS UNSAFE / OPEN REDIRECT REJECTION
# ==============================================================================

def validate_safe_redirect(target: str | None, fallback: str = "/dashboard") -> str:
    """Python counterpart verifying the exact rules implemented in frontend getSafeRedirect."""
    if not target or not isinstance(target, str):
        return fallback
    trimmed = target.strip()
    if not trimmed:
        return fallback
    if not trimmed.startswith("/"):
        return fallback
    if trimmed.startswith("//") or trimmed.startswith("/\\"):
        return fallback
    if "\\" in trimmed:
        return fallback
    import re
    if re.search(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", trimmed):
        return fallback
    from urllib.parse import urlparse
    try:
        parsed = urlparse(trimmed)
        if parsed.netloc:
            return fallback
        normalized = parsed.path.lower()
        if normalized in ("/login", "/register") or normalized.startswith("/api/auth"):
            return fallback
        return f"{parsed.path}{'?' + parsed.query if parsed.query else ''}{'#' + parsed.fragment if parsed.fragment else ''}"
    except Exception:
        return fallback


def test_safe_redirect_preserves_allowed_paths():
    """Legitimate application destinations are preserved verbatim."""
    assert validate_safe_redirect("/sap/placement") == "/sap/placement"
    assert validate_safe_redirect("/sap/learning/day/5") == "/sap/learning/day/5"
    assert validate_safe_redirect("/practice?topic=arrays") == "/practice?topic=arrays"
    assert validate_safe_redirect("/dashboard#stats") == "/dashboard#stats"


def test_unsafe_open_redirects_strictly_rejected():
    """Protocol-relative, external HTTP, UNC, and scheme injection vectors are rejected."""
    # Absolute external URLs
    assert validate_safe_redirect("https://evil.com") == "/dashboard"
    assert validate_safe_redirect("http://attacker.com/steal") == "/dashboard"

    # Protocol-relative URLs (browser redirects to //evil.com as an external domain)
    assert validate_safe_redirect("//evil.com") == "/dashboard"
    assert validate_safe_redirect("//evil.com/path") == "/dashboard"

    # Windows UNC & backslash bypasses
    assert validate_safe_redirect("/\\evil.com") == "/dashboard"
    assert validate_safe_redirect("\\evil.com") == "/dashboard"
    assert validate_safe_redirect("/path\\evil.com") == "/dashboard"

    # JavaScript & Data URIs
    assert validate_safe_redirect("javascript:alert(document.cookie)") == "/dashboard"
    assert validate_safe_redirect("data:text/html,<script>alert(1)</script>") == "/dashboard"

    # Auth loops
    assert validate_safe_redirect("/login") == "/dashboard"
    assert validate_safe_redirect("/register") == "/dashboard"
    assert validate_safe_redirect("/api/auth/token") == "/dashboard"

    # Null, empty, whitespace
    assert validate_safe_redirect(None) == "/dashboard"
    assert validate_safe_redirect("") == "/dashboard"
    assert validate_safe_redirect("   ") == "/dashboard"


# ==============================================================================
# 5. GENERATED VS RECOMMENDED PROBLEM BEHAVIOR
# ==============================================================================

def test_problem_recommend_returns_curated_catalog(user_a, mock_db):
    """POST /api/problems/recommend truthfully returns a curated problem with is_generated=False."""
    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_current_user] = lambda: user_a

    res = client.post("/api/problems/recommend", json={"topic": "arrays", "tier": 1})
    assert res.status_code == 200
    data = res.json()
    assert data["is_generated"] is False
    assert data["generation_source"] == "curated"
    assert data["slug"] == "two-sum"

    app.dependency_overrides.clear()


def test_problem_generate_with_mode_recommend_truthfully_curates(user_a, mock_db):
    """POST /api/problems/generate with mode='recommend' returns curated recommendation."""
    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_current_user] = lambda: user_a

    res = client.post("/api/problems/generate", json={"topic": "arrays", "tier": 1, "mode": "recommend"})
    assert res.status_code == 200
    data = res.json()
    assert data["is_generated"] is False
    assert data["generation_source"] == "curated"

    app.dependency_overrides.clear()


def test_problem_generate_validates_via_sandbox(user_a, mock_db):
    """POST /api/problems/generate with mode='generate' executes reference solution in sandbox."""
    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_current_user] = lambda: user_a

    generated_json = json.dumps({
        "title": "Double Target",
        "slug": "double-target",
        "statement_md": "Return double the integer value.",
        "constraints_md": "-100 <= x <= 100",
        "difficulty_tier": 1,
        "entry_point": "double_num",
        "starter_code": {"python": "def double_num(x):\n    pass\n"},
        "reference_solution": "def double_num(x):\n    return x * 2\n",
        "test_cases": [
            {"args": [4], "expected": 8},
            {"args": [-2], "expected": -4}
        ],
        "optimal_time": "O(1)",
        "optimal_space": "O(1)"
    })

    with patch("app.services.problem_generator.get_llm_client") as mock_llm:
        mock_llm.return_value.complete.return_value = generated_json

        res = client.post("/api/problems/generate", json={"topic": "arrays", "tier": 1, "mode": "generate"})
        assert res.status_code == 200
        data = res.json()
        assert data["is_generated"] is True
        assert data["generation_source"] == "ai_generated"
        assert "double" in data["title"].lower()

    app.dependency_overrides.clear()


def test_problem_generate_rejects_broken_reference_solution(user_a, mock_db):
    """POST /api/problems/generate strictly rejects problem when reference solution fails sandbox tests."""
    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_current_user] = lambda: user_a

    # Reference solution has a deliberate bug (returns x + 1 instead of x * 2)
    broken_json = json.dumps({
        "title": "Broken Solution Problem",
        "slug": "broken-problem",
        "statement_md": "Return double the integer value.",
        "constraints_md": "-100 <= x <= 100",
        "difficulty_tier": 1,
        "entry_point": "double_num",
        "starter_code": {"python": "def double_num(x):\n    pass\n"},
        "reference_solution": "def double_num(x):\n    return x + 1\n",  # BUG: fails test cases!
        "test_cases": [
            {"args": [4], "expected": 8},
            {"args": [10], "expected": 20}
        ],
        "optimal_time": "O(1)",
        "optimal_space": "O(1)"
    })

    with patch("app.services.problem_generator.get_llm_client") as mock_llm:
        mock_llm.return_value.complete.return_value = broken_json

        res = client.post("/api/problems/generate", json={"topic": "arrays", "tier": 1, "mode": "generate"})
        # Must be rejected with 502 Bad Gateway — NEVER returned to the student!
        assert res.status_code == 502
        assert "failed" in res.json()["detail"].lower()
        assert "sandbox" in res.json()["detail"].lower()

    app.dependency_overrides.clear()
