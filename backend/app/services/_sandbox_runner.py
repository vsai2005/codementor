"""Child process entry point for sandboxed execution (Phase 1).

Executed as:
    python3 -I -s _sandbox_runner.py

Hardening layers:
  1. POSIX rlimits (2s CPU, 256MB AS, 10 NPROC, 1MB FSIZE)
  2. Drop privileges to nobody if root
  3. Network socket neutering and sensitive file blocking
  4. Stream output buffering capped at 64 KB
"""

from __future__ import annotations

import io
import json
import os
import sys

MAX_OUTPUT_BYTES = 64 * 1024  # 64 KB cap on captured output


def _drop_privileges(uid: int, gid: int) -> None:
    if not hasattr(os, "getuid") or os.getuid() != 0:
        return  # already unprivileged or non-POSIX
    try:
        os.setgroups([])
        os.setgid(gid)
        os.setuid(uid)
    except (OSError, PermissionError):
        pass


def _apply_rlimits(cpu_seconds: int = 2, memory_bytes: int = 256 * 1024 * 1024) -> None:
    try:
        import resource

        # RLIMIT_CPU: 2s limit
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds))
        # RLIMIT_AS: 256 MB
        resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))
        # RLIMIT_FSIZE: 1 MB writes
        fsize_bytes = 1024 * 1024
        resource.setrlimit(resource.RLIMIT_FSIZE, (fsize_bytes, fsize_bytes))
        # RLIMIT_NPROC: 10 subprocesses
        if hasattr(resource, "RLIMIT_NPROC"):
            resource.setrlimit(resource.RLIMIT_NPROC, (10, 10))
        # RLIMIT_CORE: 0
        if hasattr(resource, "RLIMIT_CORE"):
            resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    except (ImportError, OSError, ValueError):
        pass


_BLOCKED_EXACT = frozenset(
    {
        "socket.__new__",
        "socket.bind",
        "socket.connect",
        "socket.getaddrinfo",
        "socket.gethostbyname",
        "socket.sendto",
        "socket.sethostname",
        "os.system",
        "os.fork",
        "os.forkpty",
        "os.posix_spawnp",
        "os.spawn",
        "os.putenv",
        "pty.spawn",
        "subprocess.Popen",
        "ctypes.dlopen",
        "ctypes.dlsym",
        "ctypes.call_function",
        "ctypes.get_errno",
        "urllib.Request",
        "http.client.connect",
        "ftplib.connect",
        "smtplib.connect",
        "webbrowser.open",
    }
)

_BLOCKED_PREFIX = ("os.exec", "os.spawn", "os.posix_spawn", "socket.", "ctypes.")
_WRITE_MODES = ("w", "a", "x", "+")
_SENSITIVE_FILES = ("/etc/passwd", "/etc/shadow", "/etc/hosts", ".env", "/proc")


class SandboxViolation(PermissionError):
    """Raised inside the audit hook when unauthorized operations occur."""


def _audit(event: str, args: tuple) -> None:
    if event == "open":
        path = str(args[0]) if args else ""
        mode = args[1] if len(args) > 1 else None

        for sensitive in _SENSITIVE_FILES:
            if sensitive in path:
                raise SandboxViolation(f"blocked: unauthorized filesystem access ({path!r})")

        if isinstance(mode, str) and any(m in mode for m in _WRITE_MODES):
            if not path.startswith("/tmp") and not path.startswith("cm_sbx_"):
                raise SandboxViolation(f"blocked: write outside /tmp ({path!r})")
        return

    if event in _BLOCKED_EXACT or any(event.startswith(p) for p in _BLOCKED_PREFIX):
        raise SandboxViolation(f"blocked operation: {event}")


def _block_network_and_env() -> None:
    """Neuter socket creation and sensitive module access."""
    try:
        import socket

        def _denied(*_args, **_kwargs):
            raise PermissionError("network access is disabled in the sandbox")

        for name in (
            "socket",
            "create_connection",
            "create_server",
            "socketpair",
            "getaddrinfo",
            "gethostbyname",
        ):
            if hasattr(socket, name):
                setattr(socket, name, _denied)

        sys.modules["_socket"] = None  # type: ignore[assignment]
        for blocked in ("urllib.request", "http.client", "ftplib", "smtplib", "webbrowser"):
            sys.modules[blocked] = None  # type: ignore[assignment]
    except Exception:
        pass


def _emit(payload: dict) -> None:
    sys.__stdout__.write(json.dumps(payload))
    sys.__stdout__.flush()


def main() -> None:
    raw = sys.stdin.read()
    if not raw:
        return
    job = json.loads(raw)

    uid = job.get("uid", 65534)
    gid = job.get("gid", 65534)
    cpu_s = job.get("cpu_seconds", 2)
    mem_b = job.get("memory_bytes", 256 * 1024 * 1024)

    _drop_privileges(uid, gid)
    _apply_rlimits(cpu_s, mem_b)
    _block_network_and_env()

    captured = io.StringIO()
    sys.stdout = captured

    namespace: dict = {"__name__": "__solution__"}
    try:
        compiled = compile(job["code"], "solution.py", "exec")
    except SyntaxError as exc:
        _emit(
            {
                "status": "error",
                "error_type": "SyntaxError",
                "stderr": f"{exc.msg} (line {exc.lineno})"[:MAX_OUTPUT_BYTES],
                "stdout": "",
            }
        )
        return

    sys.addaudithook(_audit)

    try:
        exec(compiled, namespace)  # noqa: S102 -- isolated child process
        if job.get("entry_point"):
            entry = namespace.get(job["entry_point"])
            if not callable(entry):
                _emit(
                    {
                        "status": "error",
                        "error_type": "MissingEntryPoint",
                        "stderr": f"expected a function named {job['entry_point']!r}"[:MAX_OUTPUT_BYTES],
                        "stdout": captured.getvalue()[:MAX_OUTPUT_BYTES],
                    }
                )
                return
            returned = entry(*job["args"])
        else:
            returned = None
    except MemoryError:
        _emit(
            {
                "status": "memory",
                "error_type": "MemoryError",
                "stderr": "Memory limit exceeded (256 MB)",
                "stdout": "",
            }
        )
        return
    except BaseException as exc:  # noqa: BLE001 -- must not leak a crash
        import traceback

        _emit(
            {
                "status": "error",
                "error_type": type(exc).__name__,
                "stderr": traceback.format_exc(limit=3)[:MAX_OUTPUT_BYTES],
                "stdout": captured.getvalue()[:MAX_OUTPUT_BYTES],
            }
        )
        return

    try:
        json.dumps(returned)
        serialisable = returned
    except (TypeError, ValueError):
        serialisable = repr(returned)

    _emit(
        {
            "status": "ok",
            "returned": serialisable,
            "stdout": captured.getvalue()[:MAX_OUTPUT_BYTES],
            "stderr": "",
        }
    )


if __name__ == "__main__":
    main()
