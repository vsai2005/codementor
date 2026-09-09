import os
import sys

sys.path.insert(0, os.path.abspath("."))
from scratch.build_curriculum_practice_map import MAPPING

curriculum_day_practice = {}
practice_slug_to_days = {}

for day, (primary, slugs, tier, req, top) in MAPPING.items():
    curriculum_day_practice[day] = primary
    for s in slugs:
        practice_slug_to_days.setdefault(s, []).append(day)

out_file = os.path.join("backend", "app", "core", "curriculum_map.py")
with open(out_file, "w", encoding="utf-8") as f:
    f.write('"""Curriculum to Practice Mapping for 160-day roadmap."""\n\n')
    f.write(f'CURRICULUM_DAY_PRACTICE = {repr(curriculum_day_practice)}\n\n')
    f.write(f'PRACTICE_SLUG_TO_DAYS = {repr(practice_slug_to_days)}\n')

print(f"Generated {out_file} successfully: {len(curriculum_day_practice)} days.")
