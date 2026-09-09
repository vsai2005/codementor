import json
import os
import sys

sys.path.insert(0, os.path.abspath("."))
import dev_backend.server as s

problems_by_slug = {p["slug"]: p for p in s.PROBLEMS.values()}
with open("scratch/curriculum_160.json", "r", encoding="utf-8") as f:
    curriculum = json.load(f)

print(f"{'Day':<4} | {'Section':<22} | {'Title':<45}")
print("-" * 75)
for d in curriculum:
    print(f"{d['day_number']:<4} | {d['section_id']:<22} | {d['title']:<45}")
