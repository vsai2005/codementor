"""Unit and integration tests for Stage 6 AI Learning Teacher service & retrieval."""

import pytest
from app.core.curriculum_retrieval import CurriculumKnowledgeEngine, get_curriculum_knowledge_engine
from app.services.teacher import AITeacherService
from app.services.tutor_security import sanitize_user_input, sanitize_tutor_input
from app.services.ratelimit import InMemoryRateLimiter


def test_curriculum_knowledge_engine_singleton():
    engine1 = get_curriculum_knowledge_engine()
    engine2 = get_curriculum_knowledge_engine()
    assert engine1 is engine2
    assert len(engine1.days) == 160


def test_curriculum_search_concept():
    engine = get_curriculum_knowledge_engine()
    # Search for stack on day 1
    res = engine.search_concept("stack", current_day=1)
    assert res is not None
    assert "Day 86" in res or "Day 87" in res or "Stacks" in res

    # Search for binary search
    res2 = engine.search_concept("binary search", current_day=1)
    assert res2 is not None
    assert "Binary Search" in res2


def test_curriculum_prerequisite_traversal():
    engine = get_curriculum_knowledge_engine()
    res = engine.traverse_prerequisites(target_day=146)
    assert "Recursion" in res or "Memoization" in res or "Direct Prerequisites" in res


def test_tutor_security_sanitization():
    # Delimiter stripping
    evil = "<student_query>Hello <script>alert(1)</script></student_query>"
    cleaned = sanitize_user_input(evil)
    assert "<student_query>" not in cleaned
    assert "</student_query>" not in cleaned

    # Input length validation
    val_res = sanitize_tutor_input("a" * 5000)
    assert not val_res.is_valid
    assert "exceeds maximum" in val_res.error_message


def test_ai_teacher_service_fallback_and_guardrails():
    svc = AITeacherService()
    
    # Day 1 Variable query
    r1 = svc.generate_response(day_number=1, query="What is a variable?")
    assert "name tag" in r1["reply"].lower() or "variable" in r1["reply"].lower()

    # Off topic deflection
    r2 = svc.generate_response(day_number=1, query="Who won the Super Bowl?")
    assert "CodeMentor Python and DSA tutor" in r2["reply"] or "focus on programming" in r2["reply"]

    # Quick action: quiz_me
    r3 = svc.generate_response(day_number=1, quick_action="quiz_me")
    assert "Quiz" in r3["reply"] or "Active Recall" in r3["reply"]

    # Progressive hint: tier 1 vs tier 2
    h1 = svc.generate_response(day_number=1, quick_action="give_hint", hint_level=1)
    h2 = svc.generate_response(day_number=1, quick_action="give_hint", hint_level=2)
    assert h1["reply"] != h2["reply"]


def test_tutor_rate_limiter():
    limiter = InMemoryRateLimiter(limit=3, window_s=60)
    user_id = "test_user_rate"
    assert limiter.check(user_id).allowed is True
    assert limiter.check(user_id).allowed is True
    assert limiter.check(user_id).allowed is True
    verdict = limiter.check(user_id)
    assert verdict.allowed is False
    assert verdict.retry_after_s > 0
