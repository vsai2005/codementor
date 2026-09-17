"""SAP Placement and Diagnostic Engine.

Classifies incoming learners into one of 5 distinct enterprise personas:
1. Fresher (Starts Day 1)
2. Beginner (Starts Day 9, skips Days 1–8)
3. Functional SAP User (Starts Day 23, skips Days 1–22)
4. ECC Consultant / Developer (Starts Day 45, skips Days 1–44)
5. Experienced S/4HANA Developer (Starts Day 77, skips Days 1–76)
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sap_models import (
    SAPDayStatus,
    SAPPlacementProfile,
    SAPPlacementStatus,
    SAPUserDayState,
    SAPUserState,
)
from app.sap.data.placement_questions import evaluate_assessment_answers
from app.sap.services.mastery import SAPMasteryService


class SAPPlacementService:
    PERSONA_CONFIG = {
        "fresher": {
            "title": "Fresher / ERP Newcomer",
            "default_start_day": 1,
            "max_waivable_days": [],
            "rationale": "Recommended starting from Day 1 to build solid foundations of enterprise systems, architecture, and core navigation.",
        },
        "beginner": {
            "title": "Beginner / CS Student",
            "default_start_day": 9,
            "max_waivable_days": list(range(1, 9)),
            "rationale": "Demonstrated foundational computing and ERP concepts. Accelerated directly to S/4HANA In-Memory architecture (Day 9).",
        },
        "functional_user": {
            "title": "Functional SAP User / Business Analyst",
            "default_start_day": 23,
            "max_waivable_days": list(range(1, 23)),
            "rationale": "Demonstrated core business processes (P2P/O2C/GL). Accelerated past standard workflows to S/4HANA End-to-End Business Processes (Day 23).",
        },
        "ecc_developer": {
            "title": "ECC Consultant / Classic ABAP Developer",
            "default_start_day": 45,
            "max_waivable_days": list(range(1, 45)),
            "rationale": "Classic ECC/ABAP verified. Fast-tracked to S/4HANA Core Data Services and Code Pushdown (Day 45).",
        },
        "experienced_s4hana": {
            "title": "Experienced S/4HANA Developer / Solution Architect",
            "default_start_day": 77,
            "max_waivable_days": list(range(1, 77)),
            "rationale": "High proficiency in S/4HANA CDS and transactional RAP modeling. Routed to ABAP Cloud & RAP (Day 77).",
        },
    }

    @classmethod
    def evaluate_diagnostic(
        cls,
        db: Session,
        user_id: uuid.UUID,
        experience_level: str | None = None,
        answers: dict[str, str] | None = None,
        domain_scores: dict[str, float] | None = None,
        experience_years: float = 0.0,
        persona_self_select: str | None = None,
        concept_responses: dict[str, float] | None = None,
    ) -> SAPPlacementProfile:
        """Evaluates concept evidence and prerequisite mastery to compute starting day and waived days.

        Never fabricates scores:
        - 'fresher' -> No assessment required, places at Day 1.
        - 'experienced' -> Graded against 10 technical questions; evaluated on overall score + topic scores + prerequisite mastery.
        - 'not_sure' -> Graded against 6 fundamental questions; evaluated on foundational grasp.
        """
        level = (experience_level or persona_self_select or "fresher").strip().lower()
        if level in ("fresher", "beginner_fresher"):
            level = "fresher"

        answers = answers or {}
        demonstrated_concepts: list[str] = []
        gap_concepts: list[str] = []
        evaluated_domain_scores: dict[str, float] = {}
        topic_breakdown: list[dict[str, Any]] = []

        # 1. Evaluate according to track
        if level == "fresher":
            overall_score = 0.0
            starting_day = 1
            resolved_persona = "fresher"
            waived_days = []
            rationale = "Fresher track selected. You will build comprehensive foundational mastery starting at Day 1: Enterprise Systems & Cross-Functional Flows."
            evaluated_domain_scores = {
                "enterprise_architecture": 0.0,
                "s4hana_inmemory": 0.0,
                "business_processes": 0.0,
                "cds_data_semantics": 0.0,
                "abap_cloud_rap": 0.0,
            }

        elif level == "experienced":
            overall_score, evaluated_domain_scores, demonstrated_concepts, gap_concepts = evaluate_assessment_answers(
                "experienced", answers
            )

            arch_score = evaluated_domain_scores.get("enterprise_architecture", 0.0)
            org_score = evaluated_domain_scores.get("org_structure", 0.0)
            inmemory_score = evaluated_domain_scores.get("s4hana_inmemory", 0.0)
            proc_score = evaluated_domain_scores.get("business_processes", 0.0)
            cds_score = evaluated_domain_scores.get("cds_data_semantics", 0.0)
            rap_score = evaluated_domain_scores.get("abap_cloud_rap", 0.0)

            # Check prerequisite mastery:
            has_arch_prereq = "three-tier-architecture" in demonstrated_concepts or arch_score >= 50.0
            has_inmemory_prereq = "acdoca-table-architecture" in demonstrated_concepts or inmemory_score >= 50.0
            has_cds_prereq = "cds-associations-concept" in demonstrated_concepts or cds_score >= 50.0
            has_rap_prereq = "abap-cloud-paradigm" in demonstrated_concepts or rap_score >= 50.0

            # Prerequisite-aware decision tree:
            # Tier 4: Day 77 (ABAP Cloud & RAP)
            if overall_score >= 80.0 and has_arch_prereq and has_inmemory_prereq and cds_score >= 80.0 and rap_score >= 80.0:
                starting_day = 77
                resolved_persona = "experienced_s4hana"
                waived_days = list(range(1, 77))
                rationale = "Exceptional performance across enterprise data modeling, CDS VDM, and RAP transactional architecture. Fast-tracked directly to Phase 7: ABAP Cloud & RAP (Day 77)."

            # Tier 3: Day 45 (HANA Engine & CDS)
            elif overall_score >= 60.0 and has_arch_prereq and (has_inmemory_prereq or cds_score >= 50.0 or proc_score >= 50.0):
                starting_day = 45
                resolved_persona = "ecc_developer"
                waived_days = list(range(1, 45))
                rationale = "Strong proficiency in enterprise architecture, S/4HANA core data models, and business flows. Fast-tracked to Phase 4: HANA Engine & CDS Data Semantics (Day 45)."

            # Tier 2: Day 23 (End-to-End Business Processes)
            elif overall_score >= 40.0 and has_arch_prereq and (proc_score >= 50.0 or has_inmemory_prereq):
                starting_day = 23
                resolved_persona = "functional_user"
                waived_days = list(range(1, 23))
                rationale = "Solid enterprise architecture intuition and business process understanding verified. Fast-tracked to Phase 3: Core End-to-End Business Processes (Day 23)."

            # Tier 1: Day 9 (S/4HANA Architecture)
            elif overall_score >= 30.0 and has_arch_prereq:
                starting_day = 9
                resolved_persona = "beginner"
                waived_days = list(range(1, 9))
                rationale = "Fundamental understanding of 3-tier enterprise architecture demonstrated. Days 1–8 waived; starting at S/4HANA Architecture (Day 9)."

            # Tier 0: Day 1 (Prerequisite conflict or low overall score)
            else:
                starting_day = 1
                resolved_persona = "fresher"
                waived_days = []
                if not has_arch_prereq and overall_score >= 40.0:
                    rationale = "Prerequisite conflict detected: advanced concepts attempted but fundamental enterprise architecture was not demonstrated. Starting from Day 1 ensures full conceptual grounding."
                else:
                    rationale = "Assessment indicated foundational gaps across core enterprise architecture. Starting from Day 1 to build end-to-end fluency."

        elif level == "not_sure":
            overall_score, evaluated_domain_scores, demonstrated_concepts, gap_concepts = evaluate_assessment_answers(
                "not_sure", answers
            )

            has_fund = "erp-evolution" in demonstrated_concepts or evaluated_domain_scores.get("enterprise_architecture", 0.0) >= 50.0
            has_org = "org-structure-company-code" in demonstrated_concepts or evaluated_domain_scores.get("org_structure", 0.0) >= 50.0

            if overall_score >= 80.0 and (has_fund or has_org):
                starting_day = 9
                resolved_persona = "beginner"
                waived_days = list(range(1, 9))
                rationale = "Demonstrated clear grasp of foundational ERP concepts and organizational structures. Days 1–8 waived; starting at S/4HANA In-Memory Architecture (Day 9)."
            else:
                starting_day = 1
                resolved_persona = "fresher"
                waived_days = []
                rationale = "Foundational track recommended. Starting from Day 1 provides full step-by-step intuition across enterprise systems."

        else:
            # Fallback for legacy calls passing raw domain_scores
            overall_score = 0.0
            starting_day = 1
            resolved_persona = "fresher"
            waived_days = []
            rationale = "Starting from Day 1 to build complete enterprise computing foundations."

        # If legacy domain_scores was passed without answers, preserve backward compatibility
        if not answers and domain_scores:
            erp = float(domain_scores.get("erp_basics", domain_scores.get("fundamentals", 0.0)))
            proc = float(domain_scores.get("business_processes", erp))
            delta = float(domain_scores.get("s4hana_delta", domain_scores.get("ddic_and_sql", 0.0)))
            cds = float(domain_scores.get("modern_abap_cds", domain_scores.get("modern_s4hana_rap", 0.0)))
            rap = float(domain_scores.get("rap_foundations", domain_scores.get("modern_s4hana_rap", 0.0)))

            overall_score = round((erp * 0.2) + (proc * 0.2) + (delta * 0.2) + (cds * 0.2) + (rap * 0.2), 1)
            evaluated_domain_scores = domain_scores

            if rap >= 75.0 and cds >= 75.0:
                starting_day = 77
                resolved_persona = "experienced_s4hana"
                waived_days = list(range(1, 77))
                rationale = "Demonstrated mastery of S/4HANA CDS and RAP architecture. Accelerated to Day 77."
            elif cds >= 60.0 or delta >= 60.0:
                starting_day = 45
                resolved_persona = "ecc_developer"
                waived_days = list(range(1, 45))
                rationale = "Demonstrated core data models and business processes. Accelerated to Day 45."
            elif proc >= 50.0:
                starting_day = 23
                resolved_persona = "functional_user"
                waived_days = list(range(1, 23))
                rationale = "Demonstrated business processes. Accelerated to Day 23."
            elif erp >= 50.0:
                starting_day = 9
                resolved_persona = "beginner"
                waived_days = list(range(1, 9))
                rationale = "Fundamental ERP demonstrated. Accelerated to Day 9."

        now = datetime.now(timezone.utc)

        # Record concept evidence for demonstrated concepts into the DAG
        for c_slug in demonstrated_concepts:
            try:
                SAPMasteryService.record_concept_attempt(
                    db=db,
                    user_id=user_id,
                    concept_slug=c_slug,
                    score=100.0,
                )
            except Exception:
                pass

        # Build topic breakdown for client visualization
        for topic_key, score_val in evaluated_domain_scores.items():
            topic_breakdown.append({
                "topic": topic_key,
                "label": topic_key.replace("_", " ").title(),
                "score": score_val,
            })

        # Persist diagnostic placement profile
        profile = db.execute(
            select(SAPPlacementProfile).where(SAPPlacementProfile.user_id == user_id)
        ).scalar_one_or_none()

        diagnostic_results = {
            "overall_score": overall_score,
            "experience_level": level,
            "waived_days": waived_days,
            "unlocked_days": waived_days + [starting_day],
            "demonstrated_concepts": demonstrated_concepts,
            "gap_concepts": gap_concepts,
            "topic_breakdown": topic_breakdown,
            "evaluation_timestamp": now.isoformat(),
        }

        if profile is None:
            profile = SAPPlacementProfile(
                user_id=user_id,
                persona=resolved_persona,
                experience_years=experience_years,
                prior_sap_experience=experience_years > 0.5 or overall_score > 30.0 or level == "experienced",
                diagnostic_results=diagnostic_results,
                concept_benchmarks=evaluated_domain_scores,
                recommended_start_day=starting_day,
                rationale=rationale,
                completed_at=now,
            )
            db.add(profile)
        else:
            profile.persona = resolved_persona
            profile.experience_years = experience_years
            profile.prior_sap_experience = experience_years > 0.5 or overall_score > 30.0 or level == "experienced"
            profile.diagnostic_results = diagnostic_results
            profile.concept_benchmarks = evaluated_domain_scores
            profile.recommended_start_day = starting_day
            profile.rationale = rationale
            profile.completed_at = now

        # Update macro SAPUserState: completed_days_count strictly does NOT count waived days
        user_state = db.execute(
            select(SAPUserState).where(SAPUserState.user_id == user_id)
        ).scalar_one_or_none()

        if user_state is None:
            user_state = SAPUserState(
                user_id=user_id,
                current_recommended_day=starting_day,
                onboarding_persona=resolved_persona,
                placement_status=SAPPlacementStatus.COMPLETED.value,
                placement_score=overall_score,
                completed_days_count=0,  # Strict: waived days do NOT count as completed!
                last_active_at=now,
            )
            db.add(user_state)
        else:
            user_state.current_recommended_day = starting_day
            user_state.onboarding_persona = resolved_persona
            user_state.placement_status = SAPPlacementStatus.COMPLETED.value
            user_state.placement_score = overall_score
            user_state.last_active_at = now

        # Record waived days in sap_user_day_state with explicit status
        for day_num in waived_days:
            day_state = db.execute(
                select(SAPUserDayState).where(
                    SAPUserDayState.user_id == user_id,
                    SAPUserDayState.day_number == day_num,
                )
            ).scalar_one_or_none()

            if day_state is None:
                day_state = SAPUserDayState(
                    user_id=user_id,
                    day_number=day_num,
                    status=SAPDayStatus.WAIVED_BY_PLACEMENT.value,
                    waived=True,
                    lesson_started=False,
                    lesson_completed=False,
                    assessment_passed=False,
                    completed=False,
                )
                db.add(day_state)
            else:
                day_state.status = SAPDayStatus.WAIVED_BY_PLACEMENT.value
                day_state.waived = True
                if not day_state.completed:
                    day_state.lesson_completed = False
                    day_state.assessment_passed = False

        db.commit()
        db.refresh(profile)
        return profile

    @classmethod
    def choose_start_day(
        cls,
        db: Session,
        user_id: uuid.UUID,
        start_day: int,
    ) -> SAPPlacementProfile:
        """Allows learner to override starting point (e.g. choose Day 1 instead of recommended Day X)."""
        profile = db.execute(
            select(SAPPlacementProfile).where(SAPPlacementProfile.user_id == user_id)
        ).scalar_one_or_none()

        if not profile:
            raise ValueError("No diagnostic profile found for this user.")

        now = datetime.now(timezone.utc)
        user_state = db.execute(
            select(SAPUserState).where(SAPUserState.user_id == user_id)
        ).scalar_one_or_none()

        if user_state:
            user_state.current_recommended_day = start_day
            user_state.last_active_at = now

        # Update profile recommended start day
        profile.recommended_start_day = start_day
        db.commit()
        db.refresh(profile)
        return profile

