"""Synthetic adapter checks; never make model requests or measure configurations."""
import copy,json,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
import catalog_v164 as m
import native_apps_v164 as native

def fixture(engine='hnswlib'):
 c=native.candidates(engine);s={'ids':list(range(10)),'labels':[[float(i+1)] for i in range(10)],'order':list(range(64))};j={'eligible':list(range(10,64)),'condition':'catalog','domains':c['grid_domains'],'sampling_seed':1};return c,s,j
@pytest.mark.parametrize('engine',['ripgrep','hnswlib'])
def test_catalog_features_only(engine):
 c,s,j=fixture(engine);before=copy.deepcopy(s);b=json.loads(m.messages(engine,c,s,'catalog')[1]['content']);assert s==before and len(b['observed_examples'])==10 and len(b['eligible_candidates'])==54
 assert all(len(x)==5 for x in b['eligible_candidates']) and [int(x[0]) for x in b['eligible_candidates']]==list(range(10,64))
 assert 'projection' not in b and len(b['feature_order'])==4

def response(rows):return {'truncated':False,'stop_type':'eos','tokens_predicted':51,'content':json.dumps(rows,separators=(',',':'))}

def test_roundtrip_duplicates_retained():
 c,s,j=fixture();r=response(['10']*10);assert m.parse(r,j)==[10]*10;ids,diag=native.project(c,s,[c['indices'][i] for i in m.parse(r,j)]);assert len(set(ids))==10 and sum(d['duplicate_proposal'] for d in diag)==9
@pytest.mark.parametrize('row',['00','64','99','1',10,None,True])
def test_bad_ids(row):
 _,_,j=fixture()
 with pytest.raises(ValueError):m.parse(response([row]*10),j)

def test_no_normalization_change():
 c,s,j=fixture();ds=[c['indices'][i] for i in range(10,20)];ids,d=native.project(c,s,ds);assert ids==list(range(10,20)) and not any(x['distance'] for x in d)

def test_capacity_bound_and_binding():
 _,_,j=fixture();p=m.make_payload('test',j);rt=type('Fake',(),{'authorized':{}})();v=list('0123456789[],"');proof=m.authorize(rt,p,j,v,500);assert proof['constructive_token_upper_bound_including_eos']==52 and proof['eligible_ids']==j['eligible']
 with pytest.raises(ValueError):m.authorize(rt,{**p,'grammar':'wrong'},j,v,500)
 with pytest.raises(ValueError):m.authorize(rt,p,j,v,3500)

def test_paid_guard():
 from runtime_models_v164 import Runtime
 with pytest.raises(AssertionError):Runtime(Path('/tmp/never-created'),{'allow_paid_api':True})

def test_bad_eligible_grammar():
 with pytest.raises(ValueError):m.id_grammar([1]*54)

def test_unknown_interface():
 c,s,_=fixture()
 with pytest.raises(ValueError):m.messages('hnswlib',c,s,'other')
