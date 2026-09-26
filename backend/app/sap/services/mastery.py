"""SAP Concept Mastery Service.

Continuous knowledge tracing across atomic concepts in the SAP DAG.
Strictly decoupled from Python's UserTopicState and tier-based difficulty.
"""

from __future__ import annotations

import math
import uuid
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.sap_curriculum_retrieval import SAPCurriculumKnowledgeEngine
from app.models.sap_models import (
    SAPConcept,
    SAPMasteryState,
    SAPSkillEvidence,
    SAPUserConceptMastery,
)


class SAPMasteryService:
    PASSING_THRESHOLD = 80.0
    REMEDIATION_THRESHOLD = 60.0

    @classmethod
    def record_concept_attempt(
        cls,
        db: Session,
        user_id: uuid.UUID,
        concept_slug: str,
        score: float,
    ) -> SAPUserConceptMastery:
        """Records an assessment attempt against a concept and transitions mastery state.

        Internal only: callers must pass a score the server computed from graded evidence.
        No API route forwards a client-supplied score here.
        """
        if isinstance(score, bool) or not isinstance(score, (int, float)) or not math.isfinite(score):
            raise ValueError("Concept mastery score must be a finite number.")
        if score < 0.0 or score > 100.0:
            raise ValueError("Concept mastery score must be between 0 and 100.")
        score = float(score)
        # Ensure concept exists in DB or create it from knowledge engine
        concept = db.execute(
            select(SAPConcept).where(SAPConcept.slug == concept_slug)
        ).scalar_one_or_none()

        if concept is None:
            engine = SAPCurriculumKnowledgeEngine.get_instance()
            c_meta = engine.get_concept(concept_slug)
            if c_meta is None:
                raise ValueError(f"Concept '{concept_slug}' is not registered in the SAP knowledge engine.")
            concept = SAPConcept(
                slug=c_meta.slug,
                name=c_meta.name,
                category=c_meta.category,
                difficulty=c_meta.difficulty,
            )
            db.add(concept)
            db.flush()

        # Find or create user mastery record
        record = db.execute(
            select(SAPUserConceptMastery).where(
                SAPUserConceptMastery.user_id == user_id,
                SAPUserConceptMastery.concept_id == concept.id,
            )
        ).scalar_one_or_none()

        now = datetime.now(timezone.utc)

        if record is None:
            record = SAPUserConceptMastery(
                user_id=user_id,
                concept_id=concept.id,
                mastery_score=score,
                confidence=0.5,
                attempts=1,
                successful_attempts=1 if score >= cls.PASSING_THRESHOLD else 0,
                mastery_state=SAPMasteryState.LEARNING.value,
                last_assessed_at=now,
                history=[{"score": score, "timestamp": now.isoformat()}],
            )
            db.add(record)
        else:
            record.attempts += 1
            if score >= cls.PASSING_THRESHOLD:
                record.successful_attempts += 1

            # Exponential moving average: 70% current attempt + 30% historical
            record.mastery_score = round((0.7 * score) + (0.3 * record.mastery_score), 1)
            record.confidence = round(min(1.0, 0.4 + (0.1 * min(record.attempts, 6))), 2)
            record.last_assessed_at = now
            hist = list(record.history or [])
            hist.append({"score": score, "timestamp": now.isoformat()})
            record.history = hist[-20:]  # keep last 20

        # State transition rules
        if score >= cls.PASSING_THRESHOLD:
            if record.successful_attempts >= 2 or record.mastery_score >= 85.0:
                record.mastery_state = SAPMasteryState.MASTERED.value
                record.last_mastered_at = now
            else:
                record.mastery_state = SAPMasteryState.PRACTICING.value
        elif score < cls.REMEDIATION_THRESHOLD:
            record.mastery_state = SAPMasteryState.NEEDS_REMEDIATION.value
        else:
            if record.mastery_state != SAPMasteryState.MASTERED.value:
                record.mastery_state = SAPMasteryState.LEARNING.value

        db.commit()
        db.refresh(record)
        return record

    @classmethod
    def get_user_mastery_summary(cls, db: Session, user_id: uuid.UUID) -> dict:
        records = db.execute(
            select(SAPUserConceptMastery, SAPConcept.slug)
            .join(SAPConcept, SAPUserConceptMastery.concept_id == SAPConcept.id)
            .where(SAPUserConceptMastery.user_id == user_id)
        ).all()

        breakdown = {state.value: 0 for state in SAPMasteryState}
        items = []

        for r, slug in records:
            breakdown[r.mastery_state] = breakdown.get(r.mastery_state, 0) + 1
            items.append({
                "concept_slug": slug,
                "mastery_state": SAPMasteryState(r.mastery_state),
                "mastery_score": r.mastery_score,
                "confidence": r.confidence,
                "attempts": r.attempts,
                "successful_attempts": r.successful_attempts,
                "last_assessed_at": r.last_assessed_at,
                "last_mastered_at": r.last_mastered_at,
            })

        return {
            "total_tracked": len(items),
            "breakdown": breakdown,
            "concepts": items,
        }

    @classmethod
    def record_skill_evidence(
        cls,
        db: Session,
        user_id: uuid.UUID,
        concept_slug: str,
        evidence: dict[str, Any],
    ) -> SAPSkillEvidence:
        """Records explicit skill evidence for a concept and updates concept mastery dynamically."""
        concept = db.execute(
            select(SAPConcept).where(SAPConcept.slug == concept_slug)
        ).scalar_one_or_none()

        if concept is None:
            engine = SAPCurriculumKnowledgeEngine.get_instance()
            c_meta = engine.get_concept(concept_slug)
            if c_meta is None:
                raise ValueError(f"Concept '{concept_slug}' is not registered in the SAP knowledge engine.")
            concept = SAPConcept(
                slug=c_meta.slug,
                name=c_meta.name,
                category=c_meta.category,
                difficulty=c_meta.difficulty,
            )
            db.add(concept)
            db.flush()

        if "score" not in evidence:
            raise ValueError("Skill evidence requires a server-computed score.")
        score = evidence["score"]
        if isinstance(score, bool) or not isinstance(score, (int, float)) or not math.isfinite(score):
            raise ValueError("Skill evidence score must be a finite number.")
        score = float(score)
        record_evidence = SAPSkillEvidence(
            user_id=user_id,
            concept_id=concept.id,
            source_type=evidence.get("source_type", "mission"),
            source_id=str(evidence.get("source_id", "manual")),
            mode=evidence.get("mode", "MISSION"),
            assistance_level=evidence.get("assistance_level", "TRAINING"),
            difficulty=int(evidence.get("difficulty", 1)),
            score=score,
            result=evidence.get("result", "passed" if score >= cls.PASSING_THRESHOLD else "failed"),
            evidence_summary=evidence.get("evidence_summary", f"Demonstrated skill in {concept.name}"),
            details=evidence.get("details", {}),
            recorded_at=datetime.now(timezone.utc),
        )
        db.add(record_evidence)
        db.flush()

        # Update concept mastery via moving average
        cls.record_concept_attempt(db, user_id=user_id, concept_slug=concept_slug, score=score)

        return record_evidence

    @classmethod
    def get_concept_evidence(
        cls, db: Session, user_id: uuid.UUID, concept_slug: str
    ) -> list[dict[str, Any]]:
        """Retrieves complete evidence audit trail showing WHY a concept is mastered."""
        concept = db.execute(
            select(SAPConcept).where(SAPConcept.slug == concept_slug)
        ).scalar_one_or_none()
        if not concept:
            return []

        evidences = db.execute(
            select(SAPSkillEvidence)
            .where(
                SAPSkillEvidence.user_id == user_id,
                SAPSkillEvidence.concept_id == concept.id,
            )
            .order_by(SAPSkillEvidence.recorded_at.desc())
        ).scalars().all()

        return [
            {
                "id": str(e.id),
                "concept_slug": concept_slug,
                "source_type": e.source_type,
                "source_id": e.source_id,
                "mode": e.mode,
                "assistance_level": e.assistance_level,
                "difficulty": e.difficulty,
                "score": e.score,
                "result": e.result,
                "evidence_summary": e.evidence_summary,
                "details": e.details,
                "recorded_at": e.recorded_at.isoformat() if e.recorded_at else None,
            }
            for e in evidences
        ]

    @classmethod
    def list_learner_evidence(
        cls, db: Session, user_id: uuid.UUID, limit: int = 50
    ) -> list[dict[str, Any]]:
        """Lists recent skill evidence records across all concepts and learning modes."""
        rows = db.execute(
            select(SAPSkillEvidence, SAPConcept.slug, SAPConcept.name)
            .join(SAPConcept, SAPSkillEvidence.concept_id == SAPConcept.id)
            .where(SAPSkillEvidence.user_id == user_id)
            .order_by(SAPSkillEvidence.recorded_at.desc())
            .limit(limit)
        ).all()

        return [
            {
                "id": str(e.id),
                "concept_slug": c_slug,
                "concept_name": c_name,
                "source_type": e.source_type,
                "source_id": e.source_id,
                "mode": e.mode,
                "assistance_level": e.assistance_level,
                "difficulty": e.difficulty,
                "score": e.score,
                "result": e.result,
                "evidence_summary": e.evidence_summary,
                "details": e.details,
                "recorded_at": e.recorded_at.isoformat() if e.recorded_at else None,
            }
            for e, c_slug, c_name in rows
        ]
