import pytest
import uuid
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.main import app
from app.api.deps import get_db
from tests.conftest import requires_db
from app.core.curriculum_map import CURRICULUM_DAY_PRACTICE
from app.models.models import Topic, Problem, User

pytestmark = [pytest.mark.integration, requires_db]


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client, db):
    username = f"user_{uuid.uuid4().hex[:8]}"
    pwd = "SecurePassword123!"
    reg_resp = client.post("/api/auth/register", json={
        "email": f"{username}@example.com",
        "password": pwd,
        "username": username,
        "name": "E2E Tester",
    })
    assert reg_resp.status_code == 200, reg_resp.text
    token = reg_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def mapped_problem(db):
    topic = db.execute(select(Topic).where(Topic.slug == "test-topic")).scalars().first()
    if not topic:
        topic = Topic(id=uuid.uuid4(), name="Test Topic", slug="test-topic")
        db.add(topic)
        db.commit()
        db.refresh(topic)

    slug = CURRICULUM_DAY_PRACTICE[1]
    problem = db.execute(select(Problem).where(Problem.slug == slug)).scalars().first()
    if not problem:
        problem = Problem(
            id=uuid.uuid4(),
            topic_id=topic.id,
            title="Celsius to Fahrenheit",
            slug=slug,
            statement_md="Convert celsius to fahrenheit.",
            constraints_md="None",
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
        db.add(problem)
        db.commit()
        db.refresh(problem)
    else:
        problem.entry_point = "celsius_to_fahrenheit"
        problem.test_cases = [
            {"args": [0], "expected": 32.0},
            {"args": [100], "expected": 212.0},
        ]
        db.commit()
        db.refresh(problem)
    return problem


def test_wrong_answer_submission_does_not_set_practice_passed(client, auth_headers, mapped_problem):
    code = "def celsius_to_fahrenheit(c):\n    return 0.0"
    resp = client.post(
        "/api/submissions",
        json={"problem_id": str(mapped_problem.id), "language": "python", "code": code},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["tests"]["all_passed"] is False

    prog_resp = client.get("/api/learning/progress", headers=auth_headers)
    assert prog_resp.status_code == 200
    assert prog_resp.json()["day_states"]["1"]["practice_passed"] is False


def test_syntax_error_submission_does_not_set_practice_passed(client, auth_headers, mapped_problem):
    code = "def celsius_to_fahrenheit(c):\n    return 0.0 ("
    resp = client.post(
        "/api/submissions",
        json={"problem_id": str(mapped_problem.id), "language": "python", "code": code},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["tests"]["all_passed"] is False

    prog_resp = client.get("/api/learning/progress", headers=auth_headers)
    assert prog_resp.status_code == 200
    assert prog_resp.json()["day_states"]["1"]["practice_passed"] is False


def test_timeout_submission_does_not_set_practice_passed(client, auth_headers, mapped_problem):
    code = "def celsius_to_fahrenheit(c):\n    while True:\n        pass"
    resp = client.post(
        "/api/submissions",
        json={"problem_id": str(mapped_problem.id), "language": "python", "code": code},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["tests"]["all_passed"] is False

    prog_resp = client.get("/api/learning/progress", headers=auth_headers)
    assert prog_resp.status_code == 200
    assert prog_resp.json()["day_states"]["1"]["practice_passed"] is False


def test_correct_submission_sets_practice_passed(client, auth_headers, mapped_problem):
    code = """def celsius_to_fahrenheit(c):
    return (c * 9.0 / 5.0) + 32.0
"""
    resp = client.post(
        "/api/submissions",
        json={"problem_id": str(mapped_problem.id), "language": "python", "code": code},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["tests"]["all_passed"] is True

    prog_resp = client.get("/api/learning/progress", headers=auth_headers)
    assert prog_resp.status_code == 200
    assert prog_resp.json()["day_states"]["1"]["practice_passed"] is True
    assert prog_resp.json()["day_states"]["1"]["completed"] is False


def test_correct_submission_plus_lesson_unlocks_next_day(client, auth_headers, mapped_problem):
    # Complete lesson for Day 1
    res_lesson = client.post("/api/learning/complete-lesson", json={"day_number": 1}, headers=auth_headers)
    assert res_lesson.status_code == 200

    code = """def celsius_to_fahrenheit(c):
    return (c * 9.0 / 5.0) + 32.0
"""
    resp = client.post(
        "/api/submissions",
        json={"problem_id": str(mapped_problem.id), "language": "python", "code": code},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["tests"]["all_passed"] is True

    prog_resp = client.get("/api/learning/progress", headers=auth_headers)
    assert prog_resp.status_code == 200
    assert prog_resp.json()["day_states"]["1"]["completed"] is True
    assert prog_resp.json()["day_states"]["2"]["unlocked"] is True
    assert prog_resp.json()["completed_days"] == [1]


def test_unmapped_problem_submission_does_not_affect_curriculum(client, auth_headers, db):
    topic = db.execute(select(Topic).where(Topic.slug == "unmapped-topic")).scalars().first()
    if not topic:
        topic = Topic(id=uuid.uuid4(), name="Unmapped Topic", slug="unmapped-topic")
        db.add(topic)
        db.commit()
        db.refresh(topic)

    problem = db.execute(select(Problem).where(Problem.slug == "unrelated-problem")).scalars().first()
    if not problem:
        problem = Problem(
            id=uuid.uuid4(),
            topic_id=topic.id,
            title="Unrelated Problem",
            slug="unrelated-problem",
            statement_md="Unrelated statement.",
            constraints_md="None",
            difficulty_tier=1,
            optimal_time="O(n)",
            optimal_space="O(n)",
            entry_point="two_sum",
            test_cases=[
                {"args": [[2, 7, 11, 15], 9], "expected": [0, 1]},
                {"args": [[3, 2, 4], 6], "expected": [1, 2]},
            ],
            starter_code={"python": "def two_sum(nums, target):\n    pass\n"},
        )
        db.add(problem)
        db.commit()
        db.refresh(problem)

    code = """def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        diff = target - n
        if diff in seen:
            return [seen[diff], i]
        seen[n] = i
    return []
"""
    resp = client.post(
        "/api/submissions",
        json={"problem_id": str(problem.id), "language": "python", "code": code},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["tests"]["all_passed"] is True

    prog_resp = client.get("/api/learning/progress", headers=auth_headers)
    for day, state in prog_resp.json()["day_states"].items():
        assert state["practice_passed"] is False


def test_repeat_correct_submission_is_idempotent(client, auth_headers, mapped_problem):
    code = """def celsius_to_fahrenheit(c):
    return (c * 9.0 / 5.0) + 32.0
"""

    # First submission
    resp1 = client.post(
        "/api/submissions",
        json={"problem_id": str(mapped_problem.id), "language": "python", "code": code},
        headers=auth_headers,
    )
    assert resp1.status_code == 200

    prog_resp_1 = client.get("/api/learning/progress", headers=auth_headers)
    practice_passed_at_1 = prog_resp_1.json()["day_states"]["1"].get("practice_passed_at")
    assert practice_passed_at_1 is not None

    # Complete lesson to trigger day completion
    client.post("/api/learning/complete-lesson", json={"day_number": 1}, headers=auth_headers)

    # Second submission
    resp2 = client.post(
        "/api/submissions",
        json={"problem_id": str(mapped_problem.id), "language": "python", "code": code},
        headers=auth_headers,
    )
    assert resp2.status_code == 200

    prog_resp_2 = client.get("/api/learning/progress", headers=auth_headers)
    practice_passed_at_2 = prog_resp_2.json()["day_states"]["1"].get("practice_passed_at")

    assert practice_passed_at_1 == practice_passed_at_2
    assert prog_resp_2.json()["completed_days"] == [1]
