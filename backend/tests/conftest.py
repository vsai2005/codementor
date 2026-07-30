"""Shared fixtures.

DB-backed tests are opt-in: they run only when TEST_DATABASE_URL points at a
real Postgres with pgvector. Without it they skip rather than fail, so the
unit suite stays runnable anywhere while the integration suite stays honest
about what it needs.

    docker compose up -d
    export TEST_DATABASE_URL=postgresql+psycopg://codementor:codementor@localhost:5432/codementor_test
    pytest -m integration
"""

from __future__ import annotations

import os
import uuid

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

requires_db = pytest.mark.skipif(
    not TEST_DATABASE_URL,
    reason="set TEST_DATABASE_URL to run DB-backed tests",
)


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "integration: requires a real Postgres + pgvector")


@pytest.fixture(scope="session")
def engine():
    if not TEST_DATABASE_URL:
        pytest.skip("TEST_DATABASE_URL not set")
    eng = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
    with eng.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    yield eng
    eng.dispose()


@pytest.fixture(scope="session")
def migrated(engine):
    """Apply migrations once per session, against the test database."""
    from alembic import command
    from alembic.config import Config

    cfg = Config("alembic.ini")
    cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL or "")
    command.upgrade(cfg, "head")
    yield
    command.downgrade(cfg, "base")


@pytest.fixture
def db(engine, migrated) -> Session:
    """A session wrapped in a transaction that is always rolled back.

    Tests therefore never see each other's rows, and the schema is migrated
    once rather than per test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection, expire_on_commit=False)()
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def make_user(db):
    from app.models.models import User

    def _make(email: str | None = None):
        user = User(
            id=uuid.uuid4(),
            email=email or f"{uuid.uuid4().hex[:8]}@example.com",
            name="Test User",
        )
        db.add(user)
        db.flush()
        return user

    return _make


@pytest.fixture
def make_topic(db):
    from app.models.models import Topic

    def _make(slug: str | None = None):
        s = slug or f"topic-{uuid.uuid4().hex[:6]}"
        topic = Topic(id=uuid.uuid4(), slug=s, name=s.title())
        db.add(topic)
        db.flush()
        return topic

    return _make


@pytest.fixture
def make_problem(db, make_topic):
    from app.models.models import Problem

    def _make(topic=None, tier: int = 1):
        topic = topic or make_topic()
        problem = Problem(
            id=uuid.uuid4(),
            slug=f"p-{uuid.uuid4().hex[:8]}",
            title="Test Problem",
            statement_md="Do the thing.",
            constraints_md="",
            difficulty_tier=tier,
            topic_id=topic.id,
            entry_point="solve",
            test_cases=[{"args": [1], "expected": 1}],
            starter_code={"python": "def solve(x):\n    pass\n"},
        )
        db.add(problem)
        db.flush()
        return problem

    return _make
