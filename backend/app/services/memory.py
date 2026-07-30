"""Personal memory, Layer B (PRD 3.3, 5.7).

The hard requirement: every vector query filters on user_id. Cross-user
leakage is a security failure, not a relevance bug.

That filter is enforced structurally rather than by convention. There is no
public method that builds a query without a user_id, and `_select` refuses to
construct one -- so "someone forgot the WHERE clause" cannot happen in a code
path that type-checks.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Protocol, Sequence

log = logging.getLogger(__name__)

MAX_NOTE_CHARS = 300
DEDUPE_THRESHOLD = 0.95
DEFAULT_K = 5


@dataclass
class MemoryNote:
    id: str
    user_id: str
    content: str
    topic_id: str | None = None
    submission_id: str | None = None
    similarity: float = 0.0


class Embedder(Protocol):
    def embed(self, text: str) -> list[float]: ...


class MemoryRepository(Protocol):
    """Storage port. Implementations MUST scope every read to user_id."""

    def search(self, user_id: str, embedding: Sequence[float], limit: int) -> list[MemoryNote]: ...
    def insert(self, note: MemoryNote, embedding: Sequence[float]) -> None: ...


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def truncate_note(content: str, limit: int = MAX_NOTE_CHARS) -> str:
    content = " ".join(content.split())
    if len(content) <= limit:
        return content
    cut = content[: limit - 1]
    # Prefer a word boundary so the note does not end mid-token.
    space = cut.rfind(" ")
    if space > limit * 0.6:
        cut = cut[:space]
    return cut.rstrip() + "…"


def deduplicate(notes: Sequence[MemoryNote],
                embeddings: dict[str, Sequence[float]],
                threshold: float = DEDUPE_THRESHOLD) -> list[MemoryNote]:
    """Drop notes that are near-identical to one already kept (PRD 3.3).

    Input is assumed ordered by descending similarity to the query, so the
    first of any duplicate pair is the more relevant one and survives.
    """
    kept: list[MemoryNote] = []
    for note in notes:
        vec = embeddings.get(note.id)
        if vec is None:
            kept.append(note)
            continue
        if any(cosine_similarity(vec, embeddings[k.id]) > threshold
               for k in kept if k.id in embeddings):
            continue
        kept.append(note)
    return kept


class MemoryService:
    def __init__(self, repo: MemoryRepository, embedder: Embedder) -> None:
        self._repo = repo
        self._embedder = embedder

    def retrieve(self, user_id: str, query: str, k: int = DEFAULT_K) -> list[MemoryNote]:
        if not user_id:
            raise ValueError("user_id is required for every memory query")
        if not query.strip():
            return []
        try:
            vector = self._embedder.embed(query)
        except Exception:
            log.exception("embedding failed during retrieval; returning no memory")
            return []

        # Over-fetch so dedupe cannot starve the result set.
        candidates = self._repo.search(user_id, vector, limit=k * 3)

        leaked = [n for n in candidates if n.user_id != user_id]
        if leaked:
            log.error("memory repository returned %d foreign notes -- dropping", len(leaked))
            candidates = [n for n in candidates if n.user_id == user_id]

        candidates.sort(key=lambda n: n.similarity, reverse=True)
        embeddings = {n.id: self._safe_embed(n.content) for n in candidates}
        embeddings = {i: v for i, v in embeddings.items() if v}
        return deduplicate(candidates, embeddings)[:k]

    def store_note(self, *, user_id: str, content: str, topic_id: str | None = None,
                   submission_id: str | None = None, note_id: str | None = None) -> bool:
        """Persist a memory note. Returns False on failure -- never raises.

        PRD 5.7: an embedding failure is logged and skipped, never surfaced to
        the user, because this runs after the submission response is already
        committed.
        """
        import uuid

        try:
            text = truncate_note(content)
            if not text:
                return False
            vector = self._embedder.embed(text)
            self._repo.insert(
                MemoryNote(
                    id=note_id or str(uuid.uuid4()),
                    user_id=user_id,
                    content=text,
                    topic_id=topic_id,
                    submission_id=submission_id,
                ),
                vector,
            )
            return True
        except Exception:
            log.exception("memory note storage failed for user %s -- skipping", user_id)
            return False

    def _safe_embed(self, text: str) -> list[float] | None:
        try:
            return self._embedder.embed(text)
        except Exception:
            return None


NOTE_PROMPT = """Summarise this submission as a single memory note for the \
student's long-term profile.

Rules:
- One or two sentences, under {limit} characters.
- Describe the MISTAKE PATTERN, not the specific problem.
- Write in the third person: "User ..."
- If the submission was flawless, say what the student did well, briefly.

Problem: {problem}
Score: {score}
Summary of review: {summary}
Weak topics: {weak_topics}

Return the note text only, no quotes, no preamble."""


def build_note_prompt(problem: str, score: int, summary: str,
                      weak_topics: list[str]) -> str:
    return NOTE_PROMPT.format(
        limit=MAX_NOTE_CHARS, problem=problem, score=score,
        summary=summary, weak_topics=", ".join(weak_topics) or "none",
    )
