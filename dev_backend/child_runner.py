"""Windows-safe, hardened code executor for the dev backend.

Runs as a fresh subprocess: reads a JSON job from stdin, execs the user's code
with a RESTRICTED set of builtins (no open/eval/exec/__import__ except a small
allow-list of safe modules), calls the entry point against one test case, and
prints a JSON result.

This is the DEV stand-in for backend/app/services/_sandbox_runner.py. Real OS
isolation (uid drop, rlimits, network namespace) is Linux-only and lives in the
production backend. Here we harden what is possible in portable stdlib Python:
  * the parent launches us with a SCRUBBED environment (no API keys reachable),
  * imports are limited to an algorithm-friendly allow-list,
  * dangerous builtins are removed.
Combined with the parent's static AST check and wall-clock timeout, this is
enough to safely let strangers try coding problems in a small public demo. It is
NOT a substitute for a real sandbox at scale — use Judge0/containers for that.
"""

from __future__ import annotations

import builtins as _builtins
import io
import json
import sys

MAX_OUTPUT_BYTES = 10 * 1024

# Modules a normal algorithm/data-structure solution might legitimately use.
ALLOWED_MODULES = {
    "math", "cmath", "collections", "itertools", "functools", "heapq", "bisect",
    "string", "re", "random", "statistics", "operator", "typing", "numbers",
    "fractions", "decimal", "datetime", "copy", "array", "enum", "dataclasses",
    "abc", "queue",
}

_REAL_IMPORT = _builtins.__import__


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
    safe["__build_class__"] = _builtins.__build_class__  # needed for `class` defs
    return safe


def _emit(payload: dict) -> None:
    sys.__stdout__.write(json.dumps(payload))
    sys.__stdout__.flush()


def main() -> None:
    job = json.loads(sys.stdin.read())

    captured = io.StringIO()
    sys.stdout = captured

    namespace: dict = {"__name__": "__solution__", "__builtins__": _safe_builtins()}
    try:
        compiled = compile(job["code"], "solution.py", "exec")
    except SyntaxError as exc:
        _emit({"status": "error", "error_type": "SyntaxError",
               "stderr": f"{exc.msg} (line {exc.lineno})", "stdout": ""})
        return

    try:
        exec(compiled, namespace)  # noqa: S102 -- restricted builtins, scrubbed env
        entry = namespace.get(job["entry_point"])
        if not callable(entry):
            _emit({"status": "error", "error_type": "MissingEntryPoint",
                   "stderr": f"expected a function named {job['entry_point']!r}",
                   "stdout": captured.getvalue()[:MAX_OUTPUT_BYTES]})
            return
        returned = entry(*job["args"])
    except BaseException as exc:  # noqa: BLE001 -- must not leak a crash
        import traceback
        _emit({"status": "error", "error_type": type(exc).__name__,
               "stderr": traceback.format_exc(limit=3)[-2000:],
               "stdout": captured.getvalue()[:MAX_OUTPUT_BYTES]})
        return

    try:
        json.dumps(returned)
        serialisable = returned
    except (TypeError, ValueError):
        serialisable = repr(returned)

    _emit({"status": "ok", "returned": serialisable,
           "stdout": captured.getvalue()[:MAX_OUTPUT_BYTES], "stderr": ""})


if __name__ == "__main__":
    main()
