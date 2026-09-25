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
    "MALLOC_ARENA_MAX": "1",
    "PYTHONHASHSEED": "0",
}

_WIN32_QUOTA_EXCEEDED = (3221225540, -1073741756, 3221225495, -1073741801)


def _truncate_utf8(s: str, max_bytes: int = MAX_OUTPUT_BYTES) -> str:
    """Truncate string `s` so that len(result.encode('utf-8')) <= max_bytes,
    guaranteeing no multibyte UTF-8 character is ever split.
    """
    if max_bytes <= 0 or not s:
        return ""
    candidate = s[:max_bytes]
    raw = candidate.encode("utf-8")
    if len(raw) <= max_bytes:
        return candidate
    return raw[:max_bytes].decode("utf-8", errors="ignore")


def _setup_win32_job_object(pid: int):
    """Enforces Job Object process containment and active process limits on Windows child processes.
    
    Avoids setting virtual commit quotas (JOB_OBJECT_LIMIT_JOB_MEMORY / PROCESS_MEMORY) which
    falsely terminate legitimate moderate Python workloads. Memory abuse is authoritatively
    enforced by the active physical RSS process-tree watchdog.
    """
    if sys.platform != "win32" or not pid:
        return None
    try:
        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.windll.kernel32

        class IO_COUNTERS(ctypes.Structure):
            _fields_ = [
                ("ReadOperationCount", ctypes.c_uint64),
                ("WriteOperationCount", ctypes.c_uint64),
                ("OtherOperationCount", ctypes.c_uint64),
                ("ReadTransferCount", ctypes.c_uint64),
                ("WriteTransferCount", ctypes.c_uint64),
                ("OtherTransferCount", ctypes.c_uint64),
            ]

        class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("BasicLimitInformation_PerProcessUserTimeLimit", ctypes.c_int64),
                ("BasicLimitInformation_PerJobUserTimeLimit", ctypes.c_int64),
                ("BasicLimitInformation_LimitFlags", wintypes.DWORD),
                ("BasicLimitInformation_MinimumWorkingSetSize", ctypes.c_size_t),
                ("BasicLimitInformation_MaximumWorkingSetSize", ctypes.c_size_t),
                ("BasicLimitInformation_ActiveProcessLimit", wintypes.DWORD),
                ("BasicLimitInformation_Affinity", ctypes.c_size_t),
                ("BasicLimitInformation_PriorityClass", wintypes.DWORD),
                ("BasicLimitInformation_SchedulingClass", wintypes.DWORD),
                ("IoInfo", IO_COUNTERS),
                ("ProcessMemoryLimit", ctypes.c_size_t),
                ("JobMemoryLimit", ctypes.c_size_t),
                ("PeakProcessMemoryUsed", ctypes.c_size_t),
                ("PeakJobMemoryUsed", ctypes.c_size_t),
            ]

        job = kernel32.CreateJobObjectW(None, None)
        if not job:
            return None

        limits = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE (0x2000) | JOB_OBJECT_LIMIT_ACTIVE_PROCESS (0x0008)
        limits.BasicLimitInformation_LimitFlags = 0x2000 | 0x0008
        limits.BasicLimitInformation_ActiveProcessLimit = 10

        kernel32.SetInformationJobObject(
            job, 9, ctypes.byref(limits), ctypes.sizeof(JOBOBJECT_EXTENDED_LIMIT_INFORMATION)
        )

        h_proc = kernel32.OpenProcess(0x1F0FFF, False, pid)
        if h_proc:
            try:
                kernel32.AssignProcessToJobObject(job, h_proc)
            finally:
                kernel32.CloseHandle(h_proc)

        return job
    except Exception:
        return None


def _terminate_win32_job(job) -> None:
    if sys.platform == "win32" and job:
        try:
            import ctypes
            ctypes.windll.kernel32.TerminateJobObject(job, 1)
        except Exception:
            pass


def _close_win32_job(job) -> None:
    if sys.platform == "win32" and job:
        try:
            import ctypes
            ctypes.windll.kernel32.CloseHandle(job)
        except Exception:
            pass


def _get_process_tree_rss(pid: int) -> int | None:
    """Returns the total physical resident memory (RSS / Working Set) of process `pid`
    and all its descendant processes in bytes.
    """
    if not pid:
        return None

    # Strategy 1: psutil (cross-platform, reliable, accounts for full descendant tree)
    try:
        import psutil

        proc = psutil.Process(pid)
        total_rss = proc.memory_info().rss
        for child in proc.children(recursive=True):
            try:
                total_rss += child.memory_info().rss
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return total_rss
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None
    except Exception:
        pass

    # Strategy 2: Linux /proc filesystem (RSS pages * page_size) + child tree
    if sys.platform != "win32":
        try:
            total_rss = 0
            page_size = os.sysconf("SC_PAGE_SIZE")
            pids = [pid]
            try:
                with open(f"/proc/{pid}/task/{pid}/children", "r") as f:
                    pids.extend(int(p) for p in f.read().split())
            except Exception:
                pass

            for p in pids:
                try:
                    with open(f"/proc/{p}/statm", "r") as f:
                        parts = f.read().split()
                        if len(parts) >= 2:
                            total_rss += int(parts[1]) * page_size
                except Exception:
                    pass
            return total_rss if total_rss > 0 else None
        except Exception:
            return None

    # Strategy 3: Windows psapi via ctypes (measures physical WorkingSetSize, NOT commit charge)
    try:
        import ctypes
        from ctypes import wintypes

        class PROCESS_MEMORY_COUNTERS(ctypes.Structure):
            _fields_ = [
                ("cb", wintypes.DWORD),
                ("PageFaultCount", wintypes.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t),
            ]

        psapi = ctypes.windll.psapi
        psapi.GetProcessMemoryInfo.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(PROCESS_MEMORY_COUNTERS),
            wintypes.DWORD,
        ]
        psapi.GetProcessMemoryInfo.restype = wintypes.BOOL

        h = ctypes.windll.kernel32.OpenProcess(0x1000 | 0x0400, False, pid)
        if h:
            try:
                counters = PROCESS_MEMORY_COUNTERS()
                counters.cb = ctypes.sizeof(PROCESS_MEMORY_COUNTERS)
                if psapi.GetProcessMemoryInfo(h, ctypes.byref(counters), counters.cb):
                    return counters.WorkingSetSize
            finally:
                ctypes.windll.kernel32.CloseHandle(h)
    except Exception:
        pass

    return None


async def _watch_process_memory(
    pid: int,
    limit_bytes: int,
    violation_flag: list[bool],
    stop_event: asyncio.Event,
    win_job=None,
) -> None:
    """Async background task that polls process-tree physical memory every 15ms and terminates on breach."""
    if not pid:
        return
    while not stop_event.is_set():
        try:
            mem = _get_process_tree_rss(pid)
            if mem is not None and mem > limit_bytes:
                violation_flag[0] = True
                _kill_process_group(pid, win_job=win_job)
                break
        except Exception:
            break
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=0.015)
        except (asyncio.TimeoutError, TimeoutError):
            pass


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


def _kill_process_group(pid: int, win_job=None) -> None:
    if sys.platform == "win32":
        if win_job:
            _terminate_win32_job(win_job)
        try:
            import psutil

            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            for child in children:
                try:
                    child.kill()
                except Exception:
                    pass
            parent.kill()
            return
        except Exception:
            pass
        try:
            os.kill(pid, signal.SIGTERM)
        except Exception:
            pass
        return

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
    win_job = None
    stop_watchdog = asyncio.Event()
    mem_violation = [False]
    watchdog_task = None
    timed_out = False
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

        if proc.pid:
            if sys.platform == "win32":
                win_job = _setup_win32_job_object(proc.pid)
            watchdog_task = asyncio.create_task(
                _watch_process_memory(proc.pid, MEMORY_BYTES, mem_violation, stop_watchdog, win_job=win_job)
            )

        stdout_bytes, stderr_bytes = await asyncio.wait_for(
            proc.communicate(input=job.encode("utf-8")),
            timeout=WALL_SECONDS,
        )
    except (asyncio.TimeoutError, TimeoutError):
        timed_out = True
        if proc and proc.pid:
            _kill_process_group(proc.pid, win_job=win_job)
            try:
                await proc.wait()
            except Exception:
                pass
        stdout_bytes = b""
        stderr_bytes = b"Time Limit Exceeded"
    finally:
        stop_watchdog.set()
        if watchdog_task:
            try:
                await watchdog_task
            except Exception:
                pass
        if win_job:
            _close_win32_job(win_job)
        if proc and proc.pid:
            _kill_process_group(proc.pid, win_job=None)
        shutil.rmtree(workdir, ignore_errors=True)

    runtime_ms = int((time.perf_counter() - started) * 1000)

    if mem_violation[0]:
        return TestResult(
            index=index,
            passed=False,
            status="memory",
            runtime_ms=runtime_ms,
            stderr="Memory Limit Exceeded (256 MB)",
            expected=expected,
        )

    if timed_out:
        return TestResult(
            index=index,
            passed=False,
            status="timeout",
            runtime_ms=runtime_ms,
            stderr="Time Limit Exceeded",
            expected=expected,
        )

    # Windows Job Object quota or Out-of-Memory exit codes
    if sys.platform == "win32" and proc and proc.returncode:
        if proc.returncode in (0xC0000044, -1073741756, 3221225540, 0xC0000017, -1073741801, 3221225495):
            return TestResult(
                index, False, "memory", runtime_ms, stderr="Memory Limit Exceeded (256 MB)", expected=expected
            )

    # Decode and parse payload envelope with byte-safe truncation
    raw_out = _truncate_utf8(stdout_bytes.decode("utf-8", "replace"), 512 * 1024)
    raw_err = _truncate_utf8(stderr_bytes.decode("utf-8", "replace"), MAX_OUTPUT_BYTES)

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
            stderr=_truncate_utf8(raw_err or "sandbox produced no parseable output", MAX_OUTPUT_BYTES),
            expected=expected,
        )

    status = payload.get("status")
    stdout = _truncate_utf8(str(payload.get("stdout", "")), MAX_OUTPUT_BYTES)
    stderr = _truncate_utf8(str(payload.get("stderr", "")), MAX_OUTPUT_BYTES)

    if status == "memory":
        return TestResult(index, False, "memory", runtime_ms, stderr="Memory Limit Exceeded (256 MB)", expected=expected)
    if status == "error":
        err_msg = f"{payload.get('error_type')}: {stderr}".strip()
        return TestResult(index, False, "error", runtime_ms, stdout=stdout, stderr=_truncate_utf8(err_msg, MAX_OUTPUT_BYTES), expected=expected)

    returned = payload.get("returned")
    passed = returned == expected
    return TestResult(
        index,
        passed,
        "ok" if passed else "wrong_answer",
        runtime_ms,
        stdout=stdout,
        stderr=stderr,
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
    win_job = None
    stop_watchdog = asyncio.Event()
    mem_violation = [False]
    watchdog_task = None
    timed_out = False
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
        if proc.pid:
            if sys.platform == "win32":
                win_job = _setup_win32_job_object(proc.pid)
            watchdog_task = asyncio.create_task(
                _watch_process_memory(proc.pid, MEMORY_BYTES, mem_violation, stop_watchdog, win_job=win_job)
            )

        stdout_raw, stderr_raw = await asyncio.wait_for(
            proc.communicate(input=job.encode("utf-8")),
            timeout=WALL_SECONDS,
        )
    except (asyncio.TimeoutError, TimeoutError):
        timed_out = True
        if proc is not None and proc.pid:
            _kill_process_group(proc.pid, win_job=win_job)
            try:
                await proc.wait()
            except Exception:
                pass
        stdout_raw = b""
        stderr_raw = b"Time Limit Exceeded (Execution timed out)"
    finally:
        stop_watchdog.set()
        if watchdog_task:
            try:
                await watchdog_task
            except Exception:
                pass
        if win_job:
            _close_win32_job(win_job)
        if proc and proc.pid:
            _kill_process_group(proc.pid, win_job=None)
        shutil.rmtree(workdir, ignore_errors=True)

    runtime_ms = int((time.perf_counter() - started) * 1000)

    if mem_violation[0]:
        return {
            "status": "memory",
            "stdout": "",
            "stderr": "Memory Limit Exceeded (256 MB)",
            "runtime_ms": runtime_ms,
        }

    if timed_out:
        return {
            "status": "timeout",
            "stdout": "",
            "stderr": "Time Limit Exceeded (Execution timed out)",
            "runtime_ms": runtime_ms,
        }

    if sys.platform == "win32" and proc and proc.returncode:
        if proc.returncode in (0xC0000044, -1073741756, 3221225540, 0xC0000017, -1073741801, 3221225495):
            return {
                "status": "memory",
                "stdout": "",
                "stderr": "Memory Limit Exceeded (256 MB)",
                "runtime_ms": runtime_ms,
            }

    if proc and proc.returncode and proc.returncode < 0:
        sig = -proc.returncode
        if hasattr(signal, "SIGXCPU") and sig == signal.SIGXCPU:
            return {
                "status": "timeout",
                "stdout": "",
                "stderr": "Time Limit Exceeded",
                "runtime_ms": runtime_ms,
            }
        return {
            "status": "memory",
            "stdout": "",
            "stderr": "Memory Limit Exceeded (256 MB)",
            "runtime_ms": runtime_ms,
        }

    try:
        payload = json.loads(stdout_raw.decode("utf-8", errors="replace"))
        err_type = payload.get("error_type")
        err_msg = _truncate_utf8(str(payload.get("stderr", "")), MAX_OUTPUT_BYTES)
        if err_type and not err_msg.startswith(err_type):
            err_msg = f"{err_type}: {err_msg}"
        return {
            "status": payload.get("status", "ok"),
            "stdout": _truncate_utf8(str(payload.get("stdout", "")), MAX_OUTPUT_BYTES),
            "stderr": _truncate_utf8(err_msg, MAX_OUTPUT_BYTES),
            "runtime_ms": runtime_ms,
        }
    except Exception:
        return {
            "status": "error",
            "stdout": _truncate_utf8(stdout_raw.decode("utf-8", errors="replace"), MAX_OUTPUT_BYTES),
            "stderr": _truncate_utf8(stderr_raw.decode("utf-8", errors="replace") or "Unknown execution error", MAX_OUTPUT_BYTES),
            "runtime_ms": runtime_ms,
        }


async def run_custom_async(code: str, entry_point: str, args: list[Any]) -> TestResult:
    """Asynchronously run `code` against custom input arguments (for live problem testing)."""
    return await _run_one_async(code, entry_point, args, expected=None, index=0)


