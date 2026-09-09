"""Sandboxed execution of untrusted user code (Phase 1).

Zero-trust process isolation:
  - Kernel-level rlimits (2s CPU, 256MB AS, 10 NPROC, 1MB FSIZE)
  - Async process execution via `asyncio.create_subprocess_exec`
  - Sterile minimal environment (dropping all secrets from os.environ)
  - 3.5s execution deadline via `asyncio.wait_for` with process-group SIGKILL on timeout
  - Standard I/O streams capped at 64 KB
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import signal
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

CPU_SECONDS = 2
WALL_SECONDS = 3.5
MEMORY_BYTES = 256 * 1024 * 1024
MAX_OUTPUT_BYTES = 64 * 1024

_RUNNER = str(Path(__file__).with_name("_sandbox_runner.py"))
_UNPRIVILEGED_USER = "nobody"

CLEAN_ENV = {
    "PATH": "/usr/local/bin:/usr/bin:/bin",
    "PYTHONUNBUFFERED": "1",
    "PYTHONDONTWRITEBYTECODE": "1",
}


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
    if not hasattr(os, "getuid") or os.getuid() != 0:
        return 65534, 65534
    try:
        import pwd
        entry = pwd.getpwnam(_UNPRIVILEGED_USER)
        return entry.pw_uid, entry.pw_gid
    except (KeyError, ImportError):
        return 65534, 65534


def _network_namespace_available() -> bool:
    """Probe whether unshare -n can be invoked."""
    if not shutil.which("unshare"):
        return False
    try:
        probe = shutil.which("unshare")
        if not probe:
            return False
        import subprocess
        res = subprocess.run(["unshare", "-n", "true"], capture_output=True, timeout=3)
        return res.returncode == 0
    except (OSError, Exception):
        return False


_NETNS_AVAILABLE: bool | None = None


def network_isolation_available() -> bool:
    global _NETNS_AVAILABLE
    if _NETNS_AVAILABLE is None:
        _NETNS_AVAILABLE = _network_namespace_available()
    return _NETNS_AVAILABLE


def _build_argv() -> list[str]:
    base = [sys.executable, "-I", "-s", "-B", _RUNNER]
    if network_isolation_available():
        return ["unshare", "-n", *base]
    return base


def _posix_preexec():
    if hasattr(os, "setsid"):
        try:
            os.setsid()
        except OSError:
            pass


def _kill_process_group(pid: int) -> None:
    sigkill = getattr(signal, "SIGKILL", getattr(signal, "SIGTERM", 9))
    if hasattr(os, "killpg") and hasattr(os, "getpgid"):
        try:
            pgid = os.getpgid(pid)
            os.killpg(pgid, sigkill)
            return
        except (ProcessLookupError, PermissionError, OSError):
            pass
    try:
        os.kill(pid, sigkill)
    except (ProcessLookupError, PermissionError, OSError):
        pass


async def _run_one_async(code: str, entry_point: str, args: list, expected: Any, index: int) -> TestResult:
    uid, gid = _unprivileged_ids()
    workdir = tempfile.mkdtemp(prefix="cm_sbx_")
    try:
        os.chmod(workdir, 0o777)
    except OSError:
        pass

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

    env = dict(CLEAN_ENV)
    env["HOME"] = workdir
    env["TMPDIR"] = workdir

    started = time.perf_counter()
    argv = _build_argv()
    preexec = _posix_preexec if sys.platform != "win32" else None

    proc = None
    try:
        proc = await asyncio.create_subprocess_exec(
            *argv,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=workdir,
            env=env,
            preexec_fn=preexec,
        )

        stdout_bytes, stderr_bytes = await asyncio.wait_for(
            proc.communicate(input=job.encode("utf-8")),
            timeout=WALL_SECONDS,
        )
        timed_out = False
    except (asyncio.TimeoutError, TimeoutError):
        timed_out = True
        if proc and proc.pid:
            _kill_process_group(proc.pid)
            try:
                await proc.wait()
            except Exception:
                pass
        stdout_bytes = b""
        stderr_bytes = b"Time Limit Exceeded"
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    runtime_ms = int((time.perf_counter() - started) * 1000)

    if timed_out:
        return TestResult(
            index=index,
            passed=False,
            status="timeout",
            runtime_ms=runtime_ms,
            stderr="Time Limit Exceeded",
            expected=expected,
        )

    # Decode and parse payload envelope (captured stdout in payload is capped at 64 KB)
    raw_out = stdout_bytes[: 512 * 1024].decode("utf-8", "replace")
    raw_err = stderr_bytes[:MAX_OUTPUT_BYTES].decode("utf-8", "replace")

    # Check return code signal on POSIX
    if proc and proc.returncode and proc.returncode < 0:
        sig = -proc.returncode
        if (hasattr(signal, "SIGXCPU") and sig == signal.SIGXCPU) or sig in (
            getattr(signal, "SIGKILL", 9),
            getattr(signal, "SIGTERM", 15),
        ):
            return TestResult(index, False, "timeout", runtime_ms, stderr="Time Limit Exceeded", expected=expected)
        return TestResult(index, False, "memory", runtime_ms, stderr="Memory Limit Exceeded (256 MB)", expected=expected)

    try:
        payload = json.loads(raw_out)
    except (ValueError, TypeError):
        return TestResult(
            index,
            False,
            "error",
            runtime_ms,
            stderr=(raw_err or "sandbox produced no parseable output")[:MAX_OUTPUT_BYTES],
            expected=expected,
        )

    status = payload.get("status")
    stdout = str(payload.get("stdout", ""))[:MAX_OUTPUT_BYTES]

    if status == "memory":
        return TestResult(index, False, "memory", runtime_ms, stderr="Memory Limit Exceeded (256 MB)", expected=expected)
    if status == "error":
        err_msg = f"{payload.get('error_type')}: {payload.get('stderr', '')}"[:MAX_OUTPUT_BYTES]
        return TestResult(index, False, "error", runtime_ms, stdout=stdout, stderr=err_msg, expected=expected)

    returned = payload.get("returned")
    passed = returned == expected
    return TestResult(
        index,
        passed,
        "ok" if passed else "wrong_answer",
        runtime_ms,
        stdout=stdout,
        expected=expected,
        returned=returned,
    )


async def run_test_cases_async(code: str, entry_point: str, test_cases: list[dict]) -> ExecutionReport:
    """Asynchronously run `code` against every test case in parallel/sequence."""
    report = ExecutionReport(network_isolated=network_isolation_available())
    for i, case in enumerate(test_cases):
        res = await _run_one_async(code, entry_point, case.get("args", []), case.get("expected"), i)
        report.results.append(res)
    return report


def run_test_cases(code: str, entry_point: str, test_cases: list[dict]) -> ExecutionReport:
    """Synchronous bridge for callers running outside an existing asyncio event loop."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # In a running loop thread without await, run in a secondary thread with new loop
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            return pool.submit(asyncio.run, run_test_cases_async(code, entry_point, test_cases)).result()
    return asyncio.run(run_test_cases_async(code, entry_point, test_cases))


async def execute_script_async(code: str) -> dict:
    """Execute arbitrary student script in the zero-trust sandbox for interactive lessons."""
    uid, gid = _unprivileged_ids()
    workdir = tempfile.mkdtemp(prefix="cm_sbx_")
    try:
        os.chmod(workdir, 0o777)
    except OSError:
        pass

    job = json.dumps(
        {
            "code": code,
            "entry_point": None,
            "args": [],
            "uid": uid,
            "gid": gid,
            "cpu_seconds": CPU_SECONDS,
            "memory_bytes": MEMORY_BYTES,
        }
    )

    env = dict(CLEAN_ENV)
    env["HOME"] = workdir
    env["TMPDIR"] = workdir

    started = time.perf_counter()
    argv = _build_argv()
    preexec = _posix_preexec if sys.platform != "win32" else None

    proc = None
    try:
        proc = await asyncio.create_subprocess_exec(
            *argv,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=workdir,
            env=env,
            preexec_fn=preexec,
        )
        stdout_raw, stderr_raw = await asyncio.wait_for(
            proc.communicate(input=job.encode("utf-8")),
            timeout=WALL_SECONDS,
        )
        runtime_ms = int((time.perf_counter() - started) * 1000)
    except asyncio.TimeoutError:
        runtime_ms = int((time.perf_counter() - started) * 1000)
        if proc is not None and proc.pid:
            _kill_process_group(proc.pid)
        return {
            "status": "timeout",
            "stdout": "",
            "stderr": "Time Limit Exceeded (Execution timed out)",
            "runtime_ms": runtime_ms,
        }
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    try:
        payload = json.loads(stdout_raw.decode("utf-8", errors="replace"))
        err_type = payload.get("error_type")
        err_msg = payload.get("stderr", "")
        if err_type and not err_msg.startswith(err_type):
            err_msg = f"{err_type}: {err_msg}"
        return {
            "status": payload.get("status", "ok"),
            "stdout": payload.get("stdout", "")[:MAX_OUTPUT_BYTES],
            "stderr": err_msg[:MAX_OUTPUT_BYTES],
            "runtime_ms": runtime_ms,
        }
    except Exception:
        return {
            "status": "error",
            "stdout": stdout_raw.decode("utf-8", errors="replace")[:MAX_OUTPUT_BYTES],
            "stderr": stderr_raw.decode("utf-8", errors="replace")[:MAX_OUTPUT_BYTES] or "Unknown execution error",
            "runtime_ms": runtime_ms,
        }

