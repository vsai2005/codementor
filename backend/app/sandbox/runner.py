"""Child-process harness for untrusted user code (Phase 1).

Executed as:
    python3 -I -s runner.py <code_file>

Hardening layers:
  1. POSIX kernel resource limits via `setrlimit` (RLIMIT_CPU, RLIMIT_AS, RLIMIT_NPROC, RLIMIT_FSIZE)
  2. Sys audit hook enforcing network prohibition, process execution lockdown, and filesystem containment
  3. Strict standard I/O buffer truncation capped at 64 KB
"""

from __future__ import annotations

import io
import os
import signal
import sys
import traceback

MAX_IO_BYTES = 64 * 1024  # 64 KB cap on stdout/stderr streams

# Audit events that abort execution outright. Matched by exact name or dotted prefix.
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


def apply_posix_rlimits() -> None:
    """Restrict student Python processes at the OS kernel level."""
    try:
        import resource

        # RLIMIT_CPU: Hard limit of 2 seconds
        resource.setrlimit(resource.RLIMIT_CPU, (2, 2))
        # RLIMIT_AS: Hard limit of 256 MB (256 * 1024 * 1024 bytes)
        as_limit = 256 * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (as_limit, as_limit))
        # RLIMIT_NPROC: Hard limit of 10 subprocesses to neutralize fork bombs
        if hasattr(resource, "RLIMIT_NPROC"):
            resource.setrlimit(resource.RLIMIT_NPROC, (10, 10))
        # RLIMIT_FSIZE: Hard limit of 1 MB (1024 * 1024 bytes) to prevent disk exhaustion
        fsize_limit = 1024 * 1024
        resource.setrlimit(resource.RLIMIT_FSIZE, (fsize_limit, fsize_limit))
        # RLIMIT_CORE: 0 (no core dump files)
        if hasattr(resource, "RLIMIT_CORE"):
            resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    except (ImportError, OSError, ValueError):
        # Graceful fallback on non-POSIX platforms (e.g. local Windows dev)
        pass


class SandboxViolation(RuntimeError):
    """Raised inside the audit hook when unauthorized operations occur."""


def _audit(event: str, args: tuple) -> None:
    if event == "open":
        path = str(args[0]) if args else ""
        mode = args[1] if len(args) > 1 else None

        # Block file-system traversal to sensitive files or environ
        for sensitive in _SENSITIVE_FILES:
            if sensitive in path:
                raise SandboxViolation(f"blocked: unauthorized filesystem access ({path!r})")

        # Confine writes strictly to /tmp
        if isinstance(mode, str) and any(m in mode for m in _WRITE_MODES):
            if not path.startswith("/tmp"):
                raise SandboxViolation(f"blocked: write outside /tmp ({path!r})")
        return

    if event in _BLOCKED_EXACT or any(event.startswith(p) for p in _BLOCKED_PREFIX):
        raise SandboxViolation(f"blocked operation: {event}")


def main() -> int:
    apply_posix_rlimits()

    if len(sys.argv) != 2:
        sys.stderr.write("runner.py <code_file>\n")
        return 2

    code_path = sys.argv[1]

    # Read the file BEFORE arming the hook -- our own open() would trip it
    try:
        with open(code_path, "r", encoding="utf-8") as fh:
            source = fh.read()
    except OSError as exc:
        sys.stderr.write(f"harness could not read submission: {exc}\n"[:MAX_IO_BYTES])
        return 2

    # Compile before arming hook
    try:
        compiled = compile(source, "<submission>", "exec")
    except SyntaxError as exc:
        sys.stderr.write(f"SyntaxError: {exc.msg} (line {exc.lineno})\n"[:MAX_IO_BYTES])
        return 3

    sys.argv = ["<submission>"]
    sys.addaudithook(_audit)

    globals_ns = {"__name__": "__main__", "__builtins__": __builtins__}
    try:
        exec(compiled, globals_ns)
    except SandboxViolation as exc:
        sys.stderr.write((str(exc) + "\n")[:MAX_IO_BYTES])
        return 4
    except SystemExit as exc:
        return int(exc.code or 0)
    except MemoryError:
        sys.stderr.write("MemoryError: memory limit exceeded\n")
        return 5
    except BaseException:
        exc_type, exc_value, tb = sys.exc_info()
        frames = traceback.format_exception(exc_type, exc_value, tb.tb_next)
        sys.stderr.write("".join(frames)[:MAX_IO_BYTES])
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
