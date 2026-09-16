"""Export SAP Execution Providers and Factory."""

from __future__ import annotations

from app.sap.services.execution.abap_cloud import ABAPCloudProvider
from app.sap.services.execution.base import (
    DiagnosticFinding,
    ExecutionCategory,
    SAPExecutionProvider,
    SAPExecutionRequest,
    SAPExecutionResult,
)
from app.sap.services.execution.cds_validator import CDSValidationProvider
from app.sap.services.execution.simulation import SimulationProvider


def get_execution_provider(provider_type: str) -> SAPExecutionProvider:
    if provider_type == "simulation":
        return SimulationProvider()
    elif provider_type == "cds_validation":
        return CDSValidationProvider()
    elif provider_type == "abap_cloud":
        return ABAPCloudProvider()
    else:
        raise ValueError(f"Unknown SAP execution provider type: {provider_type}")


__all__ = [
    "ExecutionCategory",
    "SAPExecutionProvider",
    "SAPExecutionRequest",
    "SAPExecutionResult",
    "DiagnosticFinding",
    "SimulationProvider",
    "CDSValidationProvider",
    "ABAPCloudProvider",
    "get_execution_provider",
]
