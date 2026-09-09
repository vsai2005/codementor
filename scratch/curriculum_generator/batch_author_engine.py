"""
Curriculum authoring engine for Batches 3 through 8 (Days 41 to 160).
Contains domain definitions, detailed explanations, code snippets,
conceptual checkpoints with full 4-option explanations, guided practice challenges with # TODO,
expected output patterns, and mastery recap tables.
"""

import json
import os
from .common import (
    CURRICULUM_MAP,
    get_difficulty,
    get_next_preview,
    make_explanation_step,
    make_checkpoint_step,
    make_practice_step,
    make_completion_step,
)

def build_batch_ts_file(batch_num: int, days_dict: dict, out_path: str):
    lines = []
    lines.append('import { DailyLessonPackage } from "../types";')
    lines.append("")
    lines.append(f"export const BATCH_{batch_num}_LESSONS: Record<number, DailyLessonPackage> = {{")

    for day_num in sorted(days_dict.keys()):
        day_obj = days_dict[day_num]
        steps_val = day_obj.pop("steps", None)
        day_json = json.dumps(day_obj, indent=2)
        steps_json = json.dumps(steps_val, indent=4)
        day_ts = day_json[:-1] + f',\n  "steps": {steps_json}\n}}'
        lines.append(f"  {day_num}: {day_ts},")

    lines.append("};")
    lines.append("")
    
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Successfully wrote {out_path} with {len(days_dict)} days!")
