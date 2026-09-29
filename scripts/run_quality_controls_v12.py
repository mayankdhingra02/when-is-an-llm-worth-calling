"""Actual recorded-table acquisitions; all online target reads are charged."""
import sys,csv,random,time,fcntl,math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import read,write,append,lines,now
from escalation.data import sha
from escalation.finite_v6 import load_candidates
from escalation.study_v8 import run_config,verify
from escalation.resources import Resources
from escalation.quality_controls_v12 import choose
from escalation.quality_v11 import fastest
OUT=Path('results/v12_controls')

class JointOracle:
    def __init__(self,d,c,context,prefix=None):
        self.d=d;self.c=c;self.context=context;self.acquired={} if prefix is None else dict(zip(prefix['ids'],prefix['labels']))
    def acquire(self,i):
        if i in self.acquired or len(self.acquired)>=20:raise ValueError('duplicate or over-budget')
        with Path(self.d['path']).open(newline='') as f:
            for line,row in enumerate(csv.DictReader(f,delimiter=self.d['delimiter']),2):
                if line==self.c.source_ids[i]:
                    append(OUT/'acquisitions.jsonl',{**self.context,'at':now(),'row_id':i,'source_line':line,'raw_runtime':row['performance'],'raw_size':row['size'],'vector_charge':1})
                    pair=[float(row['performance']),float(row['size'])]
                    if not all(math.isfinite(x) and x>0 for x in pair):raise ValueError('invalid charged joint target')
                    self.acquired[i]=pair;return pair
        raise ValueError('source row missing')

def run(resources):
    verify()
    for p,h in read('reports/protocol_v12_controls.freeze.json')['sha256'].items():assert sha(p)==h,p
    m=read('data/manifest_v8.json');datasets=[d for d in m['datasets'] if d['id'] in ['brotli','lrzip']];stop=None
    if not (OUT/'manifest.json').exists():write(OUT/'manifest.json',{'at':now(),'namespace':'measured_joint_classical_v12','baseline_ledger':read('artifacts/resource_ledger_v2.json'),'intended_cases':10,'intended_branches':20,'intended_new_vector_accesses':300})
    try:
        for d in datasets:
            c=load_candidates(d)
            for seed in m['seeds']:
                resources.check();key=d['id']+'_'+str(seed);pp=OUT/'prefixes'/(key+'.json');ctx={'dataset':d['id'],'seed':seed,'system_group':d['system_group'],'split':'development','namespace':'measured_joint_classical_v12'}
                original=read('results/v6/prefixes/'+key+'.json')['state']
                if pp.exists():p=read(pp)
                else:
                    marker=OUT/'starts'/(key+'_prefix.json')
                    if marker.exists():raise RuntimeError('interrupted prefix; audit journal first')
                    write(marker,{'at':now()});o=JointOracle(d,c,{**ctx,'arm':'shared_prefix'});ids=[];labels=[]
                    for i in original['ids']:
                        resources.check();labels.append(o.acquire(i));ids.append(i)
                    anchor=min(range(10),key=lambda j:labels[j][0]);p={**ctx,'ids':ids,'labels':labels,'order':original['order'],'anchor_row':ids[anchor],'size_cap':labels[anchor][1]};write(pp,p)
                for method in ['joint_3nn','random']:
                    dest=OUT/method/(key+'.json')
                    if dest.exists():continue
                    marker=OUT/'starts'/(key+'_'+method+'.json')
                    if marker.exists():raise RuntimeError('interrupted arm; audit journal first')
                    write(marker,{'at':now()});t=time.perf_counter();ids=list(p['ids']);labels=[list(x) for x in p['labels']];events=[];o=JointOracle(d,c,{**ctx,'arm':method},p)
                    while len(ids)<20:
                        resources.check();i,event=choose(c,p['order'],ids,labels,p['size_cap'],method);y=o.acquire(i)
                        ids.append(i);labels.append(y);events.append({'row_id':i,**event})
                        write(OUT/'checkpoints'/(key+'_'+method+'.json'),{'ids':ids,'labels':labels,'events':events})
                    eligible=[j for j,y in enumerate(labels) if y[1]<=p['size_cap']];j=min(eligible,key=lambda j:labels[j][0])
                    write(dest,{**ctx,'arm':method,'ids':ids,'labels':labels,'events':events,'size_cap':p['size_cap'],'best_row':ids[j],'best_runtime':labels[j][0],'best_size':labels[j][1],
                        'actual_new_vector_accesses':10,'logical_evaluations':20,'infeasible_new_acquisitions':sum(y[1]>p['size_cap'] for y in labels[10:]),'branch_seconds':time.perf_counter()-t,'status':'completed'})
                    print(key,method,'completed',flush=True)
    except Exception as exc:stop=f'{type(exc).__name__}: {exc}';print('STOP',stop,flush=True)
    intended=[{'dataset':d['id'],'seed':seed,'arm':arm,'status':'completed' if (OUT/arm/(d['id']+'_'+str(seed)+'.json')).exists() else 'blocked'} for d in datasets for seed in m['seeds'] for arm in ['joint_3nn','random']]
    write(OUT/'progress.json',{'at':now(),'intended':intended,'complete':all(r['status']=='completed' for r in intended),'stop_reason':stop,'actual_vector_accesses':len(lines(OUT/'acquisitions.jsonl'))})
    return 0 if stop is None else 1

if __name__=='__main__':
    with Path('artifacts/resource_ledger.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        with Resources(run_config(),'artifacts/resource_ledger_v2.json') as r:raise SystemExit(run(r))
