import pytest
from escalation.rocksdb_binding_v69 import active_readback

def test_stale_log_cannot_certify_current_cache(tmp_path):
    c={'cache_mib':1,'block_size':4096,'restart_interval':16}
    (tmp_path/'OPTIONS-000001').write_text('block_size=4096\nblock_restart_interval=16\n')
    (tmp_path/'LOG.old.1').write_text('capacity : 1048576\n')
    (tmp_path/'LOG').write_text('RocksDB version: 9.8.4\n capacity : 8388608\n')
    with pytest.raises(ValueError,match='active cache mismatch'):active_readback(tmp_path,c)
    (tmp_path/'LOG').write_text('RocksDB version: 9.8.4\n capacity : 1048576\n')
    assert active_readback(tmp_path,c)['cache_capacity_bytes']==1048576
