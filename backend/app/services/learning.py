"""Service layer for Curriculum Progression (Stage 5)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.curriculum_map import (
    CURRICULUM_DAY_PRACTICE,
    is_practice_for_day,
    practice_days_for_slug,
)
from app.models.models import UserLearningDayState


def compute_user_progress(db: Session, user_id: uuid.UUID) -> dict:
    """Computes full curriculum progress for a user across all 160 days."""
    rows = db.execute(
        select(UserLearningDayState).where(UserLearningDayState.user_id == user_id)
    ).scalars().all()
    state_by_day = {r.day_number: r for r in rows}

    completed_days: list[int] = []
    day_states: dict[str, dict] = {}
    found_current = False
    current_day = 1

    for day in range(1, 161):
        r = state_by_day.get(day)
        lesson_done = bool(r.lesson_completed) if r else False
        practice_done = bool(r.practice_passed) if r else False
        is_completed = lesson_done and practice_done

        if is_completed:
            completed_days.append(day)

        is_unlocked = (day == 1) or ((day - 1) in completed_days)

        if is_completed:
            st = "completed"
        elif is_unlocked:
            if not found_current:
                st = "current"
                current_day = day
                found_current = True
            else:
                st = "available"
        else:
            st = "locked"

        day_states[str(day)] = {
            "day_number": day,
            "lesson_completed": lesson_done,
            "lesson_completed_at": r.lesson_completed_at if r else None,
            "practice_passed": practice_done,
            "practice_passed_at": r.practice_passed_at if r else None,
            "completed": is_completed,
            "completed_at": r.completed_at if r else None,
            "unlocked": is_unlocked,
            "status": st,
            "practice_problem_slug": CURRICULUM_DAY_PRACTICE.get(day),
        }

    if not found_current and len(completed_days) == 160:
        current_day = 160

    return {
        "current_day": current_day,
        "completed_days": completed_days,
        "total_days": 160,
        "day_states": day_states,
    }


def complete_lesson(db: Session, user_id: uuid.UUID, day_number: int) -> dict:
    """Marks day lesson completed after validating day is unlocked."""
    if day_number < 1 or day_number > 160:
        raise ValueError(f"Day {day_number} does not exist. Valid curriculum days are 1–160.")
    progress = compute_user_progress(db, user_id)
    day_info = progress["day_states"].get(str(day_number))
    if not day_info or not day_info["unlocked"]:
        raise ValueError(f"Day {day_number} is locked. Complete Day {day_number - 1} first.")

    r = db.execute(
        select(UserLearningDayState).where(
            UserLearningDayState.user_id == user_id,
            UserLearningDayState.day_number == day_number,
        )
    ).scalar_one_or_none()

    now = datetime.now(timezone.utc)
    if r is None:
        r = UserLearningDayState(
            user_id=user_id,
            day_number=day_number,
            lesson_completed=True,
            lesson_completed_at=now,
        )
        db.add(r)
    else:
        r.lesson_completed = True
        if not r.lesson_completed_at:
            r.lesson_completed_at = now

    if r.practice_passed and not r.completed:
        r.completed = True
        r.completed_at = now

    db.commit()
    db.refresh(r)

    updated = compute_user_progress(db, user_id)
    return {
        "day_number": day_number,
        "lesson_completed": True,
        "day_completed": r.completed,
        "unlocked_next_day": r.completed and day_number < 160,
        "current_day": updated["current_day"],
        "day_state": updated["day_states"][str(day_number)],
    }


def record_practice_passed(
    db: Session,
    user_id: uuid.UUID,
    problem_slug: str,
    day_number: int | None = None,
) -> dict | None:
    """Records that a practice problem was passed and credits ONLY the intended, accessible curriculum day.
    
    Rules:
    - If day_number is provided:
        1. Validates that problem_slug is mapped to day_number.
        2. Validates that day_number is currently accessible (unlocked) for the learner.
        Target day is day_number.
    - If day_number is not provided (standalone Practice):
        A day is inferred ONLY when exactly one day is eligible: a day whose authoritative
        practice problem is problem_slug, that is unlocked, and whose practice is not yet
        passed. Zero eligible days (not a curriculum problem, all mapped days locked, or all
        already passed) or several eligible days (ambiguous) return None with no mutation;
        the learner must submit from the Learning day to credit it explicitly.
    """
    progress = compute_user_progress(db, user_id)
    day_states = progress["day_states"]

    if day_number is not None:
        if day_number < 1 or day_number > 160:
            raise ValueError(f"Day {day_number} does not exist. Valid curriculum days are 1–160.")
        if not is_practice_for_day(problem_slug, day_number):
            raise ValueError(f"Problem '{problem_slug}' is not mapped to Day {day_number}.")
        day_info = day_states.get(str(day_number))
        if not day_info or not day_info["unlocked"]:
            raise ValueError(f"Day {day_number} is locked. Complete prior days first.")
        target_day = day_number
    else:
        eligible = [
            d for d in practice_days_for_slug(problem_slug)
            if day_states.get(str(d), {}).get("unlocked")
            and not day_states[str(d)].get("practice_passed")
        ]
        if len(eligible) != 1:
            return None
        target_day = eligible[0]

    now = datetime.now(timezone.utc)
    newly_completed = []
    affected = [target_day]

    r = db.execute(
        select(UserLearningDayState).where(
            UserLearningDayState.user_id == user_id,
            UserLearningDayState.day_number == target_day,
        )
    ).scalar_one_or_none()

    if r is None:
        r = UserLearningDayState(
            user_id=user_id,
            day_number=target_day,
            practice_passed=True,
            practice_passed_at=now,
        )
        db.add(r)
    else:
        r.practice_passed = True
        if not r.practice_passed_at:
            r.practice_passed_at = now

    if r.lesson_completed and not r.completed:
        r.completed = True
        r.completed_at = now
        newly_completed.append(target_day)

    db.commit()
    updated = compute_user_progress(db, user_id)
    return {
        "problem_slug": problem_slug,
        "affected_days": affected,
        "newly_completed_days": newly_completed,
        "unlocked_days": [d + 1 for d in newly_completed if d < 160],
        "current_day": updated["current_day"],
        "day_states": updated["day_states"],
    }
