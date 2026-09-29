"""Independent stdlib/Fraction replay of every V41 contrast and policy mean."""
import csv,json
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def events(p):return [json.loads(s) for s in (ROOT/p).read_text().splitlines()]
def close(a,b):
    if abs(float(a)-float(b))>1e-12*max(1,abs(float(a)),abs(float(b))):raise ValueError('Numerical replay mismatch')

def main():
    summary=read('results/v41_model_analysis/summary.json');manifest=read('data/manifest_v41.json')
    specs={d['id']:d for d in manifest['datasets']};raw=defaultdict(dict)
    for e in events('results/v41_transfer/acquisitions.jsonl'):
        key=(e['dataset'],e['seed'],e['arm'])
        if e['row_id'] in raw[key]:raise ValueError('Duplicate source event')
        raw[key][e['row_id']]=F(e['raw_target'])
    for e in events('results/v41_models/acquisitions.jsonl'):
        key=(e['dataset'],e['seed'],'model'+e['model_size'])
        if e['row_id'] in raw[key]:raise ValueError('Duplicate model source event')
        raw[key][e['row_id']]=F(e['raw_target'])
    def target(dataset,seed,arm,record):
        prefix=raw[(dataset,seed,'prefix')];tail=raw[(dataset,seed,arm)]
        if set(prefix)&set(tail) or len(prefix)!=10 or len(tail)!=10:raise ValueError('Paired budget/source overlap')
        values={**prefix,**tail};state=record['state']
        if set(state['ids'])!=set(values) or len(state['ids'])!=20:raise ValueError('State/source mismatch')
        for i,y in zip(state['ids'],state['labels']):close(values[i],y[0])
        return (min if specs[dataset]['direction']=='-' else max)(values.values())
    def family_mean(values):
        groups=defaultdict(list)
        for dataset,value in values:groups[specs[dataset]['system_group']].append(value)
        return sum(sum(v)/len(v) for v in groups.values())/len(groups)
    gains={}
    with (ROOT/'results/v41_model_analysis/paired_cases.csv').open(newline='') as f:
        for row in csv.DictReader(f):
            d,seed,size,arm=row['dataset'],int(row['seed']),row['model_size'],row['reference'];key=f'{d}_{seed}'
            classical=read(f'results/v41_transfer/arms/{key}_{arm}.json');model=read(f'results/v41_models/{size}/arms/{key}.json')
            old=target(d,seed,arm,classical);new=target(d,seed,'model'+size,model)
            gain=(old-new)/old if specs[d]['direction']=='-' else (new-old)/old
            close(old,row['reference_best']);close(new,row['llm_best']);close(gain,row['relative_gain'])
            gains[(size,arm,d,seed)]=gain
    if len(gains)!=420:raise ValueError('Expected420 measured contrasts')
    for c in summary['contrasts']:
        values=[(d,v) for (size,arm,d,seed),v in gains.items() if (size,arm)==(c['model_size'],c['reference'])]
        close(family_mean(values),c['family_mean_gain'])
        if len(values)!=30:raise ValueError('Contrast denominator')
        if (sum(v>F('1e-12') for _,v in values),sum(abs(v)<=F('1e-12') for _,v in values),sum(v< -F('1e-12') for _,v in values))!=(c['wins'],c['ties'],c['harms']):raise ValueError('Win/tie/harm count')
    committed=read('results/v41_policy_precommit/decisions.json')
    for p in summary['policies']:
        penalty=F(str(p['hypothetical_relative_penalty_per_call']));quality=[];net=[];calls=0
        for i,case in enumerate(committed['rows']):
            d,seed=case['dataset'],case['seed'];g=gains[(p['model_size'],p['reference'],d,seed)]
            call=g>penalty if p['policy']=='hindsight_oracle_diagnostic' else committed['masks'][p['policy']][i]
            calls+=call;quality.append((d,g if call else F(0)));net.append((d,g-penalty if call else F(0)))
        if calls!=p['calls']:raise ValueError('Policy call count')
        close(family_mean(quality),p['quality']['family_mean_gain']);close(family_mean(net),p['net_utility']['family_mean_gain'])
    print(json.dumps({'verified_fraction_contrasts':len(gains),'verified_summaries':len(summary['contrasts']),
        'verified_policy_means':len(summary['policies']),'new_model_calls':0,'new_acquisitions':0,
        'scope':'Independent acquired-journal arithmetic replay; source authenticity checked separately'},indent=2))
if __name__=='__main__':main()
