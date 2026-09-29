"""Synthetic API faults and a bounded owned-process resource check."""
import sys,ctypes,os,subprocess,time
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from process_rss_v129 import TaskInfo,group_rss,read_pid,rss

class Fake:
    def __init__(self,count=2,partial=False):self.count=count;self.partial=partial
    def proc_listpgrppids(self,p,buf,n):buf[0]=10;buf[1]=11;return self.count
    def proc_pidinfo(self,p,f,arg,buf,n):
        ctypes.cast(buf,ctypes.POINTER(TaskInfo)).contents.resident_size=p*1024
        return n-1 if self.partial else n

def test_pid_count_not_bytes_and_group_sum():assert group_rss(Fake(),123)==21*1024
@pytest.mark.parametrize('count',[0,-1,4096,4097])
def test_missing_truncated_groups_rejected(count):
    with pytest.raises(OSError):group_rss(Fake(count),123)
def test_partial_pid_read_rejected():
    with pytest.raises(OSError):read_pid(Fake(partial=True),10)
@pytest.mark.skipif(sys.platform!='darwin',reason='local macOS monitor')
def test_owned_live_process_and_repeated_reads():
    assert rss(-1)>0
    p=subprocess.Popen([sys.executable,'-c','import time; time.sleep(10)'],start_new_session=True)
    try:
        time.sleep(.15);start=time.monotonic();values=[rss(p.pid) for _ in range(100)]
        assert min(values)>0 and max(values)<1024**3 and time.monotonic()-start<5
    finally:p.terminate();p.wait(timeout=3)
