"""Sandboxed execution of untrusted user code (PRD 5.5).

Design: one subprocess per test case. That gives a clean per-case CPU budget
and means a single hostile case cannot poison the others.

Two independent timeouts are required and they catch different attacks:
  * RLIMIT_CPU  -- kills `while True: pass` (burns CPU)
  * wall clock  -- kills `time.sleep(3600)` (burns no CPU at all)

Neither alone is sufficient. The child is started in its own session so the
parent can kill the entire process group, not just the direct child.
"""

from __future__ import annotations

import json
import os
import pwd
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

CPU_SECONDS = 5
WALL_SECONDS = 7  # > CPU limit, so RLIMIT_CPU wins where it applies
MEMORY_BYTES = 256 * 1024 * 1024
MAX_OUTPUT_BYTES = 10 * 1024

_RUNNER = str(Path(__file__).with_name("_sandbox_runner.py"))
_UNPRIVILEGED_USER = "nobody"


@dataclass
class TestResult:
    __test__ = False  # not a pytest collection target

    index: int
    passed: bool
    status: str  # ok | wrong_answer | timeout | memory | error
    runtime_ms: int
    stdout: str = ""
    stderr: str = ""
    expected: Any = None
    returned: Any = None


@dataclass
class ExecutionReport:
    results: list[TestResult] = field(default_factory=list)
    network_isolated: bool = False

    @property
    def passed_count(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def all_passed(self) -> bool:
        return self.total > 0 and self.passed_count == self.total

    @property
    def timed_out(self) -> bool:
        return any(r.status == "timeout" for r in self.results)


def _unprivileged_ids() -> tuple[int, int]:
    if os.getuid() != 0:
        return os.getuid(), os.getgid()
    try:
        entry = pwd.getpwnam(_UNPRIVILEGED_USER)
        return entry.pw_uid, entry.pw_gid
    except KeyError:
        return 65534, 65534


def _network_namespace_available() -> bool:
    """Probe once whether we can actually unshare a network namespace."""
    if not shutil.which("unshare"):
        return False
    try:
        probe = subprocess.run(
            ["unshare", "-n", "true"],
            capture_output=True,
            timeout=5,
        )
        return probe.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


_NETNS_AVAILABLE: bool | None = None


def network_isolation_available() -> bool:
    global _NETNS_AVAILABLE
    if _NETNS_AVAILABLE is None:
        _NETNS_AVAILABLE = _network_namespace_available()
    return _NETNS_AVAILABLE


def _build_argv() -> list[str]:
    base = [sys.executable, "-I", "-B", _RUNNER]
    if network_isolation_available():
        return ["unshare", "-n", *base]
    return base


def _run_one(code: str, entry_point: str, args: list, expected: Any, index: int) -> TestResult:
    uid, gid = _unprivileged_ids()
    workdir = tempfile.mkdtemp(prefix="cm_sbx_")
    os.chmod(workdir, 0o777)

    job = json.dumps(
        {
            "code": code,
            "entry_point": entry_point,
            "args": args,
            "uid": uid,
            "gid": gid,
            "cpu_seconds": CPU_SECONDS,
            "memory_bytes": MEMORY_BYTES,
        }
    )

    started = time.perf_counter()
    proc = subprocess.Popen(
        _build_argv(),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=workdir,
        env={"PATH": "/usr/bin:/bin", "HOME": workdir, "TMPDIR": workdir},
        start_new_session=True,  # own process group, so we can kill descendants
        text=True,
    )

    try:
        raw_out, raw_err = proc.communicate(job, timeout=WALL_SECONDS)
        timed_out = False
    except subprocess.TimeoutExpired:
        _kill_group(proc)
        raw_out, raw_err = "", "wall-clock limit exceeded"
        timed_out = True
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    runtime_ms = int((time.perf_counter() - started) * 1000)

    if timed_out:
        return TestResult(index, False, "timeout", runtime_ms,
                          stderr="Time Limit Exceeded", expected=expected)

    # RLIMIT_CPU raises SIGXCPU; RLIMIT_AS usually surfaces as MemoryError but
    # can also SIGKILL if the allocation happens inside the interpreter core.
    if proc.returncode and proc.returncode < 0:
        sig = -proc.returncode
        if sig in (signal.SIGXCPU, signal.SIGKILL) and runtime_ms >= CPU_SECONDS * 900:
            return TestResult(index, False, "timeout", runtime_ms,
                              stderr="Time Limit Exceeded", expected=expected)
        return TestResult(index, False, "memory", runtime_ms,
                          stderr="Memory Limit Exceeded", expected=expected)

    try:
        payload = json.loads(raw_out)
    except (ValueError, TypeError):
        return TestResult(
            index, False, "error", runtime_ms,
            stderr=(raw_err or "sandbox produced no parseable output")[:2000],
            expected=expected,
        )

    status = payload.get("status")
    stdout = payload.get("stdout", "")[:MAX_OUTPUT_BYTES]

    if status == "memory":
        return TestResult(index, False, "memory", runtime_ms,
                          stderr="Memory Limit Exceeded", expected=expected)
    if status == "error":
        return TestResult(
            index, False, "error", runtime_ms, stdout=stdout,
            stderr=f"{payload.get('error_type')}: {payload.get('stderr', '')}"[:2000],
            expected=expected,
        )

    returned = payload.get("returned")
    passed = returned == expected
    return TestResult(
        index, passed, "ok" if passed else "wrong_answer", runtime_ms,
        stdout=stdout, expected=expected, returned=returned,
    )


def _kill_group(proc: subprocess.Popen) -> None:
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        proc.kill()
    try:
        proc.communicate(timeout=2)
    except subprocess.SubprocessError:
        pass


def run_test_cases(code: str, entry_point: str, test_cases: list[dict]) -> ExecutionReport:
    """Run `code` against every test case. Never raises on user error."""
    report = ExecutionReport(network_isolated=network_isolation_available())
    for i, case in enumerate(test_cases):
        report.results.append(
            _run_one(code, entry_point, case.get("args", []), case.get("expected"), i)
        )
    return report
