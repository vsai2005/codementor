"""Child-process harness for untrusted user code.

Never imported by the API process. Invoked as:

    python3 -I -B -q runner.py <code_file>

Layering (each layer is independently insufficient; together they are the v1
bar defined in PRD 5.5):

  1. Parent sets POSIX rlimits + a process group it can kill  (services/sandbox.py)
  2. Parent drops to a non-root uid                            (services/sandbox.py)
  3. This file installs a sys audit hook before user code runs

Layer 3 exists because rlimits do NOT restrict network access -- RLIMIT_* caps
CPU, address space, file size and fd count, and nothing else. PRD 5.5 requires
"no network access from executed code", so something has to actually enforce it.

An audit hook is the right primitive here: CPython provides no API to remove a
hook once installed, so user code cannot uninstall it, and the events fire
inside the C implementation rather than at the Python name, so rebinding
`socket.socket` or re-importing does not evade it.

This is defense in depth, not a jail. A CPython sandbox escape is a real
category of bug. v2 is one container per execution (PRD 9), and that is where
this stops being the only thing between user code and the host.
"""

from __future__ import annotations

import io
import runpy
import sys
import traceback

# Audit events that abort execution outright. Matched by exact name or by
# prefix for the dotted families (socket.*, os.exec*, ...).
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

# Writes are confined to /tmp. Reads are unrestricted -- the interpreter needs
# to read its own stdlib, and there is nothing secret on the image.
_WRITE_MODES = ("w", "a", "x", "+")


class SandboxViolation(RuntimeError):
    """Raised inside the audit hook. Surfaces to the parent as a failed test."""


def _audit(event: str, args: tuple) -> None:
    if event == "open":
        # args = (path, mode, flags); mode is None for the low-level os.open path
        mode = args[1] if len(args) > 1 else None
        if isinstance(mode, str) and any(m in mode for m in _WRITE_MODES):
            path = str(args[0]) if args else ""
            if not path.startswith("/tmp"):
                raise SandboxViolation(
                    f"blocked: write outside /tmp ({path!r})"
                )
        return

    if event in _BLOCKED_EXACT or event.startswith(_BLOCKED_PREFIX):
        raise SandboxViolation(f"blocked operation: {event}")


def main() -> int:
    if len(sys.argv) != 2:
        print("runner.py <code_file>", file=sys.stderr)
        return 2

    code_path = sys.argv[1]

    # Read the file BEFORE arming the hook -- our own open() would trip it.
    try:
        with open(code_path, "r", encoding="utf-8") as fh:
            source = fh.read()
    except OSError as exc:  # pragma: no cover - parent always writes this file
        print(f"harness could not read submission: {exc}", file=sys.stderr)
        return 2

    # Compile before arming too, so a SyntaxError is reported as a clean
    # compile failure rather than something that happened "in the sandbox".
    try:
        compiled = compile(source, "<submission>", "exec")
    except SyntaxError as exc:
        print(f"SyntaxError: {exc.msg} (line {exc.lineno})", file=sys.stderr)
        return 3

    # Drop the import machinery's ability to reach the submission directory
    # after this point; everything user code needs is already importable.
    sys.argv = ["<submission>"]

    sys.addaudithook(_audit)  # point of no return

    globals_ns = {"__name__": "__main__", "__builtins__": __builtins__}
    try:
        exec(compiled, globals_ns)
    except SandboxViolation as exc:
        print(str(exc), file=sys.stderr)
        return 4
    except SystemExit as exc:
        return int(exc.code or 0)
    except MemoryError:
        print("MemoryError: memory limit exceeded", file=sys.stderr)
        return 5
    except BaseException:
        # Trim the harness frames so the user sees only their own traceback.
        exc_type, exc_value, tb = sys.exc_info()
        frames = traceback.format_exception(exc_type, exc_value, tb.tb_next)
        sys.stderr.write("".join(frames))
        return 1

    return 0


if __name__ == "__main__":
    # runpy is imported but unused in the fast path; keep the reference so the
    # module is resident before the hook arms (importing under the hook is fine,
    # but resident-before-arm is one less thing to reason about).
    _ = runpy, io
    sys.exit(main())
