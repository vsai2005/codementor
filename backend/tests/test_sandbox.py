"""Sandbox tests. These are the ones that catch real bugs (BUILD_PROMPTS).

If the API process hangs while running these, the sandbox is wrong.
"""

import time

import pytest

from app.services import sandbox

TWO_SUM_CASES = [
    {"args": [[2, 7, 11, 15], 9], "expected": [0, 1]},
    {"args": [[3, 2, 4], 6], "expected": [1, 2]},
    {"args": [[3, 3], 6], "expected": [0, 1]},
    {"args": [[], 0], "expected": []},              # edge: empty
    {"args": [[1], 1], "expected": []},             # edge: single element
    {"args": [[-3, 4, 3, 90], 0], "expected": [0, 2]},  # edge: negatives
]

CORRECT = """
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return []
"""

WRONG = """
def two_sum(nums, target):
    # off by one: skips the final element
    for i in range(len(nums)):
        for j in range(i + 1, len(nums) - 1):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
"""


def test_correct_solution_passes_every_case():
    report = sandbox.run_test_cases(CORRECT, "two_sum", TWO_SUM_CASES)
    assert report.all_passed, [(r.index, r.status, r.returned) for r in report.results]
    assert report.passed_count == 6


def test_wrong_solution_fails_only_the_cases_it_should():
    report = sandbox.run_test_cases(WRONG, "two_sum", TWO_SUM_CASES)
    assert not report.all_passed
    assert report.passed_count > 0, "a partially-wrong solution must still pass some cases"
    failed = {r.index for r in report.results if not r.passed}
    assert 1 in failed  # [3,2,4] target 6 needs the last element
    assert all(r.status in ("ok", "wrong_answer") for r in report.results)


def test_infinite_loop_times_out_without_hanging_the_caller():
    code = "def solve():\n    while True:\n        pass\n"
    started = time.perf_counter()
    report = sandbox.run_test_cases(code, "solve", [{"args": [], "expected": None}])
    elapsed = time.perf_counter() - started

    assert report.results[0].status == "timeout"
    assert not report.results[0].passed
    assert elapsed < sandbox.WALL_SECONDS + 3, f"caller was blocked for {elapsed:.1f}s"


def test_sleeping_code_is_killed_by_the_wall_clock_not_cpu_limit():
    # Burns no CPU, so RLIMIT_CPU never fires. Only the wall timeout catches it.
    code = "import time\ndef solve():\n    time.sleep(600)\n"
    started = time.perf_counter()
    report = sandbox.run_test_cases(code, "solve", [{"args": [], "expected": None}])
    elapsed = time.perf_counter() - started

    assert report.results[0].status == "timeout"
    assert elapsed < sandbox.WALL_SECONDS + 3


def test_memory_bomb_is_killed_cleanly():
    code = "def solve():\n    x = [0] * (10 ** 9)\n    return len(x)\n"
    report = sandbox.run_test_cases(code, "solve", [{"args": [], "expected": 10 ** 9}])
    result = report.results[0]
    assert not result.passed
    assert result.status in ("memory", "error"), result.status
    assert "MemoryError" in result.stderr or "Memory Limit" in result.stderr


def test_network_access_is_denied():
    code = (
        "import socket\n"
        "def solve():\n"
        "    s = socket.create_connection(('1.1.1.1', 80), timeout=3)\n"
        "    return 'CONNECTED'\n"
    )
    report = sandbox.run_test_cases(code, "solve", [{"args": [], "expected": "CONNECTED"}])
    result = report.results[0]
    assert not result.passed, "user code reached the network"
    assert result.returned != "CONNECTED"


def test_network_denied_via_urllib_too():
    code = (
        "def solve():\n"
        "    import urllib.request\n"
        "    return urllib.request.urlopen('http://1.1.1.1', timeout=3).status\n"
    )
    report = sandbox.run_test_cases(code, "solve", [{"args": [], "expected": 200}])
    assert not report.results[0].passed


def test_syntax_error_returns_clean_failure_not_a_crash():
    code = "def solve(:\n    return 1\n"
    report = sandbox.run_test_cases(code, "solve", [{"args": [], "expected": 1}])
    result = report.results[0]
    assert result.status == "error"
    assert "SyntaxError" in result.stderr
    assert not result.passed


def test_runtime_exception_is_reported_not_raised():
    code = "def solve():\n    return 1 / 0\n"
    report = sandbox.run_test_cases(code, "solve", [{"args": [], "expected": 1}])
    assert report.results[0].status == "error"
    assert "ZeroDivisionError" in report.results[0].stderr


def test_missing_entry_point_is_a_clean_error():
    report = sandbox.run_test_cases("x = 1\n", "solve", [{"args": [], "expected": 1}])
    assert report.results[0].status == "error"
    assert "MissingEntryPoint" in report.results[0].stderr


def test_stdout_is_truncated_at_10kb():
    code = "def solve():\n    print('A' * 50000)\n    return 1\n"
    report = sandbox.run_test_cases(code, "solve", [{"args": [], "expected": 1}])
    result = report.results[0]
    assert result.passed
    assert len(result.stdout) <= sandbox.MAX_OUTPUT_BYTES


def test_filesystem_writes_outside_tmp_are_denied():
    code = (
        "def solve():\n"
        "    open('/etc/codementor_pwned', 'w').write('x')\n"
        "    return 'WROTE'\n"
    )
    report = sandbox.run_test_cases(code, "solve", [{"args": [], "expected": "WROTE"}])
    assert not report.results[0].passed


def test_runtime_is_measured():
    report = sandbox.run_test_cases(CORRECT, "two_sum", TWO_SUM_CASES[:1])
    assert report.results[0].runtime_ms >= 0
    assert report.results[0].runtime_ms < 7000
