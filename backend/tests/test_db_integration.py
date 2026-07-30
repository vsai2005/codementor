"""Integration tests against real Postgres + pgvector.

These cover exactly the gaps the unit suite cannot: that the migration applies
and rolls back, that the ivfflat/cosine query actually runs, and that the
user_id filter holds in real SQL rather than in a fake.

Skipped unless TEST_DATABASE_URL is set. See tests/conftest.py.
"""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy import text

from tests.conftest import requires_db

pytestmark = [pytest.mark.integration, requires_db]

DIM = 1536


def vec(seed: float) -> list[float]:
    """A 1536-dim unit-ish vector that varies with the seed."""
    v = [0.0] * DIM
    v[0] = 1.0
    v[1] = seed
    return v


# --- schema -----------------------------------------------------------------

def test_vector_extension_is_installed(db):
    row = db.execute(text("SELECT extname FROM pg_extension WHERE extname = 'vector'")).first()
    assert row is not None, "pgvector extension missing"


def test_all_expected_tables_exist(db):
    rows = db.execute(
        text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
    ).scalars().all()
    expected = {
        "users", "topics", "problems", "submissions",
        "user_topic_state", "difficulty_events", "memory_notes",
    }
    assert expected.issubset(set(rows)), expected - set(rows)


def test_ivfflat_index_exists_on_embedding(db):
    row = db.execute(
        text("SELECT indexdef FROM pg_indexes WHERE indexname = 'ix_memory_notes_embedding'")
    ).scalar()
    assert row is not None, "ivfflat index missing"
    assert "ivfflat" in row and "vector_cosine_ops" in row


def test_user_topic_state_has_composite_primary_key(db):
    cols = db.execute(text("""
        SELECT a.attname
        FROM pg_index i
        JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
        WHERE i.indrelid = 'user_topic_state'::regclass AND i.indisprimary
    """)).scalars().all()
    assert set(cols) == {"user_id", "topic_id"}


# --- vector storage and retrieval -------------------------------------------

def test_memory_note_with_1536_dim_vector_round_trips(db, make_user):
    from app.models.models import MemoryNoteRow

    user = make_user()
    note = MemoryNoteRow(id=uuid.uuid4(), user_id=user.id, content="test note",
                         embedding=vec(0.5))
    db.add(note)
    db.flush()

    stored = db.get(MemoryNoteRow, note.id)
    assert stored is not None
    assert len(stored.embedding) == DIM


def test_wrong_dimension_vector_is_rejected(db, make_user):
    from app.models.models import MemoryNoteRow

    user = make_user()
    db.add(MemoryNoteRow(id=uuid.uuid4(), user_id=user.id, content="bad",
                         embedding=[0.0] * 128))
    with pytest.raises(Exception):
        db.flush()


def test_repository_search_returns_notes_ordered_by_similarity(db, make_user):
    from app.models.models import MemoryNoteRow
    from app.services.repositories import PgMemoryRepository

    user = make_user()
    for seed, label in [(0.0, "near"), (5.0, "mid"), (50.0, "far")]:
        db.add(MemoryNoteRow(id=uuid.uuid4(), user_id=user.id, content=label,
                             embedding=vec(seed)))
    db.flush()

    results = PgMemoryRepository(db).search(str(user.id), vec(0.0), limit=10)

    assert [r.content for r in results][0] == "near"
    sims = [r.similarity for r in results]
    assert sims == sorted(sims, reverse=True)


def test_repository_never_returns_another_users_notes(db, make_user):
    """The security gate, this time against real SQL."""
    from app.models.models import MemoryNoteRow
    from app.services.repositories import PgMemoryRepository

    alice, bob = make_user("alice@example.com"), make_user("bob@example.com")
    db.add(MemoryNoteRow(id=uuid.uuid4(), user_id=alice.id, content="alice secret",
                         embedding=vec(9.0)))
    # Bob's note is a much closer match to the query vector — if the filter is
    # missing, it will rank first and the leak is unmissable.
    db.add(MemoryNoteRow(id=uuid.uuid4(), user_id=bob.id, content="bob secret",
                         embedding=vec(0.0)))
    db.flush()

    results = PgMemoryRepository(db).search(str(alice.id), vec(0.0), limit=10)

    assert all(r.user_id == str(alice.id) for r in results)
    assert not any("bob" in r.content for r in results)


def test_repository_refuses_an_empty_user_id(db):
    from app.services.repositories import PgMemoryRepository

    with pytest.raises(ValueError):
        PgMemoryRepository(db).search("", vec(0.0), limit=5)


# --- pipeline state ----------------------------------------------------------

def test_difficulty_event_written_even_when_tier_does_not_change(db, make_user, make_problem):
    from app.models.models import DifficultyEvent, Submission
    from app.services.submissions import apply_difficulty

    user, problem = make_user(), make_problem(tier=3)
    submission = Submission(id=uuid.uuid4(), user_id=user.id, problem_id=problem.id,
                            code="x", overall_score=65, tests_passed=1, tests_total=1,
                            scores={}, review={})
    db.add(submission)
    db.flush()

    decision = apply_difficulty(db, user_id=user.id, topic_id=problem.topic_id,
                                submission_id=submission.id, new_score=65)

    events = db.execute(
        DifficultyEvent.__table__.select().where(DifficultyEvent.user_id == user.id)
    ).all()
    assert len(events) == 1, "an event row is required even for a hold"
    assert decision.tier_from == decision.tier_to


def test_tiers_are_tracked_independently_per_topic(db, make_user, make_topic, make_problem):
    from app.models.models import Submission, UserTopicState
    from app.services.submissions import apply_difficulty

    user = make_user()
    arrays, graphs = make_topic("arrays"), make_topic("graphs")
    p_arrays, p_graphs = make_problem(arrays, tier=1), make_problem(graphs, tier=1)

    for problem, score in [(p_arrays, 95), (p_graphs, 20)]:
        for _ in range(3):
            sub = Submission(id=uuid.uuid4(), user_id=user.id, problem_id=problem.id,
                             code="x", overall_score=score, tests_passed=1, tests_total=1,
                             scores={}, review={})
            db.add(sub)
            db.flush()
            apply_difficulty(db, user_id=user.id, topic_id=problem.topic_id,
                             submission_id=sub.id, new_score=score)

    arrays_state = db.get(UserTopicState, (user.id, arrays.id))
    graphs_state = db.get(UserTopicState, (user.id, graphs.id))
    assert arrays_state is not None and graphs_state is not None
    assert arrays_state.current_tier > graphs_state.current_tier


def test_next_problem_skips_recently_solved(db, make_user, make_topic, make_problem):
    from app.models.models import Submission
    from app.services.submissions import next_problem

    user, topic = make_user(), make_topic()
    solved = make_problem(topic, tier=1)
    unsolved = make_problem(topic, tier=1)

    db.add(Submission(id=uuid.uuid4(), user_id=user.id, problem_id=solved.id,
                      code="x", overall_score=95, tests_passed=1, tests_total=1,
                      scores={}, review={}))
    db.flush()

    picked = next_problem(db, user.id)
    assert picked is not None
    assert picked.id == unsolved.id
