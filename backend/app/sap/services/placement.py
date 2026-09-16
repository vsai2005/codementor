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
            "default_start_day": 45,
            "max_waivable_days": list(range(1, 45)),
            "rationale": "Demonstrated core business processes (P2P/O2C/GL). Accelerated past standard workflows to S/4HANA CDS and Data Semantics (Day 45).",
        },
        "ecc_developer": {
            "title": "ECC Consultant / Classic ABAP Developer",
            "default_start_day": 45,
            "max_waivable_days": list(range(1, 45)),
            "rationale": "Classic ECC/ABAP verified. Fast-tracked to S/4HANA Core Data Services and Code Pushdown (Day 45) or ABAP Cloud (Day 77).",
        },
        "experienced_s4hana": {
            "title": "Experienced S/4HANA Developer / Solution Architect",
            "default_start_day": 84,
            "max_waivable_days": list(range(1, 90)),
            "rationale": "High proficiency in S/4HANA CDS and transactional RAP modeling. Routed to Advanced RAP (Day 84) or BTP Integration (Day 90).",
        },
    }

    # Core concept benchmarks mapping to diagnostic domains
    DOMAIN_TESTED_CONCEPTS = {
        "erp_basics": [
            "erp-evolution", "three-tier-architecture", "master-data-concept",
            "org-structure-company-code", "sap-gui-navigation",
        ],
        "business_processes": [
            "p2p-pr-creation", "p2p-po-processing", "p2p-goods-receipt-migo",
            "o2c-sales-order-creation", "o2c-billing-creation", "gl-journal-entry",
        ],
        "s4hana_delta": [
            "s4hana-value-drivers", "universal-journal-concept", "acdoca-table-architecture",
            "matdoc-table-architecture", "business-partner-cvi",
        ],
        "classic_abap_ddic": [
            "relational-modeling", "sql-joins-foundations", "cardinality-rules",
            "oop-fundamentals", "pfcg-authorizations",
        ],
        "modern_abap_cds": [
            "cds-fundamentals", "cds-syntax-expressions", "cds-associations-concept",
            "vdm-architecture-tiers", "modern-abap-syntax",
        ],
        "rap_foundations": [
            "abap-cloud-paradigm", "rap-architecture-overview", "bdef-syntax",
            "managed-vs-unmanaged-rap", "rap-save-sequence",
        ],
        "btp_integration": [
            "sync-vs-async-integration", "api-oauth2-fundamentals",
            "cloud-integration-cpi", "sap-event-mesh",
        ],
    }

    @classmethod
    def evaluate_diagnostic(
        cls,
        db: Session,
        user_id: uuid.UUID,
        domain_scores: dict[str, float],
        experience_years: float = 0.0,
        persona_self_select: str | None = None,
        concept_responses: dict[str, float] | None = None,
    ) -> SAPPlacementProfile:
        """Evaluates concept evidence and prerequisite mastery to compute starting day and waived days."""
        erp = float(domain_scores.get("erp_basics", domain_scores.get("fundamentals", 0.0)))
        proc = float(domain_scores.get("business_processes", erp))
        delta = float(domain_scores.get("s4hana_delta", domain_scores.get("ddic_and_sql", 0.0)))
        abap = float(domain_scores.get("classic_abap", domain_scores.get("classic_abap_ddic", 0.0)))
        cds = float(domain_scores.get("modern_abap_cds", domain_scores.get("modern_s4hana_rap", 0.0)))
        rap = float(domain_scores.get("rap_foundations", domain_scores.get("modern_s4hana_rap", 0.0)))
        btp = float(domain_scores.get("btp_integration", 0.0))

        overall_score = round(
            (erp * 0.15) + (proc * 0.15) + (delta * 0.15) + (abap * 0.20) + (rap * 0.20) + (btp * 0.15), 1
        )

        resolved_persona = "fresher"
        starting_day = 1
        waived_days: list[int] = []
        rationale: str = ""

        # Evidence-based decision routing
        if persona_self_select == "fresher":
            resolved_persona = "fresher"
            starting_day = 1
            waived_days = []
            rationale = "Fresher track selected. Full 100-day guided roadmap starting at Day 1."

        elif persona_self_select == "experienced_s4hana" or (rap >= 75.0 and cds >= 75.0):
            resolved_persona = "experienced_s4hana"
            if rap >= 85.0 and btp >= 75.0:
                starting_day = 90  # Route to BTP & Enterprise Integration
                waived_days = list(range(1, 90))
                rationale = "Demonstrated mastery of S/4HANA CDS, VDM, and Full-Stack RAP. Accelerated to SAP BTP Integration Suite (Day 90)."
            else:
                starting_day = 84  # Route to Advanced RAP (Draft, Numbering, Concurrency)
                waived_days = list(range(1, 84))
                rationale = "Demonstrated core RAP transactional architecture. Fast-tracked to Advanced RAP Draft & Concurrency patterns (Day 84)."

        elif persona_self_select == "ecc_developer" or (abap >= 70.0 and (delta >= 60.0 or erp >= 70.0)):
            resolved_persona = "ecc_developer"
            if cds >= 75.0 and rap >= 65.0:
                starting_day = 77  # Accelerated directly to ABAP Cloud & RAP
                waived_days = list(range(1, 77))
                rationale = "Demonstrated classic ABAP mastery and S/4HANA CDS VDM concepts. Fast-tracked to ABAP Cloud & RAP (Day 77)."
            else:
                starting_day = 45  # Routed to Phase 4: CDS & Code Pushdown
                waived_days = list(range(1, 45))
                rationale = "Strong classic ABAP/DDIC foundations verified. Fast-tracked to S/4HANA In-Memory CDS, VDM, and Code Pushdown (Day 45)."

        elif persona_self_select == "functional_user" or (proc >= 70.0 and erp >= 65.0):
            resolved_persona = "functional_user"
            if delta >= 65.0:
                starting_day = 45  # Business processes + Universal Journal delta verified
                waived_days = list(range(1, 45))
                rationale = "Strong mastery of E2E business processes (P2P/O2C/GL) and Universal Journal. Routed to CDS Data Semantics (Day 45)."
            else:
                starting_day = 23  # Focus on S/4HANA specific process execution
                waived_days = list(range(1, 23))
                rationale = "Foundational ERP knowledge demonstrated. Fast-tracked to S/4HANA End-to-End P2P, O2C, and Financial workflows (Day 23)."

        elif erp >= 60.0:
            resolved_persona = "beginner"
            starting_day = 9
            waived_days = list(range(1, 9))
            rationale = "Fundamental ERP and computing concepts demonstrated. Days 1–8 waived; starting at S/4HANA Architecture (Day 9)."

        else:
            resolved_persona = "fresher"
            starting_day = 1
            waived_days = []
            rationale = "Starting from Day 1 to build complete enterprise computing foundations."

        now = datetime.now(timezone.utc)

        # Record concept evidence ONLY for tested concepts with passing scores
        tested_concepts_passed: list[str] = []
        scores_by_domain = {
            "erp_basics": erp,
            "business_processes": proc,
            "s4hana_delta": delta,
            "classic_abap_ddic": abap,
            "modern_abap_cds": cds,
            "rap_foundations": rap,
            "btp_integration": btp,
        }

        # Apply specific concept responses if submitted, otherwise apply domain benchmark
        for domain, d_score in scores_by_domain.items():
            if d_score >= 80.0:
                for c_slug in cls.DOMAIN_TESTED_CONCEPTS.get(domain, []):
                    score_to_record = concept_responses.get(c_slug, d_score) if concept_responses else d_score
                    if score_to_record >= 80.0:
                        try:
                            SAPMasteryService.record_concept_attempt(
                                db=db,
                                user_id=user_id,
                                concept_slug=c_slug,
                                score=score_to_record,
                            )
                            tested_concepts_passed.append(c_slug)
                        except Exception:
                            pass

        # Persist diagnostic placement profile
        profile = db.execute(
            select(SAPPlacementProfile).where(SAPPlacementProfile.user_id == user_id)
        ).scalar_one_or_none()

        diagnostic_results = {
            "overall_score": overall_score,
            "waived_days": waived_days,
            "unlocked_days": waived_days + [starting_day],
            "tested_concepts_passed": tested_concepts_passed,
            "evaluation_timestamp": now.isoformat(),
        }

        if profile is None:
            profile = SAPPlacementProfile(
                user_id=user_id,
                persona=resolved_persona,
                experience_years=experience_years,
                prior_sap_experience=experience_years > 0.5 or overall_score > 30.0,
                diagnostic_results=diagnostic_results,
                concept_benchmarks=domain_scores,
                recommended_start_day=starting_day,
                rationale=rationale,
                completed_at=now,
            )
            db.add(profile)
        else:
            profile.persona = resolved_persona
            profile.experience_years = experience_years
            profile.diagnostic_results = diagnostic_results
            profile.concept_benchmarks = domain_scores
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
                completed_days_count=0,  # Strict: waived days do not count as completed!
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
