import re
import json

with open('backend/app/seed.py', encoding='utf-8') as f:
    text = f.read()

# Let's extract TOPICS and PROBLEMS using Python execution
snippet = text[text.index("TOPICS = ["):text.index("def seed(")]
ns = {}
exec(snippet, ns)

topics = ns["TOPICS"]
problems = ns["PROBLEMS"]

print(f"Total topics: {len(topics)}")
for slug, name in topics:
    print(f"  Topic: {slug:20s} -> {name}")

print(f"\nTotal problems: {len(problems)}")
tier_counts = {}
topic_counts = {}
for i, p in enumerate(problems, 1):
    slug = p["slug"]
    title = p["title"]
    topic = p["topic"]
    tier = p["difficulty_tier"]
    cases_count = len(p["test_cases"])
    tier_counts[tier] = tier_counts.get(tier, 0) + 1
    topic_counts[topic] = topic_counts.get(topic, 0) + 1
    if i <= 10 or i >= 65:
        print(f"#{i:2d}: [{topic:15s}] Tier {tier} | {slug:25s} | {title} ({cases_count} cases)")

print("\nDifficulty Tier Breakdown:")
for t in sorted(tier_counts.keys()):
    print(f"  Tier {t}: {tier_counts[t]} problems")

print("\nTopic Breakdown:")
for top, cnt in sorted(topic_counts.items()):
    print(f"  {top:20s}: {cnt} problems")
