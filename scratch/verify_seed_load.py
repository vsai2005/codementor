import os
import uuid

SEED_PATH = os.path.join("backend", "app", "seed.py")
with open(SEED_PATH, encoding="utf-8") as fh:
    src = fh.read()

snippet = src[src.index("TOPICS = ["):src.index("def seed(")]
ns = {}
exec(snippet, ns)

topics = ns["TOPICS"]
problems = ns["PROBLEMS"]

print(f"Total topics: {len(topics)}")
print(f"Total problems: {len(problems)}")

NS = uuid.UUID("00000000-0000-0000-0000-0000000c0de0")
slugs = set()
topic_slugs = {t[0] for t in topics}

for p in problems:
    assert p["slug"] not in slugs, f"Duplicate slug: {p['slug']}"
    slugs.add(p["slug"])
    assert p["topic"] in topic_slugs, f"Unknown topic {p['topic']} for problem {p['slug']}"
    pid = str(uuid.uuid5(NS, "problem:" + p["slug"]))
    assert len(pid) == 36

print("All problems have valid, unique slugs and mapped to valid topics!")
