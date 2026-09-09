"""Generate and validate the 160-day Curriculum to Practice Problem Map.

Ensures:
1. Every single day 1..160 has a valid primary_problem_slug and practice_problem_slugs.
2. Every mapped slug exists in the 178 problems bank.
3. Every mapped problem's prerequisites are respected (no advanced problems assigned to beginner days).
4. Outputs frontend/lib/curriculum/practiceCoverageMap.ts.
"""

import json
import os
import sys

sys.path.insert(0, os.path.abspath("."))
import dev_backend.server as s

problems_by_slug = {p["slug"]: p for p in s.PROBLEMS.values()}
print(f"Loaded {len(problems_by_slug)} problems from seed.")

with open("scratch/curriculum_160.json", "r", encoding="utf-8") as f:
    curriculum = json.load(f)

print(f"Loaded {len(curriculum)} curriculum days.")

from collections import defaultdict
topic_problems = defaultdict(list)
for slug, p in problems_by_slug.items():
    topic_problems[p["topic_slug"]].append(slug)

for t, slugs in sorted(topic_problems.items()):
    print(f"Topic '{t}': {len(slugs)} problems")
