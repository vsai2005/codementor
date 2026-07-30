"""Child process entry point for sandboxed execution.

This module is executed as a fresh subprocess -- it is NEVER imported by the
API process. It reads a JSON job from stdin, hardens itself, runs exactly one
test case, and writes a JSON result to stdout.

Hardening layers, applied in order:
  1. (parent) network namespace via `unshare -n`, if available
  2. drop to an unprivileged uid/gid
  3. RLIMIT_AS / RLIMIT_CPU / RLIMIT_FSIZE / RLIMIT_NPROC
  4. socket-module neutering (the fallback when layer 1 is unavailable)

Layer 4 matters: PRD 5.5 requires "no network access from executed code", but
resource.setrlimit does not restrict sockets at all. On a host where we cannot
create a network namespace (unprivileged container, e.g. Render free tier),
layer 4 is the only thing standing between user code and the internet.
"""

from __future__ import annotations

import io
import json
import os
import resource
import sys

MAX_OUTPUT_BYTES = 10 * 1024


def _drop_privileges(uid: int, gid: int) -> None:
    if os.getuid() != 0:
        return  # already unprivileged, nothing to drop
    os.setgroups([])
    os.setgid(gid)
    os.setuid(uid)
    if os.getuid() == 0:
        raise RuntimeError("failed to drop privileges")


def _apply_rlimits(cpu_seconds: int, memory_bytes: int) -> None:
    resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds))
    resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1 << 20, 1 << 20))  # 1MB writes
    resource.setrlimit(resource.RLIMIT_NPROC, (64, 64))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def _block_network() -> None:
    """Neuter socket creation for code running in this process.

    Not a substitute for a network namespace -- a determined attacker with
    ctypes can go around it -- but it stops the realistic case and it is the
    only layer available when the host forbids CLONE_NEWNET.
    """
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
    for blocked in ("urllib.request", "http.client", "ftplib", "smtplib"):
        sys.modules[blocked] = None  # type: ignore[assignment]


def _emit(payload: dict) -> None:
    sys.__stdout__.write(json.dumps(payload))
    sys.__stdout__.flush()


def main() -> None:
    job = json.loads(sys.stdin.read())

    _drop_privileges(job["uid"], job["gid"])
    _apply_rlimits(job["cpu_seconds"], job["memory_bytes"])
    _block_network()

    captured = io.StringIO()
    sys.stdout = captured

    namespace: dict = {"__name__": "__solution__"}
    try:
        compiled = compile(job["code"], "solution.py", "exec")
    except SyntaxError as exc:
        # A syntax error is user error, not a crash. Report it as a clean
        # failure so the API never turns it into a 500.
        _emit(
            {
                "status": "error",
                "error_type": "SyntaxError",
                "stderr": f"{exc.msg} (line {exc.lineno})",
                "stdout": "",
            }
        )
        return

    try:
        exec(compiled, namespace)  # noqa: S102 -- isolated child process
        entry = namespace.get(job["entry_point"])
        if not callable(entry):
            _emit(
                {
                    "status": "error",
                    "error_type": "MissingEntryPoint",
                    "stderr": f"expected a function named {job['entry_point']!r}",
                    "stdout": captured.getvalue()[:MAX_OUTPUT_BYTES],
                }
            )
            return
        returned = entry(*job["args"])
    except MemoryError:
        _emit({"status": "memory", "error_type": "MemoryError", "stderr": "memory limit exceeded", "stdout": ""})
        return
    except BaseException as exc:  # noqa: BLE001 -- must not leak a crash
        import traceback

        _emit(
            {
                "status": "error",
                "error_type": type(exc).__name__,
                "stderr": traceback.format_exc(limit=3)[-2000:],
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
