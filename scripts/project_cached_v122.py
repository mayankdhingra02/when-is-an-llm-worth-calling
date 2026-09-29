"""Feature-only projection of preserved real V119 responses, no objective reads."""
import json
from table_check_v119 import ROOT,read,write,sha,now,candidates
from escalation.finite_v6 import ALPHABET
VERSION='v122_exact_strings_nominal_remaining_shortlist'

def project(raw,c,p):
    strings=raw.splitlines()
    if len(strings)!=10 or len(set(strings))!=10:raise ValueError('Ten distinct configurations required')
    decoded=[]
    for s in strings:
        if len(s)!=len(c.names):raise ValueError('Wrong feature count')
        vals=[]
        for letter,domain in zip(s,c.domains):
            if letter not in ALPHABET or ALPHABET.index(letter)>=len(domain):raise ValueError('Illegal feature index')
            vals.append(domain[ALPHABET.index(letter)])
        decoded.append(vals)
    pool=set(p['pool']['ranked']);available=[i for i in p['state']['order'] if i in pool and i not in p['state']['ids']];chosen=[];trace=[]
    assert len(available)==20
    for raw,x in zip(strings,decoded):
        distance=lambda i:sum(a!=b for a,b in zip(x,c.x[i]))
        original=min(available,key=distance);remaining=[i for i in available if i not in chosen];row=min(remaining,key=distance)
        trace.append({'raw':raw,'decoded':x,'row':row,'distance':distance(row),'projected':distance(row)>0,'closest_already_used':original in chosen});chosen.append(row)
    return chosen,trace

def frozen():
    for n,h in read(ROOT/'reports/protocol_v122.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n

def main():
    frozen();out=ROOT/'results/v122_projection';out.mkdir(exist_ok=False);_,c,_=candidates();responses=[json.loads(x) for x in (ROOT/'results/v119_reasoning/responses.jsonl').read_text().splitlines()];rm={r['case']:r for r in responses};starts=[json.loads(x) for x in (ROOT/'results/v119_reasoning/generation_starts.jsonl').read_text().splitlines()];sm={r['identity']:r for r in starts};choices=[]
    for job in read(ROOT/'artifacts/study_v119/jobs.json'):
        key=job['key'];p=read(ROOT/job['prefix']);response=rm[key];start=sm[key+'_final'];pre=read(ROOT/f'results/v119_reasoning/preflight/{key}.json');assert pre['messages']==p['messages'] and pre['prefix_sha256']==sha(ROOT/job['prefix']) and response['key']==key+'_final' and start['payload']['seed']==1009
        try:selected,trace=project(response['response']['content'],c,p);status='projected';error=None
        except ValueError as e:
            from escalation.core import State
            from escalation.transfer_v41 import rank
            selected=rank(c,State(**p['state']),p['pool']['ranked'])[:10];trace=[];status='fallback';error=str(e)
        identity={'parser':VERSION,'prefix_sha256':sha(ROOT/job['prefix']),'response':response,'request':start}
        cache=__import__('hashlib').sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
        row={'key':key,'seed':job['optimization_seed'],'prefix':job['prefix'],'selected_rows':selected,'trace':trace,'status':status,'error':error,'cache_key':cache,'parser':VERSION};write(out/'choices'/f'{key}.json',row);choices.append(row)
    write(out/'selection_seal.json',{'at':now(),'choices':choices,'sha256':{str(p.relative_to(ROOT)):sha(p) for p in (out/'choices').glob('*.json')},'new_model_requests':0,'new_acquisitions':0})
    print('Frozen feature-only choices for',len(choices),'real cached responses')
if __name__=='__main__':main()
