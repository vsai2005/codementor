"""SAP Curriculum and DAG Endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.core.sap_curriculum_retrieval import SAPCurriculumKnowledgeEngine
from app.sap.schemas.api import (
    SAPConceptDetail,
    SAPDayDetail,
    SAPDaySummary,
    SAPPhaseSummary,
    SAPRemediationCapsuleDetail,
)

router = APIRouter()


@router.get("", response_model=dict)
def get_curriculum_overview() -> dict:
    engine = SAPCurriculumKnowledgeEngine.get_instance()
    days = engine.get_all_days()

    # Load phases from manifest
    with open(engine.manifest_path, "r", encoding="utf-8") as f:
        import json
        manifest = json.load(f)

    return {
        "course": manifest.get("course"),
        "phases": [SAPPhaseSummary(**p).model_dump() for p in manifest.get("phases", [])],
        "total_days": len(days),
        "days": [
            SAPDaySummary(
                day_number=d.day_number,
                phase_number=d.phase_number,
                slug=d.slug,
                title=d.title,
                description=d.description,
                tier=d.tier,
                env_tier=d.env_tier,
                estimated_minutes=d.estimated_minutes,
                atomic_concepts=list(d.atomic_concepts),
                practice_types=list(d.practice_types),
                assessment_types=list(d.assessment_types),
            ).model_dump()
            for d in days
        ],
    }


@router.get("/days/{day_number}", response_model=SAPDayDetail)
def get_day_detail(day_number: int) -> SAPDayDetail:
    engine = SAPCurriculumKnowledgeEngine.get_instance()
    day = engine.get_day(day_number)
    if not day:
        raise HTTPException(status_code=404, detail=f"SAP Day {day_number} not found.")

    return SAPDayDetail(
        day_number=day.day_number,
        phase_number=day.phase_number,
        slug=day.slug,
        title=day.title,
        description=day.description,
        tier=day.tier,
        env_tier=day.env_tier,
        estimated_minutes=day.estimated_minutes,
        objectives=list(day.objectives),
        env_prerequisites=day.env_prerequisites,
        atomic_concepts=list(day.atomic_concepts),
        prerequisites=list(day.prerequisites),
        practice_types=list(day.practice_types),
        assessment_types=list(day.assessment_types),
    )


@router.get("/concepts/{concept_slug}", response_model=SAPConceptDetail)
def get_concept_detail(concept_slug: str) -> SAPConceptDetail:
    engine = SAPCurriculumKnowledgeEngine.get_instance()
    concept = engine.get_concept(concept_slug)
    if not concept:
        raise HTTPException(status_code=404, detail=f"Concept '{concept_slug}' not found.")

    direct_prereqs = engine.get_direct_prerequisites(concept_slug)
    all_ancestors = engine.traverse_prerequisites(concept_slug)
    roots = engine.get_root_prerequisites(concept_slug)
    dependents = engine.traverse_dependents(concept_slug)
    capsule = engine.get_remediation_capsule(concept_slug)

    return SAPConceptDetail(
        slug=concept.slug,
        name=concept.name,
        category=concept.category,
        difficulty=concept.difficulty,
        curriculum_days=list(concept.curriculum_days),
        direct_prerequisites=direct_prereqs,
        all_ancestor_prerequisites=all_ancestors,
        root_prerequisites=roots,
        dependents=dependents,
        mastery_threshold=concept.mastery_threshold,
        remediation_available=capsule is not None,
        remediation_capsule_slug=capsule.slug if capsule else None,
    )


@router.get("/dag/prerequisites/{concept_slug}", response_model=list[str])
def get_topological_prerequisites(concept_slug: str) -> list[str]:
    engine = SAPCurriculumKnowledgeEngine.get_instance()
    try:
        return engine.traverse_prerequisites(concept_slug)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Concept '{concept_slug}' not found.")


@router.get("/dag/remediation/{concept_slug}", response_model=SAPRemediationCapsuleDetail)
def get_remediation_capsule(concept_slug: str) -> SAPRemediationCapsuleDetail:
    engine = SAPCurriculumKnowledgeEngine.get_instance()
    capsule = engine.get_remediation_capsule(concept_slug)
    if not capsule:
        raise HTTPException(status_code=404, detail=f"No remediation capsule defined for concept '{concept_slug}'.")

    return SAPRemediationCapsuleDetail(
        slug=capsule.slug,
        target_concept_slug=capsule.target_concept_slug,
        title=capsule.title,
        deficiency_triggers=list(capsule.deficiency_triggers),
        prerequisite_deficiencies=list(capsule.prerequisite_deficiencies),
        remediation_content_md=capsule.remediation_content_md,
        recovery_assessment_slug=capsule.recovery_assessment_slug,
    )


@router.get("/search", response_model=list[dict])
def search_concepts(q: str = Query(..., min_length=1)) -> list[dict]:
    engine = SAPCurriculumKnowledgeEngine.get_instance()
    matches = engine.search_concepts(q)
    return [
        {
            "slug": c.slug,
            "name": c.name,
            "category": c.category,
            "difficulty": c.difficulty,
            "curriculum_days": list(c.curriculum_days),
        }
        for c in matches
    ]
