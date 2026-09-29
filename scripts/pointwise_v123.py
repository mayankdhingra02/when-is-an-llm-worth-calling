"""Pure pointwise numeric adapter; no network, oracle or hidden-label reads."""
import json,re,copy
IDS='0123456789ABCDEFGHIJ'
ALPHABET='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
GRAMMAR='root ::= '+' | '.join(json.dumps(f'{i/100:.2f}') for i in range(101))
SYSTEM='You predict software configuration performance from observed examples. Estimate the normalized loss of the one new configuration. Smaller loss is better. Infer effects of the named settings from the examples. Return only a number from 0.00 to 1.00 with exactly two decimal places, no explanation. Use 0.00 for predictions better than the observed best and 1.00 for predictions worse than the observed worst.'
def messages(prefix,candidate,condition,meaning):
    if candidate not in IDS or condition not in ['normal','loss_blind','observations_reversed']:raise ValueError('Unknown candidate/condition')
    body=json.loads(prefix['messages'][1]['content'].split('\n',1)[1]);names=body['feature_order'];domains=body['symbol_to_value']
    def decode(s):
        if len(s)!=len(names):raise ValueError('Feature width')
        return [domain[ALPHABET.index(ch)] for domain,ch in zip(domains,s)]
    observations=[{'settings':decode(o['x']),'normalized_loss':o['loss'] if condition!='loss_blind' else .5} for o in body['observations']]
    assert len(observations)==10
    if condition=='observations_reversed':observations.reverse()
    selected=next(c for c in body['candidates'] if c['id']==candidate)
    data={'task_metric':meaning,'normalization':'0=best acquired, 1=worst acquired; only these ten observed outcomes define this scale','feature_order':names,'observations':observations,'new_configuration':decode(selected['x'])}
    return [{'role':'system','content':SYSTEM},{'role':'user','content':json.dumps(data,separators=(',',':'))}]
def payload(prompt):return {'prompt':prompt,'n_predict':16,'temperature':0,'seed':11,'grammar':GRAMMAR,'cache_prompt':False,'return_tokens':True,'stream':False,'repeat_penalty':1.0}
def check_payload(p):
    if not isinstance(p.get('prompt'),str) or p!=payload(p['prompt']):raise ValueError('Unfrozen pointwise settings')
def parse(response):
    raw=response.get('content');n=response.get('tokens_predicted')
    if not isinstance(raw,str) or re.fullmatch(r'(?:0\.\d{2}|1\.00)',raw) is None:raise ValueError('Invalid two-decimal loss')
    if type(n) is not int or not 0<n<=16 or response.get('truncated') is not False or response.get('stop_type')!='eos':raise ValueError('Incomplete score response')
    return float(raw)
def choose(scores,prefix):
    if set(scores)!=set(IDS) or any(type(v) not in [float,int] or not 0<=v<=1 for v in scores.values()):raise ValueError('Twenty valid scores required')
    # Fixed stable ID-order tie break is itself a cheap control, not model reasoning.
    selected=sorted(IDS,key=lambda i:(scores[i],IDS.index(i)))[:10]
    return selected,[prefix['pool']['mapping'][i] for i in selected]
