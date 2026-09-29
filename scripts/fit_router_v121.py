"""Seven exposed development families; no MongoDB data or outcomes are read."""
import json,math,sys
import numpy as np
from table_check_v121 import ROOT,read,write,sha,now,frozen
from escalation.io import digest
KEYS=['log_candidates','variables','objectives','symbolic_fraction','remaining','progress','plateau','separation','uncertainty']
THRESHOLDS=[0.,.02,.05,.1,None]
def fit(rows,target):
    if not rows or any(r['system_group']=='mongodb' for r in rows):raise ValueError('Test family in fitting input')
    x=np.array([[r['features'][k] for k in KEYS] for r in rows]);y=np.array([r[target] for r in rows]);groups=[r['system_group'] for r in rows]
    if not np.isfinite(x).all() or not np.isfinite(y).all():raise ValueError('Nonfinite development data')
    w=np.array([1/groups.count(g) for g in groups]);w/=w.sum();mean=np.sum(x*w[:,None],axis=0);scale=np.sqrt(np.sum((x-mean)**2*w[:,None],axis=0));scale[scale<1e-12]=1
    z=(x-mean)/scale;intercept=float(w@y);coef=np.linalg.solve(z.T@(w[:,None]*z)+np.eye(len(KEYS)),z.T@(w*(y-intercept)))
    return {'features':KEYS,'mean':mean.tolist(),'scale':scale.tolist(),'coefficient':coef.tolist(),'intercept':intercept,'ridge_lambda':1.}
def predict(m,rows):return ((np.array([[r['features'][k] for k in KEYS] for r in rows])-m['mean'])/m['scale'])@m['coefficient']+m['intercept']
def choose(scores,rows,target,grid):
    vals=[]
    for threshold in grid:
        mask=np.zeros(len(rows),dtype=bool) if threshold is None else np.array(scores)>threshold
        groups=sorted({r['system_group'] for r in rows});quality=np.mean([np.mean([r[target]*m for r,m in zip(rows,mask) if r['system_group']==g]) for g in groups])
        vals.append({'threshold':threshold,'group_mean_selected_gain':float(quality),'rate':float(mask.mean())})
    selected=max(range(len(vals)),key=lambda i:(vals[i]['group_mean_selected_gain'],-vals[i]['rate'],i))
    return vals[selected],vals
def train(rows,target):
    oof=np.zeros(len(rows));folds=[]
    for g in sorted({r['system_group'] for r in rows}):
        train=[r for r in rows if r['system_group']!=g];idx=[i for i,r in enumerate(rows) if r['system_group']==g];m=fit(train,target);oof[idx]=predict(m,[rows[i] for i in idx]);folds.append({'held_development_family':g,'training_families':sorted({r['system_group'] for r in train})})
    b,bs=choose(oof,rows,target,THRESHOLDS);u,us=choose([r['features']['uncertainty'] for r in rows],rows,target,[0.,.25,.5,.75,1.,None]);m=fit(rows,target);m.update(threshold=b['threshold'],development_oof_rate=b['rate'])
    return {'at':now(),'target':target,'development_rows_sha256':digest(rows),'development_groups':sorted({r['system_group'] for r in rows}),'benefit':m,'uncertainty':{'threshold':u['threshold'],'rate':u['rate']},'oof':{'scores':oof.tolist(),'folds':folds,'benefit_grid':bs,'uncertainty_grid':us},'qualification':'Development-adaptive on seven exposed families; one untouched prospective MongoDB family; no broad generalization claim'}
def main():
    frozen()
    out=ROOT/'results/v121_router';out.mkdir(exist_ok=False);rows=[]
    for r in read(ROOT/'results/v91_analysis/cases.json'):
        p=read(ROOT/r['prefix']);assert r['fallback_reason'] is None
        rows.append({'dataset':r['dataset'],'system_group':r['system_group'],'seed':r['seed'],'features':p['features'],'gain_primary':min(r['gains'][k] for k in ['batch_3nn','full_sequential_3nn']),'gain_first10':r['gains']['presentation_first10'],'source':'v91'})
    for r in read(ROOT/'results/v120_analysis/summary.json')['cases']:
        p=read(ROOT/f"results/v119_classical/prefixes/{r['key']}.json");choice=read(ROOT/f"results/v120_qwen/choices/{r['key']}.json");assert choice['selected_ids']==list('0123456789')
        assert r['selected_rows']==[p['pool']['mapping'][i] for i in '0123456789']
        rows.append({'dataset':p['dataset'],'system_group':'storm','seed':p['seed'],'features':p['features'],'gain_primary':min(r['gains'][k] for k in ['batch_3nn','full_sequential_3nn']),'gain_first10':0.,'source':'v120'})
    assert len(rows)==35 and len({r['system_group'] for r in rows})==7
    write(out/'development_outcomes.json',rows)
    for target,name in [('gain_primary','router_seal'),('gain_first10','router_first10_seal')]:write(out/f'{name}.json',train(rows,target))
    write(out/'router_seal.sha256.json',{'sha256':sha(out/'router_seal.json')})
    write(ROOT/'artifacts/study_v121/router_inputs.freeze.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in out.glob('*.json')}})
    print('35 development cases, seven grouped families; two fixed targets fitted; no MongoDB target access')
if __name__=='__main__':main()
