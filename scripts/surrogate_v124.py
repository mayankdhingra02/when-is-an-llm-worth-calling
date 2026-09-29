"""Acquired-only local adaptation of LLAMBO's numeric surrogate and EI.

Owner algorithm reference: Tennison Liu et al., MIT, revision196fe237.
Independent implementation; provider module is never imported.
"""
import json,re,math,statistics
IDS='0123456789ABCDEFGHIJ';ALPHABET='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';SEEDS=(101,102,103)
def messages(prefix,candidate,meaning):
    if candidate not in IDS:raise ValueError('Candidate')
    body=json.loads(prefix['messages'][1]['content'].split('\n',1)[1]);names=body['feature_order'];domains=body['symbol_to_value']
    def decode(s):return [domain[ALPHABET.index(ch)] for domain,ch in zip(domains,s)]
    # Fixed template seed0 permutation, matching the owner template's default.
    # Local RNG avoids mutating shared optimizer state.
    import numpy as np
    order=np.random.RandomState(0).permutation(10)
    if len(prefix['state']['labels'])!=10:raise ValueError('Prefix10 required')
    examples=[{'settings':decode(body['observations'][int(i)]['x']),'performance':f"{prefix['state']['labels'][int(i)][0]:.6f}"} for i in order]
    candidate_x=decode(next(x['x'] for x in body['candidates'] if x['id']==candidate))
    user={'task':f'Predict software configuration performance measured as {meaning}. Smaller performance values are better.','feature_order':names,'observed_examples':examples,'new_configuration':candidate_x,'response_format':'Return only the predicted performance in the format ## performance ##. Use the same units as the examples.'}
    return [{'role':'system','content':'You are an AI assistant that helps people find information.'},{'role':'user','content':json.dumps(user,separators=(',',':'))}]
def payload(prompt,seed):
    return {'prompt':prompt,'n_predict':32,'temperature':.7,'top_p':.95,'top_k':0,'min_p':0.,'seed':seed,'cache_prompt':False,'return_tokens':True,'stream':False,'repeat_penalty':1.0}
def check_payload(p):
    if not isinstance(p.get('prompt'),str) or type(p.get('seed')) is not int or p['seed'] not in SEEDS or p!=payload(p['prompt'],p['seed']):raise ValueError('Unfrozen request')
def parse(r):
    raw=r.get('content');n=r.get('tokens_predicted')
    if not isinstance(raw,str):raise ValueError('No text')
    m=re.fullmatch(r'\s*## (-?(?:\d+(?:\.\d*)?|\.\d+)) ##\s*',raw)
    if m is None or type(n) is not int or not 0<n<=32 or r.get('truncated') is not False or r.get('stop_type')!='eos':raise ValueError('Invalid/incomplete numeric response')
    v=float(m[1])
    if not math.isfinite(v):raise ValueError('Nonfinite')
    return v

def expected_improvement(mean,std,best):
    if not all(math.isfinite(v) for v in [mean,std,best]) or std<0:raise ValueError('Invalid EI input')
    # Same population standard deviation floor as owner implementation.
    std=max(std,1e-5);delta=best-mean;z=delta/std
    return max(0.,delta*.5*(1+math.erf(z/math.sqrt(2)))+std*math.exp(-.5*z*z)/math.sqrt(2*math.pi))
def predictions(scores,prefix):
    if set(scores)!=set(IDS) or any(len(v) not in [2,3] or any(type(x) not in [int,float] or not math.isfinite(x) for x in v) for v in scores.values()):raise ValueError('At least2valid samples for every candidate required')
    best=min(y[0] for y in prefix['state']['labels']);stats={}
    for i,values in scores.items():
        mean=statistics.mean(values);std=statistics.pstdev(values);stats[i]={'values':values,'mean':mean,'population_std':std,'ei':expected_improvement(mean,std,best)}
    return stats

def choose(stats,prefix,mode):
    if mode not in ['ei','mean'] or set(stats)!=set(IDS):raise ValueError('Choice contract')
    ids=sorted(IDS,key=lambda i:((-stats[i]['ei'] if mode=='ei' else stats[i]['mean']),IDS.index(i)))[:10]
    return ids,[prefix['pool']['mapping'][i] for i in ids]
