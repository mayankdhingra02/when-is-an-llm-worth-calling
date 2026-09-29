"""Bounded acquisition; full-table scoring lives only in the separate evaluator."""
import hashlib,os,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
from escalation.io import read,write,append,lines,digest,now
from escalation.config import load_config
from escalation.resources import Resources
from escalation.larger_v22 import authorization_config,require
from escalation.finite_v6 import load_candidates
from escalation.constrained_v34 import JointOracle,continuation,MODES
OUT=Path('results/v34_constrained')

def main():
    require(not OUT.exists(),'Preserve started/completed transaction')
    for p,h in read('reports/protocol_v34_constrained.freeze.json')['sha256'].items():
        require(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,'Frozen input changed: '+p)
    m=read('data/constrained_v34.json');before=read('artifacts/resource_ledger_v2.json');count=0;stop=None
    cfg=authorization_config(load_config('configs/followup_v3.yaml'),read('configs/authorization_v22.json'))
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        require(resource.remaining()>120,'120-second reserve');deadline=time.monotonic()+120
        write(OUT/'started.json',{'at':now(),'intended_arms':70,'intended_new_accesses':800,'baseline_ledger':before})
        try:
            for case in m['cases']:
                key=f"{case['dataset']}_{case['seed']}";spec=next(d for d in m['datasets'] if d['id']==case['dataset'])
                c=load_candidates(spec);original=read(case['prefix_path'])['state']
                ctx={'dataset':case['dataset'],'system_group':spec['system_group'],'seed':case['seed'],
                    'namespace':'measured_joint_vectors_v34','split':'exposed_development','arm':'prefix'}
                oracle=JointOracle(spec,c,lambda e:append(OUT/'acquisitions.jsonl',{**ctx,**e,'at':now()}))
                def acquire(row):
                    nonlocal count
                    resource.check();require(time.monotonic()<deadline,'120-second stage cap')
                    require(count<800,'800-vector cap');count+=1
                    return oracle.acquire(row)
                labels=[acquire(i) for i in original['ids']]
                require([y[0] for y in labels]==[y[0] for y in original['labels']],'Reacquired runtime identity')
                anchor=min(range(10),key=lambda j:labels[j][0])
                prefix={'ids':original['ids'],'labels':labels,'order':original['order'],
                    'anchor_row':original['ids'][anchor],'size_cap':labels[anchor][1]}
                prefix_hash=digest(prefix);write(OUT/'prefixes'/f'{key}.json',{'prefix':prefix,'prefix_hash':prefix_hash})
                for mode in MODES:
                    ctx={**ctx,'arm':mode,'prefix_hash':prefix_hash};start=time.perf_counter()
                    oracle=JointOracle(spec,c,lambda e:append(OUT/'acquisitions.jsonl',{**ctx,**e,'at':now()}),prefix)
                    state=continuation(c,prefix,case['pool'],mode,case['selected'].get(mode),acquire,
                        lambda s:write(OUT/'checkpoints'/f'{key}_{mode}.json',s))
                    write(OUT/'arms'/f'{key}_{mode}.json',{**ctx,'status':'completed',**state,'actual_new_accesses':oracle.new_accesses,
                        'logical_evaluations':20,'branch_seconds':time.perf_counter()-start,'cached_request':case['provenance'].get(mode)})
                print(key,'7/7 completed',flush=True)
        except Exception as e:stop=f'{type(e).__name__}: {e}'
        finally:
            statuses=[{'dataset':c['dataset'],'seed':c['seed'],'arm':mode,'status':'completed' if (OUT/'arms'/f"{c['dataset']}_{c['seed']}_{mode}.json").exists() else 'incomplete_or_unattempted'} for c in m['cases'] for mode in MODES]
            write(OUT/'progress.json',{'complete':all(r['status']=='completed' for r in statuses),'arms':statuses,'stop_reason':stop,
                'actual_new_accesses':len(lines(OUT/'acquisitions.jsonl'))})
    after=read('artifacts/resource_ledger_v2.json');require(after['requests']==before['requests']==200,'No new inference')
    write('artifacts/study_v34/collection_accounting.json',{'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],
        'cumulative_seconds':after['experiment_seconds'],'new_model_calls':0,'new_physical_trials':0,'new_vector_acquisitions':len(lines(OUT/'acquisitions.jsonl')),'active_since':after['active_since']})
    if stop:raise RuntimeError(stop)

if __name__=='__main__':main()
