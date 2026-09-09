import re
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from scratch.practice_generator.sec1_sec2 import SEC1_SEC2_PROBLEMS
from scratch.practice_generator.sec3_sec4 import SEC3_SEC4_PROBLEMS
from scratch.practice_generator.sec5_sec6 import SEC5_SEC6_PROBLEMS
from scratch.practice_generator.sec7_sec8 import SEC7_SEC8_PROBLEMS
from scratch.practice_generator.sec9_trees import SEC9_TREES_PROBLEMS
from scratch.practice_generator.sec10_heaps import SEC10_HEAPS_PROBLEMS
from scratch.practice_generator.sec11_graphs import SEC11_GRAPHS_PROBLEMS
from scratch.practice_generator.sec12_greedy import SEC12_GREEDY_PROBLEMS
from scratch.practice_generator.sec13_dp import SEC13_DP_PROBLEMS
from scratch.practice_generator.sec14_adv import SEC14_ADV_PROBLEMS

ALL_NEW = (
    SEC1_SEC2_PROBLEMS +
    SEC3_SEC4_PROBLEMS +
    SEC5_SEC6_PROBLEMS +
    SEC7_SEC8_PROBLEMS +
    SEC9_TREES_PROBLEMS +
    SEC10_HEAPS_PROBLEMS +
    SEC11_GRAPHS_PROBLEMS +
    SEC12_GREEDY_PROBLEMS +
    SEC13_DP_PROBLEMS +
    SEC14_ADV_PROBLEMS
)

print(f"Total new problems to append: {len(ALL_NEW)}")

with open('backend/app/seed.py', encoding='utf-8') as f:
    seed_code = f.read()

# 1. Update TOPICS
NEW_TOPICS_STR = '''TOPICS = [
    ("arrays", "Arrays & Hashing"),
    ("two-pointers", "Two Pointers"),
    ("strings", "Strings"),
    ("stacks", "Stacks & Queues"),
    ("binary-search", "Binary Search"),
    ("graphs", "Graphs & Trees"),
    ("python-basics", "Python Basics"),
    ("linked-lists", "Linked Lists"),
    ("trees", "Trees & BST"),
    ("heaps", "Heaps & Priority Queues"),
    ("searching-sorting", "Searching & Sorting"),
    ("hashing", "Hashing & Hash Tables"),
    ("greedy", "Greedy Algorithms"),
    ("dynamic-programming", "Dynamic Programming"),
    ("bit-manipulation", "Bit Manipulation"),
    ("advanced-dsa", "Advanced DSA & Capstone"),
]'''

seed_code = re.sub(r'TOPICS = \[.*?\]', NEW_TOPICS_STR, seed_code, flags=re.DOTALL)

# 2. Update def P helper to accept reference_solution=""
NEW_P_DEF = '''def P(slug, title, topic, tier, entry, statement, constraints,
      opt_t, opt_s, starter, cases, reference_solution=""):
    return {
        "slug": slug, "title": title, "topic": topic, "difficulty_tier": tier,
        "entry_point": entry, "statement_md": statement, "constraints_md": constraints,
        "optimal_time": opt_t, "optimal_space": opt_s,
        "starter_code": {"python": starter}, "test_cases": cases,
        "reference_solution": reference_solution,
    }'''

seed_code = re.sub(r'def P\(slug, title, topic, tier, entry, statement, constraints,\s+opt_t, opt_s, starter, cases\):.*?return \{.*?\}', NEW_P_DEF, seed_code, flags=re.DOTALL)

# 3. Update sort-by-parity statement
seed_code = seed_code.replace(
    '"Return an array with all even elements first (any order among evens is fine, but keep evens in their original relative order), then the odds in original relative order."',
    '"Return an array with all even elements first (preserving their original relative order), then the odd elements (preserving their original relative order)."'
)

# 4. Update min-stack-ops title
seed_code = seed_code.replace(
    'P("min-stack-ops", "Minimum After Operations", "stacks", 3, "min_operations",',
    'P("min-stack-ops", "Baseball Game Operations", "stacks", 3, "min_operations",'
)

# 5. Format new problems code
import pprint

new_probs_code = []
for p in ALL_NEW:
    p_code = f"""    P({repr(p['slug'])}, {repr(p['title'])}, {repr(p['topic'])}, {p['difficulty_tier']}, {repr(p['entry_point'])},
      {repr(p['statement_md'])},
      {repr(p['constraints_md'])}, {repr(p['optimal_time'])}, {repr(p['optimal_space'])},
      {repr(p['starter_code']['python'])},
      {pprint.pformat(p['test_cases'], indent=7)},
      {repr(p['reference_solution'])}),
"""
    new_probs_code.append(p_code)

formatted_new_problems = "\n" + "\n".join(new_probs_code)

# Insert right before the closing bracket of PROBLEMS = [ ... ]
# Find the line with `PROBLEMS = [` and its matching `\n]` before `def seed`
marker = "\n]\n\n\ndef seed() -> None:"
if marker not in seed_code:
    raise ValueError("Could not find end of PROBLEMS list marker!")

seed_code = seed_code.replace(marker, formatted_new_problems + marker)

# 6. Update seed() to pop reference_solution and use uuid5
NEW_SEED_FUNC = '''def seed() -> None:
    db = SessionLocal()
    NS = uuid.UUID("00000000-0000-0000-0000-0000000c0de0")
    try:
        topic_ids: dict[str, uuid.UUID] = {}
        for slug, name in TOPICS:
            topic = db.execute(select(Topic).where(Topic.slug == slug)).scalars().first()
            if topic is None:
                topic = Topic(id=uuid.uuid5(NS, "topic:" + slug), slug=slug, name=name)
                db.add(topic)
                db.flush()
            topic_ids[slug] = topic.id

        created = updated = 0
        for spec in PROBLEMS:
            data = dict(spec)
            topic_slug = data.pop("topic")
            data.pop("reference_solution", None)  # Not stored in DB column
            existing = db.execute(
                select(Problem).where(Problem.slug == data["slug"])
            ).scalars().first()

            if existing is None:
                db.add(Problem(id=uuid.uuid5(NS, "problem:" + data["slug"]), topic_id=topic_ids[topic_slug], **data))
                created += 1
            else:
                for key, value in data.items():
                    setattr(existing, key, value)
                existing.topic_id = topic_ids[topic_slug]
                updated += 1

        db.commit()
        tiers = sorted({p["difficulty_tier"] for p in PROBLEMS})
        print(f"seeded {len(TOPICS)} topics, {created} new / {updated} updated problems (total: {len(PROBLEMS)})")
        print(f"tiers present: {tiers}")
    finally:
        db.close()
'''

seed_code = re.sub(r'def seed\(\) -> None:.*?finally:\s+db\.close\(\)', NEW_SEED_FUNC, seed_code, flags=re.DOTALL)

with open('backend/app/seed.py', 'w', encoding='utf-8') as f:
    f.write(seed_code)

print("Successfully written updated backend/app/seed.py!")
