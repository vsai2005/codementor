import json
import os
import sys

from scratch.curriculum_generator.gen_batch2_part1 import get_batch2_days as get_b2_p1
from scratch.curriculum_generator.gen_batch2_part2 import get_batch2_part2_days as get_b2_p2
from scratch.curriculum_generator.sec3_and_sec4_part import get_batch2_tail_days as get_b2_tail

def build_batch_ts(batch_num, days_dict, imports_header=""):
    lines = []
    lines.append('import { DailyLessonPackage } from "../types";')
    if imports_header:
        lines.append(imports_header)
    lines.append("")
    lines.append(f"export const BATCH_{batch_num}_LESSONS: Record<number, DailyLessonPackage> = {{")

    for day_num in sorted(days_dict.keys()):
        day_obj = days_dict[day_num]
        use_import = day_obj.pop("_use_imported_steps", None)
        
        # Format as json
        steps_val = day_obj.pop("steps", None)
        day_json = json.dumps(day_obj, indent=2)
        
        # Insert steps with leading comma
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
    b2_days = {}
    b2_days.update(get_b2_p1())    # Days 21-30
    b2_days.update(get_b2_p2())    # Days 31-32
    b2_days.update(get_b2_tail())  # Days 33-40

    ts_content = build_batch_ts(2, b2_days)

    out_path = "frontend/lib/lessons/batches/batch2.ts"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(ts_content)

    print(f"Generated {out_path} with {len(b2_days)} days successfully!")

if __name__ == "__main__":
    main()
