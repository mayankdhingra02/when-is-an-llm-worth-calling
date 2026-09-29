"""Synthetic budget/projection/leakage guards, no measured research results."""
import copy,json,sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import native_study_v153 as n

def prefix():return {'ids':list(range(10)),'labels':[[float(20-i)] for i in range(10)],'order':list(range(64))}
def test_candidate_schema():
 c=n.candidate();assert len(c['x'])==len({tuple(x) for x in c['raw_features']})==64
 assert all(len(d)==8 for d in c['domains'])
def test_projection_unique_and_valid():
 c=n.candidate();s=prefix();ids,diag=n.project(c,s,[[0,0]]*10);assert len(set(ids))==10;assert not set(ids)&set(s['ids']);assert sum(x['repeated_proposal'] for x in diag)==9
 assert len(ids[:7])==7
@pytest.mark.parametrize('bad',[[[8,0]]*10,[[0,0]]*9,[[False,0]]*10])
def test_bad_proposal_rejected(bad):
 with pytest.raises(ValueError):n.project(n.candidate(),prefix(),bad)
def test_search_stops_at17_reserving3_validation():
 s=prefix()
 for _ in range(7):
  i=n.choose(n.candidate(),s,'sequential_3nn');s['ids'].append(i);s['labels'].append([10.])
 assert len(s['ids'])+3==20
 with pytest.raises(ValueError):n.choose(n.candidate(),s,'sequential_3nn')
def test_prompt_prefix_only():
 c=n.candidate();s=prefix();a=n.messages(c,s);c['hidden_labels']=[-1e9]*64;assert a==n.messages(c,s)
 body=json.loads(a[1]['content']);assert len(body['observed_examples'])==10 and 'hidden_labels' not in body
 assert 'first seven' in a[0]['content']
def test_global_budget_prevents_native_start(tmp_path,monkeypatch):
 monkeypatch.setattr(n,'O',tmp_path);(tmp_path/'ledger.json').write_text(json.dumps({'acquisitions':400,'collection_started_unix':0}))
 monkeypatch.setattr(n.subprocess,'Popen',lambda *a,**k:pytest.fail('Native process must not launch'))
 with pytest.raises(PermissionError):n.measure(0,'synthetic','validation')
def test_classical_gate_incomplete_before_inference(tmp_path,monkeypatch):
 monkeypatch.setattr(n,'O',tmp_path);(tmp_path/'ledger.json').write_text(json.dumps({'acquisitions':224}))
 with pytest.raises(AssertionError):n.classical_gate()
