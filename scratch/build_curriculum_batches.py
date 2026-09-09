"""
Generates the complete 160-day Python -> DSA curriculum across 8 code-split TypeScript batch files.
Batch 1: Days 1-20 (preserves Day 1 & Day 2)
Batch 2: Days 21-40
Batch 3: Days 41-60
Batch 4: Days 61-80
Batch 5: Days 81-100
Batch 6: Days 101-120
Batch 7: Days 121-140
Batch 8: Days 141-160
"""

import json
import os
import re

with open("scratch/curriculum_160.json", "r", encoding="utf-8") as f:
    CURRICULUM = json.load(f)

CURRICULUM_BY_DAY = {d["day_number"]: d for d in CURRICULUM}

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

print(f"Loaded {len(CURRICULUM)} days of curriculum metadata.")
