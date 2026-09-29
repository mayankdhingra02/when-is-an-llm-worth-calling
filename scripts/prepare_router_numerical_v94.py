"""Fit on old groups and seal decisions before ANY new continuation outcome."""
import math,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from collect_smollm_v47 import read,write,sha,now
from escalation.core import State
from escalation.finite_v6 import features
from escalation.numerical_v94 import candidates

def fit(x,y):
    mean=x.mean(axis=0);scale=x.std(axis=0);scale[scale==0]=1.
    z=(x-mean)/scale;intercept=float(y.mean())
    coefficient=np.linalg.solve(z.T@z+np.eye(x.shape[1]),z.T@(y-intercept))
    return dict(mean=mean.tolist(),scale=scale.tolist(),coefficient=coefficient.tolist(),intercept=intercept)
def predict(x,m):return (x-np.array(m['mean']))/np.array(m['scale']) @ np.array(m['coefficient'])+m['intercept']
def choose(scores,y,groups,thresholds):
    choices=[]
    for threshold in thresholds:
        mask=scores>threshold
        utility=np.mean([np.mean(((y-.05)*mask)[groups==g]) for g in sorted(set(groups))])
        choices.append((float(utility),-int(sum(mask)),threshold))
    utility,negcalls,threshold=max(choices)
    return dict(threshold=None if math.isinf(threshold) else float(threshold),development_calls=-negcalls,
                development_rate=-negcalls/len(y),development_utility=utility)

def main():
    output=ROOT/'artifacts/study_v94/router_precommit.json';assert not output.exists()
    assert not list((ROOT/'results/v94_native/branches').glob('*.json'))
    assert len(list((ROOT/'results/v94_native/requests').glob('*.json')))==100
    cases=read(ROOT/'results/v91_analysis/cases.json')
    paths=['reports/protocol_v94_router_addendum.md','scripts/prepare_router_numerical_v94.py',
           'results/v91_analysis/cases.json','src/escalation/finite_v6.py','artifacts/study_v94/jobs.json']
    fs=[];groups=[];targets=[]
    for case in cases:
        p=read(ROOT/case['prefix']);paths.append(case['prefix'])
        fs.append(p['features']);groups.append(case['system_group']);targets.append(case['gains']['full_sequential_3nn'])
    keys=sorted(fs[0]);x=np.asarray([[f[k] for k in keys] for f in fs]);y=np.asarray(targets);groups=np.asarray(groups)
    assert len(set(groups))==6 and len(cases)==30
    oof=np.empty(len(y))
    for group in sorted(set(groups)):
        train=groups!=group;test=~train;oof[test]=predict(x[test],fit(x[train],y[train]))
    benefit=choose(oof,y,groups,[-.1,-.05,0.,.01,.05,.1,math.inf]);model=fit(x,y)
    u=x[:,keys.index('uncertainty')]
    uncertainty=choose(u,y,groups,[*np.quantile(u,[0,.25,.5,.75,1]),math.inf])
    rows=[]
    for job in read(ROOT/'artifacts/study_v94/jobs.json'):
        p=read(ROOT/job['prefix']);paths.append(job['prefix'])
        f,_=features(candidates(p['family']),State(**p['state']),p['seed'])
        assert set(f)==set(keys)
        score=float(predict(np.asarray([[f[k] for k in keys]]),model)[0])
        rows.append({'key':job['key'],'family':p['family'],'seed':p['seed'],'features':f,'benefit_prediction':score})
    assert not set(groups)&{r['family'] for r in rows}
    masks={'never':[False]*10,'always':[True]*10,
        'benefit':[r['benefit_prediction']>(math.inf if benefit['threshold'] is None else benefit['threshold']) for r in rows],
        'uncertainty':[r['features']['uncertainty']>(math.inf if uncertainty['threshold'] is None else uncertainty['threshold']) for r in rows]}
    order=sorted(range(10),key=lambda i:rows[i]['key'])
    for j,(name,selector) in enumerate([('benefit',benefit),('uncertainty',uncertainty)]):
        rng=random.Random(94011+j);chosen={i:rng.random()<selector['development_rate'] for i in order}
        masks['random_development_'+name]=[chosen[i] for i in range(10)]
        selected=set(random.Random(94001+j).sample(order,sum(masks[name])))
        masks['random_matched_'+name+'_diagnostic']=[i in selected for i in range(10)]
    write(output,{'at':now(),'scope':'secondary precontinuation exploratory transfer; six dev/two test groups',
        'features':keys,'model':model,'benefit':benefit,'uncertainty':uncertainty,'development_groups':sorted(set(groups)),
        'development_oof_predictions':oof.tolist(),'development_targets':y.tolist(),'rows':rows,'masks':masks,
        'sha256':{n:sha(ROOT/n) for n in paths}})
    print({k:sum(v) for k,v in masks.items()})
if __name__=='__main__':main()
