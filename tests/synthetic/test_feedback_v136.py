"""Synthetic-only information-flow, representation and budget contracts."""
import copy,sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from feedback_v136 import messages,capacity,parse,project,payload,check_payload,ALPHABET
def fixture():
 xs=[(float(i%2),float(i//2)) for i in range(24)]
 p={'ids':list(range(10)),'labels':[[float(i+1)] for i in range(10)],'order':list(range(24))}
 s=copy.deepcopy(p);s['ids'] += [10,11];s['labels'] += [[.5],[.2]]
 return xs,p,s
def test_masked_noninterference_and_feedback_sensitivity():
 xs,p,s=fixture();other=copy.deepcopy(s);other['labels'][-2:]=[[999.],[888.]]
 f=lambda st,mode:messages(['a','b'],xs,p,st,'time','-',mode)
 assert f(s,'masked')==f(other,'masked')
 assert f(s,'feedback')!=f(other,'feedback')
 assert f(p,'feedback')==f(p,'masked')
def test_prefix_tamper_rejected():
 xs,p,s=fixture();s['labels'][0]=[123.]
 with pytest.raises(ValueError):messages(['a','b'],xs,p,s,'time','-','masked')
def test_capacity_and_context():
 ds=[[0,1]]*59
 assert capacity(ds,list(ALPHABET+'[],"'),3000)['constructive_token_upper_bound_including_eos']==126
 with pytest.raises(ValueError):capacity(ds,list(ALPHABET+'[],"'),4000)
 with pytest.raises(ValueError):capacity(ds,[],10)
def test_repeated_projection_still_acquires_unique_rows():
 xs,p,s=fixture();rows,diag=project([xs[0],xs[0]],xs,s)
 assert len(set(rows))==2 and not set(rows)&set(s['ids']) and diag[1]['repeated_proposal']
def test_parse_and_payload_fail_closed():
 ds=[[0,1]]*2;r={'truncated':False,'stop_type':'eos','tokens_predicted':8,'content':'["00","11"]'}
 assert parse(r,ds)==[(0,0),(1,1)]
 for bad in [{'truncated':True},{'content':'["02","11"]'},{'tokens_predicted':257},{'content':'["00", "11"]'}]:
  with pytest.raises(ValueError):parse({**r,**bad},ds)
 p=payload('test',1,ds);check_payload(p);p['n_predict']=1024
 with pytest.raises(ValueError):check_payload(p)
