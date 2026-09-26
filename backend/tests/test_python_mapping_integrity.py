"""Python Practice mapping integrity (Batch 3).

The day -> practice-problem map (CURRICULUM_DAY_PRACTICE) is the single authority; the
reverse lookup is derived from it. These tests prove the derivation is exact over all 160
days, that duplicate-slug days are explicit, and that no submission can credit a day the
problem is not authoritatively mapped to, including the nine previously stale reverse
entries (Days 50, 60, 75, 110, 120, 135, 145, 160).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select

from app.api.deps import get_db
from app.core.curriculum_map import (
    CURRICULUM_DAY_PRACTICE,
    PRACTICE_SLUG_TO_DAYS,
    is_practice_for_day,
    practice_days_for_slug,
)
from app.main import app
from app.models.models import Problem, Submission, Topic, UserLearningDayState
from app.seed import PROBLEMS
from app.services.learning import compute_user_progress, record_practice_passed

# Reverse-only entries that existed in the old hand-written map: (slug, day it wrongly
# pointed at). Kept here as regression fixtures; none may ever credit that day again.
FORMERLY_STALE = [
    ("container-most-water", 50),
    ("relative-sort-array", 60),
    ("lru-cache", 75),
    ("serialize-and-deserialize-binary-tree", 110),
    ("find-median-from-data-stream", 120),
    ("network-delay-time", 135),
    ("gas-station", 145),
    ("n-queens", 160),
    ("word-search-ii", 160),
]

EXPECTED_DUPLICATES = {
    "sort-colors": (22, 57),
    "trapping-rain-water": (40, 50),
    "sort-an-array": (56, 60),
    "longest-consecutive-sequence": (70, 75),
    "valid-parentheses": (86, 87),
    "validate-binary-search-tree": (101, 110),
    "merge-k-sorted-lists": (115, 120),
    "find-median-from-data-stream": (116, 119),
    "min-cost-to-connect-all-points": (131, 132),
    "critical-connections-in-a-network": (133, 134),
    "maximum-units-on-a-truck": (136, 138),
    "candy": (143, 145),
}


# =============================================================================
# 1. Static mapping integrity over all 160 days
# =============================================================================

def test_forward_map_covers_all_160_days_with_existing_problems():
    assert sorted(CURRICULUM_DAY_PRACTICE) == list(range(1, 161))
    seeded = {p["slug"] for p in PROBLEMS}
    missing = {d: s for d, s in CURRICULUM_DAY_PRACTICE.items() if s not in seeded}
    assert missing == {}


def test_reverse_lookup_is_exactly_the_inverse_of_the_forward_map():
    expected: dict[str, list[int]] = {}
    for day in range(1, 161):
        expected.setdefault(CURRICULUM_DAY_PRACTICE[day], []).append(day)
    assert {s: list(d) for s, d in PRACTICE_SLUG_TO_DAYS.items()} == expected
    # No stale reverse-only relationship survives.
    for slug, days in PRACTICE_SLUG_TO_DAYS.items():
        for day in days:
            assert CURRICULUM_DAY_PRACTICE[day] == slug, (slug, day)


def test_duplicate_slug_days_are_explicit_and_complete():
    dups = {s: tuple(d) for s, d in PRACTICE_SLUG_TO_DAYS.items() if len(d) > 1}
    assert dups == EXPECTED_DUPLICATES
    for slug, days in EXPECTED_DUPLICATES.items():
        assert practice_days_for_slug(slug) == days
        assert all(is_practice_for_day(slug, d) for d in days)


def test_reverse_lookup_is_read_only():
    with pytest.raises(TypeError):
        PRACTICE_SLUG_TO_DAYS["x"] = (1,)  # type: ignore[index]
    assert isinstance(PRACTICE_SLUG_TO_DAYS["candy"], tuple)


@pytest.mark.parametrize("slug,day", FORMERLY_STALE)
def test_formerly_stale_pairs_are_not_mappings(slug, day):
    assert not is_practice_for_day(slug, day)
    assert day not in practice_days_for_slug(slug)


# =============================================================================
# Helpers (DB)
# =============================================================================

def _user(db):
    from app.models.models import User
    u = User(id=uuid.uuid4(), email=f"map_{uuid.uuid4().hex[:8]}@example.com", name="Map")
    db.add(u)
    db.commit()
    return u


def _complete_days(db, user_id, days):
    now = datetime.now(timezone.utc)
    for d in days:
        db.add(UserLearningDayState(
            user_id=user_id, day_number=d, lesson_completed=True, lesson_completed_at=now,
            practice_passed=True, practice_passed_at=now, completed=True, completed_at=now,
        ))
    db.commit()


def _rows(db, user_id):
    db.expire_all()
    return sorted(
        (r.day_number, r.lesson_completed, r.practice_passed, r.practice_passed_at, r.completed)
        for r in db.execute(select(UserLearningDayState).where(UserLearningDayState.user_id == user_id)).scalars()
    )


# =============================================================================
# 2. Service-level progression rules
# =============================================================================

@pytest.mark.parametrize("slug,day", FORMERLY_STALE)
def test_formerly_stale_slug_never_credits_that_day(db, slug, day):
    """Learner sits exactly on the formerly-stale day; the slug must not credit it."""
    user = _user(db)
    _complete_days(db, user.id, range(1, day))
    assert compute_user_progress(db, user.id)["day_states"][str(day)]["unlocked"] is True
    before = _rows(db, user.id)

    with pytest.raises(ValueError, match="not mapped"):
        record_practice_passed(db, user.id, slug, day_number=day)
    assert record_practice_passed(db, user.id, slug) is None  # its real days are already passed
    assert _rows(db, user.id) == before


def test_forged_day_number_raises_with_zero_mutation(db):
    user = _user(db)
    before = _rows(db, user.id)
    with pytest.raises(ValueError, match="not mapped"):
        record_practice_passed(db, user.id, CURRICULUM_DAY_PRACTICE[1], day_number=2)
    with pytest.raises(ValueError, match="does not exist"):
        record_practice_passed(db, user.id, CURRICULUM_DAY_PRACTICE[1], day_number=161)
    with pytest.raises(ValueError, match="locked"):
        record_practice_passed(db, user.id, CURRICULUM_DAY_PRACTICE[3], day_number=3)
    assert _rows(db, user.id) == before


def test_omitted_day_credits_the_single_eligible_day(db):
    user = _user(db)
    res = record_practice_passed(db, user.id, CURRICULUM_DAY_PRACTICE[1])
    assert res["affected_days"] == [1]
    assert _rows(db, user.id)[0][:3] == (1, False, True)


def test_omitted_day_never_credits_a_locked_day(db):
    user = _user(db)
    assert record_practice_passed(db, user.id, CURRICULUM_DAY_PRACTICE[5]) is None
    assert _rows(db, user.id) == []


def test_duplicate_slug_credits_only_the_eligible_occurrence(db):
    """valid-parentheses is Day 86 and 87: with 86 passed and 87 open, only 87 is credited."""
    user = _user(db)
    _complete_days(db, user.id, range(1, 87))
    res = record_practice_passed(db, user.id, "valid-parentheses")
    assert res["affected_days"] == [87]
    # Both occurrences now passed: a further standalone solve changes nothing.
    snap = _rows(db, user.id)
    assert record_practice_passed(db, user.id, "valid-parentheses") is None
    assert _rows(db, user.id) == snap


def test_duplicate_slug_later_occurrence_locked_credits_earlier_only(db):
    user = _user(db)
    _complete_days(db, user.id, range(1, 22))
    res = record_practice_passed(db, user.id, "sort-colors")
    assert res["affected_days"] == [22]
    day57 = [r for r in _rows(db, user.id) if r[0] == 57]
    assert day57 == []


def test_ambiguous_duplicate_is_not_inferred(db, monkeypatch):
    """Two mapped days both open and unpassed: no guessing, no mutation.

    Real progress cannot produce this (only the frontier day is ever open and unpassed), so
    the rule is exercised against a crafted progress snapshot.
    """
    import app.services.learning as learning

    user = _user(db)
    real = learning.compute_user_progress

    def two_open_days(db_, user_id):
        prog = real(db_, user_id)
        for d in ("86", "87"):
            prog["day_states"][d] = {**prog["day_states"][d], "unlocked": True, "practice_passed": False}
        return prog

    monkeypatch.setattr(learning, "compute_user_progress", two_open_days)
    assert learning.record_practice_passed(db, user.id, "valid-parentheses") is None
    assert _rows(db, user.id) == []
    # Explicit day context still credits exactly that day.
    res = learning.record_practice_passed(db, user.id, "valid-parentheses", day_number=87)
    assert res["affected_days"] == [87]
    assert [r[0] for r in _rows(db, user.id)] == [87]


def test_non_curriculum_problem_changes_no_progression(db):
    user = _user(db)
    assert record_practice_passed(db, user.id, "not-a-curriculum-problem") is None
    assert _rows(db, user.id) == []


def test_repeated_explicit_submission_is_idempotent(db):
    user = _user(db)
    record_practice_passed(db, user.id, CURRICULUM_DAY_PRACTICE[1], day_number=1)
    first = _rows(db, user.id)
    for _ in range(3):
        record_practice_passed(db, user.id, CURRICULUM_DAY_PRACTICE[1], day_number=1)
    assert _rows(db, user.id) == first


# =============================================================================
# 3. API-level: forged / omitted / standalone submissions
# =============================================================================

@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth(client):
    name = f"map_api_{uuid.uuid4().hex[:8]}"
    r = client.post("/api/auth/register", json={"username": name, "password": "SecurePassword123!",
                                                 "email": f"{name}@example.com", "name": "Map API"})
    assert r.status_code == 200, r.text
    return {"headers": {"Authorization": f"Bearer {r.json()['access_token']}"},
            "user_id": uuid.UUID(r.json()["user"]["id"])}


def _problem(db, slug):
    existing = db.execute(select(Problem).where(Problem.slug == slug)).scalars().first()
    if existing:
        return existing
    topic = db.execute(select(Topic).where(Topic.slug == "map-tests")).scalars().first()
    if not topic:
        topic = Topic(id=uuid.uuid4(), name="Map Tests", slug="map-tests")
        db.add(topic)
        db.commit()
    p = Problem(id=uuid.uuid4(), topic_id=topic.id, title=slug, slug=slug, statement_md="Echo.",
                difficulty_tier=1, optimal_time="O(1)", optimal_space="O(1)", entry_point="echo",
                test_cases=[{"args": [1], "expected": 1}, {"args": [2], "expected": 2}],
                starter_code={"python": "def echo(x):\n    pass\n"})
    db.add(p)
    db.commit()
    return p


SOLUTION = "def echo(x):\n    return x\n"


def _submission_count(db, user_id):
    return db.execute(select(func.count()).select_from(Submission).where(Submission.user_id == user_id)).scalar_one()


def test_api_forged_day_number_rejected_before_execution(client, db, auth):
    prob = _problem(db, "container-most-water")
    _complete_days(db, auth["user_id"], range(1, 50))
    before = _rows(db, auth["user_id"])
    res = client.post("/api/submissions", headers=auth["headers"], json={
        "problem_id": str(prob.id), "language": "python", "code": SOLUTION, "day_number": 50})
    assert res.status_code == 400
    assert _rows(db, auth["user_id"]) == before
    assert _submission_count(db, auth["user_id"]) == 0


def test_api_omitted_day_on_formerly_stale_slug_credits_nothing(client, db, auth):
    prob = _problem(db, "container-most-water")
    _complete_days(db, auth["user_id"], range(1, 50))  # Day 39 passed, Day 50 open
    before = _rows(db, auth["user_id"])
    res = client.post("/api/submissions", headers=auth["headers"], json={
        "problem_id": str(prob.id), "language": "python", "code": SOLUTION})
    assert res.status_code == 200 and res.json()["tests"]["all_passed"] is True
    assert _rows(db, auth["user_id"]) == before  # Day 50 NOT credited
    assert _submission_count(db, auth["user_id"]) == 1  # standalone practice still recorded


def test_api_standalone_practice_on_non_curriculum_problem(client, db, auth):
    prob = _problem(db, f"standalone-{uuid.uuid4().hex[:6]}")
    res = client.post("/api/submissions", headers=auth["headers"], json={
        "problem_id": str(prob.id), "language": "python", "code": SOLUTION})
    assert res.status_code == 200 and res.json()["tests"]["all_passed"] is True
    assert _rows(db, auth["user_id"]) == []
    assert _submission_count(db, auth["user_id"]) == 1


def test_api_duplicate_accepted_submission_is_idempotent(client, db, auth):
    prob = _problem(db, CURRICULUM_DAY_PRACTICE[1])
    body = {"problem_id": str(prob.id), "language": "python", "code": SOLUTION, "day_number": 1}
    assert prob.entry_point == "echo", "test DB must not contain a seeded Day 1 problem"
    assert client.post("/api/submissions", headers=auth["headers"], json=body).status_code == 200
    first = _rows(db, auth["user_id"])
    assert first and first[0][2] is True
    assert client.post("/api/submissions", headers=auth["headers"], json=body).status_code == 200
    assert _rows(db, auth["user_id"]) == first
