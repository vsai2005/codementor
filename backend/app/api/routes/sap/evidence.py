"""SAP Skill Evidence Endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import User
from app.sap.schemas.api import (
    SAPSkillEvidenceItem,
    SAPSkillEvidenceSummaryResponse,
)
from app.sap.services.mastery import SAPMasteryService

router = APIRouter()


@router.get("", response_model=SAPSkillEvidenceSummaryResponse)
def list_learner_evidence(
    limit: int = Query(50, ge=1, le=200),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPSkillEvidenceSummaryResponse:
    """Lists recent skill evidence records across both Guided Learning and Enterprise Missions."""
    evidences = SAPMasteryService.list_learner_evidence(db, user_id=user.id, limit=limit)
    return SAPSkillEvidenceSummaryResponse(
        user_id=str(user.id),
        total_evidence_count=len(evidences),
        evidences=[SAPSkillEvidenceItem(**e) for e in evidences],
    )


@router.get("/concepts/{slug}", response_model=list[SAPSkillEvidenceItem])
def get_concept_evidence_trail(
    slug: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[SAPSkillEvidenceItem]:
    """Retrieves the evidence audit trail demonstrating WHY a concept is mastered."""
    evidences = SAPMasteryService.get_concept_evidence(db, user_id=user.id, concept_slug=slug)
    return [SAPSkillEvidenceItem(**e) for e in evidences]
