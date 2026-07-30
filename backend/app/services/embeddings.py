"""Embedding provider (1536-dim, PRD 5.1)."""

from __future__ import annotations

import os

EMBED_DIM = 1536


class EmbeddingError(RuntimeError):
    pass


class OpenAIEmbedder:
    def __init__(self, api_key: str, model: str = "text-embedding-3-small") -> None:
        self._api_key = api_key
        self._model = model

    def embed(self, text: str) -> list[float]:
        import httpx

        try:
            r = httpx.post(
                "https://api.openai.com/v1/embeddings",
                headers={"Authorization": f"Bearer {self._api_key}"},
                json={"model": self._model, "input": text[:8000]},
                timeout=10.0,
            )
        except httpx.HTTPError as exc:
            raise EmbeddingError(str(exc)) from exc

        if r.status_code >= 400:
            raise EmbeddingError(f"{r.status_code}: {r.text[:200]}")

        vector = r.json()["data"][0]["embedding"]
        if len(vector) != EMBED_DIM:
            raise EmbeddingError(f"expected {EMBED_DIM} dims, got {len(vector)}")
        return vector


def get_embedder():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise EmbeddingError("OPENAI_API_KEY is not set")
    return OpenAIEmbedder(key, os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))
