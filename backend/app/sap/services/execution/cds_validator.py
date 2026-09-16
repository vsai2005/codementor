"""Local Static Core Data Services (CDS) DDL and Annotation Verification Provider.

TRUTHFULNESS NOTICE:
This provider performs local static regex and pattern validation on CDS view syntax
and enterprise annotations. It does NOT compile or activate CDS views in the ABAP
Dictionary / SAP HANA database, nor does it deploy RAP data models to a live SAP system.
"""

from __future__ import annotations

import re
import time
from typing import Any

from app.sap.services.execution.base import (
    DiagnosticFinding,
    ExecutionCategory,
    SAPExecutionProvider,
    SAPExecutionRequest,
    SAPExecutionResult,
)


class CDSValidationProvider(SAPExecutionProvider):
    """Performs static syntax and annotation compliance checks on Core Data Services (CDS) DDL."""

    category: ExecutionCategory = ExecutionCategory.STATIC_VALIDATION

    REQUIRED_ANNOTATIONS = [
        (r"@EndUserText\.label\s*:\s*'.*'", "MISSING_LABEL_ANNOTATION", "Missing @EndUserText.label annotation."),
        (r"@AccessControl\.authorizationCheck\s*:\s*#(CHECK|NOT_REQUIRED)", "MISSING_AUTH_ANNOTATION", "Missing @AccessControl.authorizationCheck annotation."),
    ]

    async def execute(self, request: SAPExecutionRequest) -> SAPExecutionResult:
        start = time.perf_counter()
        findings = await self.validate_syntax(request.code_or_payload, request.context_parameters)
        errors = [f for f in findings if f.severity == "error"]
        success = len(errors) == 0

        return SAPExecutionResult(
            success=success,
            status="ok" if success else "syntax_error",
            output="Local static CDS View entity definition and annotations valid." if success else f"Local static CDS verification failed with {len(errors)} error(s).",
            findings=findings,
            metadata={
                "provider_category": ExecutionCategory.STATIC_VALIDATION.value,
                "is_sandboxed_simulation": False,
                "is_live_sap_system": False,
            },
            runtime_ms=int((time.perf_counter() - start) * 1000),
            provider_category=ExecutionCategory.STATIC_VALIDATION,
            is_sandboxed_simulation=False,
            is_live_sap_system=False,
        )

    async def validate_syntax(self, code_or_payload: str, context: dict[str, Any]) -> list[DiagnosticFinding]:
        findings: list[DiagnosticFinding] = []
        code = code_or_payload

        # Check for modern view entity syntax
        code_lower = code.lower()
        if "define view entity" not in code_lower and "define root view entity" not in code_lower:
            findings.append(
                DiagnosticFinding(
                    severity="error",
                    rule_code="DEPRECATED_CDS_SYNTAX",
                    message="Use modern 'define [root] view entity' syntax instead of legacy 'define view'.",
                )
            )

        # Check required annotations if requested in context or by default
        require_annotations = context.get("require_enterprise_annotations", True)
        if require_annotations:
            for pattern, rule_code, msg in self.REQUIRED_ANNOTATIONS:
                if not re.search(pattern, code, re.IGNORECASE):
                    findings.append(
                        DiagnosticFinding(
                            severity="error",
                            rule_code=rule_code,
                            message=msg,
                        )
                    )

        # Check for balanced braces
        open_braces = code.count("{")
        close_braces = code.count("}")
        if open_braces != close_braces:
            findings.append(
                DiagnosticFinding(
                    severity="error",
                    rule_code="UNBALANCED_BRACES",
                    message=f"Syntax error: Unbalanced braces (opened {open_braces}, closed {close_braces}).",
                )
            )

        return findings
