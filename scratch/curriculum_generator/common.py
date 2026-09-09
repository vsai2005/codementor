import json
import os

with open("scratch/curriculum_160.json", "r", encoding="utf-8") as f:
    CURRICULUM_DATA = json.load(f)

CURRICULUM_MAP = {d["day_number"]: d for d in CURRICULUM_DATA}

def get_difficulty(day: int) -> str:
    if day <= 10:
        return "BEGINNER"
    elif day <= 25:
        return "FOUNDATIONAL"
    elif day <= 65:
        return "DEVELOPING"
    elif day <= 110:
        return "INTERMEDIATE"
    elif day <= 145:
        return "ADVANCED"
    else:
        return "EXPERT"

def get_next_preview(day: int):
    next_day = CURRICULUM_MAP.get(day + 1)
    if next_day:
        return {
            "dayNumber": day + 1,
            "title": next_day["title"],
            "description": next_day["description"],
        }
    return {
        "dayNumber": day,
        "title": "Curriculum Completion",
        "description": "Congratulations! You have completed the complete 160-day Python to DSA curriculum.",
    }

def make_explanation_step(
    step_id: str,
    step_num: int,
    title: str,
    short_label: str,
    heading: str,
    subheading: str,
    paragraphs: list,
    snippets: list = None,
    callouts: list = None,
    takeaway: str = ""
) -> dict:
    step = {
        "id": step_id,
        "stepNumber": step_num,
        "title": title,
        "shortLabel": short_label,
        "type": "explanation",
        "isGated": False,
        "heading": heading,
        "subheading": subheading,
        "markdownContent": paragraphs,
        "snippets": snippets or [],
        "callouts": callouts or [],
    }
    if takeaway:
        step["keyTakeaway"] = takeaway
    return step

def make_checkpoint_step(
    step_id: str,
    step_num: int,
    title: str,
    short_label: str,
    heading: str,
    subheading: str,
    checkpoints: list,
    takeaway: str = ""
) -> dict:
    step = {
        "id": step_id,
        "stepNumber": step_num,
        "title": title,
        "shortLabel": short_label,
        "type": "checkpoint",
        "isGated": True,
        "heading": heading,
        "subheading": subheading,
        "checkpoints": checkpoints,
    }
    if takeaway:
        step["keyTakeaway"] = takeaway
    return step

def make_practice_step(
    step_id: str,
    step_num: int,
    title: str,
    short_label: str,
    heading: str,
    subheading: str,
    task_title: str,
    instructions: list,
    starter_code: str,
    solution_code: str,
    expected_patterns: list,
    hint: str,
    takeaway: str = ""
) -> dict:
    step = {
        "id": step_id,
        "stepNumber": step_num,
        "title": title,
        "shortLabel": short_label,
        "type": "practice",
        "isGated": True,
        "heading": heading,
        "subheading": subheading,
        "task": {
            "title": task_title,
            "instructions": instructions,
            "starterCode": starter_code,
            "solutionCode": solution_code,
            "expectedOutputPatterns": expected_patterns,
            "hint": hint,
        }
    }
    if takeaway:
        step["keyTakeaway"] = takeaway
    return step

def make_completion_step(
    step_id: str,
    step_num: int,
    title: str,
    short_label: str,
    day_num: int,
    heading: str,
    subheading: str,
    recap_rows: list,
    solidified_concepts: list,
    next_preview: dict
) -> dict:
    return {
        "id": step_id,
        "stepNumber": step_num,
        "title": title,
        "shortLabel": short_label,
        "type": "completion",
        "isGated": False,
        "dayNumber": day_num,
        "heading": heading,
        "subheading": subheading,
        "recapRows": recap_rows,
        "solidifiedConcepts": solidified_concepts,
        "nextDayPreview": next_preview,
    }
