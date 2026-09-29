import copy,json
import pytest
from escalation.size_prompt_v38 import transform,authorization_config
from escalation.config import load_config
from escalation.io import read
from escalation.larger_v22 import MODEL_ID,REVISION

def fixture():
    body={'observations':[{'x':str(i),'loss':i/10} for i in range(10)],'candidates':[{'id':i,'x':i} for i in '0123456789ABCDEFGHIJ']}
    return {'messages':[{'role':'system','content':'old'},{'role':'user','content':'intro\n'+json.dumps(body)}]}, {'ids':list(range(10)),'labels':[['1',str(i+1)] for i in range(10)],'anchor_row':0,'size_cap':'1'}

def test_treatment_preserves_candidate_order_ids_and_runtime_observations():
    j,p=fixture();before=copy.deepcopy((j,p));new=json.loads(transform(j,p)[1]['content'].split('\n',1)[1]);old=json.loads(j['messages'][1]['content'].split('\n',1)[1])
    assert (j,p)==before and new['candidates']==old['candidates']
    assert [{k:v for k,v in row.items() if k!='output_size'} for row in new['observations']]==old['observations']
    assert [r['output_size'] for r in new['observations']]==[y[1] for y in p['labels']]
    assert new['constraint']['max_output_size']=='1'

def test_hidden_values_are_not_prompt_inputs():
    j,p=fixture();original=transform(j,p);j['hidden_outcomes']=['DO_NOT_LEAK']*100
    assert transform(j,p)==original and 'DO_NOT_LEAK' not in str(original)

@pytest.mark.parametrize('approval',[None,{}, {'granted':False},{'granted':True}])
def test_permission_gate_closed_without_exact_new_approval(approval):
    with pytest.raises(PermissionError):authorization_config(load_config('configs/followup_v3.yaml'),read('configs/authorization_v22.json'),approval,'freeze')

def test_new_approval_preserves_other_limits_and_paid_guard():
    a={'granted':True,'request_cap':230,'additional_requests':30,'runtime_cap_seconds':3600,'stage_seconds':600,'max_new_vectors':300,
       'external_spend_usd':0,'new_downloads':0,'model_id':MODEL_ID,'revision':REVISION,'protocol_freeze_sha256':'freeze','user_authorization':'synthetic test only'}
    base=load_config('configs/followup_v3.yaml');cfg=authorization_config(base,read('configs/authorization_v22.json'),a,'freeze')
    assert cfg['inference']['max_new_model_requests']==230 and cfg['resources']['max_experiment_runtime_minutes']==60 and cfg['inference']['max_retries_per_request']==0
    with pytest.raises(PermissionError):authorization_config(base,read('configs/authorization_v22.json'),a,'changed')
    base['inference']['allow_paid_api']=True
    with pytest.raises((PermissionError,ValueError)):authorization_config(base,read('configs/authorization_v22.json'),a,'freeze')
