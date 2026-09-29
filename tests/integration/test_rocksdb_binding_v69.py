"""Real native engine on tiny SYNTHETIC fixtures, not performance measurements."""
import sys
from pathlib import Path
import pytest

RUNTIME=Path(__file__).resolve().parents[2]/'.local-runtime/rocksdb-v69'
pytestmark=pytest.mark.skipif(not (RUNTIME/'rocksdict').exists(),reason='optional pinned local runtime absent')

@pytest.mark.parametrize('cache_mib',[1,2,8])
def test_native_reopen_keeps_requested_cache(tmp_path,monkeypatch,cache_mib):
    monkeypatch.syspath_prepend(str(RUNTIME))
    from escalation.rocksdb_binding_v69 import open_configured,active_readback
    config={'cache_mib':cache_mib,'block_size':4096,'restart_interval':16}
    db,cache=open_configured(tmp_path/'db',config)
    db[b'synthetic-key']=b'x'*1000
    db.flush();db.close();del db,cache
    db,cache=open_configured(tmp_path/'db',config)
    try:
        assert db[b'synthetic-key']==b'x'*1000
        assert active_readback(tmp_path/'db',config)['cache_capacity_bytes']==cache_mib*1024**2
        assert cache.get_usage()>0  # the supplied cache is actually attached
    finally:db.close()
