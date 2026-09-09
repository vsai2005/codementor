"""Inject canonical reference solutions for the 70 original problems into backend/app/seed.py."""

import json
import re
import sys
import os

sys.path.insert(0, os.path.abspath("."))
from scratch.add_70_reference_solutions import SOLUTIONS

seed_path = "backend/app/seed.py"
with open(seed_path, "r", encoding="utf-8") as f:
    content = f.read()

modified_count = 0
for slug, sol in SOLUTIONS.items():
    escaped_slug = re.escape(slug)
    # Match starting with P("slug", and ending with ]) followed by optional newline or comma
    # Look for P("slug", ... ])
    start_str1 = f'P("{slug}",'
    start_str2 = f"P('{slug}',"
    start_pos = content.find(start_str1)
    if start_pos == -1:
        start_pos = content.find(start_str2)
    if start_pos == -1:
        print(f"Could not find start for slug: {slug}")
        continue

    # Find the closing ]) of this P(...) call
    # It will be the first '])' after start_pos before the next 'P('
    next_p = content.find('\n    P(', start_pos + 1)
    if next_p == -1:
        next_p = len(content)

    call_chunk = content[start_pos:next_p]
    # Find the last '])' in call_chunk
    end_bracket_pos = call_chunk.rfind('])')
    if end_bracket_pos == -1:
        print(f"Could not find '])' for slug: {slug}")
        continue

    # Check if reference_solution is already injected
    if 'reference_solution=' in call_chunk:
        continue

    # Slice and replace
    exact_idx = start_pos + end_bracket_pos + 2 # right after ])
    sol_repr = repr(sol)
    content = content[:exact_idx] + f", reference_solution={sol_repr}" + content[exact_idx:]
    modified_count += 1

print(f"Injected reference solutions for {modified_count} problems.")

with open(seed_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated backend/app/seed.py successfully.")
