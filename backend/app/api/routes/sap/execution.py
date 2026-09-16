"""SAP Local Static Validation and Mock Simulation Endpoints.

TRUTHFULNESS NOTICE:
Endpoints in this router dispatch strictly to local static validators and
mock step sequence simulators. They do NOT connect to a live SAP system, execute
ABAP code against a real kernel, activate CDS views on HANA, or deploy RAP models.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.sap.schemas.api import (
    DiagnosticFindingOut,
    SAPExecutionValidateRequest,
    SAPExecutionValidateResponse,
)
from app.sap.services.execution import SAPExecutionRequest, get_execution_provider

router = APIRouter()


@router.post(
    "/validate",
    response_model=SAPExecutionValidateResponse,
    summary="Validate artifact using local static analysis or mock simulation",
    description=(
        "Executes local static syntax/scope checks or in-memory process mock simulation. "
        "Returns explicit truthfulness metadata (provider_category, is_sandboxed_simulation, "
        "and is_live_sap_system=False) to ensure no false claims of live SAP execution."
    ),
)
async def validate_sap_artifact(payload: SAPExecutionValidateRequest) -> SAPExecutionValidateResponse:
    try:
        provider = get_execution_provider(payload.provider_type)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

    req = SAPExecutionRequest(
        provider_type=payload.provider_type,
        code_or_payload=payload.code_or_payload,
        context_parameters=payload.context_parameters,
    )
    res = await provider.execute(req)

    category_str = (
        res.provider_category.value
        if hasattr(res.provider_category, "value")
        else str(res.provider_category)
    )

    return SAPExecutionValidateResponse(
        success=res.success,
        status=res.status,
        output=res.output,
        findings=[
            DiagnosticFindingOut(
                severity=f.severity,
                line=f.line,
                column=f.column,
                rule_code=f.rule_code,
                message=f.message,
            )
            for f in res.findings
        ],
        runtime_ms=res.runtime_ms,
        provider_category=category_str,
        is_sandboxed_simulation=res.is_sandboxed_simulation,
        is_live_sap_system=res.is_live_sap_system,
    )
