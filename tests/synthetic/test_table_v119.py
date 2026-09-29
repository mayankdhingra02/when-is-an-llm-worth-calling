"""Protocol and inherited isolation checks; these are not measured outcomes."""
import sys,json
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'src'))
from escalation.finite_v6 import load_candidates
from escalation.transfer_v41 import IndexedOracle
from evaluate_table_v119 import known_sum


def spec(path):
    import hashlib
    return dict(path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),delimiter=',',feature_names=['x'],objective_columns=['throughput','latency'],primary_objective='latency',metadata_columns=[],filters={},rows=30,duplicates=0,direction='-')


def test_hidden_targets_can_be_poisoned(tmp_path):
    p=tmp_path/'t.csv';p.write_text('x,throughput,latency\n'+''.join(f'{i},IGNORE,POISON\n' for i in range(30)))
    c=load_candidates(spec(p));assert len(c.x)==30
    o=IndexedOracle(spec(p),c)
    with pytest.raises(ValueError):o.acquire(0)
    assert o.new_accesses==1 and 0 in o.acquired


def test_unused_throughput_and_budget(tmp_path):
    p=tmp_path/'t.csv';p.write_text('x,throughput,latency\n'+''.join(f'{i},POISON,{i+1}\n' for i in range(30)))
    s=spec(p);c=load_candidates(s);o=IndexedOracle(s,c)
    for i in range(20):assert o.acquire(i)==[i+1]
    with pytest.raises(RuntimeError):o.acquire(20)
    assert o.new_accesses==20


def test_missing_usage_is_unknown():
    assert known_sum([20,None]) is None
    assert known_sum([20,30])==50


def test_fixed_external_scope_and_bounded_limits():
    c=json.loads((ROOT/'configs/study_v119.json').read_text());m=json.loads((ROOT/'data/manifest_v119.json').read_text())
    assert c['new_generation_request_cap']==5 and c['max_allocated_output_tokens']==640
    assert c['max_classical_acquisitions']+c['max_llm_continuation_acquisitions']==c['max_new_recorded_objective_acquisitions']==300
    assert not c['allow_paid_api'] and c['max_external_spend_usd']==0
    assert m['datasets'][0]['stronger_v52_admission'] is False and m['datasets'][0]['system_group']=='storm'
