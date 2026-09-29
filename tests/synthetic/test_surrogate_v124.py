"""Synthetic source-contract/EI/guard checks, never research observations."""
import sys,math,copy,json
from pathlib import Path
import pytest
from scipy.stats import norm
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from surrogate_v124 import messages,payload,check_payload,parse,predictions,choose,expected_improvement,IDS
from runtime_surrogate_v124 import Runtime

def prefix():
 body={'feature_order':['switch'],'symbol_to_value':[[0,1]],'observations':[{'x':str(i%2),'loss':i/9} for i in range(10)],'candidates':[{'id':k,'x':str(i%2)} for i,k in enumerate(IDS)]}
 return {'messages':[{}, {'content':'preamble\n'+json.dumps(body)}],'state':{'labels':[[i+20.] for i in range(10)]},'pool':{'mapping':{k:i+10 for i,k in enumerate(IDS)}}}

def test_acquired_only_raw_metric_and_fixed_permutation():
 p=prefix();a=messages(p,'A','runtime');p['unobserved_labels']=object();assert messages(p,'A','runtime')==a
 b=json.loads(a[1]['content']);assert b['new_configuration']==[0] and len(b['observed_examples'])==10 and 'candidates' not in b
 assert sorted(float(o['performance']) for o in b['observed_examples'])==list(range(20,30))
 assert [float(o['performance']) for o in b['observed_examples']]==[22,28,24,29,21,26,27,23,20,25]

@pytest.mark.parametrize('mean,std,best',[(5.,2.,4.),(1.,0.,2.),(9.,.1,2.),(0.,3.,0.),(30.,7.,40.)])
def test_ei_against_published_scipy_formula(mean,std,best):
 sd=max(std,1e-5);delta=best-mean;z=delta/sd;ref=delta*norm.cdf(z)+sd*norm.pdf(z)
 assert expected_improvement(mean,std,best)==pytest.approx(ref,abs=1e-14)

def response(s):return {'content':s,'tokens_predicted':12,'truncated':False,'stop_type':'eos'}
@pytest.mark.parametrize('s,value',[('## 0.366 ##',.366),('## -12.5 ##',-12.5),(' \n## 7123. ##\n',7123.),('## .5 ##',.5),('## 0 ##',0.)])
def test_numeric_contract(s,value):assert parse(response(s))==value
@pytest.mark.parametrize('s',['0.36','## 1e3 ##','## nan ##','reason: ## 1.2 ##','## 1 ## ## 2 ##','<think>done</think> ## 2 ##'])
def test_invalid_outputs(s):
 with pytest.raises(ValueError):parse(response(s))
@pytest.mark.parametrize('k,v',[('tokens_predicted',33),('tokens_predicted',None),('tokens_predicted',True),('truncated',True),('stop_type','limit')])
def test_incomplete(k,v):
 r=response('## 1 ##');r[k]=v
 with pytest.raises(ValueError):parse(r)

def test_partial_samples_are_not_imputed_and_missing_candidate_fails():
 p=prefix();scores={i:[20.,22.,24.] for i in IDS};scores['A']=[20.,24.];stats=predictions(scores,p)
 assert stats['A']['population_std']==2. and len(stats['A']['values'])==2
 assert choose(stats,p,'mean')[0]==list(IDS[:10])
 scores['A']=[20.]
 with pytest.raises(ValueError):predictions(scores,p)

def test_uncertainty_can_change_ei_without_changing_mean():
 p=prefix();scores={i:[21.,21.,21.] for i in IDS};scores['J']=[17.,21.,25.];s=predictions(scores,p)
 assert choose(s,p,'mean')[0]==list(IDS[:10]);assert choose(s,p,'ei')[0][0]=='J'

def test_payload_and_charged_failure(tmp_path):
 p=payload('example',101);check_payload(p);p['grammar']='root ::= "0"'
 with pytest.raises(ValueError):check_payload(p)
 with pytest.raises(ValueError):check_payload(payload('example',999))
 cfg={'new_generation_request_cap':1,'scientific_request_cap':1,'max_generation_stage_seconds':1500,'max_allocated_output_tokens':32};r=Runtime(tmp_path,cfg)
 def fail(*_):raise TimeoutError('synthetic')
 r._send=fail
 with pytest.raises(TimeoutError):r.generate(payload('example',101),'scientific','case')
 assert r.ledger['generation_requests']==1 and r.ledger['allocated_output_tokens']==32
 with pytest.raises(PermissionError):r.generate(payload('example',102),'scientific','retry')
