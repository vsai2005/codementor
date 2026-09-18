"""SAP Multi-Modal Assessment Evaluation Service."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.sap_curriculum_retrieval import SAPCurriculumKnowledgeEngine
from app.models.sap_models import (
    SAPAssessment,
    SAPAssessmentAttempt,
    SAPAssessmentAttemptType,
    SAPDayStatus,
    SAPUserDayState,
    SAPUserState,
)
from app.sap.services.mastery import SAPMasteryService


class SAPAssessmentService:
    @classmethod
    def evaluate(
        cls,
        db: Session,
        user_id: uuid.UUID,
        day_number: int,
        assessment_id: str,
        assessment_type: str,
        rubric_spec: dict[str, Any] | None = None,
        submission_payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Evaluates an assessment attempt strictly from server-side definitions."""
        from app.data.sap_lessons import SAP_DAYS_CONTENT

        # 1. Authoritative lesson content lookup
        day_data = SAP_DAYS_CONTENT.get(day_number)
        if not day_data:
            raise ValueError(f"SAP Day {day_number} content definition not found.")

        assessment_step = None
        for step in day_data.get("steps", []):
            if step.get("step_type") == "assessment":
                assessment_step = step
                break

        if not assessment_step:
            raise ValueError(f"No assessment defined for SAP Day {day_number}.")

        # 2. Validate assessment type against supported curriculum types
        allowed_types = {
            "mcq",
            "capstone_multi_concept",
            "scenario_decision",
            "process_ordering",
            "rubric_based",
            "simulation",
            "troubleshooting",
            "abap_challenge",
            "cds_challenge",
            "rap_challenge",
        }
        if assessment_type not in allowed_types:
            raise ValueError(f"Unsupported assessment type: '{assessment_type}'.")

        # 3. Validate submission payload
        if not submission_payload or not isinstance(submission_payload, dict):
            raise ValueError("Malformed assessment payload: submission must be a valid non-empty JSON object.")

        # 4. Authoritative questions and evaluation
        # Authoritative questions come strictly from server-side definitions, never from client rubric_spec
        server_questions = assessment_step.get("questions", [])
        server_concept_slug = assessment_step.get("concept_slug") or (day_data.get("atomic_concepts") or [f"sap-day-{day_number}"])[0]
        pass_score = float(assessment_step.get("pass_score", 70.0))

        concept_results: dict[str, float] = {}

        if server_questions:
            answers = submission_payload.get("answers")
            if not isinstance(answers, dict):
                answers = {k: v for k, v in submission_payload.items() if k not in ("duration_seconds", "selected_option_ids")}

            if not answers:
                raise ValueError("Malformed assessment payload: answers dictionary is required.")

            if not any(v is not None and str(v).strip() != "" for v in answers.values()):
                raise ValueError("Malformed assessment payload: answers cannot be empty.")

            correct_count = 0
            concept_totals: dict[str, dict[str, int]] = {}

            for q in server_questions:
                qid = q.get("id") or q.get("question_id")
                c_slug = q.get("concept_slug") or server_concept_slug
                correct_opt = next((o["id"] for o in q.get("options", []) if o.get("is_correct")), None)
                user_ans = answers.get(qid)
                # Also check case-insensitive match on ID
                if user_ans is None and qid:
                    for k, v in answers.items():
                        if str(k).lower() == str(qid).lower():
                            user_ans = v
                            break

                is_corr = bool(
                    user_ans is not None
                    and correct_opt is not None
                    and str(user_ans).strip().lower() == str(correct_opt).strip().lower()
                )
                if is_corr:
                    correct_count += 1

                if c_slug:
                    if c_slug not in concept_totals:
                        concept_totals[c_slug] = {"correct": 0, "total": 0}
                    concept_totals[c_slug]["total"] += 1
                    if is_corr:
                        concept_totals[c_slug]["correct"] += 1

            score = round((correct_count / max(1, len(server_questions))) * 100.0, 1)
            feedback = "All assessment questions verified successfully!" if score >= 80.0 else f"Scored {score}%. Review the concepts requiring remediation below."
            breakdown = {"correct": correct_count, "total": len(server_questions)}

            for c_slug, counts in concept_totals.items():
                concept_results[c_slug] = round((counts["correct"] / max(1, counts["total"])) * 100.0, 1)

        elif assessment_type == "mcq":
            server_spec = assessment_step.get("spec") or assessment_step
            score, feedback, breakdown = cls._eval_mcq(server_spec, submission_payload)
        elif assessment_type == "process_ordering":
            server_spec = assessment_step.get("spec") or assessment_step
            score, feedback, breakdown = cls._eval_ordering(server_spec, submission_payload)
        elif assessment_type == "scenario_decision":
            server_spec = assessment_step.get("spec") or assessment_step
            score, feedback, breakdown = cls._eval_scenario(server_spec, submission_payload)
        elif assessment_type == "rubric_based":
            server_spec = assessment_step.get("spec") or assessment_step
            score, feedback, breakdown = cls._eval_rubric(server_spec, submission_payload)
        else:
            raise ValueError(f"No evaluation handler for assessment type '{assessment_type}' without questions definition.")

        passed = score >= pass_score

        # Lookup or create assessment entity from server definitions
        assessment = db.execute(
            select(SAPAssessment).where(SAPAssessment.slug == assessment_id)
        ).scalar_one_or_none()

        if assessment is None:
            assessment = SAPAssessment(
                slug=assessment_id,
                day_number=day_number,
                title=assessment_step.get("title", f"Assessment Day {day_number}"),
                assessment_type=assessment_type,
                prompt_md=assessment_step.get("instruction", "Assessment Task"),
                scoring_criteria={"questions_count": len(server_questions), "pass_score": pass_score},
                pass_score=int(pass_score),
            )
            db.add(assessment)
            db.flush()

        now = datetime.now(timezone.utc)

        # 3. Record attempt
        attempt = SAPAssessmentAttempt(
            user_id=user_id,
            assessment_id=assessment.id,
            attempt_type=SAPAssessmentAttemptType.DAILY_CHECK.value,
            response=submission_payload,
            evaluation=breakdown,
            score=score,
            passed=passed,
            duration_seconds=submission_payload.get("duration_seconds"),
            created_at=now,
        )
        db.add(attempt)

        # 4. Multi-concept evaluations, Skill Evidence, and Remediation Capsules
        engine = SAPCurriculumKnowledgeEngine.get_instance()
        concept_evaluations: list[dict[str, Any]] = []
        remediation_capsules_triggered: list[dict[str, Any]] = []

        # If no per-question concepts, use the root concept_slug from server definition
        if not concept_results and assessment_step.get("concept_slug"):
            concept_results[assessment_step["concept_slug"]] = score

        is_capstone = bool(assessment_step.get("is_capstone") or assessment_type == "capstone_multi_concept")

        for c_slug, c_score in concept_results.items():
            c_passed = c_score >= pass_score

            # Record Skill Evidence & update Concept Mastery
            SAPMasteryService.record_skill_evidence(
                db=db,
                user_id=user_id,
                concept_slug=c_slug,
                evidence={
                    "score": c_score,
                    "source_type": "capstone_assessment" if is_capstone else "guided_assessment",
                    "source_id": str(assessment.id),
                    "mode": "GUIDED",
                    "assistance_level": "TRAINING",
                    "difficulty": int(assessment_step.get("difficulty", 1)),
                    "result": "passed" if c_passed else "failed",
                    "evidence_summary": f"Day {day_number} Assessment ({c_slug}): {'PASSED' if c_passed else 'NEEDS REMEDIATION'}",
                    "details": {"score": c_score, "assessment_slug": assessment_id},
                },
            )

            capsule_info = None
            if not c_passed:
                cap = engine.get_remediation_capsule(c_slug)
                if cap:
                    capsule_info = {
                        "slug": cap.slug,
                        "target_concept_slug": cap.target_concept_slug,
                        "title": cap.title,
                        "deficiency_triggers": list(cap.deficiency_triggers),
                        "prerequisite_deficiencies": list(cap.prerequisite_deficiencies),
                        "remediation_content_md": cap.remediation_content_md,
                        "recovery_assessment_slug": cap.recovery_assessment_slug,
                    }
                    remediation_capsules_triggered.append(capsule_info)

            concept_evaluations.append({
                "concept_slug": c_slug,
                "score": c_score,
                "passed": c_passed,
                "remediation_capsule": capsule_info,
            })

        remediation_required = len(remediation_capsules_triggered) > 0
        primary_remediation = remediation_capsules_triggered[0] if remediation_capsules_triggered else None

        day_completed = False
        unlocked_next_day = False
        current_day = day_number
        next_day_number = min(100, day_number + 1) if day_number < 100 else None

        # 5. If passed, update day state & macro user state
        if passed:
            day_state = db.execute(
                select(SAPUserDayState).where(
                    SAPUserDayState.user_id == user_id,
                    SAPUserDayState.day_number == day_number,
                )
            ).scalar_one_or_none()

            if day_state is None:
                day_state = SAPUserDayState(
                    user_id=user_id,
                    day_number=day_number,
                    status=SAPDayStatus.IN_PROGRESS.value,
                    assessment_passed=True,
                    assessment_passed_at=now,
                )
                db.add(day_state)
            else:
                day_state.assessment_passed = True
                day_state.assessment_passed_at = now

            was_already_completed = bool(day_state.completed)
            can_complete_day = bool(
                day_state.lesson_completed
                and day_state.practice_completed
                and passed
                and day_state.status != SAPDayStatus.WAIVED_BY_PLACEMENT.value
            )

            if can_complete_day and not was_already_completed:
                day_state.completed = True
                day_state.completed_at = now
                day_state.status = SAPDayStatus.COMPLETED.value
                day_completed = True
            elif not day_state.completed and day_state.status != SAPDayStatus.WAIVED_BY_PLACEMENT.value:
                day_state.status = SAPDayStatus.IN_PROGRESS.value

            if day_state.completed:
                day_completed = True
                user_state = db.execute(
                    select(SAPUserState).where(SAPUserState.user_id == user_id)
                ).scalar_one_or_none()
                if user_state is None:
                    user_state = SAPUserState(
                        user_id=user_id,
                        current_recommended_day=min(100, day_number + 1 if can_complete_day else day_number),
                        completed_days_count=1 if can_complete_day else 0,
                        last_active_at=now,
                    )
                    db.add(user_state)
                    unlocked_next_day = can_complete_day and (day_number < 100)
                    current_day = user_state.current_recommended_day
                else:
                    user_state.last_active_at = now
                    # Only advance if newly completed and on current recommended day
                    if can_complete_day and not was_already_completed and day_number == user_state.current_recommended_day:
                        user_state.current_recommended_day = min(100, day_number + 1)
                        user_state.completed_days_count += 1
                        unlocked_next_day = day_number < 100
                    current_day = user_state.current_recommended_day
            else:
                user_state = db.execute(
                    select(SAPUserState).where(SAPUserState.user_id == user_id)
                ).scalar_one_or_none()
                if user_state:
                    user_state.last_active_at = now
                    current_day = user_state.current_recommended_day

        db.commit()

        return {
            "submission_id": str(attempt.id),
            "passed": passed,
            "score": score,
            "feedback": feedback,
            "evaluation_breakdown": breakdown,
            "mastery_updated": len(concept_results) > 0,
            "concept_evaluations": concept_evaluations,
            "remediation_required": remediation_required,
            "remediation_capsule": primary_remediation,
            "all_remediations": remediation_capsules_triggered,
            "day_completed": day_completed,
            "unlocked_next_day": unlocked_next_day,
            "current_day": current_day,
            "next_day_number": next_day_number,
        }

    @staticmethod
    def _eval_mcq(spec: dict, payload: dict) -> tuple[float, str, dict]:
        selected = set(payload.get("selected_option_ids", []))
        correct = set(spec.get("correct_option_ids", []))

        if not correct:
            return 100.0, "Passed.", {"matches": True}

        if selected == correct:
            return 100.0, "Correct! Exceptional understanding of S/4HANA principles.", {"accuracy": 1.0}

        true_positives = len(selected & correct)
        false_positives = len(selected - correct)
        raw_score = max(0.0, (true_positives - (0.5 * false_positives)) / max(len(correct), 1)) * 100.0
        feedback = spec.get("explanations", {}).get(next(iter(selected - correct), ""), "Incorrect selection. Review the relevant architecture guidelines.")

        return round(raw_score, 1), feedback, {"accuracy": raw_score / 100.0}

    @staticmethod
    def _eval_ordering(spec: dict, payload: dict) -> tuple[float, str, dict]:
        submitted = payload.get("ordered_ids", [])
        target = spec.get("target_ordered_ids", [])

        if not target:
            return 100.0, "Ordered.", {"match_ratio": 1.0}

        if submitted == target:
            return 100.0, "Process sequence perfectly ordered!", {"match_ratio": 1.0}

        matches = sum(1 for i, item in enumerate(submitted) if i < len(target) and item == target[i])
        score = round((matches / max(len(target), 1)) * 100.0, 1)
        return score, "One or more process steps are out of sequence.", {"matched_positions": matches, "total_positions": len(target)}

    @staticmethod
    def _eval_scenario(spec: dict, payload: dict) -> tuple[float, str, dict]:
        chosen_id = payload.get("decision_id")
        decisions = spec.get("decisions", {})

        outcome = decisions.get(chosen_id, {})
        score = float(outcome.get("score", 0.0))
        feedback = outcome.get("rationale", "Decision evaluated against enterprise guidelines.")
        return score, feedback, outcome.get("impact_metrics", {})

    @staticmethod
    def _eval_rubric(spec: dict, payload: dict) -> tuple[float, str, dict]:
        criteria = spec.get("criteria", [])
        ratings = payload.get("ratings", {})

        total_score = 0.0
        breakdown = {}
        for c in criteria:
            name = c["name"]
            weight = c.get("weight", 1.0)
            max_p = c.get("max_points", 10.0)
            achieved = min(float(ratings.get(name, 0.0)), max_p)
            norm = (achieved / max_p) * 100.0
            total_score += norm * weight
            breakdown[name] = {"achieved": achieved, "weighted": norm * weight}

        total_weight = sum(c.get("weight", 1.0) for c in criteria) or 1.0
        final_score = round(total_score / total_weight, 1)
        return final_score, "Rubric evaluation completed.", breakdown
