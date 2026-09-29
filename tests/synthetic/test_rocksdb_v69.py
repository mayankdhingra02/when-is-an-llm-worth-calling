"""Synthetic domain, payload, request and engine-readback fixtures only."""
import pytest
from escalation.rocksdb_v69 import grid, validate_config, trace, fnv64, payload, verify_value, readback


def test_grid_is_nominal_and_distinct():
    rows=grid();assert len(rows)==512
    assert len({tuple(r.values()) for r in rows})==512
    for r in rows:validate_config(r)


@pytest.mark.parametrize('change',[{'cache_mib':0},{'block_size':1000},{'restart_interval':True},{'extra':1}])
def test_invalid_domain(change):
    row=grid()[0]|change
    with pytest.raises(ValueError):validate_config(row)


def test_frozen_trace_deterministic():
    a=trace(count=1000);assert a==trace(count=1000)
    assert a!=trace(seed=69002,count=1000)
    assert all(0<=x<65536 for x in a)
    assert len(set(a))<len(a)


def test_fnv_independent_byte_reference():
    for n in [0,1,12345,10000000000]:
        h=14695981039346656037
        for b in n.to_bytes(8,'little'):
            h=((h^b)*1099511628211)%(2**64)
        assert fnv64(n)==abs(int.from_bytes(h.to_bytes(8,'little'),'little',signed=True))


@pytest.mark.parametrize('mode',['missing','extra','corrupt','none'])
def test_exact_payload_rejects(mode):
    expected=payload(2);assert len(expected)==1000;verify_value(expected,expected)
    v={'missing':expected[:-100],'extra':expected+b'x','corrupt':b'x'+expected[1:],'none':None}[mode]
    with pytest.raises(ValueError):verify_value(v,expected)


def test_readback(tmp_path):
    c={'cache_mib':8,'block_size':4096,'restart_interval':16}
    (tmp_path/'OPTIONS-0001').write_text('block_size=4096\nblock_restart_interval=16\n')
    (tmp_path/'LOG').write_text('capacity : 8388608\n')
    assert readback(tmp_path,c)['cache_capacity_bytes']==8388608
    (tmp_path/'LOG').write_text('capacity : 1048576\n')
    with pytest.raises(ValueError):readback(tmp_path,c)
    (tmp_path/'LOG').write_text('capacity : 8388608\n')
    (tmp_path/'OPTIONS-0001').write_text('block_size=1024\nblock_restart_interval=16\n')
    with pytest.raises(ValueError):readback(tmp_path,c)
