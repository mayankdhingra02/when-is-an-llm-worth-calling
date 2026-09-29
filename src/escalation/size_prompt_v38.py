"""Acquired-only size-aware prompt treatment and exact bounded authorization gate."""
import copy,json
from .io import digest
from .larger_v22 import MODEL_ID,REVISION,authorization_config as v22_config

def transform(job,prefix):
    messages=copy.deepcopy(job['messages']);_,raw=messages[-1]['content'].split('\n',1);body=json.loads(raw)
    if len(prefix['ids'])!=10 or len(prefix['labels'])!=10 or len(body['observations'])!=10:raise ValueError('Ten acquired observations required')
    if prefix['anchor_row'] not in prefix['ids'] or prefix['size_cap']!=prefix['labels'][prefix['ids'].index(prefix['anchor_row'])][1]:raise ValueError('Acquired anchor cap')
    for observation,label in zip(body['observations'],prefix['labels']):observation['output_size']=label[1]
    body['constraint']={'max_output_size':prefix['size_cap'],'inclusive':True,'units':'unchanged source output-size units'}
    messages[0]['content']='You optimize software configurations. Select ten distinct candidate IDs expected to achieve low runtime loss while satisfying output_size <= max_output_size. Infer runtime and size only from the acquired observations. Candidate outcomes are unknown. Output only ten supplied IDs, one per line, without explanations.'
    messages[-1]['content']='Observed runtime losses use the original acquired-only normalization. output_size and max_output_size use the same source units. Feature strings use the original symbol_to_value encoding. Select ten promising distinct IDs for fast configurations expected to satisfy the size cap.\n'+json.dumps(body,separators=(',',':'))
    return messages

def authorization_config(base,prior,approval,freeze_hash):
    if not approval or approval.get('granted') is not True:raise PermissionError('Requires explicit30additional local attempts; follow-up cap200->230')
    expected={'request_cap':230,'additional_requests':30,'runtime_cap_seconds':3600,'stage_seconds':600,'max_new_vectors':300,
        'external_spend_usd':0,'new_downloads':0,'model_id':MODEL_ID,'revision':REVISION,'protocol_freeze_sha256':freeze_hash}
    if any(approval.get(k)!=v for k,v in expected.items()) or not approval.get('user_authorization'):raise PermissionError('Exact frozen V38 authorization required')
    cfg=v22_config(base,prior)
    if cfg['inference']['allow_paid_api'] or cfg['inference']['max_external_spend_usd']!=0:raise PermissionError('Paid inference prohibited')
    cfg['inference']['max_new_model_requests']=230
    return cfg
