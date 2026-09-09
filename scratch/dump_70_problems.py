import json

with open('backend/app/seed.py', encoding='utf-8') as f:
    src = f.read()

snippet = src[src.index("TOPICS = ["):src.index("def seed(")]
ns = {}
exec(snippet, ns)

problems = ns["PROBLEMS"]
topics = ns["TOPICS"]

data = {
    "total_problems": len(problems),
    "topics": topics,
    "problems": problems
}

with open('scratch/existing_70_problems.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Successfully dumped {len(problems)} problems to scratch/existing_70_problems.json")
