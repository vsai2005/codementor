"""SAP Curriculum Progression Service.

Computes milestones, lesson completion, and unlocks across the 100-day S/4HANA journey.
Strictly isolated from Python's UserLearningDayState and 160-day logic.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.sap_curriculum_retrieval import SAPCurriculumKnowledgeEngine
from app.models.sap_models import (
    SAPDayStatus,
    SAPPlacementProfile,
    SAPUserDayState,
    SAPUserState,
)


class SAPProgressionService:
    TOTAL_DAYS = 100

    @classmethod
    def compute_user_progress(cls, db: Session, user_id: uuid.UUID) -> dict:
        """Computes complete 100-day S/4HANA curriculum progress using 5 explicit day states."""
        # 1. Fetch placement profile for recommended starting day or waived days
        placement = db.execute(
            select(SAPPlacementProfile).where(SAPPlacementProfile.user_id == user_id)
        ).scalar_one_or_none()

        waived_by_placement = set(placement.diagnostic_results.get("waived_days", [])) if placement else set()
        starting_day = placement.recommended_start_day if placement else 1

        # 2. Fetch all recorded day states for this user
        rows = db.execute(
            select(SAPUserDayState).where(SAPUserDayState.user_id == user_id)
        ).scalars().all()
        state_by_day = {r.day_number: r for r in rows}

        completed_days: list[int] = []
        waived_days: list[int] = sorted(list(waived_by_placement))
        day_states: dict[str, dict] = {}
        found_current = False
        current_day = starting_day

        for day in range(1, cls.TOTAL_DAYS + 1):
            r = state_by_day.get(day)
            lesson_started = bool(r.lesson_started) if r else False
            lesson_done = bool(r.lesson_completed) if r else False
            assessment_done = bool(r.assessment_passed) if r else False
            practice_done = bool(r.practice_completed) if r else False
            is_waived = (day in waived_by_placement) or (bool(r.waived) if r else False)

            # Strictly completed ONLY if lesson, practice, and assessment were passed and not waived
            is_completed = lesson_done and practice_done and assessment_done and not is_waived

            if is_completed:
                completed_days.append(day)

            # Unlocked logic: Day 1, or starting day, or prior day completed/waived, or in placement waiver
            prior_cleared = (day == 1) or ((day - 1) in completed_days) or ((day - 1) in waived_days)
            is_unlocked = prior_cleared or (day == starting_day) or is_waived

            # Compute explicit 5-state status
            if is_completed:
                st = SAPDayStatus.COMPLETED.value
            elif is_waived:
                st = SAPDayStatus.WAIVED_BY_PLACEMENT.value
            elif not is_unlocked:
                st = SAPDayStatus.LOCKED.value
            else:
                if lesson_started or practice_done or lesson_done:
                    st = SAPDayStatus.IN_PROGRESS.value
                elif not found_current and day >= starting_day:
                    st = SAPDayStatus.IN_PROGRESS.value if lesson_started else SAPDayStatus.AVAILABLE.value
                else:
                    st = SAPDayStatus.AVAILABLE.value

                if not found_current and day >= starting_day and not is_waived:
                    current_day = day
                    found_current = True

            day_states[str(day)] = {
                "day_number": day,
                "lesson_completed": lesson_done,
                "lesson_completed_at": r.lesson_completed_at if r else None,
                "practice_completed": practice_done,
                "practice_completed_at": r.practice_completed_at if r else None,
                "assessment_passed": assessment_done,
                "assessment_passed_at": r.assessment_passed_at if r else None,
                "completed": is_completed,
                "completed_at": r.completed_at if r else None,
                "waived": is_waived,
                "unlocked": is_unlocked,
                "status": st,
            }

        if not found_current:
            for d in range(1, cls.TOTAL_DAYS + 1):
                if d not in completed_days and d not in waived_days:
                    current_day = d
                    break
            else:
                current_day = cls.TOTAL_DAYS

        return {
            "course_slug": "sap-s4hana-mastery",
            "current_day": current_day,
            "completed_days": completed_days,
            "waived_days": waived_days,
            "total_days": cls.TOTAL_DAYS,
            "day_states": day_states,
        }

    @classmethod
    def complete_lesson(cls, db: Session, user_id: uuid.UUID, day_number: int) -> dict:
        if day_number < 1 or day_number > cls.TOTAL_DAYS:
            raise ValueError(f"SAP Day {day_number} does not exist. Valid curriculum days are 1–{cls.TOTAL_DAYS}.")

        progress = cls.compute_user_progress(db, user_id)
        day_info = progress["day_states"].get(str(day_number))

        if not day_info or not day_info["unlocked"]:
            raise ValueError(f"SAP Day {day_number} is locked. Complete Day {day_number - 1} or diagnostic placement first.")

        r = db.execute(
            select(SAPUserDayState).where(
                SAPUserDayState.user_id == user_id,
                SAPUserDayState.day_number == day_number,
            )
        ).scalar_one_or_none()

        now = datetime.now(timezone.utc)
        if r is None:
            r = SAPUserDayState(
                user_id=user_id,
                day_number=day_number,
                status=SAPDayStatus.IN_PROGRESS.value,
                lesson_started=True,
                lesson_started_at=now,
                lesson_completed=True,
                lesson_completed_at=now,
            )
            db.add(r)
        else:
            r.lesson_completed = True
            if not r.lesson_completed_at:
                r.lesson_completed_at = now
            if not r.completed and r.status != SAPDayStatus.WAIVED_BY_PLACEMENT.value:
                r.status = SAPDayStatus.IN_PROGRESS.value

        was_already_completed = bool(r.completed)
        can_complete = bool(
            r.lesson_completed
            and r.practice_completed
            and r.assessment_passed
            and r.status != SAPDayStatus.WAIVED_BY_PLACEMENT.value
        )

        if can_complete and not was_already_completed:
            r.completed = True
            r.completed_at = now
            r.status = SAPDayStatus.COMPLETED.value

        # Update or create macro SAPUserState only if newly completed
        if can_complete and not was_already_completed:
            user_state = db.execute(
                select(SAPUserState).where(SAPUserState.user_id == user_id)
            ).scalar_one_or_none()
            if user_state is None:
                user_state = SAPUserState(
                    user_id=user_id,
                    current_recommended_day=min(cls.TOTAL_DAYS, day_number + 1),
                    completed_days_count=1,
                    last_active_at=now,
                )
                db.add(user_state)
            else:
                user_state.last_active_at = now
                if day_number == user_state.current_recommended_day:
                    user_state.current_recommended_day = min(cls.TOTAL_DAYS, day_number + 1)
                    user_state.completed_days_count += 1
        else:
            user_state = db.execute(
                select(SAPUserState).where(SAPUserState.user_id == user_id)
            ).scalar_one_or_none()
            if user_state:
                user_state.last_active_at = now

        db.commit()
        db.refresh(r)

        updated = cls.compute_user_progress(db, user_id)
        return {
            "day_number": day_number,
            "lesson_completed": True,
            "day_completed": r.completed,
            "unlocked_next_day": r.completed and day_number < cls.TOTAL_DAYS,
            "current_day": updated["current_day"],
            "day_state": updated["day_states"][str(day_number)],
        }

    @classmethod
    def record_practice_completed(cls, db: Session, user_id: uuid.UUID, day_number: int) -> dict:
        if day_number < 1 or day_number > cls.TOTAL_DAYS:
            raise ValueError(f"SAP Day {day_number} does not exist. Valid curriculum days are 1–{cls.TOTAL_DAYS}.")

        progress = cls.compute_user_progress(db, user_id)
        day_info = progress["day_states"].get(str(day_number))

        if not day_info or not day_info["unlocked"]:
            raise ValueError(f"SAP Day {day_number} is locked. Complete Day {day_number - 1} or diagnostic placement first.")

        if day_info.get("waived"):
            raise ValueError(f"SAP Day {day_number} was waived by diagnostic placement.")

        r = db.execute(
            select(SAPUserDayState).where(
                SAPUserDayState.user_id == user_id,
                SAPUserDayState.day_number == day_number,
            )
        ).scalar_one_or_none()

        now = datetime.now(timezone.utc)
        if r is None:
            r = SAPUserDayState(
                user_id=user_id,
                day_number=day_number,
                status=SAPDayStatus.IN_PROGRESS.value,
                lesson_started=True,
                lesson_started_at=now,
                practice_completed=True,
                practice_completed_at=now,
            )
            db.add(r)
        else:
            r.practice_completed = True
            r.practice_completed_at = now
            if not r.completed and r.status != SAPDayStatus.WAIVED_BY_PLACEMENT.value:
                r.status = SAPDayStatus.IN_PROGRESS.value

        was_already_completed = bool(r.completed)
        can_complete = bool(
            r.lesson_completed
            and r.practice_completed
            and r.assessment_passed
            and r.status != SAPDayStatus.WAIVED_BY_PLACEMENT.value
        )

        if can_complete and not was_already_completed:
            r.completed = True
            r.completed_at = now
            r.status = SAPDayStatus.COMPLETED.value

        # Update macro SAPUserState only if newly completed
        if can_complete and not was_already_completed:
            user_state = db.execute(
                select(SAPUserState).where(SAPUserState.user_id == user_id)
            ).scalar_one_or_none()
            if user_state is None:
                user_state = SAPUserState(
                    user_id=user_id,
                    current_recommended_day=min(cls.TOTAL_DAYS, day_number + 1),
                    completed_days_count=1,
                    last_active_at=now,
                )
                db.add(user_state)
            else:
                user_state.last_active_at = now
                if day_number == user_state.current_recommended_day:
                    user_state.current_recommended_day = min(cls.TOTAL_DAYS, day_number + 1)
                    user_state.completed_days_count += 1
        else:
            user_state = db.execute(
                select(SAPUserState).where(SAPUserState.user_id == user_id)
            ).scalar_one_or_none()
            if user_state:
                user_state.last_active_at = now

        db.commit()
        db.refresh(r)

        updated = cls.compute_user_progress(db, user_id)
        return {
            "day_number": day_number,
            "practice_completed": True,
            "day_completed": r.completed,
            "unlocked_next_day": r.completed and day_number < cls.TOTAL_DAYS,
            "current_day": updated["current_day"],
            "day_state": updated["day_states"][str(day_number)],
        }
