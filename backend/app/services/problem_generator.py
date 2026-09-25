"""AI Problem Generation with Sandbox Validation.

Generates fresh algorithmic problems using the configured LLM service,
and rigorously validates the problem by executing its reference solution
against all generated test cases inside the sandbox before returning or saving it.
"""

from __future__ import annotations

import ast
import logging
import re
import uuid
from typing import Any
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Problem, Topic
from app.schemas.api import ProblemDetail, TopicOut
from app.services.llm import get_llm_client, extract_json
from app.services.sandbox import run_test_cases_async

log = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an expert algorithm problem author.
Generate a high quality, well-defined coding problem in Python.
You must return a valid JSON object matching the following structure:
{
  "title": "Short title",
  "slug": "kebab-case-slug",
  "statement_md": "Clear problem statement with examples",
  "constraints_md": "Constraints on input sizes",
  "difficulty_tier": 1,
  "entry_point": "function_name",
  "starter_code": {
    "python": "def function_name(arg1, arg2):\\n    pass\\n"
  },
  "reference_solution": "def function_name(arg1, arg2):\\n    return ...\\n",
  "test_cases": [
    {"args": [arg1, arg2], "expected": expected_result}
  ],
  "optimal_time": "O(N)",
  "optimal_space": "O(1)"
}
The test_cases MUST have at least 2 test cases with exact inputs and outputs.
The reference_solution MUST be 100% syntactically valid Python code and MUST pass all test_cases when called as entry_point(*args).
"""


def _sanitize_and_validate_reference_solution(code: str) -> str:
    """Validate reference solution Python syntax and guard against credentials/secrets/logs."""
    cleaned = code.strip()
    if cleaned.startswith("```python"):
        cleaned = cleaned[len("```python"):].strip()
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:].strip()
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].strip()

    cleaned = cleaned.strip()
    if not cleaned:
        raise ValueError("Reference solution cannot be empty.")

    # Ensure no secrets, credentials, or execution logs are stored
    forbidden_patterns = [
        r"api_key\b", r"apikey\b", r"secret_key\b", r"bearer\s+[a-zA-Z0-9_\-\.]+",
        r"password\s*=", r"pwd_hash\b", r"database_url\b", r"redis_url\b",
        r"gemini_api_key\b", r"aizasy[a-zA-Z0-9_\-]{30,}", r"sk-[a-zA-Z0-9_\-]{20,}",
        r"\[execution\s+log\]", r"stdout:", r"stderr:",
    ]
    for pattern in forbidden_patterns:
        if re.search(pattern, cleaned, re.IGNORECASE):
            raise ValueError(f"Reference solution contains prohibited token or credential pattern: {pattern}")

    # Must be valid Python syntax
    try:
        ast.parse(cleaned)
    except SyntaxError as e:
        raise ValueError(f"Reference solution has invalid Python syntax: {e}") from e

    return cleaned


async def generate_and_validate_problem(
    *,
    topic_slug: str | None,
    tier: int | None,
    db: Session,
) -> ProblemDetail:
    # 1. Resolve topic
    topic = None
    if topic_slug:
        topic = db.execute(select(Topic).where(Topic.slug == topic_slug)).scalar_one_or_none()
    if not topic:
        topic = db.execute(select(Topic)).scalars().first()

    target_tier = tier or 1
    topic_name = getattr(topic, "name", "Algorithms") if topic else "Algorithms"

    prompt = (
        f"Generate a Tier {target_tier} coding problem for topic '{topic_name}'.\n"
        f"Return ONLY the JSON specification with reference_solution and test_cases."
    )

    try:
        client = get_llm_client()
        raw = client.complete(prompt, system=SYSTEM_PROMPT, temperature=0.5, max_tokens=1500, timeout=12.0)
        data = extract_json(raw)
    except Exception as exc:
        log.warning("LLM problem generation failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI problem generation failed: {exc}",
        ) from exc

    # Validate essential fields
    title = str(data.get("title", "")).strip() or "Generated Problem"
    raw_slug = str(data.get("slug", "")).strip() or f"gen-{uuid.uuid4().hex[:8]}"
    slug = raw_slug if raw_slug.startswith("gen-") else f"gen-{raw_slug}"
    statement_md = str(data.get("statement_md", "")).strip()
    constraints_md = str(data.get("constraints_md", "")).strip()
    entry_point = str(data.get("entry_point", "")).strip() or "solve"
    starter_code = data.get("starter_code") or {"python": f"def {entry_point}():\n    pass\n"}
    ref_solution = str(data.get("reference_solution", "")).strip()
    test_cases = data.get("test_cases", [])
    optimal_time = str(data.get("optimal_time", "O(N)"))
    optimal_space = str(data.get("optimal_space", "O(1)"))

    if not statement_md or not ref_solution or not isinstance(test_cases, list) or len(test_cases) == 0:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI generated incomplete problem structure. Please try again.",
        )

    try:
        clean_ref_solution = _sanitize_and_validate_reference_solution(ref_solution)
    except ValueError as val_err:
        log.warning("Generated reference solution failed sanitization/validation: %s", val_err)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Generated problem rejected: invalid reference solution ({val_err}).",
        ) from val_err

    # 2. Execute reference solution against test cases in the sandbox
    try:
        report = await run_test_cases_async(clean_ref_solution, entry_point, test_cases)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Sandbox validation failed during execution: {exc}",
        ) from exc

    if not report.all_passed:
        failed_count = len(test_cases) - report.passed_count
        log.warning(
            "Generated problem %s rejected: %d/%d test cases failed in sandbox",
            slug, failed_count, len(test_cases)
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Generated problem rejected: reference solution failed {failed_count} test case(s) in sandbox.",
        )

    # 3. Persist problem in DB transactionally
    existing = db.execute(select(Problem).where(Problem.slug == slug)).scalar_one_or_none()
    if existing:
        slug = f"{slug}-{uuid.uuid4().hex[:4]}"

    new_problem = Problem(
        id=uuid.uuid4(),
        slug=slug,
        title=title,
        statement_md=statement_md,
        constraints_md=constraints_md,
        difficulty_tier=target_tier,
        topic_id=topic.id if topic else None,
        entry_point=entry_point,
        starter_code=starter_code,
        test_cases=test_cases,
        optimal_time=optimal_time,
        optimal_space=optimal_space,
        is_generated=True,
        generation_source="ai_generated",
        reference_solution=clean_ref_solution,
    )
    try:
        db.add(new_problem)
        db.commit()
        db.refresh(new_problem)
    except Exception as exc:
        db.rollback()
        log.error("Failed to persist generated problem %s: %s", slug, exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to persist generated problem.",
        ) from exc

    topic_out = (
        TopicOut.model_validate(topic)
        if (topic and hasattr(topic, "slug") and hasattr(topic, "name"))
        else TopicOut(id=uuid.uuid4(), slug="arrays", name="Arrays & Hashing")
    )
    return ProblemDetail(
        id=new_problem.id,
        slug=new_problem.slug,
        title=new_problem.title,
        difficulty_tier=new_problem.difficulty_tier,
        topic=topic_out,
        statement_md=new_problem.statement_md,
        constraints_md=new_problem.constraints_md,
        optimal_time=new_problem.optimal_time,
        optimal_space=new_problem.optimal_space,
        entry_point=new_problem.entry_point,
        starter_code=new_problem.starter_code,
        is_generated=True,
        generation_source="ai_generated",
    )
