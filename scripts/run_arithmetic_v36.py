"""Bounded exact-arithmetic continuation collection. No hidden-table evaluator import."""
import hashlib,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import read,write,append,lines,digest,now
from escalation.config import load_config
from escalation.resources import Resources
from escalation.larger_v22 import authorization_config,require
from escalation.finite_v6 import load_candidates
from escalation.arithmetic_v36 import Oracle,continuation
OUT=Path('results/v36_arithmetic');MODES=('joint_shortlist','joint_full')

def main():
    require(not OUT.exists(),'Preserve started/completed run')
    for p,h in read('reports/protocol_v36_arithmetic.freeze.json')['sha256'].items():require(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,'Frozen input: '+p)
    m=read('data/arithmetic_v36.json');before=read('artifacts/resource_ledger_v2.json');count=0;stop=None
    cfg=authorization_config(load_config('configs/followup_v3.yaml'),read('configs/authorization_v22.json'))
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        require(resource.remaining()>120,'120-second reserve');deadline=time.monotonic()+120
        write(OUT/'started.json',{'at':now(),'intended_arms':20,'intended_new_accesses':200,'baseline_ledger':before})
        try:
            for case in m['cases']:
                key=f"{case['dataset']}_{case['seed']}";spec=next(d for d in m['datasets'] if d['id']==case['dataset']);c=load_candidates(spec)
                p=case['prefix'];require(digest(p)==case['prefix_hash'],'Saved exact prefix binding')
                for mode in MODES:
                    ctx={'dataset':case['dataset'],'system_group':spec['system_group'],'seed':case['seed'],'arm':mode,'split':'exposed_development',
                        'namespace':'measured_joint_vectors_v36','prefix_hash':case['prefix_hash'],'v34_prefix_hash':case['v34_prefix_hash']}
                    oracle=Oracle(spec,c,p,lambda e:append(OUT/'acquisitions.jsonl',{**ctx,**e,'at':now()}))
                    def acquire(row):
                        nonlocal count
                        resource.check();require(time.monotonic()<deadline,'120-second collection cap');require(count<200,'200-vector cap');count+=1
                        return oracle.acquire(row)
                    start=time.perf_counter();state=continuation(c,p,case['pool'],mode,acquire,
                        lambda s:write(OUT/'checkpoints'/f'{key}_{mode}.json',s))
                    write(OUT/'arms'/f'{key}_{mode}.json',{**ctx,**state,'size_cap':p['size_cap'],'status':'completed','actual_new_accesses':oracle.new_accesses,
                        'logical_evaluations':20,'branch_seconds':time.perf_counter()-start})
                print(key,'2/2 completed',flush=True)
        except Exception as e:stop=f'{type(e).__name__}: {e}'
        finally:
            statuses=[{'dataset':c['dataset'],'seed':c['seed'],'arm':mode,'status':'completed' if (OUT/'arms'/f"{c['dataset']}_{c['seed']}_{mode}.json").exists() else 'incomplete_or_unattempted'} for c in m['cases'] for mode in MODES]
            write(OUT/'progress.json',{'complete':all(r['status']=='completed' for r in statuses),'arms':statuses,'stop_reason':stop,'actual_new_accesses':len(lines(OUT/'acquisitions.jsonl'))})
    after=read('artifacts/resource_ledger_v2.json');require(after['requests']==before['requests']==200,'No inference')
    write('artifacts/study_v36/collection_accounting.json',{'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],
        'cumulative_seconds':after['experiment_seconds'],'new_model_calls':0,'new_physical_trials':0,'new_vector_acquisitions':len(lines(OUT/'acquisitions.jsonl')),'active_since':after['active_since']})
    if stop:raise RuntimeError(stop)
if __name__=='__main__':main()
