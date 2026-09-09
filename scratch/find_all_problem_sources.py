import os
import re

print("Searching entire project directory...")
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or '.next' in root or '.system_generated' in root:
        continue
    for f in files:
        fpath = os.path.join(root, f)
        # check if file mentions "two_sum" or "problem" or has json/py/ts data
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as fh:
                text = fh.read()
                # look for arrays of problems or problem lists
                matches = re.findall(r'(\w+[\-_]\w+[\-_]?\w*)\s*:\s*\{.*?\"title\"', text)
                if len(matches) > 5:
                    print(f"File {fpath} has {len(matches)} title matches: {matches[:3]}...")
                if 'two-sum' in text and ('slug' in text or 'statement' in text):
                    print(f"File with two-sum & slug/statement: {fpath} (size: {os.path.getsize(fpath)} bytes)")
        except Exception as e:
            pass
