"""SAP Route Bundle combining all SAP endpoints."""

from fastapi import APIRouter

from app.api.routes.sap import (
    assessments,
    company,
    curriculum,
    evidence,
    execution,
    learning,
    mastery,
    missions,
    modes,
    placement,
)

sap_router = APIRouter(prefix="/api/sap")

sap_router.include_router(curriculum.router, prefix="/curriculum", tags=["sap-curriculum"])
sap_router.include_router(learning.router, prefix="/learning", tags=["sap-learning"])
sap_router.include_router(mastery.router, prefix="/mastery", tags=["sap-mastery"])
sap_router.include_router(placement.router, prefix="/placement", tags=["sap-placement"])
sap_router.include_router(assessments.router, prefix="/assessments", tags=["sap-assessments"])
sap_router.include_router(execution.router, prefix="/execution", tags=["sap-execution"])
sap_router.include_router(modes.router, prefix="/modes", tags=["sap-modes"])
sap_router.include_router(company.router, prefix="/company", tags=["sap-company"])
sap_router.include_router(missions.router, prefix="/missions", tags=["sap-missions"])
sap_router.include_router(evidence.router, prefix="/evidence", tags=["sap-evidence"])

__all__ = ["sap_router"]
