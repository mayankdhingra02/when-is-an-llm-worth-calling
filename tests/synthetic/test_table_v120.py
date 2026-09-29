"""Synthetic protocol fixtures, not measured model responses."""
import copy,sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from table_adapter_v120 import audit_case
from collect_smollm_v47 import grammar

def fixture():
    starts={};responses={};used=[];pre={'rendered':{'prompt':'synthetic prompt'}}
    for step,c in enumerate('0123456789'):
        k=f'synthetic_{step}';p={'prompt':pre['rendered']['prompt']+''.join(v+'\n' for v in used),'n_predict':1,'temperature':0,'seed':11,'grammar':grammar(used),'cache_prompt':bool(step),'return_tokens':True,'stream':False,'repeat_penalty':1.0}
        starts[k]={'payload':p};responses[k]={'payload':copy.deepcopy(p),'case':'synthetic','step':step,'response':{'content':c,'tokens_predicted':1,'truncated':False}};used.append(c)
    return {'key':'synthetic'},pre,starts,responses,{'selected_ids':used,'status':'completed'}

def test_exact_replay():assert audit_case(*fixture())['valid']
@pytest.mark.parametrize('field,value',[('grammar','root ::= "0"'),('temperature',.7),('prompt','leaked_or_altered')])
def test_changed_request_rejected(field,value):
    args=fixture();args[2]['synthetic_5']['payload'][field]=value
    with pytest.raises(AssertionError):audit_case(*args)

def test_repeated_response_cannot_be_completed():
    args=fixture();args[3]['synthetic_5']['response']['content']='0'
    with pytest.raises(AssertionError):audit_case(*args)
