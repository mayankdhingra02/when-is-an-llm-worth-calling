import sys,time
from escalation.bounded_process_v57 import run

def test_precise_exit_timestamp_with_slow_monitor(tmp_path):
    def monitor(pid):
        time.sleep(.2)
        return {'rss_bytes':0},None
    result=run([sys.executable,'-c','pass'],cwd=tmp_path,log_path=tmp_path/'log',wall_cap=2,monitor=monitor)
    assert result['exit_code']==0 and result['termination_reason'] is None
    assert result['wall_seconds'] < result['watchdog_elapsed_seconds']

def test_timeout_and_monitor_failure_terminate(tmp_path):
    result=run([sys.executable,'-c','import time; time.sleep(5)'],cwd=tmp_path,log_path=tmp_path/'timeout',wall_cap=.1)
    assert result['exit_code']<0 and result['termination_reason']=='wall_timeout'
    def monitor(pid):raise RuntimeError('synthetic monitoring failure')
    result=run([sys.executable,'-c','import time; time.sleep(5)'],cwd=tmp_path,log_path=tmp_path/'monitor',wall_cap=2,monitor=monitor)
    assert result['exit_code']<0 and result['termination_reason']=='watchdog_error'
