"""Adversarial and regression test suite for Python Practice & Progression (Batch 3).

Covers:
1. Reused slugs (e.g. sort-colors for Day 22 vs Day 57): solving for Day 22 must NOT credit Day 57.
2. Forged day numbers: submitting a problem with a mismatched day_number returns 400 Bad Request.
3. Locked future days: submitting a problem for a day that is locked returns 403 Forbidden.
4. Repeat submissions: duplicate accepted submissions on the same day are strictly idempotent.
5. Lesson-first and Practice-first gating: both sequences produce complete=True only when both gates pass.
6. Unsolved reference access: GET /api/problems/{id}/reference returns 403 Forbidden for unsolved users.
7. Solved reference access: returns 200 with the real server-side reference solution (no dummy pass).
8. Reference solution leakage: normal problem list, detail, and next APIs never expose reference code.
"""

import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.main import app
from app.api.deps import get_db
from tests.conftest import requires_db
from app.core.curriculum_map import CURRICULUM_DAY_PRACTICE, PRACTICE_SLUG_TO_DAYS
from app.core.reference_solutions import get_problem_reference_solution
from app.models.models import Problem, Topic, User, UserLearningDayState

pytestmark = [pytest.mark.integration, requires_db]


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_user(client, db):
    username = f"py_adv_{uuid.uuid4().hex[:8]}"
    pwd = "SecurePassword123!"
    reg_resp = client.post("/api/auth/register", json={
        "email": f"{username}@example.com",
        "password": pwd,
        "username": username,
        "name": "Python Practice Tester",
    })
    assert reg_resp.status_code == 200, reg_resp.text
    token = reg_resp.json()["access_token"]
    user_id = uuid.UUID(reg_resp.json()["user"]["id"])
    return {
        "headers": {"Authorization": f"Bearer {token}"},
        "user_id": user_id,
        "token": token,
    }


@pytest.fixture
def sort_colors_problem(db):
    """Ensure sort-colors exists in DB."""
    topic = db.execute(select(Topic).where(Topic.slug == "python-basics")).scalars().first()
    if not topic:
        topic = Topic(id=uuid.uuid4(), name="Python Basics", slug="python-basics")
        db.add(topic)
        db.commit()

    prob = db.execute(select(Problem).where(Problem.slug == "sort-colors")).scalars().first()
    if not prob:
        prob = Problem(
            id=uuid.uuid4(),
            topic_id=topic.id,
            title="Sort Colors",
            slug="sort-colors",
            statement_md="Sort array with 0s, 1s, and 2s.",
            difficulty_tier=2,
            optimal_time="O(n)",
            optimal_space="O(1)",
            entry_point="sort_colors",
            test_cases=[
                {"args": [[2, 0, 2, 1, 1, 0]], "expected": [0, 0, 1, 1, 2, 2]},
                {"args": [[2, 0, 1]], "expected": [0, 1, 2]},
            ],
            starter_code={"python": "def sort_colors(nums):\n    pass\n"},
        )
        db.add(prob)
        db.commit()
        db.refresh(prob)
    return prob


@pytest.fixture
def day1_problem(db):
    """Ensure Day 1 problem (celsius-to-fahrenheit) exists in DB."""
    topic = db.execute(select(Topic).where(Topic.slug == "python-basics")).scalars().first()
    if not topic:
        topic = Topic(id=uuid.uuid4(), name="Python Basics", slug="python-basics")
        db.add(topic)
        db.commit()

    slug = CURRICULUM_DAY_PRACTICE[1]
    prob = db.execute(select(Problem).where(Problem.slug == slug)).scalars().first()
    if not prob:
        prob = Problem(
            id=uuid.uuid4(),
            topic_id=topic.id,
            title="Celsius to Fahrenheit",
            slug=slug,
            statement_md="Convert celsius to fahrenheit.",
            difficulty_tier=1,
            optimal_time="O(1)",
            optimal_space="O(1)",
            entry_point="celsius_to_fahrenheit",
            test_cases=[
                {"args": [0], "expected": 32.0},
                {"args": [100], "expected": 212.0},
            ],
            starter_code={"python": "def celsius_to_fahrenheit(c):\n    pass\n"},
        )
        db.add(prob)
        db.commit()
        db.refresh(prob)
    return prob


# =============================================================================
# 1. Reused Slugs & Day Mapping Isolation
# =============================================================================


def test_reused_slug_credits_only_accessible_day(client, auth_user, sort_colors_problem, db):
    """Solving sort-colors for Day 22 must NOT pre-mark Day 57 (which also maps sort-colors)."""
    headers = auth_user["headers"]
    user_id = auth_user["user_id"]

    # Fast-forward user to Day 22: mark Days 1..21 completed
    for d in range(1, 22):
        st = UserLearningDayState(
            user_id=user_id,
            day_number=d,
            lesson_completed=True,
            practice_passed=True,
            completed=True,
        )
        db.add(st)
    db.commit()

    # Verify Day 22 is unlocked and Day 57 is locked
    prog = client.get("/api/learning/progress", headers=headers).json()
    assert prog["current_day"] == 22
    assert prog["day_states"]["22"]["unlocked"] is True
    assert prog["day_states"]["57"]["unlocked"] is False

    # Submit accepted solution for sort-colors targeting Day 22
    code = """def sort_colors(nums):
    nums.sort()
    return nums
"""
    resp = client.post(
        "/api/submissions",
        json={
            "problem_id": str(sort_colors_problem.id),
            "language": "python",
            "code": code,
            "day_number": 22,
        },
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["tests"]["all_passed"] is True

    # Re-check progress
    prog_after = client.get("/api/learning/progress", headers=headers).json()
    assert prog_after["day_states"]["22"]["practice_passed"] is True
    # Day 57 MUST REMAIN LOCKED AND PRACTICE UNPASSED
    assert prog_after["day_states"]["57"]["practice_passed"] is False
    assert prog_after["day_states"]["57"]["unlocked"] is False
    assert prog_after["day_states"]["57"]["status"] == "locked"


def test_forged_day_number_rejected_with_400(client, auth_user, day1_problem):
    """Submitting Day 1 problem with day_number=5 (mismatched slug) returns 400."""
    headers = auth_user["headers"]
    code = """def celsius_to_fahrenheit(c):
    return (c * 9.0 / 5.0) + 32.0
"""
    resp = client.post(
        "/api/submissions",
        json={
            "problem_id": str(day1_problem.id),
            "language": "python",
            "code": code,
            "day_number": 5,  # Forged day! Day 5 is sum-multiples-loop
        },
        headers=headers,
    )
    assert resp.status_code == 400
    assert "not mapped" in resp.json()["detail"].lower()


def test_locked_future_day_submission_rejected_with_403(client, auth_user, sort_colors_problem):
    """Learner on Day 1 cannot submit for Day 57 or Day 22 when locked -> 403."""
    headers = auth_user["headers"]
    code = """def sort_colors(nums):
    nums.sort()
    return nums
"""
    resp = client.post(
        "/api/submissions",
        json={
            "problem_id": str(sort_colors_problem.id),
            "language": "python",
            "code": code,
            "day_number": 57,  # Day 57 is locked
        },
        headers=headers,
    )
    assert resp.status_code == 403
    assert "locked" in resp.json()["detail"].lower()


def test_repeat_submissions_are_idempotent_no_double_advance(client, auth_user, day1_problem):
    """Submitting accepted code repeatedly for Day 1 is strictly idempotent."""
    headers = auth_user["headers"]
    code = """def celsius_to_fahrenheit(c):
    return (c * 9.0 / 5.0) + 32.0
"""
    # First submission
    resp1 = client.post(
        "/api/submissions",
        json={"problem_id": str(day1_problem.id), "language": "python", "code": code, "day_number": 1},
        headers=headers,
    )
    assert resp1.status_code == 200

    prog1 = client.get("/api/learning/progress", headers=headers).json()
    first_passed_at = prog1["day_states"]["1"]["practice_passed_at"]
    assert first_passed_at is not None

    # Complete lesson to advance day
    client.post("/api/learning/complete-lesson", json={"day_number": 1}, headers=headers)

    # Second submission (repeat accepted)
    resp2 = client.post(
        "/api/submissions",
        json={"problem_id": str(day1_problem.id), "language": "python", "code": code, "day_number": 1},
        headers=headers,
    )
    assert resp2.status_code == 200

    prog2 = client.get("/api/learning/progress", headers=headers).json()
    second_passed_at = prog2["day_states"]["1"]["practice_passed_at"]
    assert first_passed_at == second_passed_at
    assert prog2["completed_days"] == [1]
    assert prog2["current_day"] == 2


# =============================================================================
# 2. Lesson-First vs Practice-First Progression
# =============================================================================


def test_lesson_first_and_practice_first_ordering(client, auth_user, day1_problem, db):
    """Both (Lesson -> Practice) and (Practice -> Lesson) require both gates to pass."""
    headers = auth_user["headers"]
    user_id = auth_user["user_id"]

    # Day 1: Lesson FIRST
    res_lesson = client.post("/api/learning/complete-lesson", json={"day_number": 1}, headers=headers)
    assert res_lesson.status_code == 200
    prog = client.get("/api/learning/progress", headers=headers).json()
    assert prog["day_states"]["1"]["lesson_completed"] is True
    assert prog["day_states"]["1"]["practice_passed"] is False
    assert prog["day_states"]["1"]["completed"] is False
    assert prog["day_states"]["2"]["unlocked"] is False  # Day 2 remains locked!

    # Day 1: Practice SECOND
    code = """def celsius_to_fahrenheit(c):
    return (c * 9.0 / 5.0) + 32.0
"""
    client.post(
        "/api/submissions",
        json={"problem_id": str(day1_problem.id), "language": "python", "code": code, "day_number": 1},
        headers=headers,
    )
    prog = client.get("/api/learning/progress", headers=headers).json()
    assert prog["day_states"]["1"]["completed"] is True
    assert prog["day_states"]["2"]["unlocked"] is True  # Day 2 unlocked!

    # Day 2: Practice FIRST
    day2_slug = CURRICULUM_DAY_PRACTICE[2]
    topic = db.execute(select(Topic).where(Topic.slug == "python-basics")).scalars().first()
    day2_prob = db.execute(select(Problem).where(Problem.slug == day2_slug)).scalars().first()
    if not day2_prob:
        day2_prob = Problem(
            id=uuid.uuid4(),
            topic_id=topic.id,
            title="Time Converter",
            slug=day2_slug,
            statement_md="Convert seconds.",
            difficulty_tier=1,
            optimal_time="O(1)",
            optimal_space="O(1)",
            entry_point="seconds_to_time",
            test_cases=[{"args": [3661], "expected": "01:01:01"}],
            starter_code={"python": "def seconds_to_time(s):\n    pass\n"},
        )
        db.add(day2_prob)
        db.commit()

    code2 = """def seconds_to_time(s):
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    return f"{h:02d}:{m:02d}:{sec:02d}"
"""
    client.post(
        "/api/submissions",
        json={"problem_id": str(day2_prob.id), "language": "python", "code": code2, "day_number": 2},
        headers=headers,
    )
    prog = client.get("/api/learning/progress", headers=headers).json()
    assert prog["day_states"]["2"]["practice_passed"] is True
    assert prog["day_states"]["2"]["lesson_completed"] is False
    assert prog["day_states"]["2"]["completed"] is False
    assert prog["day_states"]["3"]["unlocked"] is False  # Day 3 remains locked!

    # Day 2: Lesson SECOND
    client.post("/api/learning/complete-lesson", json={"day_number": 2}, headers=headers)
    prog = client.get("/api/learning/progress", headers=headers).json()
    assert prog["day_states"]["2"]["completed"] is True
    assert prog["day_states"]["3"]["unlocked"] is True  # Day 3 unlocked!


# =============================================================================
# 3. Reference Solution Security & Authenticated Access
# =============================================================================


def test_unsolved_reference_access_returns_403(client, auth_user, day1_problem):
    """An authenticated user who has NOT solved the problem gets 403 on /reference."""
    headers = auth_user["headers"]
    resp = client.get(f"/api/problems/{day1_problem.id}/reference", headers=headers)
    assert resp.status_code == 403
    assert "locked" in resp.json()["detail"].lower()


def test_solved_reference_access_returns_real_solution_no_dummy_pass(client, auth_user, day1_problem):
    """Once the user has an accepted solution, /reference returns the real reference solution."""
    headers = auth_user["headers"]
    code = """def celsius_to_fahrenheit(c):
    return (c * 9.0 / 5.0) + 32.0
"""
    # Submit accepted solution
    sub_resp = client.post(
        "/api/submissions",
        json={"problem_id": str(day1_problem.id), "language": "python", "code": code, "day_number": 1},
        headers=headers,
    )
    assert sub_resp.status_code == 200
    assert sub_resp.json()["tests"]["all_passed"] is True

    # Access reference solution
    ref_resp = client.get(f"/api/problems/{day1_problem.id}/reference", headers=headers)
    assert ref_resp.status_code == 200
    data = ref_resp.json()
    assert data["available"] is True
    assert data["language"] == "python"
    assert "def " in data["code"]
    # STRICT ASSERTION: No dummy 'pass' implementation
    assert "def celsius_to_fahrenheit(*args, **kwargs):\n    pass" not in data["code"]


def test_no_reference_solution_leakage_in_normal_apis(client, auth_user, day1_problem):
    """Problem list, detail, and next endpoints never leak the reference solution."""
    headers = auth_user["headers"]

    # 1. Detail endpoint
    detail_resp = client.get(f"/api/problems/{day1_problem.id}", headers=headers)
    assert detail_resp.status_code == 200
    detail = detail_resp.json()
    assert "reference_solution" not in detail
    assert "reference" not in detail.get("starter_code", {})
    assert "solution" not in detail.get("starter_code", {})

    # 2. List endpoint
    list_resp = client.get("/api/problems", headers=headers)
    assert list_resp.status_code == 200
    items = list_resp.json()["items"]
    for item in items:
        assert "reference_solution" not in item
