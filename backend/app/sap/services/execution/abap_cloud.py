"""Local Static ABAP Cloud (Language Version 5) Scope and Clean ABAP Verification Provider.

TRUTHFULNESS NOTICE:
This provider performs local static regex analysis to enforce Clean ABAP and ABAP Cloud
Language Version 5 scope rules. It does NOT compile, interpret, or execute ABAP code
in any kernel or virtual machine, nor does it interact with any live SAP S/4HANA or BTP tenant.
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


class ABAPCloudProvider(SAPExecutionProvider):
    """Enforces ABAP Cloud Language Scope (Tier 1 Clean Core rules) via local static analysis."""

    category: ExecutionCategory = ExecutionCategory.STATIC_VALIDATION

    BANNED_LEGACY_PATTERNS = [
        (r"\bCALL\s+TRANSACTION\b", "CALL_TRANSACTION_FORBIDDEN", "CALL TRANSACTION is forbidden in ABAP Cloud. Use RAP actions or outbound navigation."),
        (r"\bTABLES\b\s*:", "TABLES_DECLARATION_OBSOLETE", "TABLES declaration is obsolete in ABAP Cloud. Use explicit local structure declarations."),
        (r"\bMOVE\s+.*?\s+TO\b", "OBSOLETE_MOVE_SYNTAX", "MOVE ... TO is obsolete. Use modern assignment operator '='."),
        (r"\bINSERT\s+INTO\s+(vbak|vbap|mara|bseg|bkpf|kna1|lfa1)\b", "DIRECT_STANDARD_DB_WRITE", "Direct DB modification of standard SAP tables is forbidden. Use RAP EML or released APIs."),
        (r"\bCOMMIT\s+WORK\b", "MANUAL_COMMIT_FORBIDDEN", "COMMIT WORK is forbidden inside RAP / Cloud business object logic."),
    ]

    async def execute(self, request: SAPExecutionRequest) -> SAPExecutionResult:
        start = time.perf_counter()
        findings = await self.validate_syntax(request.code_or_payload, request.context_parameters)
        errors = [f for f in findings if f.severity == "error"]
        success = len(errors) == 0

        return SAPExecutionResult(
            success=success,
            status="ok" if success else "policy_violation",
            output="Local static ABAP Cloud scope compliance check passed." if success else f"{len(errors)} ABAP Cloud rule violation(s) detected via local static check.",
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
        lines = code_or_payload.splitlines()

        for line_no, line in enumerate(lines, start=1):
            clean_line = line.split('"')[0].strip()
            if not clean_line or clean_line.startswith("*"):
                continue

            for pattern, rule_code, msg in self.BANNED_LEGACY_PATTERNS:
                if re.search(pattern, clean_line, re.IGNORECASE):
                    findings.append(
                        DiagnosticFinding(
                            severity="error",
                            line=line_no,
                            rule_code=rule_code,
                            message=msg,
                        )
                    )

        return findings
