"""Local Mock Simulation Provider for Fiori / SAP GUI process steps and events.

TRUTHFULNESS NOTICE:
This provider performs local, in-memory sequence comparison against expected mock
workflow steps. It does NOT connect to a live SAP system, execute transactions
on SAP GUI, or dispatch OData actions to live SAP Fiori / S/4HANA backends.
"""

from __future__ import annotations

import json
import time
from typing import Any

from app.sap.services.execution.base import (
    DiagnosticFinding,
    ExecutionCategory,
    SAPExecutionProvider,
    SAPExecutionRequest,
    SAPExecutionResult,
)


class SimulationProvider(SAPExecutionProvider):
    """Validates SAP GUI / Fiori transaction flows against expected mock sequences locally."""

    category: ExecutionCategory = ExecutionCategory.LOCAL_SIMULATION

    async def execute(self, request: SAPExecutionRequest) -> SAPExecutionResult:
        start = time.perf_counter()
        try:
            steps = json.loads(request.code_or_payload) if isinstance(request.code_or_payload, str) else request.code_or_payload
            expected_sequence = request.context_parameters.get("expected_sequence", [])

            findings: list[DiagnosticFinding] = []
            if isinstance(steps, list) and isinstance(expected_sequence, list):
                for idx, (actual, expected) in enumerate(zip(steps, expected_sequence)):
                    act_action = actual.get("action") if isinstance(actual, dict) else actual
                    exp_action = expected.get("action") if isinstance(expected, dict) else expected
                    if act_action != exp_action:
                        findings.append(
                            DiagnosticFinding(
                                severity="error",
                                rule_code="STEP_SEQUENCE_MISMATCH",
                                message=f"Step {idx + 1}: expected action '{exp_action}', got '{act_action}'",
                            )
                        )
                if len(steps) < len(expected_sequence):
                    findings.append(
                        DiagnosticFinding(
                            severity="error",
                            rule_code="INCOMPLETE_SEQUENCE",
                            message=f"Simulation sequence incomplete: {len(steps)} steps submitted, {len(expected_sequence)} required.",
                        )
                    )

            success = len(findings) == 0
            return SAPExecutionResult(
                success=success,
                status="ok" if success else "sequence_error",
                output="Local mock simulation sequence verified successfully." if success else "Local mock simulation steps diverged from target business process.",
                findings=findings,
                metadata={
                    "provider_category": ExecutionCategory.LOCAL_SIMULATION.value,
                    "is_sandboxed_simulation": True,
                    "is_live_sap_system": False,
                },
                runtime_ms=int((time.perf_counter() - start) * 1000),
                provider_category=ExecutionCategory.LOCAL_SIMULATION,
                is_sandboxed_simulation=True,
                is_live_sap_system=False,
            )
        except Exception as exc:
            return SAPExecutionResult(
                success=False,
                status="runtime_error",
                output=f"Failed to parse simulation payload: {exc}",
                metadata={
                    "provider_category": ExecutionCategory.LOCAL_SIMULATION.value,
                    "is_sandboxed_simulation": True,
                    "is_live_sap_system": False,
                },
                runtime_ms=int((time.perf_counter() - start) * 1000),
                provider_category=ExecutionCategory.LOCAL_SIMULATION,
                is_sandboxed_simulation=True,
                is_live_sap_system=False,
            )

    async def validate_syntax(self, code_or_payload: str, context: dict[str, Any]) -> list[DiagnosticFinding]:
        try:
            if isinstance(code_or_payload, str):
                json.loads(code_or_payload)
            return []
        except Exception as exc:
            return [
                DiagnosticFinding(
                    severity="error",
                    rule_code="INVALID_SIMULATION_JSON",
                    message=f"Malformed simulation JSON: {exc}",
                )
            ]
