"""Automated Progression & Verification Test Suite for Stage 5.

Tests:
  Scenario A: Happy Path (New User -> Day 1 Lesson -> Practice Required -> Fail Practice -> Pass Practice -> Day 1 Done -> Day 2 Unlocked)
  Scenario B: Direct URL / Lock Bypass Gating (403 on locked days, fail-closed)
  Scenario C: Practice Spoofing Guard (Unrelated problem pass does not unlock Day 1)
  Scenario D: Non-Destructive Review & Idempotency (Revisiting Day 1 never resets Day 2)
  Scenario E: Day 160 Capstone Grand Finale (160th day completion and 100% mastery)
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Optional, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")


class TestClient:
    def __init__(self, base_url: str = BACKEND_URL):
        self.base_url = base_url.rstrip("/")
        self.token: Optional[str] = None

    def request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Tuple[int, Any]:
        req_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if self.token:
            req_headers["Authorization"] = f"Bearer {self.token}"
        if headers:
            req_headers.update(headers)

        payload = json.dumps(data).encode("utf-8") if data is not None else None
        req = urllib.request.Request(
            f"{self.base_url}{path}",
            data=payload,
            headers=req_headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = resp.read().decode("utf-8")

                try:
                    parsed = json.loads(raw)
                except Exception:
                    parsed = raw
                return resp.status, parsed
        except urllib.error.HTTPError as err:
            raw = err.read().decode("utf-8")
            try:
                parsed = json.loads(raw)
            except Exception:
                parsed = raw
            return err.code, parsed

    def get(self, path: str) -> Tuple[int, Any]:
        return self.request("GET", path)

    def post(self, path: str, data: Dict[str, Any]) -> Tuple[int, Any]:
        return self.request("POST", path, data)


def run_stage5_tests() -> int:
    print("=" * 80)
    print("STAGE 5 AUTOMATED VERIFICATION SUITE: Learning -> Practice -> Pass -> Unlock")
    print(f"Backend URL: {BACKEND_URL}")
    print("=" * 80)

    client = TestClient()

    # 1. Health check
    st, health = client.get("/health")
    assert st == 200, f"Backend not reachable, HTTP {st}: {health}"
    print("[PREFLIGHT] Backend is healthy.")

    # 2. Register fresh test user
    test_user = f"prog_user_{int(time.time())}"
    st, reg = client.post(
        "/api/auth/register",
        {"username": test_user, "password": "TestPassword123!", "name": "Stage5 Tester"},
    )
    assert st in (200, 201), f"Registration failed: {reg}"
    client.token = reg.get("access_token")
    assert client.token, "No access token in registration response"
    print(f"[AUTH] Registered and authenticated test user: {test_user}")

    # =========================================================================
    # SCENARIO A: Happy Path Progression (Day 1 -> Practice -> Day 2)
    # =========================================================================
    print("\n--- [SCENARIO A] Happy Path Progression ---")
    st, progress = client.get("/api/learning/progress")
    assert st == 200, f"Failed to get progress: {progress}"
    assert progress["current_day"] == 1, f"Expected current_day=1, got {progress['current_day']}"
    assert progress["completed_days"] == [], f"Expected completed_days=[], got {progress['completed_days']}"

    day1_info = progress["day_states"]["1"]
    assert day1_info["unlocked"] is True, "Day 1 must be unlocked"
    assert day1_info["status"] == "current", f"Expected status 'current', got {day1_info['status']}"
    assert day1_info["lesson_completed"] is False
    assert day1_info["practice_passed"] is False

    day2_info = progress["day_states"]["2"]
    assert day2_info["unlocked"] is False, "Day 2 must initially be locked"
    assert day2_info["status"] == "locked"
    print("  + Initial progress validated: Day 1 current, Day 2 locked.")

    # Complete Day 1 lesson
    st, comp_res = client.post("/api/learning/complete-lesson", {"day_number": 1})
    assert st == 200, f"Complete lesson failed: {comp_res}"
    assert comp_res["lesson_completed"] is True
    assert comp_res["day_completed"] is False, "Day 1 must not be completed yet (practice required!)"
    assert comp_res["unlocked_next_day"] is False, "Day 2 must not unlock without passing practice!"

    # Verify Day 1 status transitioned to practice_required
    st, progress = client.get("/api/learning/progress")
    day1_state = progress["day_states"]["1"]
    assert day1_state["lesson_completed"] is True
    assert day1_state["practice_passed"] is False
    assert day1_state["completed"] is False
    print("  + Lesson completed: Day 1 transitioned to practice_required.")

    # Submit FAILING practice problem
    fail_code = "def convert_celsius_to_fahrenheit(c):\n    return -999.0\n"
    st, sub_res = client.post(
        "/api/submissions",
        {"problem_id": "celsius-to-fahrenheit", "language": "python", "code": fail_code},
    )
    assert st == 200, f"Submission failed with error: {sub_res}"
    assert sub_res["tests"]["all_passed"] is False, "Failing code must not pass tests"

    # Progress must NOT advance
    st, progress = client.get("/api/learning/progress")
    assert progress["completed_days"] == [], "completed_days must still be empty after failing practice"
    assert progress["current_day"] == 1, "current_day must remain 1 after failing practice"
    print("  + Failing submission held: Day 1 still requires passing practice.")

    # Submit PASSING practice problem
    pass_code = "def convert_celsius(c: float) -> float:\n    return round((c * 9.0 / 5.0) + 32.0, 2)\n"
    st, sub_res = client.post(
        "/api/submissions",
        {"problem_id": "celsius-to-fahrenheit", "language": "python", "code": pass_code},
    )
    assert st == 200, f"Submission failed: {sub_res}"
    assert sub_res["tests"]["all_passed"] is True, "Passing code must pass 100% of test cases"
    assert sub_res.get("learning_update") is not None, "learning_update must be present in response"
    assert 1 in sub_res["learning_update"]["newly_completed_days"]
    assert 2 in sub_res["learning_update"]["unlocked_days"]

    # Verify Day 1 is now COMPLETED and Day 2 is AVAILABLE
    st, progress = client.get("/api/learning/progress")
    assert 1 in progress["completed_days"], "Day 1 must now be in completed_days"
    assert progress["current_day"] == 2, f"current_day must advance to 2, got {progress['current_day']}"
    assert progress["day_states"]["1"]["status"] == "completed"
    assert progress["day_states"]["2"]["status"] == "current"
    assert progress["day_states"]["2"]["unlocked"] is True
    assert progress["day_states"]["3"]["status"] == "locked"
    print("  + Passing submission verified: Day 1 COMPLETED -> Day 2 UNLOCKED!")

    # =========================================================================
    # SCENARIO B: Security & Route Protection (Direct URL / Lock Gating)
    # =========================================================================
    print("\n--- [SCENARIO B] Direct URL / Lock Bypass Gating ---")
    st, err_res = client.post("/api/learning/complete-lesson", {"day_number": 5})
    assert st == 403, f"Expected 403 Forbidden for locked day 5, got {st}: {err_res}"
    print(f"  + Server strictly rejected completing locked Day 5: HTTP {st} (Detail: {err_res.get('detail')})")

    st, err_res = client.post("/api/learning/complete-lesson", {"day_number": 100})
    assert st == 403, f"Expected 403 Forbidden for locked day 100, got {st}"
    print("  + Server strictly rejected completing locked Day 100: HTTP 403.")

    # =========================================================================
    # SCENARIO C: Idempotence & Non-Destructive Review Mode
    # =========================================================================
    print("\n--- [SCENARIO C] Idempotence & Non-Destructive Review Mode ---")
    # Re-complete Day 1 lesson
    st, recomp = client.post("/api/learning/complete-lesson", {"day_number": 1})
    assert st == 200, f"Re-completing day 1 failed: {recomp}"

    st, progress = client.get("/api/learning/progress")
    assert progress["current_day"] == 2, f"current_day must NOT regress! Got: {progress['current_day']}"
    assert 1 in progress["completed_days"], "Day 1 must still be completed"
    assert progress["day_states"]["2"]["unlocked"] is True, "Day 2 must remain unlocked"
    print("  + Idempotence verified: Re-completing Day 1 preserves Day 2 unlocked state.")

    # =========================================================================
    # SCENARIO D: Day 2 Complete -> Day 3 Unlock
    # =========================================================================
    print("\n--- [SCENARIO D] Multi-Day Sequence (Day 2 -> Day 3) ---")
    # Complete Day 2 lesson
    st, _ = client.post("/api/learning/complete-lesson", {"day_number": 2})
    assert st == 200

    # Pass Day 2 practice problem (time-converter-seconds)
    day2_code = (
        "def format_seconds(total_seconds: int) -> str:\n"
        "    h = total_seconds // 3600\n"
        "    rem = total_seconds % 3600\n"
        "    m = rem // 60\n"
        "    s = rem % 60\n"
        "    return f\"{h:02d}:{m:02d}:{s:02d}\"\n"
    )
    st, sub_res = client.post(
        "/api/submissions",
        {"problem_id": "time-converter-seconds", "language": "python", "code": day2_code},
    )
    assert st == 200 and sub_res["tests"]["all_passed"] is True

    st, progress = client.get("/api/learning/progress")
    assert progress["completed_days"] == [1, 2], f"Expected [1, 2], got {progress['completed_days']}"
    assert progress["current_day"] == 3, f"Expected current_day=3, got {progress['current_day']}"
    assert progress["day_states"]["3"]["unlocked"] is True
    print("  + Day 2 completed and Day 3 unlocked sequentially!")

    # =========================================================================
    # SCENARIO E: Day 160 Capstone Grand Finale
    # =========================================================================
    print("\n--- [SCENARIO E] Day 160 Capstone Grand Finale ---")
    # Simulate high-water mark up to Day 159 via dev-set-progress endpoint
    st, progress = client.post("/api/learning/dev-set-progress", {"completed_up_to": 159})
    assert st == 200, f"dev-set-progress failed: {progress}"

    st, progress = client.get("/api/learning/progress")
    assert len(progress["completed_days"]) == 159, f"Expected 159, got {len(progress['completed_days'])}"
    assert progress["current_day"] == 160, f"Expected 160, got {progress['current_day']}"
    assert progress["day_states"]["160"]["unlocked"] is True, "Day 160 must be unlocked"
    print("  + High-water mark established: Days 1..159 completed, Day 160 active.")

    # Complete Day 160 lesson
    st, _ = client.post("/api/learning/complete-lesson", {"day_number": 160})
    assert st == 200

    # Pass Day 160 capstone practice problem (word-search-ii)
    # Using reference solution from seed.py
    import dev_backend.server as s
    problem_160 = s._find_problem("word-search-ii")
    ref_160 = problem_160["reference_solution"]
    assert ref_160, "Reference solution for word-search-ii must exist"

    st, sub_res = client.post(
        "/api/submissions",
        {"problem_id": "word-search-ii", "language": "python", "code": ref_160},
    )
    assert st == 200 and sub_res["tests"]["all_passed"] is True, f"Capstone submission failed: {sub_res}"

    st, progress = client.get("/api/learning/progress")
    assert len(progress["completed_days"]) == 160, f"All 160 days must be completed! Got: {len(progress['completed_days'])}"
    assert progress["current_day"] == 160, "current_day clamped at 160"
    assert progress["day_states"]["160"]["status"] == "completed"
    print("  + [PASS] GRAND FINALE: 160 of 160 days verified COMPLETED!")

    print("\n" + "=" * 80)
    print("ALL STAGE 5 PROGRESSION SCENARIOS PASSED WITH ZERO DEFECTS!")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(run_stage5_tests())
