"""No native solve or model call in these synthetic tests."""
import sys,copy,json
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
import native_apps_v163 as m
@pytest.mark.parametrize('engine',m.ENGINES)
def test_candidates(engine):
 c=m.candidates(engine);assert len(c['configs'])==64 and len(c['x'])==64 and len({str(x) for x in c['x']})==64
@pytest.mark.parametrize('engine',m.ENGINES)
def test_projection_no_duplicate(engine):
 c=m.candidates(engine);s={'ids':list(range(10)),'labels':[[1.]]*10,'order':list(range(64))};p=[c['indices'][0]]*10;ids,diag=m.project(c,s,p);assert len(set(ids))==10 and not set(ids)&set(s['ids']) and all(d['matches_prefix'] for d in diag)
def test_invalid_proposal():
 c=m.candidates('hnswlib');s={'ids':list(range(10)),'labels':[[1.]]*10,'order':list(range(64))}
 with pytest.raises(ValueError):m.project(c,s,[[9]*4]*10)
def test_prefix_prompt_only():
 c=m.candidates('ripgrep');s={'ids':list(range(10)),'labels':[[float(i+1)] for i in range(10)],'order':list(range(64))};body=json.loads(m.messages('ripgrep',c,s)[1]['content']);assert len(body['observed_examples'])==10 and len(body['feature_order'])==4
@pytest.mark.parametrize('mode',['sequential_3nn','adaptive_neighbor','gp_ei','random_full'])
def test_branch_purity(mode):
 c=m.candidates('hnswlib');s={'ids':list(range(10)),'labels':[[float(i+1)] for i in range(10)],'order':list(range(64))};old=copy.deepcopy(s);i=m.choose(c,s,mode);assert s==old and i not in s['ids']
def test_runtime_paid_disabled():
 import runtime_models_v163 as r
 with pytest.raises(AssertionError):r.Runtime(Path('/tmp/no-runtime-created'),{'allow_paid_api':True})
