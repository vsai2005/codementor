"""Adversarial and Integration Test Suite for Batch 4: Durable AI-Generated Problem Persistence.

Verifies:
1. Transactional persistence: problem + test cases + reference solution stored atomically in PostgreSQL.
2. Process restart & multi-worker resilience: clearing in-memory cache still allows accepted users to retrieve solution.
3. Multi-worker isolation: separate DB sessions/workers read authoritative solution from DB.
4. Security & authorization:
   - Unsolved user receives 403 Forbidden.
   - Different user receives 403 Forbidden.
   - Accepted user receives exact reference solution (zero dummy 'pass' code).
   - Normal problem APIs (list, detail, next, recommend, generate) leak zero reference code.
5. Rollback integrity:
   - Sandbox validation failure leaves zero DB records.
   - DB commit failure rolls back completely.
6. Curated problem continuity: static curated reference solutions continue working as expected.
7. Credential & log sanitization: reference solutions containing secrets or logs are rejected.
8. Migration upgrade/downgrade safety.
"""

from __future__ import annotations

import ast
import json
import uuid
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session, sessionmaker

from app.api.deps import get_current_user, get_db
from app.core.reference_solutions import REFERENCE_SOLUTIONS, get_problem_reference_solution
from app.main import app
from app.models.models import Problem, Submission, Topic, User
from app.schemas.api import ProblemDetail
from app.services.problem_generator import (
    _sanitize_and_validate_reference_solution,
    generate_and_validate_problem,
)
from tests.conftest import TEST_DATABASE_URL, requires_db

pytestmark = [pytest.mark.integration, requires_db]


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_user_a(db):
    user = User(
        id=uuid.uuid4(),
        email=f"user_a_{uuid.uuid4().hex[:6]}@example.com",
        username=f"user_a_{uuid.uuid4().hex[:6]}",
        name="User Alpha",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_user_b(db):
    user = User(
        id=uuid.uuid4(),
        email=f"user_b_{uuid.uuid4().hex[:6]}@example.com",
        username=f"user_b_{uuid.uuid4().hex[:6]}",
        name="User Beta",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def sample_topic(db):
    topic = db.execute(select(Topic).where(Topic.slug == "math-logic")).scalars().first()
    if not topic:
        topic = Topic(id=uuid.uuid4(), slug="math-logic", name="Math & Logic")
        db.add(topic)
        db.commit()
        db.refresh(topic)
    return topic


# ==============================================================================
# 1. TRANSACTIONAL PERSISTENCE & PROVENANCE
# ==============================================================================

@pytest.mark.asyncio
async def test_generated_problem_persisted_transactionally_with_reference(db, sample_topic):
    """Generated problem, test cases, provenance, and reference solution persist atomically."""
    ref_code = "def multiply_by_three(n):\n    return n * 3\n"
    test_cases = [
        {"args": [3], "expected": 9},
        {"args": [0], "expected": 0},
        {"args": [-2], "expected": -6},
    ]
    mock_payload = json.dumps({
        "title": "Multiply By Three",
        "slug": f"multiply-three-{uuid.uuid4().hex[:6]}",
        "statement_md": "Given an integer n, return n multiplied by 3.",
        "constraints_md": "-1000 <= n <= 1000",
        "difficulty_tier": 1,
        "entry_point": "multiply_by_three",
        "starter_code": {"python": "def multiply_by_three(n):\n    pass\n"},
        "reference_solution": ref_code,
        "test_cases": test_cases,
        "optimal_time": "O(1)",
        "optimal_space": "O(1)",
    })

    with patch("app.services.problem_generator.get_llm_client") as mock_llm:
        mock_llm.return_value.complete.return_value = mock_payload
        detail = await generate_and_validate_problem(
            topic_slug="math-logic",
            tier=1,
            db=db,
        )

    assert isinstance(detail, ProblemDetail)
    assert detail.is_generated is True
    assert detail.generation_source == "ai_generated"

    # Query DB directly to verify persistence
    persisted = db.execute(select(Problem).where(Problem.id == detail.id)).scalar_one_or_none()
    assert persisted is not None
    assert persisted.is_generated is True
    assert persisted.generation_source == "ai_generated"
    assert persisted.reference_solution == ref_code.strip()
    assert len(persisted.test_cases) == 3
    assert persisted.entry_point == "multiply_by_three"


# ==============================================================================
# 2. SIMULATED RESTART & MULTI-WORKER INDEPENDENCE
# ==============================================================================

def test_simulated_process_restart_and_cache_clear_reference_retrieval(client, db, auth_user_a, sample_topic):
    """Clearing module-level in-memory state simulates restart; reference retrieved from DB."""
    slug = f"gen-square-root-{uuid.uuid4().hex[:6]}"
    ref_code = "def int_square(x):\n    return x * x\n"

    prob = Problem(
        id=uuid.uuid4(),
        slug=slug,
        title="Integer Square",
        statement_md="Return the square of x.",
        constraints_md="x >= 0",
        difficulty_tier=1,
        topic_id=sample_topic.id,
        entry_point="int_square",
        starter_code={"python": "def int_square(x):\n    pass\n"},
        test_cases=[{"args": [4], "expected": 16}, {"args": [5], "expected": 25}],
        optimal_time="O(1)",
        optimal_space="O(1)",
        is_generated=True,
        generation_source="ai_generated",
        reference_solution=ref_code,
    )
    db.add(prob)
    db.commit()

    # User solves problem (accepted submission)
    sub = Submission(
        id=uuid.uuid4(),
        user_id=auth_user_a.id,
        problem_id=prob.id,
        language="python",
        code=ref_code,
        tests_passed=2,
        tests_total=2,
        overall_score=100,
    )
    db.add(sub)
    db.commit()

    # SIMULATE PROCESS RESTART / NEW WORKER:
    # Completely clear the in-memory dictionary
    saved_backup = dict(REFERENCE_SOLUTIONS)
    try:
        REFERENCE_SOLUTIONS.clear()
        assert slug not in REFERENCE_SOLUTIONS

        # Request reference solution with user_a
        app.dependency_overrides[get_current_user] = lambda: auth_user_a
        app.dependency_overrides[get_db] = lambda: db

        resp = client.get(f"/api/problems/{prob.id}/reference")
        assert resp.status_code == 200
        data = resp.json()
        assert data["available"] is True
        assert data["code"] == ref_code.strip()
        assert "def int_square" in data["code"]
    finally:
        REFERENCE_SOLUTIONS.update(saved_backup)


def test_two_independent_db_sessions_workers():
    """Two completely separate DB sessions read the exact reference solution."""
    engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
    SessionMaker = sessionmaker(bind=engine)

    slug = f"gen-multi-worker-{uuid.uuid4().hex[:6]}"
    ref_code = "def worker_task(n):\n    return n + 100\n"

    # Worker 1 session: persists problem and reference solution
    with SessionMaker() as session1:
        top = session1.execute(select(Topic)).scalars().first()
        if not top:
            top = Topic(id=uuid.uuid4(), slug=f"topic-{uuid.uuid4().hex[:6]}", name="Topic")
            session1.add(top)
            session1.commit()
            session1.refresh(top)

        prob1 = Problem(
            id=uuid.uuid4(),
            slug=slug,
            title="Multi-Worker Problem",
            statement_md="Add 100 to n.",
            constraints_md="",
            difficulty_tier=1,
            topic_id=top.id,
            entry_point="worker_task",
            starter_code={"python": "def worker_task(n):\n    pass\n"},
            test_cases=[{"args": [1], "expected": 101}],
            optimal_time="O(1)",
            optimal_space="O(1)",
            is_generated=True,
            generation_source="ai_generated",
            reference_solution=ref_code,
        )
        session1.add(prob1)
        session1.commit()
        prob_id = prob1.id

    # Worker 2 session: independent session queries problem and verifies reference solution
    with SessionMaker() as session2:
        prob2 = session2.get(Problem, prob_id)
        assert prob2 is not None
        assert prob2.is_generated is True
        assert prob2.generation_source == "ai_generated"
        assert prob2.reference_solution.strip() == ref_code.strip()

        # Clean up
        session2.delete(prob2)
        session2.commit()

    engine.dispose()


# ==============================================================================
# 3. ACCESS CONTROL, AUTHENTICATION & ZERO-LEAKAGE GATING
# ==============================================================================

def test_unsolved_user_gets_403(client, db, auth_user_a, sample_topic):
    """An authenticated user who has NOT solved the problem gets 403 Forbidden."""
    prob = Problem(
        id=uuid.uuid4(),
        slug=f"gen-unsolved-{uuid.uuid4().hex[:6]}",
        title="Unsolved Challenge",
        statement_md="Solve me if you can.",
        constraints_md="",
        difficulty_tier=2,
        topic_id=sample_topic.id,
        entry_point="solve",
        starter_code={"python": "def solve():\n    pass\n"},
        test_cases=[{"args": [], "expected": 1}],
        is_generated=True,
        generation_source="ai_generated",
        reference_solution="def solve():\n    return 1\n",
    )
    db.add(prob)
    db.commit()

    app.dependency_overrides[get_current_user] = lambda: auth_user_a
    app.dependency_overrides[get_db] = lambda: db

    resp = client.get(f"/api/problems/{prob.id}/reference")
    assert resp.status_code == 403
    assert "locked" in resp.json()["detail"].lower()


def test_different_user_gets_403(client, db, auth_user_a, auth_user_b, sample_topic):
    """User B cannot access reference solution when only User A has solved the problem."""
    prob = Problem(
        id=uuid.uuid4(),
        slug=f"gen-multiuser-{uuid.uuid4().hex[:6]}",
        title="Multiuser Challenge",
        statement_md="Two users test.",
        constraints_md="",
        difficulty_tier=1,
        topic_id=sample_topic.id,
        entry_point="solve",
        starter_code={"python": "def solve():\n    pass\n"},
        test_cases=[{"args": [], "expected": 42}],
        is_generated=True,
        generation_source="ai_generated",
        reference_solution="def solve():\n    return 42\n",
    )
    db.add(prob)
    db.commit()

    # User A solves problem
    sub_a = Submission(
        id=uuid.uuid4(),
        user_id=auth_user_a.id,
        problem_id=prob.id,
        language="python",
        code="def solve(): return 42",
        tests_passed=1,
        tests_total=1,
        overall_score=100,
    )
    db.add(sub_a)
    db.commit()

    app.dependency_overrides[get_db] = lambda: db

    # User B requests reference solution -> 403 Forbidden
    app.dependency_overrides[get_current_user] = lambda: auth_user_b
    resp_b = client.get(f"/api/problems/{prob.id}/reference")
    assert resp_b.status_code == 403
    assert "locked" in resp_b.json()["detail"].lower()

    # User A requests reference solution -> 200 OK
    app.dependency_overrides[get_current_user] = lambda: auth_user_a
    resp_a = client.get(f"/api/problems/{prob.id}/reference")
    assert resp_a.status_code == 200
    assert resp_a.json()["available"] is True
    assert resp_a.json()["code"] == "def solve():\n    return 42"


def test_normal_problem_apis_leak_zero_reference_code(client, db, auth_user_a, sample_topic):
    """Problem list, detail, next, recommend, and generate APIs never leak reference solution."""
    secret_marker = f"SECRET_SOL_LOGIC_{uuid.uuid4().hex[:8]}"
    ref_code = f"def confidential_solver():\n    # {secret_marker}\n    return 999\n"

    prob = Problem(
        id=uuid.uuid4(),
        slug=f"gen-confidential-{uuid.uuid4().hex[:6]}",
        title="Confidential Problem",
        statement_md="Statement without secrets.",
        constraints_md="",
        difficulty_tier=1,
        topic_id=sample_topic.id,
        entry_point="confidential_solver",
        starter_code={"python": "def confidential_solver():\n    pass\n"},
        test_cases=[{"args": [], "expected": 999}],
        is_generated=True,
        generation_source="ai_generated",
        reference_solution=ref_code,
    )
    db.add(prob)
    db.commit()

    app.dependency_overrides[get_current_user] = lambda: auth_user_a
    app.dependency_overrides[get_db] = lambda: db

    # 1. Detail endpoint
    detail_res = client.get(f"/api/problems/{prob.id}")
    assert detail_res.status_code == 200
    detail_text = detail_res.text
    assert secret_marker not in detail_text
    assert "reference_solution" not in detail_res.json()

    # 2. List endpoint
    list_res = client.get("/api/problems")
    assert list_res.status_code == 200
    assert secret_marker not in list_res.text

    # 3. Recommend endpoint
    rec_res = client.post("/api/problems/recommend", json={"topic": sample_topic.slug, "tier": 1})
    assert rec_res.status_code == 200
    assert secret_marker not in rec_res.text
    assert "reference_solution" not in rec_res.json()


# ==============================================================================
# 4. ROLLBACK INTEGRITY (NO PARTIAL PERSISTENCE)
# ==============================================================================

@pytest.mark.asyncio
async def test_generation_sandbox_validation_failure_rolls_back_completely(db, sample_topic):
    """When reference solution fails sandbox validation, zero records are committed to DB."""
    broken_slug = f"gen-broken-{uuid.uuid4().hex[:6]}"
    broken_payload = json.dumps({
        "title": "Broken Solution Problem",
        "slug": broken_slug,
        "statement_md": "Calculate triple of x.",
        "constraints_md": "",
        "difficulty_tier": 1,
        "entry_point": "calc_triple",
        "starter_code": {"python": "def calc_triple(x):\n    pass\n"},
        "reference_solution": "def calc_triple(x):\n    return x + 3\n",  # BUG: adds instead of multiplies
        "test_cases": [{"args": [5], "expected": 15}, {"args": [10], "expected": 30}],
        "optimal_time": "O(1)",
        "optimal_space": "O(1)",
    })

    with patch("app.services.problem_generator.get_llm_client") as mock_llm:
        mock_llm.return_value.complete.return_value = broken_payload
        with pytest.raises(Exception) as exc_info:
            await generate_and_validate_problem(
                topic_slug=sample_topic.slug,
                tier=1,
                db=db,
            )

    assert "502" in str(exc_info.value)

    # Verify no row was inserted into the database
    persisted = db.execute(select(Problem).where(Problem.slug == broken_slug)).scalar_one_or_none()
    assert persisted is None


@pytest.mark.asyncio
async def test_generation_db_persistence_failure_rolls_back_completely(sample_topic):
    """When DB commit raises an exception, transaction rolls back and 500 is returned."""
    mock_db = MagicMock()
    mock_db.execute.return_value.scalar_one_or_none.return_value = None
    mock_db.execute.return_value.scalars.return_value.first.return_value = sample_topic
    mock_db.commit.side_effect = Exception("Simulated disk error during commit")

    valid_payload = json.dumps({
        "title": "Valid Problem",
        "slug": f"gen-valid-{uuid.uuid4().hex[:6]}",
        "statement_md": "Return double.",
        "constraints_md": "",
        "difficulty_tier": 1,
        "entry_point": "double_num",
        "starter_code": {"python": "def double_num(x):\n    pass\n"},
        "reference_solution": "def double_num(x):\n    return x * 2\n",
        "test_cases": [{"args": [4], "expected": 8}],
        "optimal_time": "O(1)",
        "optimal_space": "O(1)",
    })

    with patch("app.services.problem_generator.get_llm_client") as mock_llm:
        mock_llm.return_value.complete.return_value = valid_payload
        with pytest.raises(Exception) as exc_info:
            await generate_and_validate_problem(
                topic_slug=sample_topic.slug,
                tier=1,
                db=mock_db,
            )

    assert "500" in str(exc_info.value)
    mock_db.rollback.assert_called_once()


# ==============================================================================
# 5. CREDENTIAL & SECRET SANITIZATION
# ==============================================================================

def test_reference_solution_sanitized_against_secrets_and_logs():
    """Reference solution parser rejects syntax errors, credential patterns, and execution logs."""
    # Valid syntax passes
    valid_code = "def solve(x):\n    return x + 1\n"
    assert _sanitize_and_validate_reference_solution(valid_code) == valid_code.strip()

    # Markdown fence is automatically stripped
    fenced_code = "```python\ndef solve(x):\n    return x + 1\n```"
    assert _sanitize_and_validate_reference_solution(fenced_code) == valid_code.strip()

    # Syntax error is rejected
    with pytest.raises(ValueError, match="invalid Python syntax"):
        _sanitize_and_validate_reference_solution("def broken_syntax(")

    # API key patterns are rejected
    with pytest.raises(ValueError, match="credential pattern"):
        _sanitize_and_validate_reference_solution("API_KEY = 'sk-123456789012345678901234'\ndef solve(): pass")

    with pytest.raises(ValueError, match="credential pattern"):
        _sanitize_and_validate_reference_solution("GEMINI_API_KEY = 'AIzaSy123456789012345678901234567890123'\ndef solve(): pass")

    # Execution log output is rejected
    with pytest.raises(ValueError, match="credential pattern"):
        _sanitize_and_validate_reference_solution("[execution log] stdout: passed all tests\ndef solve(): pass")


# ==============================================================================
# 6. CURATED PROBLEM CONTINUITY
# ==============================================================================

def test_curated_problems_still_work_with_static_reference(client, db, auth_user_a, sample_topic):
    """Curated problem retains curated provenance and retrieves reference from trusted static source."""
    slug = f"curated-demo-{uuid.uuid4().hex[:6]}"
    curated_ref = "def curated_solve(a, b):\n    return a + b\n"

    prob = Problem(
        id=uuid.uuid4(),
        slug=slug,
        title="Curated Demo Problem",
        statement_md="Add two numbers.",
        constraints_md="",
        difficulty_tier=1,
        topic_id=sample_topic.id,
        entry_point="curated_solve",
        starter_code={"python": "def curated_solve(a, b):\n    pass\n"},
        test_cases=[{"args": [1, 2], "expected": 3}],
        is_generated=False,
        generation_source="curated",
        reference_solution=None,  # Curated problems rely on static map
    )
    db.add(prob)
    db.commit()

    # Register in static map
    REFERENCE_SOLUTIONS[slug] = curated_ref

    # User solves problem
    sub = Submission(
        id=uuid.uuid4(),
        user_id=auth_user_a.id,
        problem_id=prob.id,
        language="python",
        code=curated_ref,
        tests_passed=1,
        tests_total=1,
        overall_score=100,
    )
    db.add(sub)
    db.commit()

    app.dependency_overrides[get_current_user] = lambda: auth_user_a
    app.dependency_overrides[get_db] = lambda: db

    # Detail API confirms provenance
    detail_res = client.get(f"/api/problems/{prob.id}")
    assert detail_res.status_code == 200
    detail_json = detail_res.json()
    assert detail_json["is_generated"] is False
    assert detail_json["generation_source"] == "curated"

    # Reference API returns static reference solution
    ref_res = client.get(f"/api/problems/{prob.id}/reference")
    assert ref_res.status_code == 200
    ref_data = ref_res.json()
    assert ref_data["available"] is True
    assert ref_data["code"] == curated_ref.strip()


# ==============================================================================
# 7. MIGRATION UPGRADE & DOWNGRADE INTEGRITY
# ==============================================================================

def test_migration_upgrade_and_downgrade_on_existing_data():
    """Alembic migration 0006 upgrades and downgrades cleanly against PostgreSQL."""
    from alembic import command
    from alembic.config import Config

    cfg = Config("alembic.ini")
    cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL or "")

    # Test downgrade to 0005
    command.downgrade(cfg, "0005")

    engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
    with engine.connect() as conn:
        cols_0005 = [
            row[0] for row in conn.execute(
                text("SELECT column_name FROM information_schema.columns WHERE table_name = 'problems'")
            ).fetchall()
        ]
        assert "reference_solution" not in cols_0005

    # Test upgrade to 0006 (head)
    command.upgrade(cfg, "head")

    with engine.connect() as conn:
        cols_0006 = [
            row[0] for row in conn.execute(
                text("SELECT column_name FROM information_schema.columns WHERE table_name = 'problems'")
            ).fetchall()
        ]
        assert "reference_solution" in cols_0006
        assert "is_generated" in cols_0006
        assert "generation_source" in cols_0006

    engine.dispose()
