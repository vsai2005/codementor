"""POSIX cleanup probes run in a separate session to contain killpg regressions."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import time

import psutil
import pytest

from app.services import sandbox


pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="POSIX process groups only")


_PROBE = r'''
import asyncio, json, os, sys, time
from app.services import sandbox

mode, pidfile = sys.argv[1:]
child_code = r"""
import json, subprocess, sys, time
grandchild = subprocess.Popen(
    [sys.executable, '-c', 'import time; time.sleep(60)'],
    stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
)
with open(sys.argv[1], 'w') as out:
    out.write(str(grandchild.pid))
if sys.argv[2] == 'normal':
    sys.stdin.read()
    print(json.dumps({'status': 'ok', 'returned': 1, 'stdout': '', 'stderr': ''}))
else:
    time.sleep(60)
"""
sandbox._build_argv = lambda: [sys.executable, '-c', child_code, pidfile, mode]
sandbox.WALL_SECONDS = 0.6 if mode == 'timeout' else 2.0
launch = asyncio.create_subprocess_exec
launch_options = []
async def tracked_launch(*args, **kwargs):
    if os.environ.get('CM_DISABLE_PROCESS_GROUP_ISOLATION') == '1':
        kwargs['start_new_session'] = False
    launch_options.append(kwargs.get('start_new_session'))
    process = await launch(*args, **kwargs)
    with open(pidfile + '.leader', 'w') as out:
        out.write(str(process.pid))
    if mode == 'exception':
        class BrokenCommunication:
            pid = process.pid
            async def communicate(self, input=None):
                for _ in range(100):
                    if os.path.exists(pidfile):
                        break
                    await asyncio.sleep(0.01)
                assert os.path.exists(pidfile)
                raise RuntimeError('injected communicate failure')
            async def wait(self):
                return await process.wait()
        return BrokenCommunication()
    return process
asyncio.create_subprocess_exec = tracked_launch

async def run():
    if mode == 'memory':
        def high_rss(_pid):
            return sandbox.MEMORY_BYTES + 1 if os.path.exists(pidfile) else 0
        sandbox._get_process_tree_rss = high_rss
    if mode == 'exception':
        try:
            await sandbox._run_one_async('', 'solve', [], 1, 0)
        except RuntimeError as exc:
            assert str(exc) == 'injected communicate failure'
        else:
            raise AssertionError('communication exception was suppressed')
    elif mode == 'cancel':
        task = asyncio.create_task(sandbox._run_one_async('', 'solve', [], 1, 0))
        for _ in range(100):
            if os.path.exists(pidfile):
                break
            await asyncio.sleep(0.01)
        assert os.path.exists(pidfile)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        else:
            raise AssertionError('task did not cancel')
    else:
        result = await sandbox._run_one_async('', 'solve', [], 1, 0)
        assert result.status == {'normal': 'ok', 'timeout': 'timeout', 'memory': 'memory'}[mode], result
    assert launch_options == [True], launch_options

asyncio.run(run())
'''


def _inactive(pid: int) -> bool:
    try:
        process = psutil.Process(pid)
        return not process.is_running() or process.status() == psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return True


def _remove_probe_processes(pidfile: str) -> None:
    for path in (pidfile, pidfile + ".leader"):
        if os.path.exists(path):
            pid = int(open(path, encoding="ascii").read())
            if not _inactive(pid):
                try:
                    psutil.Process(pid).kill()
                except psutil.NoSuchProcess:
                    pass


@pytest.mark.parametrize("mode", ["normal", "timeout", "memory", "cancel", "exception"])
def test_isolated_group_cleans_descendants(mode: str):
    with tempfile.TemporaryDirectory(prefix="cm_cleanup_probe_") as directory:
        pidfile = os.path.join(directory, "grandchild.pid")
        try:
            completed = subprocess.run(
                [sys.executable, "-c", _PROBE, mode, pidfile],
                capture_output=True, text=True, timeout=10, start_new_session=True,
            )
            assert completed.returncode == 0, completed.stderr
            assert os.path.exists(pidfile), "probe did not create a descendant"
            pid = int(open(pidfile, encoding="ascii").read())
            for _ in range(100):
                if _inactive(pid):
                    break
                time.sleep(0.01)
            assert _inactive(pid), f"descendant {pid} survived {mode} cleanup: {completed.stderr}"
        finally:
            _remove_probe_processes(pidfile)


def test_removing_session_isolation_is_detected():
    """Run the mutation in its own session, so a broken killpg cannot hit pytest."""
    with tempfile.TemporaryDirectory(prefix="cm_cleanup_mutation_") as directory:
        pidfile = os.path.join(directory, "grandchild.pid")
        env = dict(os.environ, CM_DISABLE_PROCESS_GROUP_ISOLATION="1")
        try:
            completed = subprocess.run(
                [sys.executable, "-c", _PROBE, "normal", pidfile],
                capture_output=True, text=True, timeout=10, start_new_session=True, env=env,
            )
            assert completed.returncode != 0
            assert "launch_options" not in completed.stderr  # no test harness error
            assert "[False]" in completed.stderr
        finally:
            _remove_probe_processes(pidfile)


def test_changed_pid_identity_cannot_signal_a_live_group():
    proc = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(15)"], start_new_session=True
    )
    try:
        birth = sandbox._process_start_time(proc.pid)
        assert birth is not None
        sandbox._kill_process_group(
            proc.pid, isolated_group=True, expected_start_time=birth + 1
        )
        assert proc.poll() is None
    finally:
        proc.kill()
        proc.wait(timeout=3)
