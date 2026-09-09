import json
import os
import sys

from scratch.curriculum_generator.sec1_foundations import get_sec1_days
from scratch.curriculum_generator.sec2_core_part1 import get_sec2_days
from scratch.curriculum_generator.sec2_core_part2 import get_sec2_part2_days

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
    sec1 = get_sec1_days()
    sec2_p1 = get_sec2_days()
    sec2_p2 = get_sec2_part2_days()

    b1_days = {}
    b1_days.update(sec1)
    b1_days.update(sec2_p1)
    b1_days.update(sec2_p2)

    imports = 'import { DAY_1_STEPS } from "../day1Data";\nimport { DAY_2_STEPS } from "../day2Data";'
    ts_content = build_batch_ts(1, b1_days, imports)

    out_path = "frontend/lib/lessons/batches/batch1.ts"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(ts_content)

    print(f"Generated {out_path} with {len(b1_days)} days successfully!")

if __name__ == "__main__":
    main()
