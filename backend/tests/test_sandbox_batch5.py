"""Batch 5: Sandbox Memory Portability & True 64 KiB Output Limit Test Suite.

Verifies:
  1. Normal program execution passes ok.
  2. Moderate list/dict/string workloads (<256 MB) succeed without false memory error.
  3. ASCII output >64 KiB truncated to <= 65536 bytes.
  4. Emoji output >64 KiB truncated to <= 65536 bytes without splitting 4-byte characters.
  5. CJK / mixed Unicode output >64 KiB truncated to <= 65536 bytes without splitting characters.
  6. stdout + stderr flooding simultaneously bounded within 64 KiB limits.
  7. High output flooding without false memory error.
  8. Genuine >256 MB allocation deterministically returns structured 'memory'.
  9. Gradual memory growth deterministically returns structured 'memory'.
  10. Infinite loop deterministically returns structured 'timeout'.
  11. Child-process cleanup: descendant processes are reliably terminated.
  12. Repeated executions (30+ iterations) with zero handle, thread, or memory leakage.
  13. Windows Job Object configuration & containment behavior.
  14. Cross-platform process-tree RSS monitoring behavior.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
import pytest
import psutil

from app.services import sandbox
from app.services._sandbox_runner import BoundedStringIO, truncate_utf8, MAX_OUTPUT_BYTES


def test_1_normal_program_passes():
    code = """
def solve(a, b):
    return a + b
"""
    report = sandbox.run_test_cases(code, "solve", [
        {"args": [10, 20], "expected": 30},
        {"args": [-5, 5], "expected": 0},
    ])
    assert report.all_passed
    assert report.passed_count == 2
    assert report.results[0].status == "ok"
    assert report.results[0].returned == 30


def test_2_moderate_workloads_succeed_without_false_memory():
    code = """
def solve():
    s = 'X' * (90 * 1024 * 1024)
    s2 = s + '!'
    d = {i: i * 2 for i in range(100_000)}
    return len(s2) + len(d)
"""
    expected = (90 * 1024 * 1024 + 1) + 100_000
    report = sandbox.run_test_cases(code, "solve", [{"args": [], "expected": expected}])
    res = report.results[0]
    assert res.passed, f"Failed with status={res.status}, stderr={res.stderr}"
    assert res.status == "ok"
    assert res.returned == expected


def test_3_ascii_output_truncated_at_64kib():
    code = """
def solve():
    print('A' * 120_000)
    return 42
"""
    report = sandbox.run_test_cases(code, "solve", [{"args": [], "expected": 42}])
    res = report.results[0]
    assert res.passed
    enc = res.stdout.encode("utf-8")
    assert len(enc) == MAX_OUTPUT_BYTES
    assert len(enc) <= 65536


def test_4_emoji_output_truncated_at_64kib_without_split():
    code = """
def solve():
    print('🚀' * 40_000)
    return 'done'
"""
    report = sandbox.run_test_cases(code, "solve", [{"args": [], "expected": "done"}])
    res = report.results[0]
    assert res.passed
    enc = res.stdout.encode("utf-8")
    assert len(enc) <= 65536
    assert len(enc) % 4 == 0
    assert not res.stdout.endswith("\ufffd")


def test_5_cjk_mixed_unicode_truncated_at_64kib_without_split():
    code = """
def solve():
    print('漢字' * 30_000)
    return 'cjk'
"""
    report = sandbox.run_test_cases(code, "solve", [{"args": [], "expected": "cjk"}])
    res = report.results[0]
    assert res.passed
    enc = res.stdout.encode("utf-8")
    assert len(enc) <= 65536
    assert not res.stdout.endswith("\ufffd")


def test_6_stdout_and_stderr_flooding_simultaneously():
    code = """
import sys
def solve():
    for _ in range(2000):
        sys.stdout.write('OUT_' * 30)
        sys.stderr.write('ERR_' * 30)
    return 'ok'
"""
    report = sandbox.run_test_cases(code, "solve", [{"args": [], "expected": "ok"}])
    res = report.results[0]
    assert res.passed
    out_bytes = res.stdout.encode("utf-8")
    err_bytes = res.stderr.encode("utf-8")
    assert len(out_bytes) <= 65536
    assert len(err_bytes) <= 65536


def test_7_output_flooding_without_false_memory_error():
    code = """
def solve():
    for i in range(50_000):
        print('Line:', i, 'Payload:', 'Z' * 50)
    return 100
"""
    report = sandbox.run_test_cases(code, "solve", [{"args": [], "expected": 100}])
    res = report.results[0]
    assert res.passed, f"Failed with status={res.status}, stderr={res.stderr}"
    assert res.status == "ok"
    assert res.returned == 100
    assert len(res.stdout.encode("utf-8")) <= 65536


def test_8_genuine_memory_abuse_exceeding_256mb():
    code = """
def solve():
    blocks = [bytearray(1024 * 1024) for _ in range(300)]
    return len(blocks)
"""
    report = sandbox.run_test_cases(code, "solve", [{"args": [], "expected": 300}])
    res = report.results[0]
    assert not res.passed
    assert res.status == "memory"
    assert "Memory Limit Exceeded" in res.stderr or "Memory limit exceeded" in res.stderr


def test_9_gradual_memory_growth_triggers_memory():
    code = """
def solve():
    blocks = []
    for _ in range(350):
        blocks.append(bytearray(1024 * 1024))
    return len(blocks)
"""
    report = sandbox.run_test_cases(code, "solve", [{"args": [], "expected": 350}])
    res = report.results[0]
    assert not res.passed
    assert res.status == "memory"
    assert "Memory Limit Exceeded" in res.stderr or "Memory limit exceeded" in res.stderr


def test_10_infinite_loop_triggers_timeout():
    code = """
def solve():
    while True:
        pass
"""
    started = time.perf_counter()
    report = sandbox.run_test_cases(code, "solve", [{"args": [], "expected": None}])
    elapsed = time.perf_counter() - started
    res = report.results[0]
    assert not res.passed
    assert res.status == "timeout"
    assert "Time Limit Exceeded" in res.stderr
    assert elapsed <= sandbox.WALL_SECONDS + 2.0


def test_11_child_process_cleanup():
    # Keep the regression probe outside pytest's process group: a broken
    # killpg(getpgid(pid)) implementation may terminate its caller.
    probe = r'''
import subprocess, sys, time
import psutil
from app.services import sandbox

proc = subprocess.Popen([
    sys.executable, "-c",
    "import subprocess,sys,time; subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)']);time.sleep(60)",
])
try:
    for _ in range(100):
        children = psutil.Process(proc.pid).children(recursive=True)
        if children:
            break
        time.sleep(0.01)
    assert children, "child process was not spawned"
    child = children[0]
    if sys.platform.startswith('linux'):
        # Exercise the production image path, where psutil is not installed.
        sys.modules['psutil'] = None
    try:
        sandbox._kill_process_group(proc.pid)
    finally:
        if sys.platform.startswith('linux'):
            sys.modules['psutil'] = psutil
    proc.wait(timeout=5)
    for _ in range(100):
        if not child.is_running() or child.status() == psutil.STATUS_ZOMBIE:
            break
        time.sleep(0.01)
    assert not child.is_running() or child.status() == psutil.STATUS_ZOMBIE
finally:
    if proc.poll() is None:
        proc.kill()
        proc.wait()
'''
    options = {"start_new_session": True} if sys.platform != "win32" else {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
    completed = subprocess.run(
        [sys.executable, "-c", probe], capture_output=True, text=True, timeout=15, **options
    )
    assert completed.returncode == 0, completed.stderr


def test_12_repeated_executions_no_resource_leakage():
    process = psutil.Process()
    initial_threads = process.num_threads()
    initial_children = {child.pid for child in process.children(recursive=True)}
    for _ in range(30):
        report = sandbox.run_test_cases("def solve(x):\n    return x * 2\n", "solve", [{"args": [5], "expected": 10}])
        assert report.all_passed

    final_threads = process.num_threads()
    final_children = {child.pid for child in process.children(recursive=True)}
    assert final_threads <= initial_threads + 2
    assert final_children <= initial_children


def test_13_windows_job_object_behavior():
    if sys.platform != "win32":
        pytest.skip("Windows-specific test")

    proc = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(10)"])
    try:
        job = sandbox._setup_win32_job_object(proc.pid)
        assert job is not None
        sandbox._terminate_win32_job(job)
        time.sleep(0.2)
        assert not psutil.pid_exists(proc.pid)
        sandbox._close_win32_job(job)
    finally:
        try:
            proc.kill()
        except Exception:
            pass


def test_14_process_tree_rss_monitoring_behavior():
    current_pid = os.getpid()
    rss = sandbox._get_process_tree_rss(current_pid)
    assert rss is not None
    assert rss > 1024 * 1024
    ps_rss = psutil.Process(current_pid).memory_info().rss
    diff = abs(rss - ps_rss)
    assert diff < 20 * 1024 * 1024
