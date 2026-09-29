"""Shared fixtures.

DB-backed tests are opt-in: they run only when TEST_DATABASE_URL points at a
real Postgres with pgvector. Without it they skip rather than fail, so the
unit suite stays runnable anywhere while the integration suite stays honest
about what it needs.

    docker compose up -d
    export TEST_DATABASE_URL=postgresql+psycopg://codementor:codementor@localhost:5433/codementor_test
    pytest -m integration
"""

from __future__ import annotations

import os
import uuid

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from tests._env_isolation import isolate

# Must run before any test module imports the app: the suite must not depend on the
# developer's .env file or exported environment variables.
isolate()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

requires_db = pytest.mark.skipif(
    not TEST_DATABASE_URL,
    reason="set TEST_DATABASE_URL to run DB-backed tests",
)


@pytest.fixture(autouse=True)
def _isolated_auth_rate_limits():
    """Auth rate limiters are process-wide; give every test fresh, empty buckets."""
    from app.services.ratelimit import reset_policy_rate_limiters

    reset_policy_rate_limiters()
    yield
    reset_policy_rate_limiters()


@pytest.fixture
def capture_logs():
    """Collect records from a named logger regardless of global logging state.

    Alembic's fileConfig (run by the DB fixtures) disables already-created loggers,
    which makes ``caplog`` order-dependent. Usage: ``records = capture_logs("app.x")``.
    """
    import logging

    undo = []

    def _capture(name: str) -> list[logging.LogRecord]:
        logger = logging.getLogger(name)
        records: list[logging.LogRecord] = []

        class _Collect(logging.Handler):
            def emit(self, record):
                records.append(record)

        handler = _Collect(level=logging.DEBUG)
        undo.append((logger, handler, logger.level, logger.disabled))
        logger.disabled = False
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        return records

    yield _capture
    for logger, handler, level, disabled in undo:
        logger.removeHandler(handler)
        logger.setLevel(level)
        logger.disabled = disabled


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


@pytest.fixture
def fresh_engine():
    """A throwaway, fully migrated database for tests that need a truly empty schema
    (first-use races, deploy seeding) while the shared test database already has data."""
    from alembic import command
    from alembic.config import Config
    from sqlalchemy.engine import make_url

    if not TEST_DATABASE_URL:
        pytest.skip("TEST_DATABASE_URL not set")
    base = make_url(TEST_DATABASE_URL)
    name = f"cm_fresh_{uuid.uuid4().hex[:12]}"
    admin = create_engine(base.set(database="postgres"), isolation_level="AUTOCOMMIT")
    with admin.connect() as conn:
        conn.execute(text(f'CREATE DATABASE "{name}"'))
    url = base.set(database=name)
    eng = create_engine(url, pool_pre_ping=True)
    try:
        with eng.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
        cfg = Config("alembic.ini")
        cfg.set_main_option("sqlalchemy.url", url.render_as_string(hide_password=False))
        command.upgrade(cfg, "head")
        yield eng
    finally:
        eng.dispose()
        with admin.connect() as conn:
            conn.execute(text(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)'))
        admin.dispose()


@pytest.fixture
def db(engine, migrated) -> Session:
    """A session wrapped in a transaction that is always rolled back.

    Tests therefore never see each other's rows, and the schema is migrated
    once rather than per test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(
        bind=connection, expire_on_commit=False, join_transaction_mode="create_savepoint"
    )()
    try:
        yield session
    finally:
        session.close()
        if transaction.is_active:
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
    from sqlalchemy import select

    def _make(slug: str | None = None):
        if slug:
            existing = db.execute(select(Topic).where(Topic.slug == slug)).scalar_one_or_none()
            if existing:
                return existing
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
