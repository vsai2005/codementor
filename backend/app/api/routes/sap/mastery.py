"""SAP Concept Mastery Endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import User
from app.sap.schemas.api import (
    SAPConceptMasteryItem,
    SAPMasterySummaryResponse,
    SAPRecordConceptMasteryRequest,
)
from app.sap.services.mastery import SAPMasteryService

router = APIRouter()


@router.get("", response_model=SAPMasterySummaryResponse)
def get_user_mastery(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPMasterySummaryResponse:
    data = SAPMasteryService.get_user_mastery_summary(db, user.id)
    return SAPMasterySummaryResponse(**data)


@router.post("/record", response_model=SAPConceptMasteryItem)
def record_concept_mastery(
    payload: SAPRecordConceptMasteryRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPConceptMasteryItem:
    try:
        record = SAPMasteryService.record_concept_attempt(
            db=db,
            user_id=user.id,
            concept_slug=payload.concept_slug,
            score=payload.score,
        )
        return SAPConceptMasteryItem(
            concept_slug=payload.concept_slug,
            mastery_state=record.mastery_state,
            mastery_score=record.mastery_score,
            confidence=record.confidence,
            attempts=record.attempts,
            successful_attempts=record.successful_attempts,
            last_assessed_at=record.last_assessed_at,
            last_mastered_at=record.last_mastered_at,
        )
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
