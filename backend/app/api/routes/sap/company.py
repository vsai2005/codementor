"""SAP Enterprise Digital Twin Endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import User
from app.sap.schemas.api import (
    SAPEnterpriseResetResponse,
    SAPEnterpriseViewResponse,
)
from app.sap.services.enterprise import SAPEnterpriseService

router = APIRouter()


@router.get("", response_model=SAPEnterpriseViewResponse)
def get_company_digital_twin(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPEnterpriseViewResponse:
    """Retrieves the learner's persistent fictional enterprise digital twin state."""
    instance = SAPEnterpriseService.get_or_create_instance(db, user_id=user.id)
    enterprise = instance.enterprise

    return SAPEnterpriseViewResponse(
        slug=enterprise.slug,
        name=enterprise.name,
        code=enterprise.code,
        industry=enterprise.industry,
        description_md=enterprise.description_md,
        company_state=instance.company_state,
        landscape_metadata=enterprise.landscape_metadata,
        state_version=instance.state_version,
        status=instance.status,
    )


@router.post("/reset", response_model=SAPEnterpriseResetResponse)
def reset_company_digital_twin(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SAPEnterpriseResetResponse:
    """Resets the learner's digital twin company state back to the original clean template."""
    instance = SAPEnterpriseService.reset_instance(db, user_id=user.id)
    return SAPEnterpriseResetResponse(
        status="reset",
        state_version=instance.state_version,
        message="Enterprise digital twin reset to original baseline state successfully.",
    )
