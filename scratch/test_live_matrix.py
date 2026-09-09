import urllib.request
import urllib.parse
import json
import sys

def test_routes():
    print("==================================================")
    print("LIVE VERIFICATION MATRIX ACROSS 160-DAY CURRICULUM")
    print("==================================================")
    
    test_days = [
        (1, "Day 1: Memory Model & Identity"),
        (2, "Day 2: Arithmetic & Numerical Types"),
        (21, "Day 21: Scope LEGB & Closures"),
        (25, "Day 25: Python Algorithmic Toolkit"),
        (41, "Day 41: Dynamic Sliding Window"),
        (56, "Day 56: Binary Search Bounds"),
        (78, "Day 78: In-Place Linked List Reversal"),
        (101, "Day 101: Invert Binary Tree"),
        (122, "Day 122: Shortest Path in Unweighted Graph"),
        (141, "Day 141: Gas Station Circuit"),
        (157, "Day 157: Segment Tree Range Sum Queries"),
        (160, "Day 160: The Complete Engineer Capstone"),
    ]
    
    errors = []
    
    # 1. Test frontend routes on port 3000
    for day, desc in test_days:
        url = f"http://localhost:3000/learning/day/{day}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=25) as resp:
                status = resp.status
                body = resp.read().decode('utf-8')
                if status == 200 and len(body) > 1000:
                    print(f"  [PASS] Day {day:3d} HTTP {status} ({len(body)} bytes) - {desc}")
                else:
                    errors.append(f"Day {day} returned status {status} or insufficient body ({len(body)} bytes)")
                    print(f"  [FAIL] Day {day:3d} HTTP {status}")
        except Exception as e:
            errors.append(f"Day {day} request failed: {e}")
            print(f"  [FAIL] Day {day:3d}: {e}")

    # 2. Test Practice Portal isolation
    practice_urls = [
        ("http://localhost:3000/practice", "Practice Portal Home"),
        ("http://localhost:3000/practice/two-sum", "Practice Problem: Two Sum"),
        ("http://localhost:3000/learning", "Learning Hub / 160-day Roadmap")
    ]
    print("\n--- Checking Practice Portal & Roadmap Isolation ---")
    for url, label in practice_urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                status = resp.status
                body = resp.read().decode('utf-8')
                if status == 200 and len(body) > 1000:
                    print(f"  [PASS] {label}: HTTP {status} ({len(body)} bytes)")
                else:
                    errors.append(f"{label} returned status {status}")
                    print(f"  [FAIL] {label}: HTTP {status}")
        except Exception as e:
            errors.append(f"{label} failed: {e}")
            print(f"  [FAIL] {label}: {e}")

    # 3. Test Backend Python Sandbox Execution
    print("\n--- Testing Backend Code Execution Sandbox ---")
    sandbox_url = "http://localhost:8000/api/learning/run"
    test_code = {
        "code": "print('CodeMentor 160-Day Curriculum Live Test')\nx = [i**2 for i in range(5)]\nprint('Squares:', x)",
        "expected_output_pattern": "Squares: [0, 1, 4, 9, 16]"
    }
    try:
        req = urllib.request.Request(
            sandbox_url,
            data=json.dumps(test_code).encode('utf-8'),
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data.get("status") in ("success", "ok") and "Squares: [0, 1, 4, 9, 16]" in data.get("stdout", ""):
                print(f"  [PASS] Backend Sandbox: Execution success! Output: {data.get('stdout').strip()}")
            else:
                errors.append(f"Backend sandbox unexpected response: {data}")
                print(f"  [FAIL] Backend Sandbox: {data}")
    except Exception as e:
        errors.append(f"Backend sandbox execution failed: {e}")
        print(f"  [FAIL] Backend Sandbox: {e}")

    print("\n==================================================")
    if not errors:
        print(">>> ALL LIVE MATRIX TESTS PASSED PERFECTLY! <<<")
        print("==================================================")
        return 0
    else:
        print(f">>> FAILED WITH {len(errors)} ERRORS <<<")
        print("==================================================")
        return 1

if __name__ == "__main__":
    sys.exit(test_routes())
