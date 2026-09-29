"""Synthetic boundary tests; never counted as live or optimizer measurements."""
import csv
import pytest
from escalation.offline_live_v16 import RecordedOracle


def source(tmp_path):
    p=tmp_path/'synthetic.csv'
    p.write_text('family,config_id,successful_trials,median_compression_ms,compressed_bytes\nsynthetic,a,3,1.5,100\nsynthetic,b,3,DO_NOT_PARSE_HIDDEN,90\n')
    return p


def test_hidden_target_is_not_parsed_and_duplicate_is_not_free(tmp_path):
    calls=[];o=RecordedOracle(source(tmp_path),'synthetic',['a','b'],calls.append)
    assert o.acquire(0)==[1.5,100]
    with pytest.raises(ValueError,match='duplicate'):o.acquire(0)
    assert len(calls)==1


def test_bad_target_attempt_is_charged_and_cannot_be_retried(tmp_path):
    calls=[];o=RecordedOracle(source(tmp_path),'synthetic',['a','b'],calls.append)
    with pytest.raises(ValueError):o.acquire(1)
    assert len(calls)==1 and o.acquired=={1:None}
    with pytest.raises(ValueError):o.acquire(1)


def test_saved_prefix_counts_toward_budget_and_is_not_shared_mutable_state(tmp_path):
    prefix={0:[1.5,100]};calls=[]
    o=RecordedOracle(source(tmp_path),'synthetic',['a','b'],calls.append,budget=1,prefix=prefix)
    prefix[0][0]=999
    assert o.acquired[0][0]==1.5
    with pytest.raises(RuntimeError,match='budget'):o.acquire(1)
    assert not calls
