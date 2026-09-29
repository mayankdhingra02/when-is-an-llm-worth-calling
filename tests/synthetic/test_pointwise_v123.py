"""Synthetic adapter/control tests. Never aggregate these as research results."""
import json,sys,copy
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from pointwise_v123 import messages,payload,check_payload,parse,choose,IDS
from runtime_pointwise_v123 import Runtime

def prefix():
    body={'feature_order':['switch'],'symbol_to_value':[[0,1]],'observations':[{'x':str(i%2),'loss':i/9} for i in range(10)],'candidates':[{'id':k,'x':str(i%2)} for i,k in enumerate(IDS)]}
    return {'messages':[{}, {'content':'preamble\n'+json.dumps(body)}],'pool':{'mapping':{k:i+10 for i,k in enumerate(IDS)}},'state':{'hidden_poison':'must not read'}}

def test_prompts_only_use_declared_observations_and_feature_values():
    p=prefix();a=messages(p,'A','normal','runtime');p['state']=object();p['unacquired_targets']=object();assert messages(p,'A','normal','runtime')==a
    body=json.loads(a[1]['content']);assert body['new_configuration']==[0] and 'candidates' not in body and 'id' not in body
    blind=json.loads(messages(p,'A','loss_blind','runtime')[1]['content']);reverse=json.loads(messages(p,'A','observations_reversed','runtime')[1]['content'])
    assert blind['observations']==[dict(o,normalized_loss=.5) for o in body['observations']]
    assert reverse['observations']==body['observations'][::-1]
    for b in [blind,reverse]:assert {k:v for k,v in b.items() if k!='observations'}=={k:v for k,v in body.items() if k!='observations'}

def response(s='0.15',**kw):return dict(content=s,tokens_predicted=4,truncated=False,stop_type='eos',**kw)
@pytest.mark.parametrize('s',['0.00','0.17','1.00'])
def test_numeric_response(s):assert parse(response(s))==float(s)
@pytest.mark.parametrize('s',[' 0.15','0.15\n','1.01','-0.01','0.1','nan','0.50 0.40','<think>0.15','1','0'])
def test_reject_invalid_outputs(s):
    with pytest.raises(ValueError):parse(response(s))
@pytest.mark.parametrize('field,value',[('tokens_predicted',None),('tokens_predicted',0),('tokens_predicted',17),('tokens_predicted',True),('truncated',True),('stop_type','limit')])
def test_reject_incomplete_response(field,value):
    r=response();r[field]=value
    with pytest.raises(ValueError):parse(r)

def test_fixed_tie_break_and_complete_scores():
    scores={k:.5 for k in IDS};assert choose(scores,prefix())==(list(IDS[:10]),list(range(10,20)))
    scores['J']=0;assert choose(scores,prefix())[0][0]=='J'
    del scores['A']
    with pytest.raises(ValueError):choose(scores,prefix())
@pytest.mark.parametrize('value',[float('nan'),float('inf'),-1,1.1,True])
def test_reject_invalid_score(value):
    s={k:.5 for k in IDS};s['A']=value
    with pytest.raises(ValueError):choose(s,prefix())

def test_request_contract_and_cap_before_network(tmp_path):
    p=payload('example');check_payload(p);p['temperature']=.5
    with pytest.raises(ValueError):check_payload(p)
    cfg={'new_generation_request_cap':0,'scientific_request_cap':0,'max_generation_stage_seconds':900,'max_allocated_output_tokens':16}
    r=Runtime(tmp_path,cfg);r._send=lambda *_:pytest.fail('network must not run')
    with pytest.raises(PermissionError):r.generate(payload('example'),'scientific','case')
    assert r.ledger['generation_requests']==0
    cfg['new_generation_request_cap']=cfg['scientific_request_cap']=1;cfg['max_allocated_output_tokens']=15
    with pytest.raises(PermissionError):r.generate(payload('example'),'scientific','case')
    assert r.ledger['generation_requests']==0

def test_transport_failure_is_charged(tmp_path):
    cfg={'new_generation_request_cap':1,'scientific_request_cap':1,'max_generation_stage_seconds':900,'max_allocated_output_tokens':16};r=Runtime(tmp_path,cfg)
    def fail(*_):raise TimeoutError('synthetic')
    r._send=fail
    with pytest.raises(TimeoutError):r.generate(payload('example'),'scientific','case')
    assert r.ledger['generation_requests']==1 and r.ledger['allocated_output_tokens']==16
    with pytest.raises(PermissionError):r.generate(payload('example'),'scientific','retry')
