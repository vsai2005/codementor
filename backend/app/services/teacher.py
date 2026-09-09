"""
Dedicated AITeacherService for CodeMentor.
Orchestrates Socratic guidance, progressive disclosure, hint escalation,
misconception diagnosis, and deterministic offline fallbacks.
"""

from __future__ import annotations

import logging
import re
from typing import Any
from app.core.curriculum_retrieval import CurriculumKnowledgeEngine
from app.services.llm import LLMClient, LLMError, get_llm_client
from app.services.tutor_security import (
    AI_TEACHER_SYSTEM_PROMPT,
    build_safe_tutor_prompt,
    sanitize_user_input,
)

log = logging.getLogger(__name__)


class AITeacherService:
    def __init__(self, client: LLMClient | None = None) -> None:
        self._client = client
        self.engine = CurriculumKnowledgeEngine.get_instance()

    @property
    def client(self) -> LLMClient:
        if self._client is None:
            self._client = get_llm_client()
        return self._client

    def chat(
        self,
        day_number: int,
        message: str,
        history: list | None = None,
        quick_action: str | None = None,
        user_code: str | None = None,
        step_number: int = 1,
        step_type: str = "explanation",
        step_heading: str | None = None,
        step_takeaway: str | None = None,
        completed_days: list[int] | None = None,
        hint_level: int = 1,
    ) -> dict[str, Any]:
        # 1. Build Curriculum Context
        curriculum_context = self.engine.build_teacher_context(
            current_day=day_number,
            student_query=message,
            step_number=step_number,
            step_type=step_type,
            step_heading=step_heading,
            step_takeaway=step_takeaway,
            current_code=user_code,
            completed_days=completed_days,
        )

        # 2. Scope Guardrail Pre-Check
        off_topic = self._check_off_topic(message)
        if off_topic:
            return {
                "reply": off_topic,
                "quick_action": quick_action,
                "related_concepts": ["Python & DSA Learning Scope"],
                "visual": None,
                "is_fallback": False,
            }

        # 3. Assemble Safe Prompt
        prompt = build_safe_tutor_prompt(
            curriculum_context=curriculum_context,
            message=message,
            history=history,
            user_code=user_code,
            quick_action=quick_action,
            hint_level=hint_level,
        )

        # 4. LLM Completion with Resilient Fallback
        try:
            raw_reply = self.client.complete(
                prompt=prompt,
                system=AI_TEACHER_SYSTEM_PROMPT,
                temperature=0.35,
                max_tokens=450,
                timeout=8.0,
            )
            reply = raw_reply.strip()
            is_fallback = False
        except (LLMError, Exception) as exc:
            log.warning("AI Teacher LLM invocation failed: %s. Using pedagogical fallback.", exc)
            reply = self._generate_fallback(
                day_number=day_number,
                message=message,
                quick_action=quick_action,
                user_code=user_code,
                hint_level=hint_level,
            )
            is_fallback = True

        day_meta = self.engine.days.get(day_number)
        related = day_meta.concepts[:3] if day_meta else ["Python Basics"]

        return {
            "reply": reply,
            "quick_action": quick_action,
            "related_concepts": related,
            "visual": None,
            "is_fallback": is_fallback,
        }

    def _check_off_topic(self, query: str) -> str | None:
        q = query.lower().strip()
        # Explicit off-topic keywords
        off_topic_patterns = [
            r"\b(world cup|super bowl|nba|olympics|messi|ronaldo)\b",
            r"\b(recipe|bake|pizza|pasta|cookie|ingredients)\b",
            r"\b(president|election|senate|politics|prime minister)\b",
            r"\b(movie|cinema|actor|celebrity|hollywood)\b",
        ]
        for pat in off_topic_patterns:
            if re.search(pat, q):
                return (
                    "I'm your CodeMentor Python and DSA tutor, so I keep all our focus on programming, "
                    "algorithms, and computer science concepts! How can I help you with today's coding lesson?"
                )
        return None

    def _generate_fallback(
        self,
        day_number: int,
        message: str,
        quick_action: str | None = None,
        user_code: str | None = None,
        hint_level: int = 1,
    ) -> str:
        day_meta = self.engine.days.get(day_number)
        topic = day_meta.title if day_meta else f"Day {day_number}"
        topic = day_meta.title if day_meta else f"Day {day_number}"
        msg = (message or "").lower().strip()

        # 1. Prioritize Quick Actions
        if quick_action == "give_hint":
            if hint_level == 1:
                return f"**Hint 1 (Conceptual Nudge):** What are the boundary conditions for {topic}? Think about what happens if the input is empty or has only 1 element."
            elif hint_level == 2:
                return f"**Hint 2 (Directional Guidance):** Consider which data structure or pointer strategy gives you fast access without nested loops. Can you track your state as you iterate?"
            else:
                return f"**Hint 3 (Algorithmic Recipe):** Maintain your invariant: advance your pointers only when your condition holds, and return the accumulated result at the boundary."

        if quick_action == "find_mistake":
            if user_code and "-" in user_code and ("add" in user_code or "sum" in user_code):
                return "Take a close look at your operator: you have a subtraction (`-`) where addition (`+`) is needed to accumulate the total."
            return "Inspect your return statement and loop boundary: make sure your function returns the computed variable rather than printing or terminating early."

        if quick_action == "quiz_me":
            return (
                f"**Active Recall Quiz on {topic}:**\n\n"
                "What is the key advantage of choosing the optimal data structure or algorithm for this problem?\n"
                "A) It makes the code shorter to type\n"
                "B) It improves the asymptotic time or space complexity\n"
                "C) It prevents Python syntax errors automatically\n"
                "D) It eliminates the need for test cases\n\n"
                "*Reply with your choice (A, B, C, or D) to check your understanding!*"
            )

        if quick_action == "show_visually":
            if "stack" in topic.lower() or "stack" in msg:
                return (
                    "**Visual Mental Model: Stack (LIFO)**\n\n"
                    "```text\n"
                    "  TOP    -> [ Plate 3 ]  ^ (pop removes from top)\n"
                    "            [ Plate 2 ]  |\n"
                    "  BOTTOM -> [ Plate 1 ]  v (push adds to top)\n"
                    "```\n\n"
                    "Items enter and exit strictly from the top in O(1) time!"
                )
            return (
                f"**Visual Mental Model for {topic}:**\n\n"
                "```text\n"
                "  INPUT ---> [ Process / Invariant Step ] ---> OUTPUT\n"
                "  State:     [ Invariant Verified: O(1) ]\n"
                "```\n\n"
                "Would you like me to walk through a step-by-step trace table with numbers?"
            )

        if quick_action == "explain_simply":
            if day_number == 1 or "variable" in msg:
                return (
                    "Think of a **variable** as a friendly name tag that you stick onto a piece of data. "
                    "For instance, `score = 10` sticks the label `score` onto the number 10. "
                    "Whenever you ask Python for `score`, it looks at that name tag and gives you 10!"
                )
            return (
                f"At its simplest, **{topic}** is about breaking down work so Python only does what is necessary. "
                "Instead of redoing calculations from scratch, we organize our data so each step builds naturally on the last."
            )

        if quick_action == "give_example":
            if day_number == 1:
                return (
                    "Here is a tiny, crystal-clear example:\n\n"
                    "```python\n"
                    "name = 'Sai'\n"
                    "print(name)\n"
                    "```\n\n"
                    "1. Line 1 creates the label `name` pointing to `'Sai'`.\n"
                    "2. Line 2 looks up `name` and outputs `Sai` to your console!"
                )
            return (
                f"Here is a small snippet illustrating {topic}:\n\n"
                "```python\n"
                "# Quick demonstration\n"
                "data = [1, 2, 3]\n"
                "print(len(data))\n"
                "```"
            )

        if quick_action == "explain_deeper":
            return (
                f"**Under the Hood of {topic}:**\n\n"
                "In Python, variables are object references stored in a local frame table. "
                "When you assign or mutate state, Python manages the memory address and reference counts automatically. "
                "This ensures clean execution, but understanding whether an operation is O(1) or O(N) allows you to write scalable code."
            )

        if quick_action == "connect_concept":
            prereqs = self.engine.get_prerequisites(day_number)
            prereq_names = ", ".join(prereqs) if prereqs else "core fundamentals"
            return (
                f"**Connecting the Dots:**\n\n"
                f"{topic} builds directly on **{prereq_names}**. "
                "Mastering this pattern now gives you the exact building blocks needed for upcoming algorithmic challenges!"
            )

        if quick_action == "teach_prerequisite":
            prereqs = self.engine.get_prerequisites(day_number)
            if prereqs:
                return f"Before mastering {topic}, ensure you are comfortable with: **{', '.join(prereqs)}**. Would you like a 2-minute refresher on any of these?"
            return f"You're already at the foundational level for {topic}! Everything you need is introduced step-by-step in today's lesson."

        # 2. Dynamic 5-Angle Adaptation for confusion signals
        if any(w in msg for w in ["don't understand", "dont understand", "confused", "explain differently", "what do you mean"]):
            return (
                f"Let's reset and look at {topic} from a different angle:\n\n"
                "**Real-World Analogy:** Imagine you are organizing books on a shelf by their color. "
                "Instead of checking every book repeatedly, you put a colored sticky note on each section.\n\n"
                "Does thinking of it as labeled sections help clarify the core idea?"
            )

        # 3. Topic & Cross-Topic Search Queries
        if day_number == 1 or "variable" in msg:
            return (
                "In Python, think of a variable as giving a friendly name tag to a piece of data. "
                "For example, `name = 'Sai'` labels the string `'Sai'` with the name `name`. "
                "When you reassign it, Python simply moves the name tag to the new object in memory! "
                "Does that name tag analogy make sense?"
            )

        if "stack" in msg:
            return (
                "A stack is a fundamental linear data structure operating under Last-In, First-Out (LIFO) discipline. "
                "Imagine a pile of plates: you add new items to the top (push) and remove from the top (pop) in O(1) time. "
                "In Python, a standard list with `.append()` and `.pop()` serves as a stack!"
            )

        if "dynamic programming" in msg or "dp" in msg:
            return (
                "Before tackling Dynamic Programming, master **Recursion** and **Memoization**! "
                "DP solves problems with overlapping subproblems and optimal substructure by caching results "
                "so identical calculations are never repeated."
            )

        return (
            f"You're exploring Day {day_number}: {topic}. "
            "Remember to trace your variables step-by-step and test boundary inputs. "
            "What specific question or code line can I clarify for you?"
        )

    def generate_response(
        self,
        day_number: int,
        step_number: int = 1,
        query: str = "",
        history: list | None = None,
        user_code: str | None = None,
        step_context: dict[str, Any] | None = None,
        quick_action: str | None = None,
        hint_level: int = 1,
        completed_days: list[int] | None = None,
    ) -> dict[str, Any]:
        sc = step_context or {}
        return self.chat(
            day_number=day_number,
            message=query,
            history=history,
            quick_action=quick_action,
            user_code=user_code,
            step_number=step_number,
            step_type=sc.get("step_type", "explanation"),
            step_heading=sc.get("heading"),
            step_takeaway=sc.get("takeaway"),
            completed_days=completed_days,
            hint_level=hint_level,
        )


_teacher_service: AITeacherService | None = None


def get_teacher_service() -> AITeacherService:
    global _teacher_service
    if _teacher_service is None:
        _teacher_service = AITeacherService()
    return _teacher_service
