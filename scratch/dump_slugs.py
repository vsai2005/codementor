import sys, os
sys.path.insert(0, os.path.abspath("."))
import dev_backend.server as s

with open("scratch/all_178_slugs.txt", "w", encoding="utf-8") as f:
    for pid, p in sorted(s.PROBLEMS.items(), key=lambda x: x[1]["slug"]):
        f.write(f"{p['slug']} | {p['topic_slug']} | {p['title']}\n")
print(f"Wrote {len(s.PROBLEMS)} slugs to scratch/all_178_slugs.txt")
