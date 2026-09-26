"""Physical process-tree memory accounting for the sandbox watchdog."""

from __future__ import annotations

import asyncio
import os
import subprocess
import sys
import time

import psutil
import pytest

from app.services import sandbox


MIB = 1024 * 1024


def _wait_for_memory(pid: int, minimum: int, timeout: float = 4.0) -> int:
    deadline = time.monotonic() + timeout
    observed = 0
    while time.monotonic() < deadline:
        observed = sandbox._get_process_tree_rss(pid) or 0
        if observed >= minimum:
            return observed
        time.sleep(0.02)
    return observed


def _stop_helper(proc: subprocess.Popen) -> None:
    sandbox._kill_process_group(proc.pid, isolated_group=sys.platform != "win32")
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=3)
    if proc.stdout:
        proc.stdout.close()


def test_near_limit_single_workload_succeeds(monkeypatch):
    # Isolate the memory boundary from cold-start CPU cost in emulated CI hosts.
    # The normal CPU and wall policies are exercised by the existing suites.
    monkeypatch.setattr(sandbox, "CPU_SECONDS", 5)
    monkeypatch.setattr(sandbox, "WALL_SECONDS", 10)
    code = """
def solve():
    data = bytearray(205 * 1024 * 1024)
    for index in range(0, len(data), 4096):
        data[index] = 1
    return len(data)
"""
    result = sandbox.run_test_cases(code, "solve", [{"args": [], "expected": 205 * MIB}]).results[0]
    assert result.passed, f"status={result.status}, stderr={result.stderr}"


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="Linux PSS accounting")
def test_forked_shared_pages_are_not_double_counted():
    # A trusted helper models fork/COW; user code cannot call os.fork in the sandbox.
    helper = """
import os, time
shared = bytearray(110 * 1024 * 1024)
for index in range(0, len(shared), 4096):
    shared[index] = 1
for _ in range(2):
    child = os.fork()
    if child == 0:
        time.sleep(15)
        os._exit(0)
print('ready', flush=True)
time.sleep(15)
"""
    proc = subprocess.Popen(
        [sys.executable, "-c", helper], stdout=subprocess.PIPE, text=True, start_new_session=True
    )
    try:
        assert proc.stdout and proc.stdout.readline().strip() == "ready"
        parent = psutil.Process(proc.pid)
        children = parent.children(recursive=True)
        assert len(children) == 2
        naive_rss = sum(member.memory_info().rss for member in [parent, *children])
        charged = _wait_for_memory(proc.pid, 100 * MIB)
        assert naive_rss > sandbox.MEMORY_BYTES
        assert 100 * MIB < charged < sandbox.MEMORY_BYTES
    finally:
        _stop_helper(proc)


def test_private_memory_of_multiple_descendants_is_combined():
    helper = """
import subprocess, sys, time
child_code = 'import time; data = bytearray(145 * 1024 * 1024); data[::4096] = bytes(len(data[::4096])); time.sleep(15)'
children = [subprocess.Popen([sys.executable, '-c', child_code]) for _ in range(2)]
print('ready', flush=True)
time.sleep(15)
"""
    proc = subprocess.Popen(
        [sys.executable, "-c", helper], stdout=subprocess.PIPE, text=True,
        start_new_session=sys.platform != "win32",
    )
    try:
        assert proc.stdout and proc.stdout.readline().strip() == "ready"
        charged = _wait_for_memory(proc.pid, sandbox.MEMORY_BYTES + 1)
        assert charged > sandbox.MEMORY_BYTES
    finally:
        _stop_helper(proc)


def test_exiting_child_during_memory_polling_is_safe():
    helper = """
import subprocess, sys, time
subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(0.05)'])
print('ready', flush=True)
time.sleep(0.3)
"""
    proc = subprocess.Popen(
        [sys.executable, "-c", helper], stdout=subprocess.PIPE, text=True,
        start_new_session=sys.platform != "win32",
    )
    try:
        assert proc.stdout and proc.stdout.readline().strip() == "ready"
        for _ in range(20):
            value = sandbox._get_process_tree_rss(proc.pid)
            assert value is None or value >= 0
            time.sleep(0.01)
    finally:
        _stop_helper(proc)


@pytest.mark.asyncio
async def test_concurrent_sandbox_executions_leave_no_watchdogs():
    code = "def solve(value):\n    return value * value\n"
    results = await asyncio.gather(*(
        sandbox._run_one_async(code, "solve", [value], value * value, value)
        for value in range(6)
    ))
    assert all(result.passed for result in results)
    await asyncio.sleep(0)
    assert not any(
        task.get_coro().__name__ == "_watch_process_memory"
        for task in asyncio.all_tasks()
    )


@pytest.mark.asyncio
async def test_script_cpu_or_wall_timeout_is_not_reported_as_memory():
    result = await sandbox.execute_script_async("while True:\n    pass\n")
    assert result["status"] == "timeout"
