"""Bounded two-request inference adaptation; no objective access."""
from decoder_v49_common import parse_native
from reasoning_v95b_common import applied_settings

END_CONTROL = '\n</think>\n\n'

def payload(prompt, seed, mode, phase):
    if mode not in ['thinking','nonthinking'] or phase not in ['thought','final']:
        raise ValueError('Unknown inference mode/phase')
    if mode=='nonthinking' and phase!='final':raise ValueError('No nonthinking thought phase')
    p=dict(prompt=prompt,seed=seed,n_predict=128 if phase=='thought' else 128,
        temperature=.6 if mode=='thinking' else .7,top_p=.95 if mode=='thinking' else .8,
        top_k=20,min_p=0.,presence_penalty=1.5,repeat_penalty=1.,stream=False,
        cache_prompt=False,return_tokens=True)
    if phase=='thought':p['stop']=['</think>']
    return p

def check_payload(p):
    mode='thinking' if (p.get('temperature'),p.get('top_p'))==(.6,.95) else 'nonthinking'
    phase='thought' if 'stop' in p else 'final'
    if type(p.get('seed')) is not int or not isinstance(p.get('prompt'),str):
        raise ValueError('Explicit prompt/seed required')
    if p != payload(p['prompt'],p['seed'],mode,phase):
        raise ValueError('Unfrozen inference settings')

def valid_thought(r):
    content=r.get('content');n=r.get('tokens_predicted')
    if not isinstance(content,str) or type(n) is not int or not 0<n<=128 or r.get('truncated') is not False:
        return False
    if '</think>' in content:return False
    return r.get('stop_type')=='limit' or (r.get('stop_type')=='word' and r.get('stopping_word')=='</think>')

def final_prompt(prompt, thought):
    if not valid_thought(thought):raise ValueError('Invalid thought response')
    # Control delimiter is scaffolding, never represented as model output.
    return prompt+thought['content']+END_CONTROL

def parse_final(r):
    raw=r.get('content');count=r.get('tokens_predicted')
    if not isinstance(raw,str) or type(count) is not int or not 0<count<=128:
        return {'valid':False,'selected_ids':[],'reasons':['invalid_response_metadata']}
    return parse_native(raw,truncated=r.get('truncated') is not False or r.get('stop_type')!='eos')

def audit_case(job, preflight, starts, responses, choice):
    """Reconstruct prompt lineage from actual first-phase output, not saved claims."""
    key=job['key'];base=preflight['rendered']['prompt'];mode=job['mode']
    expected=base;thought_id=key+'_thought';final_id=key+'_final'
    if mode=='thinking' and thought_id in responses:
        r=responses[thought_id]['response'];p=starts[thought_id]['payload']
        assert p==payload(base,job['seed'],mode,'thought')
        applied_settings(r,p)
        if valid_thought(r):expected=final_prompt(base,r)
        else:assert final_id not in starts
    if final_id in starts:
        if mode=='thinking':assert thought_id in responses and valid_thought(responses[thought_id]['response'])
        assert starts[final_id]['payload']==payload(expected,job['seed'],mode,'final')
    if final_id in responses:
        r=responses[final_id]['response'];applied_settings(r,starts[final_id]['payload'])
        parsed=parse_final(r)
        assert choice['parsed']==parsed
        assert (choice['status']=='completed')==parsed['valid']
        assert choice['selected_ids']==parsed['selected_ids']
        return parsed
    assert choice['status']!='completed' and not choice['selected_ids']
    return None
