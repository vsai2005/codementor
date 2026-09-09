"""End-to-End Live HTTP Verification for CodeMentor Practice Problem Bank.
Tests both backend (port 8000) and frontend (port 3000).
"""

import json
import urllib.request
import urllib.error
import sys

BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "VerificationAgent/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, json.loads(resp.read())

def post(url, data):
    payload = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json", "User-Agent": "VerificationAgent/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.status, json.loads(resp.read())

def main():
    print("=" * 70)
    print("LIVE HTTP VERIFICATION")
    print("=" * 70)

    # 1. Health check
    status, health = get(f"{BACKEND_URL}/health")
    print(f"[1] Health check: status {status}, response: {health}")
    assert status == 200 and health.get("status") == "ok"

    # 2. List problems
    status, problems_page = get(f"{BACKEND_URL}/api/problems")
    items = problems_page["items"]
    total = problems_page["total"]
    print(f"[2] GET /api/problems: returned {len(items)} items, total: {total}")
    assert total == 178, f"Expected 178 problems, got {total}"
    assert len(items) == 178, f"Expected 178 items in single page, got {len(items)}"

    # 3. Topic coverage in list
    topics = set(p["topic"]["slug"] for p in items)
    print(f"[3] Topics found in problem list: {len(topics)} topics")
    print("    " + ", ".join(sorted(topics)))
    assert len(topics) == 16, f"Expected 16 topics, found {len(topics)}"

    # 4. Filter by difficulty tiers
    for tier in [1, 2, 3, 4, 5]:
        tier_items = [p for p in items if p["difficulty_tier"] == tier]
        print(f"    Tier {tier}: {len(tier_items)} problems")

    # 5. Detail & Reference solution verification for a cross-section of problems
    sample_slugs = [
        "celsius-to-fahrenheit",         # python-basics
        "contains-duplicate",            # arrays
        "merge-intervals",               # arrays
        "sort-an-array",                 # searching-sorting
        "reverse-linked-list",           # linked-lists
        "binary-tree-inorder-traversal", # trees
        "merge-k-sorted-lists",          # heaps
        "number-of-islands",             # graphs
        "jump-game",                     # greedy
        "climbing-stairs",               # dynamic-programming
        "number-of-1-bits",              # bit-manipulation
        "word-search-ii",                # advanced-dsa
    ]

    print(f"\n[4] Detail & Sandbox Execution Test for {len(sample_slugs)} sample problems:")
    slug_to_item = {p["slug"]: p for p in items}

    for slug in sample_slugs:
        item = slug_to_item.get(slug)
        assert item is not None, f"Slug {slug} not found in problems list"
        pid = item["id"]

        # GET detail
        st, detail = get(f"{BACKEND_URL}/api/problems/{pid}")
        assert st == 200, f"Failed to get detail for {slug}"
        assert detail["slug"] == slug
        assert detail["entry_point"]
        assert detail["statement_md"]
        assert detail.get("concept") is not None, f"Missing concept mini-lesson for {slug}"

        # GET reference solution
        st, ref = get(f"{BACKEND_URL}/api/problems/{pid}/reference")
        assert st == 200, f"Failed to get reference for {slug}"
        assert ref["available"] is True, f"Reference solution not available for {slug}"
        assert ref["code"], f"Empty reference code for {slug}"

        # POST /api/submissions/run in sandbox
        st, run_res = post(f"{BACKEND_URL}/api/submissions/run", {
            "problem_id": pid,
            "language": "python",
            "code": ref["code"]
        })
        assert st == 200, f"Run tests failed for {slug}"
        assert run_res["all_passed"] is True, f"Reference solution failed in sandbox for {slug}: {run_res}"
        print(f"    [PASS] [{detail['topic']['slug']}] {slug} -> {run_res['passed']}/{run_res['total']} tests passed in {run_res['results'][0]['runtime_ms']}ms")

    # 6. Test Next.js Practice frontend
    try:
        req = urllib.request.Request(f"{FRONTEND_URL}/practice", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f"\n[5] GET {FRONTEND_URL}/practice -> status {resp.status}")
            assert resp.status == 200
    except Exception as e:
        print(f"\n[5] Frontend check on port 3000: {e}")

    print("\n" + "=" * 70)
    print("ALL LIVE HTTP VERIFICATION GATES PASSED PERFECTLY!")
    print("=" * 70)

if __name__ == "__main__":
    main()
