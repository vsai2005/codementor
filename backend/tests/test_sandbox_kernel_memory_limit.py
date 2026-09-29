"""Kernel memory backstop (RLIMIT_DATA) in the sandbox runner.

The parent's RSS watchdog polls every 15 ms; under host load a program that allocates
fast and returns could finish before a poll saw it. These tests blind the watchdog so
only the kernel limit can stop the program, making that race deterministic.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

from app.services import sandbox

pytestmark = pytest.mark.skipif(
    not sys.platform.startswith("linux"), reason="RLIMIT_DATA backstop is Linux-only"
)

MIB = 1024 * 1024
RUNNER_DIR = Path(sandbox._RUNNER).parent


@pytest.fixture
def blind_watchdog(monkeypatch):
    """Make the RSS watchdog see nothing, as if every poll arrived too late."""
    monkeypatch.setattr(sandbox, "_get_process_tree_rss", lambda pid: None)


def _run(code: str, expected=None):
    return sandbox.run_test_cases(code, "solve", [{"args": [], "expected": expected}]).results[0]


def test_fast_allocation_over_limit_is_stopped_by_the_kernel(blind_watchdog):
    code = "def solve():\n    blocks = [bytearray(MIB) for _ in range(300)]\n    return len(blocks)\n".replace(
        "MIB", str(MIB)
    )
    res = _run(code, expected=300)
    assert not res.passed
    assert res.status == "memory"


def test_single_huge_allocation_is_stopped_by_the_kernel(blind_watchdog):
    res = _run(f"def solve():\n    data = bytearray({1024 * MIB})\n    return len(data)\n", expected=1024 * MIB)
    assert not res.passed
    assert res.status == "memory"


def test_near_limit_legitimate_workload_still_succeeds(blind_watchdog):
    code = (
        "def solve():\n"
        f"    data = bytearray({205 * MIB})\n"
        "    data[::4096] = bytes(len(data[::4096]))\n"
        "    return len(data)\n"
    )
    res = _run(code, expected=205 * MIB)
    assert res.passed, res.stderr
    assert res.status == "ok"


def test_memory_freed_during_the_run_is_reusable(blind_watchdog):
    code = (
        "def solve():\n"
        "    total = 0\n"
        "    for _ in range(4):\n"
        f"        chunk = bytearray({150 * MIB})\n"
        "        total += len(chunk)\n"
        "        del chunk\n"
        "    return total\n"
    )
    res = _run(code, expected=4 * 150 * MIB)
    assert res.passed, res.stderr


def test_sandboxed_code_cannot_raise_the_limit():
    code = (
        "def solve():\n"
        "    try:\n"
        "        import resource\n"
        "        resource.setrlimit(resource.RLIMIT_DATA, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))\n"
        "        return 'raised'\n"
        "    except BaseException as exc:\n"
        "        return type(exc).__name__\n"
    )
    res = _run(code)
    assert res.status in ("ok", "wrong_answer", "error"), res.stderr
    assert res.returned != "raised"


def _apply_in_child(preset_hard: int | None) -> tuple[int, int]:
    """Call _apply_memory_rlimit(256 MiB) in a fresh process, optionally with a lower hard limit."""
    preset = (
        f"resource.setrlimit(resource.RLIMIT_DATA, ({preset_hard}, {preset_hard}))\n" if preset_hard else ""
    )
    probe = (
        "import resource, sys\n"
        f"sys.path.insert(0, {str(RUNNER_DIR)!r})\n"
        f"{preset}"
        "import _sandbox_runner\n"
        f"_sandbox_runner._apply_memory_rlimit({256 * MIB})\n"
        "print(*resource.getrlimit(resource.RLIMIT_DATA))\n"
    )
    out = subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True, timeout=30, env=os.environ)
    assert out.returncode == 0, out.stderr
    soft, hard = (int(x) for x in out.stdout.split())
    return soft, hard


def test_limit_is_set_with_soft_equal_to_hard():
    assert _apply_in_child(None) == (256 * MIB, 256 * MIB)


def test_an_existing_lower_hard_limit_is_respected():
    assert _apply_in_child(128 * MIB) == (128 * MIB, 128 * MIB)
