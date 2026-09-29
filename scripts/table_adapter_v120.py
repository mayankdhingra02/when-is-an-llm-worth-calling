"""Frozen provenance validation for the existing V91 constrained adapter."""
from table_check_v119 import ROOT,read,sha
from collect_smollm_v47 import grammar
from escalation.qwen_v91 import validate_response

def freeze120():
    for n,h in read(ROOT/'reports/protocol_v120.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n

def audit_case(job,pre,starts,responses,choice):
    used=[];failure=None;identities=[]
    for step in range(10):
        key=f"{job['key']}_{step}"
        if key not in starts:break
        identities.append(key);payload=starts[key]['payload']
        expected={'prompt':pre['rendered']['prompt']+''.join(c+'\n' for c in used),'n_predict':1,'temperature':0,'seed':11,'grammar':grammar(used),'cache_prompt':bool(step),'return_tokens':True,'stream':False,'repeat_penalty':1.0}
        assert payload==expected
        if key not in responses:break
        response=responses[key];assert response['payload']==payload and response['case']==job['key'] and response['step']==step
        try:used.append(validate_response(response['response'],used))
        except ValueError as e:failure=str(e);break
    assert choice['selected_ids']==used
    assert (choice['status']=='completed')==(len(used)==10)
    return {'valid':len(used)==10,'selected_ids':used,'reasons':[] if len(used)==10 else [failure or 'missing_or_failed_response']}
