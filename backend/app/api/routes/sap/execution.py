"""SAP Local Static Validation and Mock Simulation Endpoints.

TRUTHFULNESS NOTICE:
Endpoints in this router dispatch strictly to local static validators and
mock step sequence simulators. They do NOT connect to a live SAP system, execute
ABAP code against a real kernel, activate CDS views on HANA, or deploy RAP models.
"""

from __future__ import annotations

import json
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.models.models import User
from app.sap.schemas.api import (
    DiagnosticFindingOut,
    SAPExecutionValidateRequest,
    SAPExecutionValidateResponse,
)
from app.sap.services.execution import SAPExecutionRequest, get_execution_provider
from app.services.ratelimit import get_sap_execution_rate_limiter

router = APIRouter()

MAX_EXECUTION_CODE_BYTES = 64 * 1024  # 64 KB
MAX_CONTEXT_PARAMS_BYTES = 16 * 1024  # 16 KB


@router.post(
    "/validate",
    response_model=SAPExecutionValidateResponse,
    summary="Validate artifact using local static analysis or mock simulation",
    description=(
        "Executes local static syntax/scope checks or in-memory process mock simulation. "
        "Returns explicit truthfulness metadata (provider_category, is_sandboxed_simulation, "
        "and is_live_sap_system=False) to ensure no false claims of live SAP execution. "
        "Requires authentication, enforced per-user rate limits, and payload size bounds."
    ),
)
async def validate_sap_artifact(
    payload: SAPExecutionValidateRequest,
    user: User = Depends(get_current_user),
) -> SAPExecutionValidateResponse:
    # 1. Payload size protection (reject before expensive processing)
    code_bytes = len(payload.code_or_payload.encode("utf-8")) if payload.code_or_payload else 0
    if code_bytes > MAX_EXECUTION_CODE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"Execution payload exceeds maximum permitted code size of 64 KB (received {code_bytes} bytes).",
        )

    if payload.context_parameters:
        try:
            params_str = json.dumps(payload.context_parameters)
            params_bytes = len(params_str.encode("utf-8"))
            if params_bytes > MAX_CONTEXT_PARAMS_BYTES:
                raise HTTPException(
                    status_code=413,
                    detail=f"Execution context_parameters exceed maximum permitted size of 16 KB (received {params_bytes} bytes).",
                )
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=400,
                detail="Invalid context_parameters: must be JSON-serializable.",
            )

    # 2. User-aware Redis rate limiting
    verdict = get_sap_execution_rate_limiter().check(f"sap_exec:{user.id}")
    if not verdict.allowed:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please wait before executing again.",
            headers={"Retry-After": str(verdict.retry_after_s)},
        )

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
