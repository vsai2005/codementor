"""
Master Curriculum Batch Generator
Compiles all 14 sections (Days 1 to 160) into 8 code-split TypeScript packages:
frontend/lib/lessons/batches/batch1.ts through batch8.ts
"""

import json
import os
import sys

from scratch.curriculum_generator.common import (
    CURRICULUM_MAP,
    get_next_preview,
    make_explanation_step,
    make_checkpoint_step,
    make_practice_step,
    make_completion_step,
)

# Batch 1 imports
from scratch.curriculum_generator.sec1_foundations import get_sec1_days
from scratch.curriculum_generator.sec2_core_part1 import get_sec2_days
from scratch.curriculum_generator.sec2_core_part2 import get_sec2_part2_days

# Batch 2 imports
from scratch.curriculum_generator.gen_batch2_part1 import get_batch2_days as get_b2_p1
from scratch.curriculum_generator.gen_batch2_part2 import get_batch2_part2_days as get_b2_p2
from scratch.curriculum_generator.sec3_and_sec4_part import get_batch2_tail_days as get_b2_tail

# Batches 3 to 8 section definitions
from scratch.curriculum_generator.sec4_data import SEC4_DAYS
from scratch.curriculum_generator.sec5_data import SEC5_DAYS
from scratch.curriculum_generator.sec6_data import SEC6_DAYS
from scratch.curriculum_generator.sec7_data import SEC7_DAYS
from scratch.curriculum_generator.sec8_data import SEC8_DAYS
from scratch.curriculum_generator.sec9_data import SEC9_DAYS
from scratch.curriculum_generator.sec10_data import SEC10_DAYS
from scratch.curriculum_generator.sec11_data import SEC11_DAYS
from scratch.curriculum_generator.sec12_data import SEC12_DAYS
from scratch.curriculum_generator.sec13_data import SEC13_DAYS
from scratch.curriculum_generator.sec14_data import SEC14_DAYS

def make_package_from_spec(day_num: int, spec: dict) -> dict:
    meta = CURRICULUM_MAP[day_num]
    steps = [
        make_explanation_step(
            f"day{day_num}-step1", 1, f"{meta['title']}: Foundations", "Foundations",
            f"Intuition & Core Principles: {meta['topic_name']}",
            f"Understand the core intuition, mental model, and foundational motivation for {meta['topic_name']}.",
            [
                spec["summary"],
                f"### Foundational Mental Model\nWhen approaching problems requiring **{meta['topic_name']}**, remember the central principle: {spec['takeaway']}"
            ],
            snippets=[{
                "title": f"{meta['topic_name']} Implementation Template",
                "code": spec["sample_code"],
                "language": "python"
            }],
            takeaway=spec["takeaway"]
        ),
        make_explanation_step(
            f"day{day_num}-step2", 2, "Mechanics & Invariants", "Mechanics",
            f"Operational Invariants & Complexity: {meta['topic_name']}",
            "Step-by-step execution mechanics, state invariants, and algorithmic bounds.",
            [
                spec["mechanics"],
                f"### Complexity & Correctness Invariants\n- **Core Invariant**: {spec['takeaway']}\n- **Boundary Discipline**: Ensure loop termination conditions, base cases, and boundary pointers prevent edge-case failures."
            ],
            callouts=[{
                "type": "tip",
                "title": f"{meta['topic_name']} Core Invariant",
                "content": spec["takeaway"]
            }],
            takeaway=f"Operational invariant locked: {spec['takeaway']}"
        ),
        make_checkpoint_step(
            f"day{day_num}-step3", 3, f"Knowledge Check: {meta['topic_name']}", "Checkpoint",
            "Evaluate Conceptual Mastery & Edge Cases",
            "Verify your understanding of algorithmic bounds and mechanics before coding.",
            [
                {
                    "id": f"chk-d{day_num}-q1",
                    "question": spec["q1"],
                    "options": spec["q1_opts"],
                    "correctOptionId": spec["q1_ans"],
                    "explanations": spec["q1_exp"]
                },
                {
                    "id": f"chk-d{day_num}-q2",
                    "question": spec["q2"],
                    "options": spec["q2_opts"],
                    "correctOptionId": spec["q2_ans"],
                    "explanations": spec["q2_exp"]
                }
            ],
            takeaway="Checkpoint verified! You are ready for the coding challenge."
        ),
        make_practice_step(
            f"day{day_num}-step4", 4, f"Guided Practice: {meta['topic_name']}", "Practice",
            spec["practice_task"],
            f"Implement and verify {meta['topic_name']} in the interactive workspace.",
            spec["practice_task"],
            [
                spec["practice_task"],
                "Implement your solution inside the provided function stub.",
                "Ensure your code passes the test assertions and prints the expected output."
            ],
            spec["starter"],
            spec["solution"],
            spec["patterns"],
            spec["hint"],
            takeaway=f"Successfully implemented and verified {meta['topic_name']}!"
        ),
        make_completion_step(
            f"day{day_num}-step5", 5, f"Day {day_num} Complete: {meta['title']}", "Mastery",
            day_num,
            f"Mastery Achieved: {meta['title']}",
            f"You have solidified key mental models and techniques for {meta['topic_name']}.",
            spec["recap"],
            meta["concepts"],
            get_next_preview(day_num)
        )
    ]
    return {
        "dayNumber": day_num,
        "title": meta["title"],
        "topicName": meta["topic_name"],
        "sectionId": meta["section_id"],
        "estimatedMinutes": meta["estimated_minutes"],
        "difficulty": meta["difficulty"],
        "prerequisites": meta["prerequisites"],
        "concepts": meta["concepts"],
        "practiceSkills": [meta["topic_name"] + " Implementation", "Invariant Verification", "Complexity Analysis"],
        "learningObjectives": meta.get("learning_objectives", []),
        "practiceArchetype": meta.get("archetype", "guided"),
        "flowTier": meta.get("flow_tier", "tier2"),
        "steps": steps
    }

def build_batch_ts(batch_num: int, days_dict: dict, imports_header: str = "") -> str:
    lines = []
    lines.append('import { DailyLessonPackage } from "../types";')
    if imports_header:
        lines.append(imports_header)
    lines.append("")
    lines.append(f"export const BATCH_{batch_num}_LESSONS: Record<number, DailyLessonPackage> = {{")

    for day_num in sorted(days_dict.keys()):
        day_obj = days_dict[day_num].copy()
        use_import = day_obj.pop("_use_imported_steps", None)
        
        steps_val = day_obj.pop("steps", None)
        day_json = json.dumps(day_obj, indent=2)
        
        if use_import:
            day_ts = day_json[:-1] + f',\n  "steps": {use_import}\n}}'
        else:
            steps_json = json.dumps(steps_val, indent=4)
            day_ts = day_json[:-1] + f',\n  "steps": {steps_json}\n}}'

        lines.append(f"  {day_num}: {day_ts},")

    lines.append("};")
    lines.append("")
    return "\n".join(lines)

def main():
    print("Building all 8 batches for CodeMentor 160-day curriculum...")

    # Batch 1: Days 1-20
    b1_days = {}
    b1_days.update(get_sec1_days())
    b1_days.update(get_sec2_days())
    b1_days.update(get_sec2_part2_days())
    b1_imports = 'import { DAY_1_STEPS } from "../day1Data";\nimport { DAY_2_STEPS } from "../day2Data";'
    b1_content = build_batch_ts(1, b1_days, b1_imports)
    with open("frontend/lib/lessons/batches/batch1.ts", "w", encoding="utf-8") as f:
        f.write(b1_content)
    print(f"Batch 1 written ({len(b1_days)} days)")

    # Batch 2: Days 21-40
    b2_days = {}
    b2_days.update(get_b2_p1())
    b2_days.update(get_b2_p2())
    b2_days.update(get_b2_tail())
    b2_content = build_batch_ts(2, b2_days)
    with open("frontend/lib/lessons/batches/batch2.ts", "w", encoding="utf-8") as f:
        f.write(b2_content)
    print(f"Batch 2 written ({len(b2_days)} days)")

    # Batch 3: Days 41-60
    b3_days = {}
    for d in range(41, 51):
        b3_days[d] = make_package_from_spec(d, SEC4_DAYS[d])
    for d in range(51, 61):
        b3_days[d] = make_package_from_spec(d, SEC5_DAYS[d])
    b3_content = build_batch_ts(3, b3_days)
    with open("frontend/lib/lessons/batches/batch3.ts", "w", encoding="utf-8") as f:
        f.write(b3_content)
    print(f"Batch 3 written ({len(b3_days)} days)")

    # Batch 4: Days 61-80
    b4_days = {}
    for d in range(61, 66):
        b4_days[d] = make_package_from_spec(d, SEC5_DAYS[d])
    for d in range(66, 76):
        b4_days[d] = make_package_from_spec(d, SEC6_DAYS[d])
    for d in range(76, 81):
        b4_days[d] = make_package_from_spec(d, SEC7_DAYS[d])
    b4_content = build_batch_ts(4, b4_days)
    with open("frontend/lib/lessons/batches/batch4.ts", "w", encoding="utf-8") as f:
        f.write(b4_content)
    print(f"Batch 4 written ({len(b4_days)} days)")

    # Batch 5: Days 81-100
    b5_days = {}
    for d in range(81, 86):
        b5_days[d] = make_package_from_spec(d, SEC7_DAYS[d])
    for d in range(86, 96):
        b5_days[d] = make_package_from_spec(d, SEC8_DAYS[d])
    for d in range(96, 101):
        b5_days[d] = make_package_from_spec(d, SEC9_DAYS[d])
    b5_content = build_batch_ts(5, b5_days)
    with open("frontend/lib/lessons/batches/batch5.ts", "w", encoding="utf-8") as f:
        f.write(b5_content)
    print(f"Batch 5 written ({len(b5_days)} days)")

    # Batch 6: Days 101-120
    b6_days = {}
    for d in range(101, 111):
        b6_days[d] = make_package_from_spec(d, SEC9_DAYS[d])
    for d in range(111, 121):
        b6_days[d] = make_package_from_spec(d, SEC10_DAYS[d])
    b6_content = build_batch_ts(6, b6_days)
    with open("frontend/lib/lessons/batches/batch6.ts", "w", encoding="utf-8") as f:
        f.write(b6_content)
    print(f"Batch 6 written ({len(b6_days)} days)")

    # Batch 7: Days 121-140
    b7_days = {}
    for d in range(121, 136):
        b7_days[d] = make_package_from_spec(d, SEC11_DAYS[d])
    for d in range(136, 141):
        b7_days[d] = make_package_from_spec(d, SEC12_DAYS[d])
    b7_content = build_batch_ts(7, b7_days)
    with open("frontend/lib/lessons/batches/batch7.ts", "w", encoding="utf-8") as f:
        f.write(b7_content)
    print(f"Batch 7 written ({len(b7_days)} days)")

    # Batch 8: Days 141-160
    b8_days = {}
    for d in range(141, 146):
        b8_days[d] = make_package_from_spec(d, SEC12_DAYS[d])
    for d in range(146, 156):
        b8_days[d] = make_package_from_spec(d, SEC13_DAYS[d])
    for d in range(156, 161):
        b8_days[d] = make_package_from_spec(d, SEC14_DAYS[d])
    b8_content = build_batch_ts(8, b8_days)
    with open("frontend/lib/lessons/batches/batch8.ts", "w", encoding="utf-8") as f:
        f.write(b8_content)
    print(f"Batch 8 written ({len(b8_days)} days)")

    print("\nAll 8 batches generated successfully!")

if __name__ == "__main__":
    main()
