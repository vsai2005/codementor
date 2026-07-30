"""Memory / RAG tests.

The cross-user isolation test is the gate for this phase (BUILD_PROMPTS
PROMPT 5), so it is written first and it is written twice: once against a
well-behaved repository, and once against a deliberately leaky one, because
"the service is safe if the repository is safe" is not a security guarantee.
"""

import pytest

from app.services.memory import (
    MemoryNote,
    MemoryService,
    build_note_prompt,
    cosine_similarity,
    deduplicate,
    truncate_note,
)


class FakeEmbedder:
    """Deterministic 8-dim embedding -- similar text gives similar vectors."""

    def __init__(self, fail: bool = False):
        self.fail = fail
        self.calls = 0

    def embed(self, text: str) -> list[float]:
        self.calls += 1
        if self.fail:
            raise RuntimeError("embedding provider down")
        vec = [0.0] * 8
        for token in text.lower().split():
            vec[hash(token) % 8] += 1.0
        return vec or [0.0] * 8


class FakeRepo:
    """Correctly scoped repository."""

    def __init__(self, notes=None):
        self.notes = list(notes or [])
        self.queried_user_ids = []

    def search(self, user_id, embedding, limit):
        self.queried_user_ids.append(user_id)
        rows = [n for n in self.notes if n.user_id == user_id]
        return sorted(rows, key=lambda n: n.similarity, reverse=True)[:limit]

    def insert(self, note, embedding):
        self.notes.append(note)


class LeakyRepo(FakeRepo):
    """Repository with the user_id filter 'accidentally' dropped."""

    def search(self, user_id, embedding, limit):
        self.queried_user_ids.append(user_id)
        return sorted(self.notes, key=lambda n: n.similarity, reverse=True)[:limit]


def note(nid, uid, content, sim=0.5):
    return MemoryNote(id=nid, user_id=uid, content=content, similarity=sim)


# --- SECURITY: written first, gates the phase -----------------------------

def test_user_a_never_receives_user_b_notes():
    repo = FakeRepo([
        note("1", "alice", "alice uses nested loops", 0.9),
        note("2", "bob", "bob forgets base cases", 0.95),
        note("3", "bob", "bob writes exponential recursion", 0.99),
    ])
    svc = MemoryService(repo, FakeEmbedder())

    results = svc.retrieve("alice", "what am I bad at?")

    assert all(n.user_id == "alice" for n in results)
    assert {n.id for n in results} == {"1"}
    assert repo.queried_user_ids == ["alice"]


def test_service_drops_foreign_notes_even_if_the_repository_leaks():
    """Defence in depth: a bad query must not become a data breach."""
    repo = LeakyRepo([
        note("1", "alice", "alice note", 0.5),
        note("2", "bob", "bob note", 0.99),
    ])
    svc = MemoryService(repo, FakeEmbedder())

    results = svc.retrieve("alice", "anything")

    assert all(n.user_id == "alice" for n in results), "cross-user leak reached the caller"
    assert not any(n.id == "2" for n in results)


def test_retrieve_without_a_user_id_is_refused():
    svc = MemoryService(FakeRepo(), FakeEmbedder())
    with pytest.raises(ValueError):
        svc.retrieve("", "query")


def test_notes_are_stored_against_the_owning_user_only():
    repo = FakeRepo()
    svc = MemoryService(repo, FakeEmbedder())
    svc.store_note(user_id="alice", content="alice mistake")

    assert svc.retrieve("bob", "mistake") == []
    assert len(svc.retrieve("alice", "mistake")) == 1


# --- resilience -----------------------------------------------------------

def test_embedding_failure_does_not_raise_on_store():
    svc = MemoryService(FakeRepo(), FakeEmbedder(fail=True))
    assert svc.store_note(user_id="alice", content="something") is False


def test_embedding_failure_on_retrieval_returns_empty_not_an_error():
    svc = MemoryService(FakeRepo([note("1", "alice", "x")]), FakeEmbedder(fail=True))
    assert svc.retrieve("alice", "query") == []


def test_new_user_with_empty_memory_returns_nothing_and_does_not_crash():
    svc = MemoryService(FakeRepo(), FakeEmbedder())
    assert svc.retrieve("brand-new-user", "help me with graphs") == []


def test_blank_query_short_circuits_without_embedding():
    embedder = FakeEmbedder()
    svc = MemoryService(FakeRepo(), embedder)
    assert svc.retrieve("alice", "   ") == []
    assert embedder.calls == 0


# --- ordering, dedupe, truncation ----------------------------------------

def test_results_are_ordered_by_similarity():
    repo = FakeRepo([
        note("low", "alice", "graphs traversal bfs", 0.40),
        note("high", "alice", "hashmaps lookup dict", 0.95),
        note("mid", "alice", "sorting comparator stable", 0.70),
    ])
    results = MemoryService(repo, FakeEmbedder()).retrieve("alice", "q")
    sims = [n.similarity for n in results]
    assert sims == sorted(sims, reverse=True)


def test_near_duplicate_notes_are_deduplicated():
    embedder = FakeEmbedder()
    identical = "user reaches for nested loops instead of hashmaps"
    repo = FakeRepo([
        note("a", "alice", identical, 0.99),
        note("b", "alice", identical, 0.98),
        note("c", "alice", "totally different topic about graph traversal", 0.90),
    ])
    results = MemoryService(repo, embedder).retrieve("alice", "q")

    ids = {n.id for n in results}
    assert "a" in ids and "b" not in ids, "identical notes must collapse"
    assert "c" in ids, "distinct notes must survive"


def test_deduplicate_keeps_the_higher_ranked_of_a_pair():
    v = [1.0, 0.0]
    notes = [note("first", "u", "x", 0.9), note("second", "u", "x", 0.8)]
    kept = deduplicate(notes, {"first": v, "second": v})
    assert [n.id for n in kept] == ["first"]


def test_retrieve_respects_k():
    repo = FakeRepo([note(str(i), "alice", f"distinct topic number {i}", 0.9 - i * 0.01)
                     for i in range(20)])
    assert len(MemoryService(repo, FakeEmbedder()).retrieve("alice", "q", k=5)) <= 5


def test_notes_are_capped_at_three_hundred_chars():
    long = "user writes brute force solutions " * 40
    out = truncate_note(long)
    assert len(out) <= 300
    assert out.endswith("…")


def test_short_notes_are_untouched():
    assert truncate_note("user forgets edge cases") == "user forgets edge cases"


def test_cosine_similarity_basics():
    assert cosine_similarity([1, 0], [1, 0]) == pytest.approx(1.0)
    assert cosine_similarity([1, 0], [0, 1]) == pytest.approx(0.0)
    assert cosine_similarity([0, 0], [1, 1]) == 0.0


def test_note_prompt_includes_the_char_limit_and_context():
    prompt = build_note_prompt("Two Sum", 65, "nested loop", ["hashmaps"])
    assert "300" in prompt
    assert "Two Sum" in prompt and "hashmaps" in prompt
