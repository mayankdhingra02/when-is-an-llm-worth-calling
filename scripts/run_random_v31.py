"""Collect twenty frozen random continuations; never import the evaluator."""
import hashlib, os, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src')); os.chdir(ROOT)
from escalation.core import State
from escalation.io import read, write, append, lines, now, digest
from escalation.finite_v6 import load_candidates, LazyOracle
from escalation.random_v31 import MODES, branch
from escalation.resources import Resources
from escalation.config import load_config
from escalation.larger_v22 import authorization_config, require
OUT = Path('results/v31_random')

def main():
    require(not OUT.exists(), 'Preserve started or completed run')
    for name,h in read('reports/protocol_v31_random.freeze.json')['sha256'].items():
        require(hashlib.sha256(Path(name).read_bytes()).hexdigest()==h, 'Changed input: '+name)
    manifest = read('data/manifest_v30.json'); before = read('artifacts/resource_ledger_v2.json')
    cfg = authorization_config(load_config('configs/followup_v3.yaml'), read('configs/authorization_v22.json'))
    acquired = 0; stop = None
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        require(resource.remaining()>120,'120-second reserve'); deadline=time.monotonic()+120
        write(OUT/'started.json',{'at':now(),'intended_arms':20,'maximum_new_accesses':200,'baseline_ledger':before})
        try:
            for spec in manifest['datasets']:
                c = load_candidates(spec)
                for seed in manifest['seeds']:
                    key=f"{spec['id']}_{seed}"; saved=read(f'results/v30_transfer/prefixes/{key}.json')
                    prefix=State(**saved['state']); require(digest(prefix.record())==saved['prefix_hash'],'Prefix identity')
                    for mode in MODES:
                        ctx={'dataset':spec['id'],'system_group':spec['system_group'],'seed':seed,'arm':mode,
                             'namespace':'measured_exploratory_v31','prefix_hash':saved['prefix_hash']}
                        oracle=LazyOracle(spec,c,prefix=prefix.record(),journal=lambda e:append(OUT/'acquisitions.jsonl',{**ctx,**e,'at':now()}))
                        def acquire(row):
                            nonlocal acquired
                            resource.check(); require(time.monotonic()<deadline,'120-second stage cap')
                            require(acquired<200,'200 new acquisitions cap'); acquired+=1
                            return oracle.acquire(row)
                        start=time.perf_counter()
                        state,selection=branch(prefix,saved['pool']['ranked'],spec['id'],seed,mode,c.directions,acquire,
                            lambda s:write(OUT/'checkpoints'/f'{key}_{mode}.json',s.record()))
                        write(OUT/'arms'/f'{key}_{mode}.json',{**ctx,'status':'completed','state':state.record(),
                            'selection':selection,'logical_evaluations':20,'actual_new_accesses':oracle.new_accesses,
                            'branch_seconds':time.perf_counter()-start})
                        print(key,mode,'completed',flush=True)
        except Exception as exc: stop=f'{type(exc).__name__}: {exc}'
        finally:
            statuses=[{'dataset':s['id'],'seed':seed,'arm':mode,'status':'completed' if
                (OUT/'arms'/f"{s['id']}_{seed}_{mode}.json").exists() else 'incomplete_or_unattempted'}
                for s in manifest['datasets'] for seed in manifest['seeds'] for mode in MODES]
            write(OUT/'progress.json',{'complete':all(s['status']=='completed' for s in statuses),
                'arms':statuses,'stop_reason':stop,'actual_new_accesses':len(lines(OUT/'acquisitions.jsonl'))})
    after=read('artifacts/resource_ledger_v2.json'); require(after['requests']==before['requests']==200,'No inference')
    write('artifacts/study_v31/collection_accounting.json',{'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],
        'cumulative_seconds':after['experiment_seconds'],'new_objective_acquisitions':len(lines(OUT/'acquisitions.jsonl')),
        'new_model_calls':0,'active_since':after['active_since']})
    if stop: raise RuntimeError(stop)

if __name__=='__main__': main()
