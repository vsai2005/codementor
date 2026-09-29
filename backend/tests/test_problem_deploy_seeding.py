"""`python -m app.seed` runs at every deploy: idempotent, safe to run concurrently, and it
never touches AI-generated problems."""

from __future__ import annotations

import threading
import uuid

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import sessionmaker

from app import seed as problem_seed
from app.models.models import Problem, Topic
from tests.conftest import requires_db

pytestmark = [pytest.mark.integration, requires_db]


@pytest.fixture
def seed_into(fresh_engine, monkeypatch):
    monkeypatch.setattr(problem_seed, "SessionLocal", sessionmaker(bind=fresh_engine, expire_on_commit=False))
    return sessionmaker(bind=fresh_engine, expire_on_commit=False)


def _counts(Session):
    with Session() as s:
        return (
            s.execute(select(func.count()).select_from(Topic)).scalar_one(),
            s.execute(select(func.count()).select_from(Problem)).scalar_one(),
        )


def test_seed_creates_catalog_and_reruns_without_duplicates(seed_into):
    Session = seed_into
    assert _counts(Session) == (0, 0)

    problem_seed.seed()
    with Session() as s:
        ids_first = dict(s.execute(select(Problem.slug, Problem.id)).all())
    problem_seed.seed()  # every deploy / restart
    with Session() as s:
        ids_second = dict(s.execute(select(Problem.slug, Problem.id)).all())

    assert _counts(Session) == (len(problem_seed.TOPICS), len(problem_seed.PROBLEMS))
    assert ids_first == ids_second  # stable ids: submissions and progress keep their references


def test_seed_refreshes_seed_problems_but_never_touches_generated_ones(seed_into):
    Session = seed_into
    problem_seed.seed()
    first = problem_seed.PROBLEMS[0]

    with Session() as s:
        topic = s.execute(select(Topic)).scalars().first()
        generated = Problem(
            id=uuid.uuid4(),
            slug=f"gen-{uuid.uuid4().hex[:8]}",
            title="Generated",
            statement_md="AI generated.",
            constraints_md="",
            difficulty_tier=2,
            topic_id=topic.id,
            entry_point="solve",
            test_cases=[{"args": [1], "expected": 1}],
            starter_code={"python": "def solve(x):\n    pass\n"},
        )
        s.add(generated)
        seeded = s.execute(select(Problem).where(Problem.slug == first["slug"])).scalar_one()
        seeded.title = "edited out of band"
        s.commit()
        generated_id = generated.id

    problem_seed.seed()

    with Session() as s:
        assert s.execute(select(Problem.title).where(Problem.slug == first["slug"])).scalar_one() == first["title"]
        kept = s.get(Problem, generated_id)
        assert kept is not None and kept.title == "Generated"


def test_concurrent_deploy_seeds_both_succeed(seed_into):
    """Two instances starting at once on a fresh database: neither may crash its startup."""
    Session = seed_into
    barrier = threading.Barrier(2)
    errors: list[BaseException] = []

    def run():
        barrier.wait()
        try:
            problem_seed.seed()
        except BaseException as exc:  # surfaced below
            errors.append(exc)

    threads = [threading.Thread(target=run) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=120)

    assert not any(t.is_alive() for t in threads)
    assert errors == []
    assert _counts(Session) == (len(problem_seed.TOPICS), len(problem_seed.PROBLEMS))
