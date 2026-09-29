"""First-use creation of shared SAP catalog rows must be safe under concurrency.

Regression for a live E2E failure: two learners submitting placement at the same time on
a fresh database both tried to INSERT the same sap_concepts row; the loser got a
UniqueViolation and a 500. The interleaving is forced deterministically here: session A
inserts and holds its transaction open, session B blocks on the unique index, and A
commits only once Postgres reports B waiting on that lock.
"""

from __future__ import annotations

import threading
import time
import uuid
from types import SimpleNamespace

import pytest
from sqlalchemy import delete, select, text
from sqlalchemy.orm import Session, sessionmaker

from app.models.sap_models import SAPConcept, SAPEnterprise
from app.sap.services import enterprise as enterprise_mod
from app.sap.services import mastery
from tests.conftest import requires_db

pytestmark = [pytest.mark.integration, requires_db]


def _wait_for_lock_waiter(engine, worker: threading.Thread, out: dict, timeout_s: float = 15.0) -> None:
    """Block until some other backend in this database is waiting on a lock."""
    deadline = time.monotonic() + timeout_s
    with engine.connect() as conn:
        while time.monotonic() < deadline:
            if not worker.is_alive():
                # B finished without ever waiting: report what it actually did.
                if "error" in out:
                    raise AssertionError("session B failed before blocking") from out["error"]
                raise AssertionError(f"session B finished without blocking: {out.get('b')!r}")
            waiting = conn.execute(
                text(
                    "SELECT count(*) FROM pg_stat_activity "
                    "WHERE datname = current_database() AND wait_event_type = 'Lock'"
                )
            ).scalar_one()
            # pg_stat_activity is cached per transaction (stats_fetch_consistency=cache);
            # end it so the next poll sees fresh activity instead of the first snapshot.
            conn.rollback()
            if waiting:
                return
            time.sleep(0.02)
    raise AssertionError("second session never blocked on the unique index")


def _run_contended(engine, first, second):
    """Run `first` in session A (left uncommitted), then `second` in session B, which must
    block on A's uncommitted row; commit A; return (A result, B result, B session)."""
    make = sessionmaker(bind=engine, expire_on_commit=False)
    a, b = make(), make()
    out: dict[str, object] = {}

    def run_b():
        try:
            out["b"] = second(b)
        except BaseException as exc:  # surfaced to the main thread below
            out["error"] = exc

    try:
        out["a"] = first(a)
        worker = threading.Thread(target=run_b)
        worker.start()
        _wait_for_lock_waiter(engine, worker, out)
        a.commit()
        worker.join(timeout=15)
        assert not worker.is_alive(), "session B never finished"
        if "error" in out:
            raise out["error"]  # type: ignore[misc]
        return out["a"], out["b"], b
    finally:
        a.close()
        # b is returned open for the caller to verify; close it there.


def test_concurrent_first_use_of_a_concept_returns_the_winner_row(engine, migrated, monkeypatch):
    slug = f"race-concept-{uuid.uuid4().hex[:10]}"
    meta = SimpleNamespace(slug=slug, name="Race Concept", category="testing", difficulty=1)
    stub_engine = SimpleNamespace(get_concept=lambda s: meta if s == slug else None)
    monkeypatch.setattr(
        mastery.SAPCurriculumKnowledgeEngine, "get_instance", classmethod(lambda cls, *a: stub_engine)
    )

    b_session: Session | None = None
    try:
        a_row, b_row, b_session = _run_contended(
            engine,
            lambda s: mastery.get_or_create_concept(s, slug),
            lambda s: mastery.get_or_create_concept(s, slug),
        )
        assert a_row is not None and b_row is not None
        assert b_row.id == a_row.id  # type: ignore[union-attr]
        # B's transaction survived the unique violation: it can keep working and commit.
        assert b_session.execute(select(SAPConcept.id).where(SAPConcept.slug == slug)).scalar_one() == a_row.id  # type: ignore[union-attr]
        b_session.commit()
    finally:
        if b_session is not None:
            b_session.close()
        with engine.begin() as conn:
            conn.execute(delete(SAPConcept).where(SAPConcept.slug == slug))


def test_unknown_concept_is_not_created(engine, migrated, monkeypatch):
    stub_engine = SimpleNamespace(get_concept=lambda s: None)
    monkeypatch.setattr(
        mastery.SAPCurriculumKnowledgeEngine, "get_instance", classmethod(lambda cls, *a: stub_engine)
    )
    with sessionmaker(bind=engine)() as s:
        assert mastery.get_or_create_concept(s, f"nope-{uuid.uuid4().hex}") is None
        s.rollback()


def test_concurrent_first_use_of_the_enterprise_template(fresh_engine):
    engine = fresh_engine
    b_session: Session | None = None
    try:
        # A inserts but must not commit before B blocks, so stage A by hand with the same
        # INSERT the service performs; B runs the real service method.
        def stage_a(s: Session):
            data = enterprise_mod.NOVA_MANUFACTURING_TEMPLATE
            row = SAPEnterprise(
                slug=data["slug"], name=data["name"], code=data["code"], industry=data["industry"],
                description_md=data["description_md"], template_state=data["template_state"],
                landscape_metadata=data["landscape_metadata"], is_active=True,
            )
            s.add(row)
            s.flush()
            return row

        a_row, b_row, b_session = _run_contended(
            engine, stage_a, lambda s: enterprise_mod.SAPEnterpriseService.get_or_create_template(s)
        )
        assert b_row.id == a_row.id  # type: ignore[union-attr]
        b_session.commit()
    finally:
        if b_session is not None:
            b_session.close()
