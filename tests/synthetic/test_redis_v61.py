import os,sys
import numpy as np
import pytest
from escalation.redis_v61 import grid,encode,timed_child

def test_grid_has_80_unique_domain_only_encodings():
    g=grid();assert len(g)==80 and len({tuple(c.items()) for c in g})==80
    x=encode(g);assert x.shape==(80,6) and np.min(x)==0 and np.max(x)==1
    assert all(c['io-threads']!=1 or c['io-threads-do-reads']=='no' for c in g)

def test_timing_preserves_child_failure(tmp_path):
    r=timed_child([sys.executable,'-c','raise SystemExit(7)'],tmp_path/'log',os.environ.copy(),cap=2)
    assert r['exit_code']==7 and 0<r['wall_seconds']<2

def test_timing_kills_hung_fixture(tmp_path):
    with pytest.raises(TimeoutError):timed_child([sys.executable,'-c','import time;time.sleep(5)'],tmp_path/'log',os.environ.copy(),cap=.05)
