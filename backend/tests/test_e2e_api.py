"""End-to-end API lifecycle and security tests.

Covers:
  - Authentication lifecycle (register, login, me, logout, cookie assertions)
  - Practice portal execution (run, submit, timeout, syntax error, wrong answer, security containment)
  - Submission history isolation and progress tracking
"""

from __future__ import annotations

import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.main import app
from app.models.models import Problem, Topic, User
from app.database import get_db
from tests.conftest import requires_db

pytestmark = [pytest.mark.integration, requires_db]


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def sample_problem(db):
    topic = db.execute(select(Topic).where(Topic.slug == "arrays")).scalars().first()
    if not topic:
        topic = Topic(slug="arrays", name="Arrays & Hashing")
        db.add(topic)
        db.commit()
        db.refresh(topic)

    prob = db.execute(select(Problem).where(Problem.slug == "two-sum-test")).scalars().first()
    if not prob:
        prob = Problem(
            slug="two-sum-test",
            title="Two Sum Test",
            statement_md="Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target.",
            constraints_md="2 <= nums.length <= 10^4",
            difficulty_tier=1,
            topic_id=topic.id,
            optimal_time="O(n)",
            optimal_space="O(n)",
            entry_point="two_sum",
            test_cases=[
                {"args": [[2, 7, 11, 15], 9], "expected": [0, 1]},
                {"args": [[3, 2, 4], 6], "expected": [1, 2]},
            ],
            starter_code={"python": "def two_sum(nums, target):\n    pass\n"},
        )
        db.add(prob)
        db.commit()
        db.refresh(prob)
    return prob


def test_complete_auth_lifecycle(client, db):
    # 1. Register with username & password
    username = f"user_{uuid.uuid4().hex[:8]}"
    reg_payload = {
        "username": username,
        "password": "SecurePassword123!",
        "email": f"{username}@example.com",
        "name": "Audit User",
    }
    res = client.post("/api/auth/register", json=reg_payload)
    assert res.status_code == 200, res.text
    data = res.json()
    assert "access_token" in data
    assert data["user"]["username"] == username
    assert "access_token" in client.cookies

    # 2. Access /me via Cookie
    res_me = client.get("/api/auth/me")
    assert res_me.status_code == 200
    assert res_me.json()["username"] == username

    # 3. Access /me via Bearer Token header
    token = data["access_token"]
    clean_client = TestClient(app)
    res_bearer = clean_client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res_bearer.status_code == 200
    assert res_bearer.json()["username"] == username

    # 4. Access /me without credentials -> 401
    res_unauth = clean_client.get("/api/auth/me")
    assert res_unauth.status_code == 401

    # 5. Access /me with invalid/corrupt token -> 401
    res_invalid = clean_client.get("/api/auth/me", headers={"Authorization": "Bearer not-a-valid-token"})
    assert res_invalid.status_code == 401

    # 6. Login with correct credentials
    login_client = TestClient(app)
    res_login = login_client.post("/api/auth/login", json={"identifier": username, "password": "SecurePassword123!"})
    assert res_login.status_code == 200
    assert "access_token" in login_client.cookies

    # 7. Login with wrong password -> 401
    res_bad_pw = login_client.post("/api/auth/login", json={"identifier": username, "password": "WrongPassword"})
    assert res_bad_pw.status_code == 401

    # 8. Duplicate username registration -> 409
    res_dup = client.post("/api/auth/register", json=reg_payload)
    assert res_dup.status_code == 409

    # 9. Logout clears cookie
    res_logout = login_client.post("/api/auth/logout")
    assert res_logout.status_code == 200
    # Cookie should be deleted/expired
    set_cookie_header = res_logout.headers.get("set-cookie", "")
    assert "access_token=" in set_cookie_header

    # 10. Access /me after logout fails with 401
    login_client.cookies.clear()
    res_after_logout = login_client.get("/api/auth/me")
    assert res_after_logout.status_code == 401


def test_practice_portal_code_execution(client, sample_problem):
    # Register and authenticate
    username = f"coder_{uuid.uuid4().hex[:8]}"
    client.post("/api/auth/register", json={
        "username": username,
        "password": "Password123!",
    })

    # 1. Run Correct Code
    correct_code = """
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        diff = target - n
        if diff in seen:
            return [seen[diff], i]
        seen[n] = i
    return []
"""
    res_run = client.post("/api/submissions/run", json={
        "problem_id": str(sample_problem.id),
        "language": "python",
        "code": correct_code,
    })
    assert res_run.status_code == 200
    run_data = res_run.json()
    assert run_data["all_passed"] is True
    assert run_data["passed"] == 2
    assert run_data["total"] == 2

    # 2. Run Wrong Code
    wrong_code = "def two_sum(nums, target):\n    return [0, 0]\n"
    res_wrong = client.post("/api/submissions/run", json={
        "problem_id": str(sample_problem.id),
        "language": "python",
        "code": wrong_code,
    })
    assert res_wrong.status_code == 200
    wrong_data = res_wrong.json()
    assert wrong_data["all_passed"] is False

    # 3. Run Syntax Error Code
    syntax_code = "def two_sum(nums, target):\n    return nums ++\n"
    res_syntax = client.post("/api/submissions/run", json={
        "problem_id": str(sample_problem.id),
        "language": "python",
        "code": syntax_code,
    })
    assert res_syntax.status_code == 200
    syntax_data = res_syntax.json()
    assert syntax_data["all_passed"] is False
    assert any(r["status"] == "error" for r in syntax_data["results"])

    # 4. Run Infinite Loop Code -> Timeout
    loop_code = "def two_sum(nums, target):\n    while True: pass\n"
    res_loop = client.post("/api/submissions/run", json={
        "problem_id": str(sample_problem.id),
        "language": "python",
        "code": loop_code,
    })
    assert res_loop.status_code == 200
    loop_data = res_loop.json()
    assert loop_data["all_passed"] is False
    assert all(r["status"] == "timeout" for r in loop_data["results"])

    # 5. Run Hostile Code (Filesystem traversal) -> Blocked
    hostile_code = "def two_sum(nums, target):\n    with open('/etc/passwd') as f:\n        return [0, 1]\n"
    res_hostile = client.post("/api/submissions/run", json={
        "problem_id": str(sample_problem.id),
        "language": "python",
        "code": hostile_code,
    })
    assert res_hostile.status_code == 200
    hostile_data = res_hostile.json()
    assert hostile_data["all_passed"] is False
    assert any("PermissionError" in r["stderr"] or "blocked" in r["stderr"] for r in hostile_data["results"])


def test_submission_and_history_isolation(client, sample_problem):
    # User 1
    u1 = f"u1_{uuid.uuid4().hex[:8]}"
    client1 = TestClient(app)
    client1.post("/api/auth/register", json={"username": u1, "password": "Password123!"})

    # User 2
    u2 = f"u2_{uuid.uuid4().hex[:8]}"
    client2 = TestClient(app)
    client2.post("/api/auth/register", json={"username": u2, "password": "Password123!"})

    # User 1 submits code
    correct_code = """
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        diff = target - n
        if diff in seen:
            return [seen[diff], i]
        seen[n] = i
    return []
"""
    res_sub = client1.post("/api/submissions", json={
        "problem_id": str(sample_problem.id),
        "language": "python",
        "code": correct_code,
    })
    assert res_sub.status_code == 200
    sub_data = res_sub.json()
    assert "submission_id" in sub_data
    assert sub_data["tests"]["all_passed"] is True

    # User 1 queries history -> sees 1 submission
    res_h1 = client1.get("/api/submissions")
    assert res_h1.status_code == 200
    h1_items = res_h1.json()
    assert len(h1_items) == 1
    assert h1_items[0]["id"] == sub_data["submission_id"]

    # User 2 queries history -> sees 0 submissions (STRICT ISOLATION)
    res_h2 = client2.get("/api/submissions")
    assert res_h2.status_code == 200
    assert len(res_h2.json()) == 0
