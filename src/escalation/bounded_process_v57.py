"""Bounded process-group execution with an exit-waiter timestamp.

Watchdog polls memory/scratch separately; measured completion is not delayed to
its next poll. The watchdog still perturbs the host and is not a hard RSS cap.
"""
import os
import signal
import subprocess
import threading
import time


def run(command, *, cwd, log_path, wall_cap, monitor=None, env=None, interval=.1):
    start = time.monotonic()
    finished = threading.Event()
    stamp = {}
    maxima = {}
    reason = None
    with log_path.open('xb') as log:
        p = subprocess.Popen(command, cwd=cwd, stdout=log, stderr=subprocess.STDOUT,
                             start_new_session=True, env=env)
        def waiter():
            stamp['exit_code'] = p.wait()
            stamp['wall_seconds'] = time.monotonic() - start
            finished.set()
        worker = threading.Thread(target=waiter, daemon=True)
        worker.start()
        try:
            while not finished.is_set():
                if time.monotonic() - start >= wall_cap:
                    reason = 'wall_timeout'
                if monitor is not None and reason is None:
                    values, violation = monitor(p.pid)
                    for k, value in values.items():
                        maxima[k] = max(maxima.get(k, 0), value)
                    reason = violation
                if reason:
                    try:
                        os.killpg(p.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    break
                finished.wait(min(interval, max(0, wall_cap-(time.monotonic()-start))))
        except Exception as exc:
            reason = 'watchdog_error'
            stamp['watchdog_error'] = repr(exc)
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        finally:
            if not finished.wait(5):
                try:
                    os.killpg(p.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                finished.wait(5)
            worker.join(timeout=1)
    if not finished.is_set():
        raise RuntimeError('Process did not terminate after SIGKILL')
    if stamp['wall_seconds'] > wall_cap and reason is None:
        reason = 'wall_timeout'
    return {**stamp, 'termination_reason': reason, 'watchdog_elapsed_seconds': time.monotonic()-start,
            'sampled_maxima': maxima}
