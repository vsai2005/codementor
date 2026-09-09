import json

with open('scratch/curriculum_160.json', encoding='utf-8') as f:
    curr = json.load(f)

print(f"Total sections: {len(curr)}")
total_days = 0
all_practice_ids = set()
for s in curr:
    for d in s.get('days', []):
        total_days += 1
        p_ids = d.get('practice_problem_ids', [])
        for pid in p_ids:
            all_practice_ids.add(pid)

print(f"Total days: {total_days}")
print(f"Unique practice_problem_ids referenced across 160 days: {len(all_practice_ids)}")
print("Sample practice_problem_ids:", sorted(list(all_practice_ids))[:20])

# Now check how many unique problem slugs are in curriculumData.ts
with open('frontend/lib/curriculum/curriculumData.ts', encoding='utf-8') as f:
    cdata = f.read()

import re
matches = re.findall(r'practice_problem_ids:\s*\[(.*?)\]', cdata)
cdata_pids = set()
for m in matches:
    items = re.findall(r'["\']([^"\']+)["\']', m)
    for it in items:
        cdata_pids.add(it)

print(f"Unique practice_problem_ids in curriculumData.ts: {len(cdata_pids)}")
print("Count of unique pids in curriculumData.ts:", len(cdata_pids))
