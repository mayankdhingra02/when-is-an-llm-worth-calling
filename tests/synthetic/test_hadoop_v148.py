"""Synthetic tests; none of these values is a measured experimental outcome."""
import copy, json, sys, time
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import hadoop_v148 as h

def record(**extra):return {'framework':'hadoop','workload':'pagerank','datasize':'bigdata','completed':True,'elapsed_time':'100',**extra}

def test_failure_score_is_explicit_penalty_not_measured_runtime():
    assert h.score_record(record(completed=False,elapsed_time=None),'pagerank')==(7200.,'incomplete_failure_penalty')
    assert h.score_record(record(elapsed_time='9000'),'pagerank')==(7200.,'completed_capped')
    assert h.score_record(record(),'pagerank')==(100.,'completed')

@pytest.mark.parametrize('change',[{'completed':'false'},{'elapsed_time':'nan'},{'elapsed_time':'-1'},{'elapsed_time':None},{'framework':'spark'},{'datasize':'huge'}])
def test_invalid_source_fails_closed(change):
    with pytest.raises((ValueError,TypeError)):h.score_record(record(**change),'pagerank')

def fixture():
    c={'x':[[i/19,j] for i in range(20) for j in range(3)],'grid_domains':[list(range(10)),list(range(3))], 'names':['worker_count','vm_type'],'domains':[list(range(20)),['a','b','c']]}
    s={'ids':list(range(10)),'labels':[[100-i] for i in range(10)],'order':list(range(60))}
    return c,s

def test_projection_preserves_unique_budget_and_tie_order():
    c,s=fixture();ids,diags=h.project(c,s,[[0,0]]*10)
    assert len(ids)==len(set(ids))==10 and not set(ids)&set(s['ids'])
    assert sum(x['repeated_proposal'] for x in diags)==9
    t=copy.deepcopy(s);t['ids']=list(range(20));t['labels']=[[1]]*20
    with pytest.raises(ValueError):h.choose(c,t,'sequential_3nn')

def test_search_and_prompt_never_load_hidden_sources(monkeypatch):
    c,s=fixture();c['sources']=['forbidden']*60
    def forbidden(*args):raise AssertionError('Hidden source read')
    monkeypatch.setattr(h,'read',forbidden)
    assert h.choose(c,s,'sequential_3nn') not in s['ids']
    assert len(h.project(c,s,[[0,0]]*10)[0])==10
    assert 'forbidden' not in json.dumps(h.messages(c,s))

def test_charge_invalid_outcome_and_reject_duplicate(tmp_path,monkeypatch):
    monkeypatch.setattr(h,'ROOT',tmp_path);monkeypatch.setattr(h,'O',tmp_path/'results');h.O.mkdir()
    (tmp_path/'configs').mkdir();h.write(tmp_path/'configs/study_v148.json',{'total_new_recorded_acquisitions':2,'total_collection_seconds_cap':60})
    h.write(h.O/'ledger.json',{'acquisitions':0,'collection_started_unix':time.time()})
    h.write(tmp_path/'source.json',record(elapsed_time='nan'))
    c={'x':[[0,0],[1,0]],'sources':['source.json']*2,'source_hashes':[h.sha(tmp_path/'source.json')]*2,'app':'pagerank'}
    oracle=h.Oracle(c,'synthetic')
    with pytest.raises(ValueError):oracle.acquire(0)
    assert h.read(h.O/'ledger.json')['acquisitions']==1
    event=json.loads((h.O/'acquisitions.jsonl').read_text());assert event['value'] is None and event['status']=='invalid_source'
    with pytest.raises(ValueError):oracle.acquire(0)
    assert h.read(h.O/'ledger.json')['acquisitions']==1

def test_failed_classical_gate_prevents_model_start(monkeypatch):
    import collect_models_v148 as collector
    cfg={'total_request_cap':30,'total_models':2,'new_generation_request_cap':15,'max_allocated_output_tokens':15360}
    monkeypatch.setattr(collector,'read',lambda p:cfg if p.name=='study_v148.json' else {'sha256':{}})
    def stop():raise RuntimeError('Synthetic incomplete classical gate')
    monkeypatch.setattr(h,'classical_gate',stop)
    def must_not_start(*args,**kwargs):raise AssertionError('Inference constructed after failed gate')
    monkeypatch.setattr(collector,'Runtime',must_not_start)
    with pytest.raises(RuntimeError,match='incomplete classical gate'):collector.main()
