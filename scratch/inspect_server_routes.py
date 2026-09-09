with open('dev_backend/server.py', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'def do_' in line or 'class ' in line or '/api/problems' in line or 'CONCEPT_LESSONS' in line or 'OPTIMIZE_HINTS' in line:
        print(f"{idx+1}: {line.strip()}")
