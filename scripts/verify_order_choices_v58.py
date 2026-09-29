"""Independently reconstruct all V58 recommendations from each own prefix."""
import json,random,sys,time
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestRegressor
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results/v58_order_sensitivity'

def read(p):return json.loads(p.read_text())
def main():
    start=time.monotonic();count=0
    for b in read(OUT/'schedule.json'):
        family=b['family'];folder=OUT/f"{family}_perm_{b['permutation']:02d}"
        source='v54_java_screen' if family=='javagc' else 'v56_planning_screen'
        configs=[r['configuration'] for r in read(ROOT/f'results/{source}/table.json')]
        if family=='javagc':x=(np.log2(np.asarray(configs))-np.array([0.,0.,1.]))/np.array([3.,3.,2.])
        else:
            levels=[['lmcut','hmax'],['null','stubborn_sets_simple','stubborn_sets_ec','atom_centric_stubborn_sets'],['true','false'],['low_h','low_g','fifo']]
            x=np.array([[int(v==level) for v,choices in zip(c,levels) for level in choices] for c in configs])
        x=x[b['new_to_source']]
        def next_id(obs,method,seed,rng):
            nonlocal count
            if time.monotonic()-start>180:raise TimeoutError('Verification180s cap')
            count+=1;ids=[o['config_id'] for o in obs];remaining=[i for i in range(48) if i not in ids]
            if method=='random':return rng.choice(remaining)
            y=np.array([o['value_ms'] for o in obs])
            if method=='nn':
                score=[]
                for cid in remaining:
                    neighbors=sorted(range(len(ids)),key=lambda j:(float(np.abs(x[cid]-x[ids[j]]).mean()),j))[:3]
                    score.append(float(y[neighbors].mean()))
            else:
                model=RandomForestRegressor(n_estimators=64,min_samples_leaf=1,max_features=1.,bootstrap=True,n_jobs=1,random_state=seed*100+len(ids))
                model.fit(x[ids],y);pred=np.array([t.predict(x[remaining]) for t in model.estimators_]);score=pred.mean(axis=0)-pred.std(axis=0)
            return min(zip(score,remaining))[1]
        for seed in [11,23,37,53,71]:
            p=read(folder/f'prefix_{seed}.json')
            for i in range(4,10):assert next_id(p[:i],'nn',seed,None)==p[i]['config_id']
            for method in ['random','nn','rf_lcb']:
                obs=read(folder/f'arm_{seed}_{method}.json')['observations'];rng=random.Random(seed+1000)
                for i in range(10,20):assert next_id(obs[:i],method,seed,rng)==obs[i]['config_id']
    print(json.dumps({'verified':True,'reconstructed_choices':count,'runtime_seconds':time.monotonic()-start},indent=2))
if __name__=='__main__':main()
