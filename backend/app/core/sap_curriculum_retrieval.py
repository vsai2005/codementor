"""Authoritative Knowledge Engine and Directed Acyclic Graph (DAG) for SAP S/4HANA Curriculum.

Operates deterministically on in-memory adjacency structures loaded from sap_curriculum_manifest.json.
Completely isolated from Python curriculum and requires ZERO LLM dependencies for graph operations.
"""

from __future__ import annotations

import json
import logging
from collections import defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class ConceptNode:
    slug: str
    name: str
    category: str
    difficulty: int
    prerequisite_slugs: tuple[str, ...] = field(default_factory=tuple)
    curriculum_days: tuple[int, ...] = field(default_factory=tuple)
    mastery_threshold: float = 80.0
    remediation_capsule_slug: str | None = None


@dataclass(frozen=True)
class RemediationCapsule:
    slug: str
    target_concept_slug: str
    title: str
    deficiency_triggers: tuple[str, ...]
    prerequisite_deficiencies: tuple[str, ...]
    remediation_content_md: str
    recovery_assessment_slug: str


@dataclass(frozen=True)
class DayMilestone:
    day_number: int
    phase_number: int
    slug: str
    title: str
    description: str
    objectives: tuple[str, ...]
    estimated_minutes: int
    tier: int
    env_tier: str
    env_prerequisites: dict[str, Any]
    atomic_concepts: tuple[str, ...]
    prerequisites: tuple[str, ...]
    practice_types: tuple[str, ...]
    assessment_types: tuple[str, ...]


class DAGIntegrityError(RuntimeError):
    """Raised when the SAP Curriculum DAG contains invalid references or cycles."""


class SAPCurriculumKnowledgeEngine:
    """Singleton in-memory Knowledge Graph and traversal engine for SAP S/4HANA."""

    _instance: SAPCurriculumKnowledgeEngine | None = None

    def __init__(self, manifest_path: Path | str | None = None) -> None:
        if manifest_path is None:
            manifest_path = Path(__file__).resolve().parent.parent / "data" / "sap_curriculum_manifest.json"
        self.manifest_path = Path(manifest_path)

        self._days: dict[int, DayMilestone] = {}
        self._days_by_slug: dict[str, DayMilestone] = {}
        self._concepts: dict[str, ConceptNode] = {}
        self._remediation_capsules: dict[str, RemediationCapsule] = {}
        self._concept_to_remediation: dict[str, str] = {}

        # DAG Adjacency Lists:
        # direct_prereqs[C] = { P1, P2 } (P is prerequisite of C; P -> C)
        self._direct_prereqs: dict[str, set[str]] = defaultdict(set)
        # direct_dependents[P] = { C1, C2 } (C depends on P; P -> C)
        self._direct_dependents: dict[str, set[str]] = defaultdict(set)

        # Mappings
        self._concept_to_days: dict[str, set[int]] = defaultdict(set)
        self._day_to_concepts: dict[int, set[str]] = defaultdict(set)

        self._load_manifest()
        self.validate_dag_integrity()

    @classmethod
    def get_instance(cls, manifest_path: Path | str | None = None) -> SAPCurriculumKnowledgeEngine:
        if cls._instance is None:
            cls._instance = cls(manifest_path)
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        cls._instance = None

    def _load_manifest(self) -> None:
        if not self.manifest_path.exists():
            raise FileNotFoundError(f"SAP Curriculum manifest not found at: {self.manifest_path}")

        with open(self.manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 1. Load Remediation Capsules
        for c_data in data.get("remediation_capsules", []):
            cap = RemediationCapsule(
                slug=c_data["slug"],
                target_concept_slug=c_data["target_concept_slug"],
                title=c_data["title"],
                deficiency_triggers=tuple(c_data.get("deficiency_triggers", [])),
                prerequisite_deficiencies=tuple(c_data.get("prerequisite_deficiencies", [])),
                remediation_content_md=c_data.get("remediation_content_md", ""),
                recovery_assessment_slug=c_data.get("recovery_assessment_slug", "")
            )
            self._remediation_capsules[cap.slug] = cap
            self._concept_to_remediation[cap.target_concept_slug] = cap.slug

        # 2. Load Days
        for d in data.get("days", []):
            day = DayMilestone(
                day_number=d["day_number"],
                phase_number=d["phase_number"],
                slug=d["slug"],
                title=d["title"],
                description=d.get("description", ""),
                objectives=tuple(d.get("objectives", [])),
                estimated_minutes=d.get("estimated_minutes", 60),
                tier=d.get("tier", 1),
                env_tier=d.get("env_tier", "browser"),
                env_prerequisites=d.get("env_prerequisites", {}),
                atomic_concepts=tuple(d.get("atomic_concepts", [])),
                prerequisites=tuple(d.get("prerequisites", [])),
                practice_types=tuple(d.get("practice_types", [])),
                assessment_types=tuple(d.get("assessment_types", []))
            )
            self._days[day.day_number] = day
            self._days_by_slug[day.slug] = day

            for c_slug in day.atomic_concepts:
                self._concept_to_days[c_slug].add(day.day_number)
                self._day_to_concepts[day.day_number].add(c_slug)

        # 3. Load Concepts
        for c in data.get("concepts", []):
            slug = c["slug"]
            node = ConceptNode(
                slug=slug,
                name=c["name"],
                category=c.get("category", "General"),
                difficulty=c.get("difficulty", 1),
                curriculum_days=tuple(sorted(self._concept_to_days.get(slug, set()))),
                mastery_threshold=float(c.get("mastery_threshold", 80.0)),
                remediation_capsule_slug=self._concept_to_remediation.get(slug)
            )
            self._concepts[slug] = node

        # 4. Load DAG Prerequisite Edges
        for edge in data.get("prerequisites", []):
            p_slug = edge["prerequisite_slug"]
            t_slug = edge["target_slug"]
            self._direct_prereqs[t_slug].add(p_slug)
            self._direct_dependents[p_slug].add(t_slug)

    # -------------------------------------------------------------------------
    # Retrieval Methods
    # -------------------------------------------------------------------------

    def get_total_days(self) -> int:
        return len(self._days)

    def get_day(self, day_number: int) -> DayMilestone | None:
        return self._days.get(day_number)

    def get_day_by_slug(self, slug: str) -> DayMilestone | None:
        return self._days_by_slug.get(slug)

    def get_all_days(self) -> list[DayMilestone]:
        return [self._days[d] for d in sorted(self._days.keys())]

    def get_concept(self, concept_slug: str) -> ConceptNode | None:
        return self._concepts.get(concept_slug)

    def get_all_concepts(self) -> list[ConceptNode]:
        return list(self._concepts.values())

    def get_direct_prerequisites(self, concept_slug: str) -> list[str]:
        return sorted(self._direct_prereqs.get(concept_slug, set()))

    def get_direct_dependents(self, concept_slug: str) -> list[str]:
        return sorted(self._direct_dependents.get(concept_slug, set()))

    def get_days_for_concept(self, concept_slug: str) -> list[int]:
        return sorted(self._concept_to_days.get(concept_slug, set()))

    def get_concepts_for_day(self, day_number: int) -> list[str]:
        return sorted(self._day_to_concepts.get(day_number, set()))

    def get_remediation_capsule(self, concept_slug: str) -> RemediationCapsule | None:
        capsule_slug = self._concept_to_remediation.get(concept_slug)
        if capsule_slug:
            return self._remediation_capsules.get(capsule_slug)

        # 1. Alias / semantic mappings for tightly coupled concept clusters
        concept_aliases = {
            "s4hana-value-drivers": "remediation-sap-portfolio",
            "real-time-enterprise": "remediation-sap-portfolio",
            "ecc-simplification-items": "remediation-acdoca",
            "compatibility-views-concept": "remediation-acdoca",
            "universal-journal-concept": "remediation-acdoca",
            "fi-co-unification": "remediation-acdoca",
            "acdoca-table-architecture": "remediation-acdoca",
            "parallel-ledgers": "remediation-acdoca",
            "multi-currency-accounting": "remediation-acdoca",
            "in-memory-computing": "remediation-three-tier",
            "columnar-database-engine": "remediation-three-tier",
            "matdoc-table-architecture": "remediation-matdoc",
            "simplified-inventory-valuation": "remediation-matdoc",
            "business-partner-cvi": "remediation-master-data",
            "customer-vendor-synchronization": "remediation-master-data",
            "cds-fundamentals": "remediation-cds",
            "view-entity-syntax": "remediation-cds",
            "code-pushdown-philosophy": "remediation-cds",
            "transport-management-cts": "remediation-three-tier",
            "system-landscapes-3tier": "remediation-three-tier",
            "cloud-implementation-landscapes": "remediation-sap-portfolio",
            "identity-access-management": "remediation-three-tier",
            "pfcg-authorizations": "remediation-three-tier",
            "fiori-role-assignment": "remediation-three-tier",
            "embedded-analytics-foundations": "remediation-cds",
            "operational-reporting-vdm": "remediation-cds",
            "document-flow-continuity": "remediation-module-interconnectivity",
            "transactional-audit-trail": "remediation-module-interconnectivity",
            "s4hana-integrated-scenario": "remediation-module-interconnectivity",
            "s4hana-architecture-synthesis": "remediation-sap-portfolio",
            # Phase 3: P2P concepts
            "p2p-pr-creation": "remediation-module-interconnectivity",
            "account-assignment-categories": "remediation-module-interconnectivity",
            "flexible-workflow": "remediation-three-tier",
            "p2p-sourcing-rfq": "remediation-master-data",
            "source-determination": "remediation-master-data",
            "p2p-po-processing": "remediation-module-interconnectivity",
            "partner-determination": "remediation-master-data",
            "p2p-goods-receipt-migo": "remediation-matdoc",
            "gr-ir-clearing-account": "remediation-acdoca",
            "p2p-invoice-verification-miro": "remediation-acdoca",
            "three-way-matching": "remediation-module-interconnectivity",
            "payment-block-exceptions": "remediation-acdoca",
            "p2p-f110-payment-run": "remediation-acdoca",
            # Phase 3: O2C concepts
            "o2c-sales-order-creation": "remediation-module-interconnectivity",
            "condition-technique": "remediation-module-interconnectivity",
            "o2c-pricing-procedure": "remediation-module-interconnectivity",
            "advanced-atp-s4": "remediation-matdoc",
            "product-allocation": "remediation-matdoc",
            "backorder-processing": "remediation-matdoc",
            "o2c-outbound-delivery": "remediation-module-interconnectivity",
            "shipping-point-determination": "remediation-org-structure",
            "o2c-post-goods-issue": "remediation-matdoc",
            "cogs-accounting-split": "remediation-acdoca",
            "o2c-billing-creation": "remediation-acdoca",
            "revenue-recognition-posting": "remediation-acdoca",
            "o2c-customer-incoming-payment": "remediation-acdoca",
            "dunning-procedures": "remediation-acdoca",
            "credit-management": "remediation-module-interconnectivity",
            "o2c-returns-processing": "remediation-matdoc",
            "credit-memo-requests": "remediation-acdoca",
            # Phase 3: Finance, Inventory & Manufacturing concepts
            "gl-journal-entry": "remediation-acdoca",
            "posting-keys": "remediation-acdoca",
            "field-status-groups": "remediation-acdoca",
            "ap-ar-subledger-operations": "remediation-acdoca",
            "special-gl-indicators": "remediation-acdoca",
            "period-end-closing": "remediation-acdoca",
            "foreign-currency-valuation": "remediation-acdoca",
            "asset-depreciation-afab": "remediation-acdoca",
            "component-backflushing": "remediation-matdoc",
            "mfg-bom-master": "remediation-master-data",
            "mfg-work-centers-routing": "remediation-master-data",
            "production-order-lifecycle": "remediation-module-interconnectivity",
            "capacity-requirements-planning": "remediation-module-interconnectivity",
            "production-order-confirmation": "remediation-matdoc",
            "production-order-settlement": "remediation-acdoca",
            "wip-variance-calculation": "remediation-acdoca",
            "e2e-process-integration-synthesis": "remediation-module-interconnectivity",
        }
        if concept_slug in concept_aliases:
            cap_slug = concept_aliases[concept_slug]
            if cap_slug in self._remediation_capsules:
                return self._remediation_capsules[cap_slug]

        # 2. Graph neighbor fallback: check direct prerequisites and dependents
        for prereq in self.get_direct_prerequisites(concept_slug):
            if prereq in self._concept_to_remediation:
                return self._remediation_capsules.get(self._concept_to_remediation[prereq])
        for dep in self.get_direct_dependents(concept_slug):
            if dep in self._concept_to_remediation:
                return self._remediation_capsules.get(self._concept_to_remediation[dep])

        return None

    def search_concepts(self, query: str, limit: int = 10) -> list[ConceptNode]:
        q = query.lower().strip()
        if not q:
            return []
        matches: list[tuple[float, ConceptNode]] = []
        for c in self._concepts.values():
            score = 0.0
            slug_lower = c.slug.lower()
            name_lower = c.name.lower()
            cat_lower = c.category.lower()

            if q == slug_lower or q == name_lower:
                score += 10.0
            elif q in slug_lower:
                score += 5.0
            elif q in name_lower:
                score += 3.0
            elif q in cat_lower:
                score += 1.0

            if score > 0:
                matches.append((score, c))

        matches.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in matches[:limit]]

    # -------------------------------------------------------------------------
    # Deterministic DAG Traversal
    # -------------------------------------------------------------------------

    def traverse_prerequisites(self, target_concept_slug: str) -> list[str]:
        """Returns all transitive ancestors (prerequisites) in topologically sorted order."""
        if target_concept_slug not in self._concepts:
            raise KeyError(f"Concept '{target_concept_slug}' not found in SAP knowledge graph.")

        visited: set[str] = set()
        ancestors: set[str] = set()
        queue: deque[str] = deque([target_concept_slug])

        while queue:
            curr = queue.popleft()
            for p in self._direct_prereqs.get(curr, set()):
                if p not in ancestors:
                    ancestors.add(p)
                    queue.append(p)

        # Topologically sort ancestors
        subgraph_nodes = ancestors
        in_degree = {u: 0 for u in subgraph_nodes}
        for u in subgraph_nodes:
            for p in self._direct_prereqs.get(u, set()):
                if p in subgraph_nodes:
                    in_degree[u] += 1

        ready = deque(sorted([u for u, d in in_degree.items() if d == 0]))
        topo_order: list[str] = []

        while ready:
            u = ready.popleft()
            topo_order.append(u)
            for dep in self._direct_dependents.get(u, set()):
                if dep in subgraph_nodes:
                    in_degree[dep] -= 1
                    if in_degree[dep] == 0:
                        ready.append(dep)

        return topo_order

    def get_root_prerequisites(self, concept_slug: str) -> list[str]:
        """Finds foundational/root prerequisite concepts (in-degree == 0 in prerequisite graph)."""
        all_prereqs = self.traverse_prerequisites(concept_slug)
        roots: list[str] = []
        for p in all_prereqs:
            if len(self._direct_prereqs.get(p, set())) == 0:
                roots.append(p)
        return sorted(roots)

    def traverse_dependents(self, concept_slug: str) -> list[str]:
        """Returns all downstream dependent concepts reachable from this concept."""
        if concept_slug not in self._concepts:
            raise KeyError(f"Concept '{concept_slug}' not found in SAP knowledge graph.")

        dependents: set[str] = set()
        queue: deque[str] = deque([concept_slug])

        while queue:
            curr = queue.popleft()
            for dep in self._direct_dependents.get(curr, set()):
                if dep not in dependents:
                    dependents.add(dep)
                    queue.append(dep)

        return sorted(dependents)

    def analyze_learner_gaps(self, failed_concept_slug: str, mastered_concepts: set[str]) -> dict[str, Any]:
        """Identifies root and direct prerequisite knowledge gaps for a learner who failed an assessment."""
        prereqs = self.traverse_prerequisites(failed_concept_slug)
        unmastered = [p for p in prereqs if p not in mastered_concepts]
        direct_unmastered = [p for p in self.get_direct_prerequisites(failed_concept_slug) if p not in mastered_concepts]
        root_unmastered = [p for p in self.get_root_prerequisites(failed_concept_slug) if p not in mastered_concepts]

        capsule = self.get_remediation_capsule(failed_concept_slug)

        return {
            "failed_concept": failed_concept_slug,
            "total_prerequisites_count": len(prereqs),
            "unmastered_prerequisites": unmastered,
            "direct_unmastered": direct_unmastered,
            "root_unmastered": root_unmastered,
            "remediation_capsule": {
                "slug": capsule.slug,
                "title": capsule.title,
                "recovery_assessment_slug": capsule.recovery_assessment_slug,
                "prerequisite_deficiencies": list(capsule.prerequisite_deficiencies)
            } if capsule else None
        }

    # -------------------------------------------------------------------------
    # DAG Integrity Validation
    # -------------------------------------------------------------------------

    def validate_dag_integrity(self) -> None:
        """Strict validation of curriculum day completeness, concept references, and cycle freedom."""
        # 1. Exactly 100 days
        day_nums = sorted(self._days.keys())
        if len(day_nums) != 100 or day_nums != list(range(1, 101)):
            raise DAGIntegrityError(f"Curriculum must have exactly days 1..100. Found {len(day_nums)} days: {day_nums[:5]}...{day_nums[-5:]}")

        # 2. Concept reference validation in days
        for day in self._days.values():
            for c_slug in day.atomic_concepts:
                if c_slug not in self._concepts:
                    raise DAGIntegrityError(f"Day {day.day_number} references non-existent concept '{c_slug}'")

        # 3. Concept reference validation in prerequisites
        for target, prereqs in self._direct_prereqs.items():
            if target not in self._concepts:
                raise DAGIntegrityError(f"Prerequisite target '{target}' does not exist in concepts catalog.")
            for p in prereqs:
                if p not in self._concepts:
                    raise DAGIntegrityError(f"Prerequisite '{p}' for target '{target}' does not exist in concepts catalog.")
                if p == target:
                    raise DAGIntegrityError(f"Self-loop detected on concept '{p}'")

        # 4. Cycle Detection via 3-color DFS (WHITE=0, GREY=1, BLACK=2)
        WHITE, GREY, BLACK = 0, 1, 2
        color = {c: WHITE for c in self._concepts}

        def dfs(node: str, path: list[str]) -> None:
            color[node] = GREY
            path.append(node)
            for neighbor in self._direct_dependents.get(node, set()):
                if color[neighbor] == GREY:
                    cycle_path = " -> ".join(path[path.index(neighbor):] + [neighbor])
                    raise DAGIntegrityError(f"Cycle detected in SAP Curriculum DAG: {cycle_path}")
                if color[neighbor] == WHITE:
                    dfs(neighbor, path)
            path.pop()
            color[node] = BLACK

        for c_slug in self._concepts:
            if color[c_slug] == WHITE:
                dfs(c_slug, [])

        log.info(f"SAP Curriculum DAG integrity verified: 100 days, {len(self._concepts)} concepts, {sum(len(v) for v in self._direct_prereqs.values())} edges. Zero cycles.")
