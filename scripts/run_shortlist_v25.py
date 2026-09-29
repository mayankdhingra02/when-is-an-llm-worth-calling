"""Bounded classical collection. No evaluator or model provider imported."""
import hashlib,os,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
from escalation.io import read,write,append,lines,digest,now
from escalation.core import State
from escalation.config import load_config
from escalation.resources import Resources
from escalation.larger_v22 import authorization_config,require
from escalation.finite_v6 import load_candidates,LazyOracle
from escalation.selection_v8 import shortlist
from escalation.shortlist_v25 import continue_branch
OUT=Path('results/v25_shortlist')

def main():
    require(not OUT.exists(),'Preserve started/completed transaction; no automatic restart')
    for n,h in read('reports/protocol_v25_shortlist.freeze.json')['sha256'].items():
        require(hashlib.sha256(Path(n).read_bytes()).hexdigest()==h,'Frozen input changed: '+n)
    m=read('data/manifest_v8.json');require(len(m['cases'])==15,'All15 cases required')
    jobs=read('data/larger_probe_v22.json')['jobs']
    cfg=authorization_config(load_config('configs/followup_v3.yaml'),read('configs/authorization_v22.json'))
    before=read('artifacts/resource_ledger_v2.json');stop=None
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        require(resource.remaining()>60,'60seconds reserve required');deadline=time.monotonic()+60
        write(OUT/'started.json',{'at':now(),'intended_arms':15,'intended_new_accesses':150,'baseline_ledger':before,'model_calls':0})
        try:
            for case in m['cases']:
                key=f"{case['dataset']}_{case['seed']}";spec=next(d for d in m['datasets'] if d['id']==case['dataset'])
                p=read(f'results/v6/prefixes/{key}.json');s=State(**p['state']);c=load_candidates(spec)
                require(digest(s.record())==case['prefix_hash']==p['prefix_hash'],'Prefix identity')
                pool=shortlist(c,s,case['seed']);require(pool==case['pool'],'Acquired-only shortlist identity')
                require(all(set(j['mapping'].values())==set(pool['ranked']) for j in jobs if j['dataset']==case['dataset'] and j['seed']==case['seed']),'V22 search-space equality')
                ctx={'dataset':case['dataset'],'seed':case['seed'],'system_group':spec['system_group'],'split':'development','namespace':'measured_v25','arm':'adaptive_shortlist','prefix_hash':p['prefix_hash']}
                oracle=LazyOracle(spec,c,prefix=p['state'],journal=lambda event:append(OUT/'acquisitions.jsonl',{**ctx,**event,'at':now()}))
                def acquire(row):
                    resource.check();require(time.monotonic()<deadline,'60-second stage limit');return oracle.acquire(row)
                start=time.perf_counter()
                final=continue_branch(c,s,pool['ranked'],acquire,lambda state:write(OUT/'checkpoints'/f'{key}.json',state.record()))
                write(OUT/'arms'/f'{key}.json',{**ctx,'status':'completed','state':final.record(),'pool':pool,'actual_new_accesses':oracle.new_accesses,'logical_evaluations':20,'branch_seconds':time.perf_counter()-start})
                print(key,'completed',flush=True)
        except Exception as error:stop=f'{type(error).__name__}: {error}'
        finally:
            statuses=[{'dataset':c['dataset'],'seed':c['seed'],'status':'completed' if (OUT/'arms'/f"{c['dataset']}_{c['seed']}.json").exists() else 'incomplete_or_unattempted'} for c in m['cases']]
            write(OUT/'progress.json',{'complete':all(r['status']=='completed' for r in statuses),'arms':statuses,'stop_reason':stop,'actual_new_accesses':len(lines(OUT/'acquisitions.jsonl'))})
    after=read('artifacts/resource_ledger_v2.json');require(after['requests']==before['requests']==200,'No model calls')
    write('artifacts/study_v25/collection_accounting.json',{'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],'cumulative_seconds':after['experiment_seconds'],'new_model_calls':0,'new_objective_acquisitions':len(lines(OUT/'acquisitions.jsonl')),'external_spend_usd':0,'active_since':after['active_since']})
    if stop:raise RuntimeError(stop)

if __name__=='__main__':main()
