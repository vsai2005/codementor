from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.models import Problem, User
from app.schemas.api import MemoryNoteOut, TutorRequest, TutorResponse
from app.services.embeddings import get_embedder
from app.services.llm import get_llm_client
from app.services.memory import MemoryService
from app.services.ratelimit import get_rate_limiter
from app.services.repositories import PgMemoryRepository

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/tutor", tags=["tutor"])

SYSTEM = """You are a patient coding tutor for a placement-prep student.

Be concrete and brief. Use the student's past-mistake notes below to make your
answer personal — reference the pattern when it is genuinely relevant, and stay
quiet about it when it is not. Never invent a past mistake that is not listed.

Do not write the full solution unless explicitly asked; guide toward it."""


@router.post("/chat", response_model=TutorResponse)
def chat(
    payload: TutorRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TutorResponse:
    verdict = get_rate_limiter().check(f"tutor:{user.id}")
    if not verdict.allowed:
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Tutor rate limit reached. Try again shortly.",
            headers={"Retry-After": str(verdict.retry_after_s)},
        )

    notes = []
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
