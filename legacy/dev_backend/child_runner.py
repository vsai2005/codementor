"""Windows-safe, hardened code executor for the dev backend (Phase 1).

Runs as a fresh subprocess: reads a JSON job from stdin, execs the user's code
with a RESTRICTED set of builtins and safe modules, enforces resource limits where
supported, and buffers output capped at 64 KB.
"""

from __future__ import annotations

import builtins as _builtins
import io
import json
import os
import sys

MAX_OUTPUT_BYTES = 64 * 1024  # 64 KB cap on captured output

# Modules an algorithm/data-structure solution might legitimately use.
ALLOWED_MODULES = {
    "math", "cmath", "collections", "itertools", "functools", "heapq", "bisect",
    "string", "re", "random", "statistics", "operator", "typing", "numbers",
    "fractions", "decimal", "datetime", "copy", "array", "enum", "dataclasses",
    "abc", "queue",
}

_REAL_IMPORT = _builtins.__import__


def apply_rlimits() -> None:
    """Apply POSIX rlimits if available on host."""
    try:
        import resource

        # 2s CPU limit
        resource.setrlimit(resource.RLIMIT_CPU, (2, 2))
        # 256 MB Address Space
        as_bytes = 256 * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (as_bytes, as_bytes))
        # 10 Subprocesses
        if hasattr(resource, "RLIMIT_NPROC"):
            resource.setrlimit(resource.RLIMIT_NPROC, (10, 10))
        # 1 MB File Size limit
        fsize = 1024 * 1024
        resource.setrlimit(resource.RLIMIT_FSIZE, (fsize, fsize))
        if hasattr(resource, "RLIMIT_CORE"):
            resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    except (ImportError, OSError, ValueError):
        pass


def _guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
    root = name.split(".")[0]
    if level != 0 or root not in ALLOWED_MODULES:
        raise ImportError(f"import of {name!r} is blocked in the sandbox")
    return _REAL_IMPORT(name, globals, locals, fromlist, level)


def _safe_builtins() -> dict:
    """A copy of builtins with the dangerous entries removed."""
    safe = {k: getattr(_builtins, k) for k in dir(_builtins) if not k.startswith("_")}
    for name in ("open", "exec", "eval", "compile", "input", "memoryview",
                 "breakpoint", "help", "exit", "quit", "globals", "vars", "locals"):
        safe.pop(name, None)
    safe["__import__"] = _guarded_import
    safe["__build_class__"] = _builtins.__build_class__
    return safe


def _emit(payload: dict) -> None:
    sys.__stdout__.write(json.dumps(payload))
    sys.__stdout__.flush()


def main() -> None:
    apply_rlimits()
    raw = sys.stdin.read()
    if not raw:
        return
    job = json.loads(raw)

    captured = io.StringIO()
    sys.stdout = captured

    namespace: dict = {"__name__": "__solution__", "__builtins__": _safe_builtins()}
    try:
        compiled = compile(job["code"], "solution.py", "exec")
    except SyntaxError as exc:
        _emit({
            "status": "error",
            "error_type": "SyntaxError",
            "stderr": f"{exc.msg} (line {exc.lineno})"[:MAX_OUTPUT_BYTES],
            "stdout": "",
        })
        return

    try:
        exec(compiled, namespace)  # noqa: S102
        if job.get("entry_point"):
            entry = namespace.get(job["entry_point"])
            if not callable(entry):
                _emit({
                    "status": "error",
                    "error_type": "MissingEntryPoint",
                    "stderr": f"expected a function named {job['entry_point']!r}"[:MAX_OUTPUT_BYTES],
                    "stdout": captured.getvalue()[:MAX_OUTPUT_BYTES],
                })
                return
            returned = entry(*job["args"])
        else:
            returned = None
    except MemoryError:
        _emit({
            "status": "memory",
            "error_type": "MemoryError",
            "stderr": "Memory limit exceeded (256 MB)",
            "stdout": "",
        })
        return
    except BaseException as exc:  # noqa: BLE001
        import traceback
        _emit({
            "status": "error",
            "error_type": type(exc).__name__,
            "stderr": traceback.format_exc(limit=3)[:MAX_OUTPUT_BYTES],
            "stdout": captured.getvalue()[:MAX_OUTPUT_BYTES],
        })
        return

    try:
        json.dumps(returned)
        serialisable = returned
    except (TypeError, ValueError):
        serialisable = repr(returned)

    _emit({
        "status": "ok",
        "returned": serialisable,
        "stdout": captured.getvalue()[:MAX_OUTPUT_BYTES],
        "stderr": "",
    })


if __name__ == "__main__":
    main()
