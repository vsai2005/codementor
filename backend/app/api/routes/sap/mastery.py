"""SAP Concept Mastery Endpoints.

Read-only by design. Mastery is written exclusively by server-side services that have
graded trusted evidence (guided assessments, enterprise missions, diagnostic placement).
There is intentionally no endpoint that accepts a client-supplied concept score.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import User
from app.sap.schemas.api import SAPMasterySummaryResponse
from app.sap.services.mastery import SAPMasteryService

router = APIRouter()


@router.get("", response_model=SAPMasterySummaryResponse)
def get_user_mastery(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPMasterySummaryResponse:
    data = SAPMasteryService.get_user_mastery_summary(db, user.id)
    return SAPMasterySummaryResponse(**data)
