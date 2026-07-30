"""Postgres/pgvector implementation of the memory port.

Every read is scoped to user_id. The filter is applied inside this class, not
by callers, because a security control that depends on being remembered is not
a control.
"""

from __future__ import annotations

import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import MemoryNoteRow
from app.services.memory import MemoryNote


class PgMemoryRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def search(self, user_id: str, embedding: Sequence[float], limit: int) -> list[MemoryNote]:
        if not user_id:
            raise ValueError("user_id is mandatory on every memory query")

        distance = MemoryNoteRow.embedding.cosine_distance(list(embedding))
        stmt = (
            select(MemoryNoteRow, distance.label("distance"))
            .where(MemoryNoteRow.user_id == uuid.UUID(str(user_id)))  # NON-NEGOTIABLE
            .order_by(distance)
            .limit(limit)
        )
        return [
            MemoryNote(
                id=str(row.MemoryNoteRow.id),
                user_id=str(row.MemoryNoteRow.user_id),
                content=row.MemoryNoteRow.content,
                topic_id=str(row.MemoryNoteRow.topic_id) if row.MemoryNoteRow.topic_id else None,
                submission_id=(
                    str(row.MemoryNoteRow.submission_id)
                    if row.MemoryNoteRow.submission_id else None
                ),
                similarity=1.0 - float(row.distance),
            )
            for row in self._db.execute(stmt).all()
        ]

    def insert(self, note: MemoryNote, embedding: Sequence[float]) -> None:
        self._db.add(
            MemoryNoteRow(
                id=uuid.UUID(note.id),
                user_id=uuid.UUID(str(note.user_id)),
                submission_id=uuid.UUID(note.submission_id) if note.submission_id else None,
                topic_id=uuid.UUID(note.topic_id) if note.topic_id else None,
                content=note.content,
                embedding=list(embedding),
            )
        )
        self._db.commit()
