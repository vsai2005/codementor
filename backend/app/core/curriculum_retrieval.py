"""
Curriculum Context and Retrieval Engine for AI Teacher.
Provides in-memory inverted concept indexing, prerequisite DAG traversal,
concept relationship mapping, and token-budgeted prompt generation.
"""

from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

log = logging.getLogger(__name__)


class RelationType(str, Enum):
    COMPOSED_OF = "COMPOSED_OF"
    REQUIRES = "REQUIRES"
    ALTERNATIVE_TO = "ALTERNATIVE_TO"
    EXTENDS = "EXTENDS"


@dataclass(frozen=True)
class ConceptRelation:
    source_concept: str
    target_concept: str
    relation: RelationType
    source_day: int
    target_day: int
    explanation: str


@dataclass
class CurriculumDayMeta:
    day_number: int
    section_id: str
    section_number: int
    section_title: str
    title: str
    topic_name: str
    estimated_minutes: int
    difficulty: str
    prerequisites: list[int]
    flow_tier: str
    archetype: str
    concepts: list[str]
    learning_objectives: list[str]
    description: str
    practice_problem_slug: str | None = None


class CurriculumKnowledgeEngine:
    _instance: CurriculumKnowledgeEngine | None = None

    def __init__(self, manifest_path: str | None = None):
        self.days: dict[int, CurriculumDayMeta] = {}
        self.inverted_concept_index: dict[str, set[int]] = {}
        self.concept_relations: list[ConceptRelation] = []
        self.aliases: dict[str, list[int]] = {}
        self._load_curriculum(manifest_path)
        self._build_concept_relations()

    @classmethod
    def get_instance(cls, manifest_path: str | None = None) -> CurriculumKnowledgeEngine:
        if cls._instance is None:
            cls._instance = cls(manifest_path)
        return cls._instance

    def _load_curriculum(self, path: str | None = None) -> None:
        if not path:
            here = os.path.dirname(os.path.abspath(__file__))
            candidates = [
                os.path.join(here, "..", "..", "..", "scratch", "curriculum_160.json"),
                os.path.join(here, "..", "..", "scratch", "curriculum_160.json"),
                os.path.join(os.getcwd(), "scratch", "curriculum_160.json"),
            ]
            for c in candidates:
                p = os.path.abspath(c)
                if os.path.exists(p):
                    path = p
                    break

        if not path or not os.path.exists(path):
            log.warning("Curriculum manifest not found at %s. Initializing empty engine.", path)
            return

        with open(path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        sections = {
            "python-foundations": (1, "Python Foundations"),
            "python-core": (2, "Python Core and Data Structures"),
            "computational-thinking": (3, "Problem Solving and Computational Thinking"),
            "arrays-and-strings": (4, "Arrays and Strings"),
            "searching-and-sorting": (5, "Searching and Sorting Algorithms"),
            "hashing-and-hash-tables": (6, "Hashing and Hash Tables"),
            "linked-lists": (7, "Linked Lists"),
            "stacks-and-queues": (8, "Stacks and Queues"),
            "trees-and-bst": (9, "Trees and Binary Search Trees"),
            "heaps-and-priority-queues": (10, "Heaps and Priority Queues"),
            "graphs": (11, "Graphs and Graph Algorithms"),
            "greedy-algorithms": (12, "Greedy Algorithms"),
            "dynamic-programming": (13, "Dynamic Programming"),
            "advanced-dsa": (14, "Advanced DSA and Interview Mastery"),
        }

        for item in raw_data:
            day_num = item["day_number"]
            sec_id = item.get("section_id", "python-foundations")
            sec_num, sec_title = sections.get(sec_id, (1, "General"))

            meta = CurriculumDayMeta(
                day_number=day_num,
                section_id=sec_id,
                section_number=sec_num,
                section_title=sec_title,
                title=item["title"],
                topic_name=item["topic_name"],
                estimated_minutes=item.get("estimated_minutes", 30),
                difficulty=item.get("difficulty", "FOUNDATIONAL"),
                prerequisites=item.get("prerequisites", []),
                flow_tier=item.get("flow_tier", "tier1"),
                archetype=item.get("archetype", "guided"),
                concepts=item.get("concepts", []),
                learning_objectives=item.get("learning_objectives", []),
                description=item.get("description", ""),
            )
            self.days[day_num] = meta

            tokens = set()
            for c in meta.concepts:
                tokens.update(self._tokenize(c))
            tokens.update(self._tokenize(meta.title))
            tokens.update(self._tokenize(meta.topic_name))

            for tok in tokens:
                if tok not in self.inverted_concept_index:
                    self.inverted_concept_index[tok] = set()
                self.inverted_concept_index[tok].add(day_num)

        # Seed key aliases for robust lookup
        self.aliases = {
            "stack": [86, 87, 88, 89, 90, 91, 92, 93],
            "lifo": [86],
            "queue": [89, 90],
            "fifo": [89],
            "recursion": [17, 18, 28, 29, 30],
            "binary search": [51, 52, 53, 54],
            "two pointers": [39, 40, 42, 50],
            "sliding window": [43, 44, 45, 93],
            "prefix sum": [33, 37, 38],
            "hash map": [15, 66, 67, 68],
            "hash table": [66, 67, 68],
            "linked list": [76, 77, 78, 79, 80, 81, 82, 83],
            "lru cache": [73, 83, 160],
            "lru": [83, 160],
            "lfu cache": [74, 160],
            "tree": [96, 97, 98, 99, 100],
            "bst": [101, 102, 103],
            "binary search tree": [101, 102, 103],
            "heap": [111, 112, 113, 114, 115, 116],
            "priority queue": [111, 112, 113],
            "graph": [121, 122, 123, 124, 125, 126],
            "dijkstra": [128],
            "bellman ford": [129],
            "union find": [130, 131],
            "dsu": [130, 131],
            "kruskal": [131],
            "prim": [132],
            "topological sort": [125],
            "dynamic programming": [146, 147, 148, 149, 150, 151, 152, 153, 154, 155],
            "dp": [146, 147, 148, 149, 150, 151, 152, 153, 154, 155],
            "knapsack": [149, 150],
            "coin change": [150],
            "longest increasing subsequence": [151],
            "lis": [151],
            "edit distance": [153],
            "backtracking": [157],
            "n queens": [157],
            "segment tree": [158],
            "bit manipulation": [156],
        }
        for alias, d_list in self.aliases.items():
            for tok in self._tokenize(alias):
                if tok not in self.inverted_concept_index:
                    self.inverted_concept_index[tok] = set()
                self.inverted_concept_index[tok].update(d_list)

    def _tokenize(self, text: str) -> list[str]:
        cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
        tokens = [t.strip() for t in cleaned.split() if len(t.strip()) > 2]
        return tokens

    def _build_concept_relations(self) -> None:
        self.concept_relations = [
            ConceptRelation(
                source_concept="LRU Cache",
                target_concept="Hash Map",
                relation=RelationType.COMPOSED_OF,
                source_day=83,
                target_day=15,
                explanation="Hash map provides O(1) key-to-node pointer lookup for cached keys.",
            ),
            ConceptRelation(
                source_concept="LRU Cache",
                target_concept="Doubly Linked List",
                relation=RelationType.COMPOSED_OF,
                source_day=83,
                target_day=82,
                explanation="Doubly linked list enables O(1) node detachment and moving to most-recent head.",
            ),
            ConceptRelation(
                source_concept="LRU Cache",
                target_concept="LFU Cache",
                relation=RelationType.ALTERNATIVE_TO,
                source_day=83,
                target_day=160,
                explanation="LRU evicts least-recently accessed; LFU evicts lowest frequency of access.",
            ),
            ConceptRelation(
                source_concept="Dijkstra's Algorithm",
                target_concept="Graph Adjacency List",
                relation=RelationType.REQUIRES,
                source_day=128,
                target_day=121,
                explanation="Requires graph adjacency representation to explore neighbor edges in O(degree(u)).",
            ),
            ConceptRelation(
                source_concept="Dijkstra's Algorithm",
                target_concept="Priority Queue (Min-Heap)",
                relation=RelationType.REQUIRES,
                source_day=128,
                target_day=113,
                explanation="Extracts unvisited vertex with minimum tentative distance in logarithmic time.",
            ),
            ConceptRelation(
                source_concept="Dijkstra's Algorithm",
                target_concept="Greedy Choice Property",
                relation=RelationType.REQUIRES,
                source_day=128,
                target_day=136,
                explanation="Guarantees that extracting the minimum distance vertex is permanently optimal (non-negative weights).",
            ),
            ConceptRelation(
                source_concept="Dijkstra's Algorithm",
                target_concept="Breadth-First Search (BFS)",
                relation=RelationType.ALTERNATIVE_TO,
                source_day=128,
                target_day=122,
                explanation="BFS finds shortest path in unweighted graphs in O(V+E) without priority queue overhead.",
            ),
            ConceptRelation(
                source_concept="Recursion",
                target_concept="Call Stack and Stack Frames",
                relation=RelationType.REQUIRES,
                source_day=30,
                target_day=6,
                explanation="Function activation records and local variable scope explain why recursive frames isolate state.",
            ),
            ConceptRelation(
                source_concept="Recursion",
                target_concept="Space Complexity (Auxiliary Memory)",
                relation=RelationType.REQUIRES,
                source_day=30,
                target_day=28,
                explanation="Call stack frame allocation dictates recursive space complexity and prevents stack overflow.",
            ),
            ConceptRelation(
                source_concept="Dynamic Programming",
                target_concept="Recursion",
                relation=RelationType.REQUIRES,
                source_day=146,
                target_day=30,
                explanation="DP solves problems with optimal substructure by caching overlapping subproblem returns.",
            ),
            ConceptRelation(
                source_concept="Dynamic Programming",
                target_concept="Memoization",
                relation=RelationType.REQUIRES,
                source_day=146,
                target_day=146,
                explanation="Memoization stores results of expensive function calls to avoid recomputing identical states.",
            ),
            ConceptRelation(
                source_concept="Trapping Rain Water",
                target_concept="Monotonic Stack",
                relation=RelationType.ALTERNATIVE_TO,
                source_day=50,
                target_day=91,
                explanation="Solved via Two Pointers (O(1) space on Day 50) and Monotonic Stack (O(N) space on Day 91).",
            ),
        ]

    def pack_active_lesson_context(
        self,
        day_number: int,
        step_number: int = 1,
        step_type: str = "explanation",
        step_heading: str | None = None,
        step_takeaway: str | None = None,
        current_code: str | None = None,
    ) -> str:
        day = self.days.get(day_number)
        if not day:
            return f"[Active Day {day_number} Context: Not available]"

        prereq_titles = [
            f"Day {p} ({self.days[p].title})" for p in day.prerequisites if p in self.days
        ]
        prereq_str = ", ".join(prereq_titles) if prereq_titles else "None (Foundational)"
        concepts_str = ", ".join(day.concepts)

        lines = [
            "=== CURRENT LESSON CONTEXT ===",
            f"Day: {day.day_number}/160 | Section {day.section_number}: {day.section_title} | Difficulty: {day.difficulty}",
            f"Topic: {day.title}",
            f"Step: {step_number} [{step_type.upper()}] - {step_heading or day.topic_name}",
        ]
        if step_takeaway:
            lines.append(f"Step Takeaway: {step_takeaway}")
        if current_code and current_code.strip():
            code_preview = current_code.strip()[:500]
            lines.append(f"Active Code Snippet:\n```python\n{code_preview}\n```")

        lines.append(f"Key Concepts: {concepts_str}")
        lines.append(f"Direct Prerequisites: {prereq_str}")

        return "\n".join(lines)

    def search_concept(self, query: str, current_day: int) -> str | None:
        tokens = self._tokenize(query)
        if not tokens:
            return None

        day_scores: dict[int, int] = {}
        for tok in tokens:
            for d in self.inverted_concept_index.get(tok, []):
                day_scores[d] = day_scores.get(d, 0) + 1

        # Check direct alias match to prioritize canonical day
        q_clean = query.lower()
        for alias, d_list in self.aliases.items():
            if alias in q_clean or q_clean in alias:
                canonical_day = d_list[0]
                day_scores[canonical_day] = day_scores.get(canonical_day, 0) + 10

        if not day_scores:
            return None

        # Add section and title boosts
        for d in day_scores:
            meta = self.days[d]
            for tok in tokens:
                if tok in meta.title.lower():
                    day_scores[d] += 4
                if tok in meta.section_title.lower():
                    day_scores[d] += 3

        # Pick best scoring day
        best_day_num = sorted(day_scores.keys(), key=lambda d: (-day_scores[d], abs(d - current_day) == 0, d))[0]
        day = self.days[best_day_num]

        offset = day.day_number - current_day
        if offset > 0:
            status = f"UPCOMING (Day {day.day_number}, {offset} days ahead in Section {day.section_number})"
        elif offset < 0:
            status = f"ALREADY COVERED (Day {day.day_number}, {abs(offset)} days ago in Section {day.section_number})"
        else:
            status = "CURRENT TOPIC TODAY"

        relation_notes = []
        for rel in self.concept_relations:
            if (rel.source_day == current_day and rel.target_day == day.day_number) or \
               (rel.target_day == current_day and rel.source_day == day.day_number):
                relation_notes.append(f"Relationship Note: {rel.explanation}")

        bridge_text = ("\n" + "\n".join(relation_notes)) if relation_notes else ""

        return (
            "=== CROSS-TOPIC CURRICULUM CONTEXT ===\n"
            f"Queried Concept: '{query}' -> Canonical Curriculum Milestone: Day {day.day_number} ({day.title})\n"
            f"Section: Section {day.section_number}: {day.section_title} | Status: {status}\n"
            f"Summary: {day.description}\n"
            f"Key Concepts: {', '.join(day.concepts)}{bridge_text}"
        )

    def traverse_prerequisites(
        self,
        target_day: int,
        completed_days: list[int] | None = None,
        max_depth: int = 2,
    ) -> str:
        if target_day not in self.days:
            return f"Day {target_day} not found in curriculum."

        day = self.days[target_day]
        completed_set = set(completed_days or [])

        visited = set()
        queue = [(p, 1) for p in day.prerequisites]
        direct_prereqs = list(day.prerequisites)
        transitive_prereqs = []

        while queue:
            p_day, depth = queue.pop(0)
            if p_day in visited or p_day not in self.days:
                continue
            visited.add(p_day)
            if depth > 1:
                transitive_prereqs.append(p_day)

            if depth < max_depth:
                for next_p in self.days[p_day].prerequisites:
                    if next_p not in visited:
                        queue.append((next_p, depth + 1))

        lines = [
            "=== PREREQUISITE GRAPH CONTEXT ===",
            f"Target Milestone: Day {day.day_number} ({day.title})",
        ]

        if direct_prereqs:
            lines.append("Direct Prerequisites:")
            for p in direct_prereqs:
                p_meta = self.days[p]
                status = "[DONE]" if p in completed_set else "[NOT COMPLETED]"
                lines.append(f"  - {status} Day {p}: {p_meta.title} (Concepts: {', '.join(p_meta.concepts[:2])})")
        else:
            lines.append("Direct Prerequisites: None (Starting Foundation)")

        if transitive_prereqs:
            lines.append("Foundational Prerequisites:")
            for p in transitive_prereqs[:3]:
                p_meta = self.days[p]
                lines.append(f"  - Day {p}: {p_meta.title}")

        unmet = [p for p in direct_prereqs if p not in completed_set]
        if unmet:
            lines.append(f"Missing Knowledge Foundations: Day(s) {', '.join(str(u) for u in unmet)}")

        return "\n".join(lines)

    def get_prerequisites(self, day_number: int) -> list[str]:
        day = self.days.get(day_number)
        if not day or not day.prerequisites:
            return []
        res = []
        for p in day.prerequisites:
            if p in self.days:
                res.append(f"Day {p}: {self.days[p].title}")
        return res

    def build_teacher_context(
        self,
        current_day: int,
        student_query: str,
        step_number: int = 1,
        step_type: str = "explanation",
        step_heading: str | None = None,
        step_takeaway: str | None = None,
        current_code: str | None = None,
        completed_days: list[int] | None = None,
    ) -> str:
        blocks = []

        # 1. Active lesson context (always included)
        blocks.append(
            self.pack_active_lesson_context(
                day_number=current_day,
                step_number=step_number,
                step_type=step_type,
                step_heading=step_heading,
                step_takeaway=step_takeaway,
                current_code=current_code,
            )
        )

        query_lower = student_query.lower()

        # 2. Prerequisite query check
        if any(w in query_lower for w in ["before", "prerequisite", "prereq", "need to know", "first", "prep"]):
            target_prereq_day = current_day
            if "dynamic programming" in query_lower or "dp" in query_lower:
                target_prereq_day = 146
            elif "recursion" in query_lower:
                target_prereq_day = 30
            elif "graph" in query_lower or "dijkstra" in query_lower:
                target_prereq_day = 128
            elif "tree" in query_lower or "bst" in query_lower:
                target_prereq_day = 101

            blocks.append(self.traverse_prerequisites(target_prereq_day, completed_days))

        # 3. Cross-topic search check
        cross_context = self.search_concept(student_query, current_day)
        if cross_context:
            blocks.append(cross_context)

        return "\n\n".join(blocks)


def get_curriculum_knowledge_engine(manifest_path: str | None = None) -> CurriculumKnowledgeEngine:
    return CurriculumKnowledgeEngine.get_instance(manifest_path)
