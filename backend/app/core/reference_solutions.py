"""Server-side reference solutions repository (Batch 3).

Preserves real reference solutions server-side only:
- Real solutions are never leaked through normal problem/list APIs
- Exposed via GET /api/problems/{id}/reference ONLY after the authenticated
  learner has an accepted solution (100% test cases passed) for that problem
- Unsolved learners strictly receive 403 Forbidden
- Dummy 'pass' solutions are completely prohibited
"""

from __future__ import annotations

from app.seed import PROBLEMS

# Authoritative map of problem slug -> real reference solution code
REFERENCE_SOLUTIONS: dict[str, str] = {
    p["slug"]: p["reference_solution"].strip()
    for p in PROBLEMS
    if p.get("reference_solution") and p["reference_solution"].strip()
}


def get_problem_reference_solution(slug: str) -> str | None:
    """Retrieve the real server-side reference solution for a problem by slug."""
    return REFERENCE_SOLUTIONS.get(slug)


def set_custom_reference_solution(slug: str, solution: str) -> None:
    """Register or update reference solution for dynamic/generated problems."""
    REFERENCE_SOLUTIONS[slug] = solution.strip()
