import re

with open("backend/app/seed.py", "r", encoding="utf-8") as f:
    content = f.read()

# Pattern: ]), reference_solution=(.*?),\n\n
# We want to replace ]), reference_solution=... with ], reference_solution=...)
# Notice that each problem ended with ]), reference_solution=...
# Let's use regex
content = re.sub(
    r'\]\),\s*reference_solution=(.*?),\n',
    r'], reference_solution=\1),\n',
    content
)

with open("backend/app/seed.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed syntax in seed.py")
