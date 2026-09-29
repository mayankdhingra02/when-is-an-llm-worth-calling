"""Feature-only prompt interventions; no target oracle or optimization outcomes."""
import copy,json,time
from .resources import LimitReached
IDS=list('0123456789ABCDEFGHIJ')
CONDITIONS=('original','reverse_display','reverse_ids')

def transform(messages,pool,condition):
    if condition not in CONDITIONS:raise ValueError('Unknown intervention')
    result=copy.deepcopy(messages);intro,raw=result[-1]['content'].split('\n',1);body=json.loads(raw)
    candidates=body['candidates']
    if [r['id'] for r in candidates]!=IDS or set(pool['mapping'])!=set(IDS):raise ValueError('Original canonical candidate IDs required')
    mapping=dict(pool['mapping'])
    if condition=='reverse_display':body['candidates']=list(reversed(candidates))
    if condition=='reverse_ids':
        for row,new_id in zip(candidates,reversed(IDS)):row['id']=new_id
        mapping={new_id:pool['mapping'][old_id] for old_id,new_id in zip(IDS,reversed(IDS))}
    # Preserve original bytes for the fresh baseline, including serialization.
    if condition!='original':result[-1]['content']=intro+'\n'+json.dumps(body,separators=(',',':'))
    return {'messages':result,'mapping':mapping,'display_ids':[r['id'] for r in body['candidates']]}

def inspect_response(raw,job):
    ids=raw.strip().splitlines()
    if len(ids)!=10 or len(set(ids))!=10 or any(i not in job['mapping'] for i in ids):raise ValueError('Ten distinct valid IDs required')
    return {'selected_ids':ids,'selected_rows':[job['mapping'][i] for i in ids],
        'low_ids_set':set(ids)==set(IDS[:10]),'first_display_half_set':set(ids)==set(job['display_ids'][:10])}

def authorization_config(base,authorization):
    if authorization.get('granted') is not True:raise PermissionError('Nine additional requests require explicit authorization:128 to137')
    if authorization.get('request_cap')!=137 or authorization.get('additional_requests')!=9 or not authorization.get('user_authorization'):
        raise ValueError('Exact bounded authorization required')
    if authorization.get('runtime_cap_seconds')!=1800 or authorization.get('external_spend_usd')!=0:raise ValueError('Runtime/spend increase prohibited in this probe')
    c=copy.deepcopy(base);c['inference']['max_new_model_requests']=137
    c['inference']['max_output_tokens_per_request']=20;c['inference']['request_timeout_seconds']=8
    if c['resources']['max_experiment_runtime_minutes']!=30:raise ValueError('Existing runtime limit required')
    return c

class StageResources:
    """Restrict existing provider polling/request reservation to a stage deadline."""
    def __init__(self,base,seconds=40):self.base=base;self.deadline=time.monotonic()+seconds
    @property
    def d(self):return self.base.d
    def checkpoint(self):return self.base.checkpoint()
    def remaining(self):return min(self.base.remaining()-2,self.deadline-time.monotonic())
    def check(self):
        if self.remaining()<=0:raise LimitReached('Order-probe stage/global deadline')
    def request(self):self.check();return self.base.request()
