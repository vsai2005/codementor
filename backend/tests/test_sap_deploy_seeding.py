"""SAP missions are seeded at deploy time; request paths only verify they exist.

Before: every GET /api/sap/missions re-synced all missions, and the first mission
request on a fresh deployment seeded 33 missions and 84 concepts inline (seconds).
"""

from __future__ import annotations

import logging
import re
import uuid
from pathlib import Path

import pytest
from sqlalchemy import event, func, select
from sqlalchemy.orm import sessionmaker

from app.models.models import User
from app.models.sap_models import SAPMission
from app.sap import seed as seed_cli
from app.sap.services.missions import SEED_MISSIONS, SAPMissionService
from tests.conftest import requires_db

REPO = Path(__file__).resolve().parents[2]
SEED_STEP = "python -m app.sap.seed"
# Migrations, then problem catalog, then SAP missions, then the server.
DEPLOY_ORDER = (
    "alembic upgrade head &&",
    "python -m app.seed &&",
    f"{SEED_STEP} &&",
    "uvicorn app.main:app",
)


def _mission_count(session) -> int:
    return session.execute(select(func.count()).select_from(SAPMission)).scalar_one()


@pytest.fixture
def seed_calls(monkeypatch):
    """Count full seeding runs while still executing the real implementation."""
    calls: list[int] = []
    real = SAPMissionService.seed_missions_if_needed.__func__

    def counting(cls, db):
        calls.append(1)
        return real(cls, db)

    monkeypatch.setattr(SAPMissionService, "seed_missions_if_needed", classmethod(counting))
    return calls


# --- deploy command -------------------------------------------------------------------


@pytest.mark.integration
@requires_db
def test_deploy_seed_command_creates_all_missions_and_is_idempotent(fresh_engine, monkeypatch):
    monkeypatch.setattr(seed_cli, "SessionLocal", sessionmaker(bind=fresh_engine, expire_on_commit=False))
    with fresh_engine.connect() as conn:
        assert conn.execute(select(func.count()).select_from(SAPMission)).scalar_one() == 0

    assert seed_cli.seed() == len(SEED_MISSIONS)
    assert seed_cli.seed() == len(SEED_MISSIONS)  # re-run on every deploy/restart

    with sessionmaker(bind=fresh_engine)() as s:
        assert _mission_count(s) == len(SEED_MISSIONS)
        slugs = set(s.execute(select(SAPMission.slug)).scalars())
    assert slugs == {m["slug"] for m in SEED_MISSIONS}


# --- request path -----------------------------------------------------------------------


@pytest.mark.integration
@requires_db
def test_request_path_only_reads_once_missions_are_seeded(fresh_engine, seed_calls, monkeypatch):
    monkeypatch.setattr(seed_cli, "SessionLocal", sessionmaker(bind=fresh_engine, expire_on_commit=False))
    seed_cli.seed()
    seed_calls.clear()

    statements: list[str] = []
    with sessionmaker(bind=fresh_engine)() as s:
        conn = s.connection()
        event.listen(conn, "before_cursor_execute", lambda c, cur, stmt, *a: statements.append(stmt))
        SAPMissionService.ensure_missions_seeded(s)
        s.rollback()

    assert seed_calls == []
    assert len(statements) == 1
    assert statements[0].lstrip().upper().startswith("SELECT")


@pytest.mark.integration
@requires_db
def test_request_path_falls_back_to_seeding_and_warns_when_deploy_step_skipped(
    fresh_engine, seed_calls, capture_logs
):
    records = capture_logs("app.sap.services.missions")
    with sessionmaker(bind=fresh_engine, expire_on_commit=False)() as s:
        SAPMissionService.ensure_missions_seeded(s)
        assert _mission_count(s) == len(SEED_MISSIONS)
        SAPMissionService.ensure_missions_seeded(s)  # now a no-op

    assert seed_calls == [1]
    warnings = [r for r in records if r.levelno == logging.WARNING]
    assert len(warnings) == 1 and "python -m app.sap.seed" in warnings[0].getMessage()


@pytest.mark.integration
@requires_db
def test_listing_missions_does_not_resync_definitions(fresh_engine, seed_calls, monkeypatch):
    monkeypatch.setattr(seed_cli, "SessionLocal", sessionmaker(bind=fresh_engine, expire_on_commit=False))
    seed_cli.seed()
    seed_calls.clear()

    with sessionmaker(bind=fresh_engine, expire_on_commit=False)() as s:
        user = User(id=uuid.uuid4(), email=f"{uuid.uuid4().hex[:8]}@example.com", name="Learner")
        s.add(user)
        s.flush()
        missions = SAPMissionService.list_missions_for_user(s, user.id)
        s.rollback()

    assert seed_calls == []
    assert len(missions) == len(SEED_MISSIONS)


# --- deploy configuration ---------------------------------------------------------------


def _ordered(command: str, *steps: str) -> bool:
    positions = [command.find(step) for step in steps]
    return all(p >= 0 for p in positions) and positions == sorted(positions)


def test_render_runs_both_seeds_after_migrations_and_before_the_server():
    render = REPO / "render.yaml"
    if not render.exists():
        pytest.skip("render.yaml not present in this checkout")
    start = re.search(r"startCommand:\s*\"(.+)\"", render.read_text(encoding="utf-8"))
    assert start is not None
    assert _ordered(start.group(1), *DEPLOY_ORDER)


def test_docker_image_runs_both_seeds_after_migrations_and_before_the_server():
    dockerfile = REPO / "backend" / "Dockerfile"
    if not dockerfile.exists():
        pytest.skip("Dockerfile not present in this checkout")
    cmd = [line for line in dockerfile.read_text(encoding="utf-8").splitlines() if line.startswith("CMD")]
    assert len(cmd) == 1
    assert _ordered(cmd[0], *DEPLOY_ORDER)
