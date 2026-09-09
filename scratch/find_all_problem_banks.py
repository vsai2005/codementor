import os

root_dir = r"c:\Users\vsair\OneDrive\Desktop\learning platfrom"
matches = []

for root, dirs, files in os.walk(root_dir):
    if '.git' in root or 'node_modules' in root or '.next' in root or '.system_generated' in root:
        continue
    for f in files:
        fpath = os.path.join(root, f)
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as fh:
                content = fh.read()
                if 'difficulty_tier' in content or 'test_cases' in content or 'problem_bank' in content:
                    matches.append((fpath, len(content), content.count('difficulty_tier'), content.count('test_cases')))
        except Exception:
            pass

for m in matches:
    print(f"File: {m[0]} | size: {m[1]} | difficulty_tier count: {m[2]} | test_cases count: {m[3]}")
