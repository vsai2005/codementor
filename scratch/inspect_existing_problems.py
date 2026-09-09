import re
import os
import glob

print("Scanning for problem definitions across repo...")

# Check backend/app/seed.py
with open('backend/app/seed.py', encoding='utf-8') as f:
    seed_text = f.read()
seed_slugs = re.findall(r'P\("([^"]+)"', seed_text)
print(f"backend/app/seed.py has {len(seed_slugs)} problems:")
print(seed_slugs)

# Check dev_backend/server.py
with open('dev_backend/server.py', encoding='utf-8') as f:
    dev_text = f.read()
dev_slugs = re.findall(r'P\("([^"]+)"', dev_text)
print(f"dev_backend/server.py has {len(dev_slugs)} problem definitions directly.")

# Search all files for any problem lists or JSON files
for root, dirs, files in os.walk('.'):
    for fname in files:
        if fname.endswith(('.py', '.ts', '.tsx', '.json')) and not fname.startswith('curriculum_') and not 'node_modules' in root and not '.next' in root:
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if 'contains-duplicate' in content and 'backend\\app\\seed.py' not in fpath and 'scratch' not in fpath:
                        print(f"Found reference in {fpath}")
            except:
                pass
