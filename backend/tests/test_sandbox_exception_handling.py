"""Regression tests for the narrowed exception handling in app/services/sandbox.py."""

import asyncio
import logging
import os
import subprocess
import sys

import pytest

from app.services import sandbox


@pytest.fixture
def no_psutil(monkeypatch):
    """Simulate a production image without the optional psutil helper."""
    monkeypatch.setitem(sys.modules, "psutil", None)  # makes `import psutil` raise ImportError


def test_optional_psutil_returns_none_when_missing(no_psutil):
    assert sandbox._optional_psutil() is None


def test_optional_psutil_returns_module_when_present():
    pytest.importorskip("psutil")
    assert sandbox._optional_psutil().__name__ == "psutil"


def test_process_start_time_without_psutil_is_none_not_an_exception(no_psutil, monkeypatch):
    # Force the non-Linux path so /proc is not consulted.
    monkeypatch.setattr(sandbox.sys, "platform", "darwin")
    assert sandbox._process_start_time(os.getpid()) is None


@pytest.mark.skipif(sys.platform != "win32", reason="psapi fallback is Windows-only")
def test_windows_memory_measurement_falls_back_when_psutil_missing(no_psutil):
    """Previously `except (psutil.NoSuchProcess, ...)` raised NameError here."""
    rss = sandbox._get_process_tree_rss(os.getpid())
    assert isinstance(rss, int) and rss > 0


@pytest.mark.skipif(sys.platform != "win32", reason="Windows kill path")
def test_windows_kill_without_psutil_still_terminates_process(no_psutil):
    proc = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    try:
        sandbox._kill_process_group(proc.pid)
        assert proc.wait(timeout=10) is not None
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()


def test_network_probe_reports_unavailable_when_unshare_missing(monkeypatch):
    monkeypatch.setattr(sandbox.shutil, "which", lambda name: None)
    assert sandbox._network_namespace_available() is False


@pytest.mark.parametrize(
    "exc",
    [OSError("cannot exec"), subprocess.TimeoutExpired(cmd="unshare", timeout=3)],
)
def test_network_probe_handles_expected_failures(monkeypatch, exc):
    monkeypatch.setattr(sandbox.shutil, "which", lambda name: "/usr/bin/unshare")

    def boom(*args, **kwargs):
        raise exc

    monkeypatch.setattr(sandbox.subprocess, "run", boom)
    assert sandbox._network_namespace_available() is False


def test_network_probe_does_not_mask_unexpected_errors(monkeypatch):
    monkeypatch.setattr(sandbox.shutil, "which", lambda name: "/usr/bin/unshare")

    def boom(*args, **kwargs):
        raise RuntimeError("bug")

    monkeypatch.setattr(sandbox.subprocess, "run", boom)
    with pytest.raises(RuntimeError):
        sandbox._network_namespace_available()


def test_network_probe_reflects_returncode(monkeypatch):
    monkeypatch.setattr(sandbox.shutil, "which", lambda name: "/usr/bin/unshare")
    for code, expected in ((0, True), (1, False)):
        monkeypatch.setattr(
            sandbox.subprocess,
            "run",
            lambda *a, _c=code, **k: subprocess.CompletedProcess(a, _c),
        )
        assert sandbox._network_namespace_available() is expected


def test_memory_watchdog_failure_is_logged_not_silent(monkeypatch, capture_logs):
    records = capture_logs("app.services.sandbox")

    def boom(pid):
        raise RuntimeError("measurement bug")

    monkeypatch.setattr(sandbox, "_get_process_tree_rss", boom)

    async def run():
        await asyncio.wait_for(
            sandbox._watch_process_memory(12345, 1024, [False], asyncio.Event()), timeout=5
        )

    asyncio.run(run())
    errors = [r for r in records if r.levelno == logging.ERROR]
    assert len(errors) == 1
    assert errors[0].exc_info is not None and errors[0].exc_info[0] is RuntimeError


def test_memory_watchdog_still_kills_on_breach(monkeypatch):
    killed = []
    monkeypatch.setattr(sandbox, "_get_process_tree_rss", lambda pid: 10_000)
    monkeypatch.setattr(sandbox, "_kill_process_group", lambda pid, **kw: killed.append(pid))
    flag = [False]

    async def run():
        await asyncio.wait_for(
            sandbox._watch_process_memory(4321, 1024, flag, asyncio.Event()), timeout=5
        )

    asyncio.run(run())
    assert flag == [True]
    assert killed == [4321]


def test_execute_script_reports_error_for_non_object_json(monkeypatch):
    """Runner output that is JSON but not an object is an error result, not a crash."""

    class _Proc:
        pid = 0  # falsy: skips watchdog and process-group handling
        returncode = 0

        async def communicate(self, input=None):
            return b"[1, 2, 3]", b""

        async def wait(self):
            return 0

    async def fake_exec(*args, **kwargs):
        return _Proc()

    monkeypatch.setattr(sandbox.asyncio, "create_subprocess_exec", fake_exec)
    result = asyncio.run(sandbox.execute_script_async("print(1)"))
    assert result["status"] == "error"
    assert result["stdout"] == "[1, 2, 3]"
