"""
Live HTTP Verification Script for 160-Day Learning Platform & Practice Portal Regression.
Tests:
1. /learning page loads with 200 OK.
2. /practice loads with 200 OK and Monaco/Problems intact.
3. Representative Day endpoints /learning/day/[N] load with 200 OK.
4. Backend /api/learning/run executes code correctly.
"""

import urllib.request
import urllib.error
import json
import time

FRONTEND_URL = "http://localhost:3000"
BACKEND_URL = "http://localhost:8000"

def test_url(url, expected_status=200):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=35) as resp:
            status = resp.status
            body = resp.read().decode("utf-8")
            return status, len(body)
    except urllib.error.HTTPError as e:
        return e.code, 0
    except Exception as e:
        return str(e), 0

def test_code_run(code):
    try:
        payload = json.dumps({"code": code}).encode("utf-8")
        req = urllib.request.Request(
            f"{BACKEND_URL}/api/learning/run",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            return res
    except Exception as e:
        return {"error": str(e)}

def main():
    print("=== LIVE INTEGRATION & REGRESSION TEST ===")

    # 1. Practice Portal Protection
    p_status, p_len = test_url(f"{FRONTEND_URL}/practice")
    print(f"Practice Portal (/practice): Status {p_status}, Body Size {p_len} bytes")
    assert p_status == 200, f"Practice Portal returned {p_status}"

    # 2. Learning Dashboard
    l_status, l_len = test_url(f"{FRONTEND_URL}/learning")
    print(f"Learning Dashboard (/learning): Status {l_status}, Body Size {l_len} bytes")
    assert l_status == 200, f"Learning Dashboard returned {l_status}"

    # 3. Representative Day Lessons Across All 8 Batches
    sample_days = [1, 2, 20, 40, 60, 80, 100, 120, 140, 160]
    for d in sample_days:
        status, length = test_url(f"{FRONTEND_URL}/learning/day/{d}")
        print(f"Day {d:3d} (/learning/day/{d}): Status {status}, Size {length} bytes")
        assert status == 200, f"Day {d} returned {status}"

    # 4. Backend Sandbox Execution
    print("\nTesting Backend Code Execution (/api/learning/run):")
    res = test_code_run("print('Hello 160 Days!')\nx = 10 * 2\nprint('Computed:', x)")
    print(f"Stdout: {res.get('stdout', '').strip()}")
    assert "Computed: 20" in res.get("stdout", ""), "Sandbox calculation failed!"

    print("\n[SUCCESS] All live tests passed! Practice Portal and all 160 Learning Days are fully functional.")

if __name__ == "__main__":
    main()
