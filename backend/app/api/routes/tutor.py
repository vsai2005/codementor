from __future__ import annotations

import logging

import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import Problem, User
from app.schemas.api import (
    CoachDebriefRequest,
    CoachResponse,
    MemoryNoteOut,
    TutorRequest,
    TutorResponse,
)
from app.services.embeddings import get_embedder
from app.services.llm import get_llm_client
from app.services.memory import MemoryService
from app.services.ratelimit import get_coach_rate_limiter, get_tutor_rate_limiter
from app.services.repositories import PgMemoryRepository

log = logging.getLogger(__name__)
router = APIRouter(tags=["tutor"])

SYSTEM = """You are a patient coding tutor for a placement-prep student.

Be concrete and brief. Use the student's past-mistake notes below to make your
answer personal — reference the pattern when it is genuinely relevant, and stay
quiet about it when it is not. Never invent a past mistake that is not listed.

Do not write the full solution unless explicitly asked; guide toward it."""


@router.post("/api/tutor/chat", response_model=TutorResponse)
def chat(
    payload: TutorRequest,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TutorResponse:
    ratelimit_key = f"tutor:{user.id}"
    verdict = get_tutor_rate_limiter().check(ratelimit_key)
    if not verdict.allowed:
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Tutor rate limit reached. Try again shortly.",
            headers={"Retry-After": str(verdict.retry_after_s)},
        )

    notes = []
    if user:
        try:
            memory = MemoryService(PgMemoryRepository(db), get_embedder())
            notes = memory.retrieve(str(user.id), payload.message, k=5)
        except Exception:
            # A new user, or a down embedding provider, must still get an answer.
            log.exception("memory retrieval failed; answering without context")

    context = "\n".join(f"- {n.content}" for n in notes) or "- (no past notes yet)"
    problem_context = ""
    if payload.problem_id:
        problem = db.get(Problem, payload.problem_id)
        if problem:
            problem_context = f"\n\nCurrent problem: {problem.title}\n{problem.statement_md[:1500]}"

    prompt = (
        f"Student's past-mistake notes:\n{context}{problem_context}\n\n"
        f"Student asks: {payload.message}"
    )

    try:
        reply = get_llm_client().complete(prompt, system=SYSTEM, temperature=0.4,
                                          max_tokens=800, timeout=15.0)
    except Exception as exc:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "The tutor is unavailable right now. Please try again.",
        ) from exc

    return TutorResponse(
        reply=reply.strip(),
        retrieved_notes=[
            MemoryNoteOut(id=n.id, content=n.content, similarity=round(n.similarity, 4))
            for n in notes
        ],
    )


@router.post("/api/coach/debrief", response_model=CoachResponse)
def coach_debrief(
    payload: CoachDebriefRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> CoachResponse:
    ratelimit_key = f"coach:{user.id}"
    verdict = get_coach_rate_limiter().check(ratelimit_key)
    if not verdict.allowed:
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Coach debrief rate limit reached. Try again shortly.",
            headers={"Retry-After": str(verdict.retry_after_s)},
        )

    problem = None
    try:
        uid = uuid.UUID(payload.problem_id)
        problem = db.get(Problem, uid)
    except (ValueError, TypeError):
        problem = db.execute(select(Problem).where(Problem.slug == payload.problem_id)).scalar_one_or_none()

    review = payload.review or {}
    tests = payload.tests or {}
    passed = tests.get("passed", 0)
    total = tests.get("total", 0)
    overall_score = review.get("overall_score", 0)

    if problem:
        try:
            client = get_llm_client()
            prompt = (
                f"Problem: {problem.title}\n"
                f"Student code:\n{payload.code[:2000]}\n\n"
                f"Test results: {passed}/{total} passed. Overall review score: {overall_score}/100.\n"
                f"Plan: {payload.plan or 'None'}\n"
                f"Summary: {review.get('summary', '')}\n"
                f"Provide concise, encouraging coaching debrief (2-3 sentences max) highlighting what to focus on next."
            )
            msg = client.complete(
                prompt,
                system="You are an encouraging coding coach giving brief debrief feedback.",
                max_tokens=200,
                timeout=5.0,
            )
            return CoachResponse(message=msg.strip())
        except Exception:
            pass

    if passed == total and total > 0:
        msg = "Great execution! All test cases passed. Review your time and space complexity to ensure your solution scales optimally."
    elif passed > 0:
        msg = f"Solid progress with {passed}/{total} tests passing. Check your edge cases or boundary conditions on the failing inputs."
    else:
        msg = "Trace the sample input step-by-step with pen and paper before coding to verify your algorithm logic."

    return CoachResponse(message=msg)

