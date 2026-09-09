import json
import math
import copy

with open('scratch/existing_70_problems.json', encoding='utf-8') as f:
    data = json.load(f)

problems = data["problems"]
print(f"Loaded {len(problems)} existing problems.")

# Check problem structure
for i, p in enumerate(problems, 1):
    slug = p["slug"]
    entry = p["entry_point"]
    cases = p["test_cases"]
    starter = p["starter_code"].get("python", "")
    assert entry in starter, f"Problem {slug} entry_point '{entry}' not in starter_code!"
    assert len(cases) >= 5, f"Problem {slug} has fewer than 5 test cases ({len(cases)})"

print("All 70 existing problems have valid entry points and >=5 test cases!")
