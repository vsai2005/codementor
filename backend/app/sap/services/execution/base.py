"""Pluggable Local Validation and Simulation Provider Interface for SAP Learning Engine.

TRUTHFULNESS NOTICE:
Providers in this package perform LOCAL STATIC VALIDATION and IN-MEMORY MOCK SIMULATION only.
They do NOT compile or execute code on a real ABAP kernel, do NOT activate CDS views
in an SAP HANA / ABAP Dictionary catalog, do NOT deploy RAP business objects, and do NOT
connect to any live SAP tenant, NetWeaver, S/4HANA, or SAP BTP system.
"""

from __future__ import annotations

import enum
from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel, Field


class ExecutionCategory(str, enum.Enum):
    """Categorizes the nature of execution for system truthfulness."""
    STATIC_VALIDATION = "STATIC_VALIDATION"
    LOCAL_SIMULATION = "LOCAL_SIMULATION"
    REAL_SAP_EXECUTION = "REAL_SAP_EXECUTION"


class SAPExecutionRequest(BaseModel):
    provider_type: str = Field(..., description="simulation | cds_validation | abap_cloud")
    code_or_payload: str = Field(..., description="Code content or transaction event sequence JSON")
    context_parameters: dict[str, Any] = Field(default_factory=dict)
    timeout_seconds: int = Field(default=15, ge=1, le=60)


class DiagnosticFinding(BaseModel):
    severity: str = Field(..., description="error | warning | info")
    line: int | None = None
    column: int | None = None
    rule_code: str
    message: str


class SAPExecutionResult(BaseModel):
    success: bool
    status: str = Field(..., description="ok | syntax_error | runtime_error | policy_violation | sequence_error")
    output: str = ""
    findings: list[DiagnosticFinding] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    runtime_ms: int = 0
    # Truthfulness metadata
    provider_category: ExecutionCategory = Field(
        default=ExecutionCategory.STATIC_VALIDATION,
        description="STATIC_VALIDATION | LOCAL_SIMULATION | REAL_SAP_EXECUTION",
    )
    is_sandboxed_simulation: bool = Field(
        default=False,
        description="True if run within a local mock/sandboxed simulation engine",
    )
    is_live_sap_system: bool = Field(
        default=False,
        description="Truthfulness indicator: False indicates no real SAP tenant or kernel connection",
    )


class SAPExecutionProvider(ABC):
    """Abstract Base Class for local SAP validation and mock simulation backends.

    Subclasses MUST explicitly specify their ExecutionCategory and ensure
    truthfulness metadata is returned without claiming live SAP tenant execution.
    """

    category: ExecutionCategory = ExecutionCategory.STATIC_VALIDATION

    @abstractmethod
    async def execute(self, request: SAPExecutionRequest) -> SAPExecutionResult:
        """Runs local static validation or mock simulation for the requested artifact."""
        pass

    @abstractmethod
    async def validate_syntax(self, code_or_payload: str, context: dict[str, Any]) -> list[DiagnosticFinding]:
        """Performs static syntax and compliance validation without simulation."""
        pass
