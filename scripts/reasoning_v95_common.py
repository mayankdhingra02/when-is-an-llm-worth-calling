"""Fixed sampling and strict native final-answer parser for V95."""
import math
from decoder_v49_common import parse_native

def check_payload(p):
    expected=({2048:(.6,.95),128:(.7,.8)}).get(p.get('n_predict'))
    if expected is None:raise ValueError('Unfrozen generation allocation')
    if (p.get('temperature'),p.get('top_p'))!=expected:raise ValueError('Changed owner-informed sampling')
    for k,v in {'top_k':20,'min_p':0.,'presence_penalty':1.5,'repeat_penalty':1.,'stream':False,'cache_prompt':False,'return_tokens':True}.items():
        if p.get(k)!=v:raise ValueError('Changed setting '+k)
    if 'grammar' in p or type(p.get('seed')) is not int:raise ValueError('Native decoding and explicit seed required')

def parse(response,mode):
    if mode not in ['thinking','nonthinking']:raise ValueError('Unknown mode')
    raw=response.get('content');count=response.get('tokens_predicted')
    if not isinstance(raw,str) or type(count) is not int or not 0<count<=(2048 if mode=='thinking' else 128):
        return {'valid':False,'selected_ids':[],'reasons':['missing_or_invalid_response_metadata']}
    if mode=='thinking':
        if raw.count('</think>')!=1:return {'valid':False,'selected_ids':[],'reasons':['no_unique_thinking_end']}
        _,final=raw.split('</think>',1)
    else:final=raw
    result=parse_native(final,truncated=response.get('truncated') is not False or response.get('stopped_limit') is not False)
    result['final_text']=final
    return result

def applied_settings(response,payload):
    settings=response.get('generation_settings',{})
    for key in ['temperature','top_p','top_k','min_p','presence_penalty','repeat_penalty']:
        if key not in settings or not math.isclose(settings[key],payload[key],abs_tol=1e-6):
            raise ValueError('Runtime did not apply '+key)
    if settings.get('seed')!=payload['seed'] or settings.get('n_predict')!=payload['n_predict']:
        raise ValueError('Seed/output allocation mismatch')
