"""Toy objective tests in an explicit synthetic namespace, never research data."""
import json,subprocess,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
def toy(arm):
    raw=[[i//8,i%8,bool(i%2)] for i in range(32)]
    return {'raw_features':raw,'prefix':{'ids':list(range(10)),'labels':[[float(30-i)] for i in range(10)],'order':list(range(32))},'arm':arm}
def run_toy(body,offset=0):
    command=['/opt/homebrew/bin/python3.13','-c',"import sys,json;sys.path.insert(0,'scripts');from ezr_bridge_v169 import run;b=json.loads(sys.stdin.readline());print(json.dumps(run(b,lambda i,t:float(50-i))))"]
    p=subprocess.run(command,cwd=ROOT,input=json.dumps(body),capture_output=True,text=True,timeout=10);assert p.returncode==0,p.stderr;return json.loads(p.stdout)
@pytest.mark.parametrize('arm',['ezr_upstream_centroid','ezr_upstream_bayes'])
def test_source_execution_budget_and_prefix(arm):
    body=toy(arm);r=run_toy(body);ids=[x['row_id'] for x in r['new_labels']]
    assert len(ids)==len(set(ids))==7 and not set(ids)&set(body['prefix']['ids'])
    assert r['prefix_cache_hits']==body['prefix']['ids'] and r['source_defaults']['budget']==7
    assert r['symbolic']==[False,False,True] and r['headers'][-2:] == ['RowX','Loss-']
    for step,t in enumerate(r['trace']):
        assert t['acquired_ids']==list(range(10))+ids[:step]
        assert t['row_id']==min(t['scores'],key=lambda x:x['score'])['row_id']
@pytest.mark.parametrize('arm',['ezr_upstream_centroid','ezr_upstream_bayes'])
def test_repeat_deterministic_source_choices(arm):
    a=run_toy(toy(arm));b=run_toy(toy(arm));a.pop('optimizer_process_cpu_seconds');b.pop('optimizer_process_cpu_seconds');assert a==b
def test_bad_prefix_rejected():
    b=toy('ezr_upstream_centroid');b['prefix']['ids'][-1]=0
    with pytest.raises(AssertionError):run_toy(b)
def test_hidden_outcome_table_rejected():
    b=toy('ezr_upstream_centroid');b['hidden_outcomes']=[1.]*32
    with pytest.raises(AssertionError):run_toy(b)
def test_owner_scalar_distance():
    code="""import sys,json,math
sys.path.insert(0,'scripts')
from ezr_bridge_v169 import load_owner
m=load_owner();n=m.Num('X');m.adds([1.,2.,3.],n)
assert n.mu==2. and n.sd==1.
assert m.norm(n,2.)==.5
assert abs(m.aha(n,1.,3.)-(1/(1+math.exp(-1.7))-1/(1+math.exp(1.7))))<1e-12
print('ok')
"""
    p=subprocess.run(['/opt/homebrew/bin/python3.13','-c',code],cwd=ROOT,capture_output=True,text=True,timeout=10);assert p.returncode==0,p.stderr
