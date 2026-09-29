"""Synthetic accounting records only; no model outputs in research directories."""
import copy,hashlib
import pytest
from escalation.kanzi_receipt_audit_v78 import request_receipt,completed_accounting,trial_limits,selection_costs

def example():
    cases=[{'seed':seed,'fallback_steps':list(range(1,8))} for seed in [11,23,37,53,71]]
    decisions={f'v78_seed{c["seed"]}_step1':{'valid':False} for c in cases}
    starts=[{'request_id':key} for key in decisions]
    ledger={'generation_requests':5,'intended_generation_requests':35,'unattempted_generation_requests':30,'fallback_search_evaluations':35,'retries':0,'external_spend_usd':0,'stop_reason':None,'resource_guard':{'reason':None,'peak_server_rss_bytes':100},'seconds':1,'startup_seconds':0.1,'server_exit_code':0}
    return cases,decisions,starts,ledger

def test_malformed_cases_keep_full_denominator():
    assert completed_accounting(*example())=={'requests':5,'fallback_search_slots':35,'invalid_responses':5}

@pytest.mark.parametrize('change',['fallback_ledger','fallback_case','unattempted','duplicate_start','extra_request','missing_request','time_limit','memory_limit'])
def test_corrupt_accounting_rejected(change):
    cases,decisions,starts,ledger=example()
    if change=='fallback_ledger':ledger['fallback_search_evaluations']=0
    elif change=='fallback_case':cases[0]['fallback_steps']=[]
    elif change=='unattempted':ledger['unattempted_generation_requests']=0
    elif change=='duplicate_start':starts.append(starts[0])
    elif change=='extra_request':decisions['v78_seed11_step2']={'valid':True}
    elif change=='missing_request':decisions.pop('v78_seed11_step1')
    elif change=='time_limit':ledger['seconds']=1801
    elif change=='memory_limit':ledger['resource_guard']['peak_server_rss_bytes']=9*1024**3
    with pytest.raises((AssertionError,KeyError)):completed_accounting(cases,decisions,starts,ledger)

def receipt():
    payload={'prompt':'SYNTHETIC','n_predict':64,'temperature':0,'seed':11,'cache_prompt':False,'return_tokens':True,'stream':False,'repeat_penalty':1.0}
    request={'payload':payload,'prompt_sha256':hashlib.sha256(b'SYNTHETIC').hexdigest()}
    rendered={'rendered':{'prompt':'SYNTHETIC'},'tokens':[1,2]};response={'tokens_predicted':None,'tokens_evaluated':None}
    decision={'usage':dict(response),'wall_seconds':0.1}
    return request,rendered,response,decision

def test_missing_usage_remains_unknown():
    assert request_receipt(*receipt(),11)=={'tokens_predicted':None,'tokens_evaluated':None}

@pytest.mark.parametrize('change',['prompt','usage_zero','seed','token_limit','negative_usage'])
def test_provenance_or_usage_mismatch_rejected(change):
    request,rendered,response,decision=receipt()
    if change=='prompt':request['payload']['prompt']='ALTERED'
    elif change=='usage_zero':decision['usage']['tokens_predicted']=0
    elif change=='seed':request['payload']['seed']=23
    elif change=='token_limit':response['tokens_predicted']=decision['usage']['tokens_predicted']=65
    elif change=='negative_usage':response['tokens_predicted']=decision['usage']['tokens_predicted']=-1
    with pytest.raises(AssertionError):request_receipt(request,rendered,response,decision,11)

@pytest.mark.parametrize('key,value',[('wall_seconds',41),('rss_bytes',3*1024**3),('scratch_bytes',129*1024**2)])
def test_success_status_cannot_hide_limit_violation(key,value):
    phase={'exit_code':0,'termination_reason':None,'wall_seconds':1,'sampled_maxima':{'rss_bytes':100,'scratch_bytes':100}}
    result={'compression':copy.deepcopy(phase),'decompression':copy.deepcopy(phase)}
    supervision={'exit_code':0,'termination_reason':None,'wall_seconds':2}
    if key=='wall_seconds':result['compression'][key]=value
    else:result['compression']['sampled_maxima'][key]=value
    with pytest.raises(AssertionError):trial_limits(result,supervision)

def test_selection_costs_detect_duplicate_event():
    cases=[{'seed':s,'arms':{m:[{'config_id':i} for i in range(17)] for m in ['rf_lcb','nn','llm']}} for s in [11,23,37,53,71]]
    rows=[{'seed':c['seed'],'arm':m,'step':j,'config_id':j+9,'seconds':1} for c in cases for m in c['arms'] for j in range(1,8)]
    assert selection_costs(cases,rows)=={'rf_lcb':35.0,'nn':35.0,'llm':35.0}
    rows[-1]=rows[0]
    with pytest.raises(AssertionError):selection_costs(cases,rows)
