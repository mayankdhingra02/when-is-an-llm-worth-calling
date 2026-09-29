"""Bounded paired 3NN collection; no evaluator or model provider imports."""
import hashlib, os, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT/'src')); os.chdir(ROOT)
from escalation.io import read, write, append, lines, digest, now
from escalation.core import State
from escalation.config import load_config
from escalation.resources import Resources
from escalation.larger_v22 import authorization_config, require
from escalation.finite_v6 import load_candidates, LazyOracle
from escalation.selection_v8 import shortlist
from escalation.neighbors_v29 import continue_branch
OUT = Path('results/v29_neighbors')
MODES = ('batch_3nn', 'sequential_3nn')


def main():
    require(not OUT.exists(), 'Preserve started/completed transaction; no automatic restart')
    for name, h in read('reports/protocol_v29_neighbors.freeze.json')['sha256'].items():
        require(hashlib.sha256(Path(name).read_bytes()).hexdigest() == h, 'Changed frozen input: '+name)
    manifest = read('data/manifest_v8.json'); require(len(manifest['cases']) == 15, 'Fifteen cases required')
    cfg = authorization_config(load_config('configs/followup_v3.yaml'), read('configs/authorization_v22.json'))
    before = read('artifacts/resource_ledger_v2.json'); stop = None; acquired = 0
    with Resources(cfg, 'artifacts/resource_ledger_v2.json') as resource:
        require(resource.remaining() > 60, '60-second reserve'); deadline = time.monotonic()+60
        write(OUT/'started.json', {'at': now(), 'intended_arms': 30, 'intended_new_accesses': 300, 'baseline_ledger': before})
        try:
            for case in manifest['cases']:
                key = f"{case['dataset']}_{case['seed']}"
                p = read(f'results/v6/prefixes/{key}.json')['state']
                require(digest(p) == case['prefix_hash'], 'Prefix identity')
                spec = next(d for d in manifest['datasets'] if d['id'] == case['dataset'])
                require(spec['direction'] == '-', 'Minimized objective required')
                candidates = load_candidates(spec)
                pool = shortlist(candidates, State(**p), case['seed'])
                require(pool == case['pool'], 'Feature/acquired-label shortlist identity')
                for mode in MODES:
                    ctx = {'dataset': case['dataset'], 'seed': case['seed'], 'system_group': spec['system_group'],
                           'prefix_hash': case['prefix_hash'], 'split': 'development', 'namespace': 'measured_v29', 'arm': mode}
                    oracle = LazyOracle(spec, candidates, prefix=p,
                        journal=lambda e: append(OUT/'acquisitions.jsonl', {**ctx, **e, 'at': now()}))
                    def acquire(row):
                        nonlocal acquired
                        resource.check(); require(time.monotonic() < deadline, '60-second collection limit')
                        require(acquired < 300, '300-access stage cap'); acquired += 1
                        return oracle.acquire(row)
                    start = time.perf_counter()
                    state, trace = continue_branch(candidates, State(**p), pool['ranked'], mode, acquire,
                        lambda s, t: write(OUT/'checkpoints'/f'{key}_{mode}.json', {'state': s.record(), 'trace': t}))
                    write(OUT/'arms'/f'{key}_{mode}.json', {**ctx, 'status': 'completed', 'state': state.record(),
                        'trace': trace, 'pool': pool['ranked'], 'actual_new_accesses': oracle.new_accesses,
                        'logical_evaluations': 20, 'branch_seconds': time.perf_counter()-start})
                    print(key, mode, 'completed', flush=True)
        except Exception as e:
            stop = f'{type(e).__name__}: {e}'
        finally:
            statuses = [{'dataset': c['dataset'], 'seed': c['seed'], 'arm': mode,
                'status': 'completed' if (OUT/'arms'/f"{c['dataset']}_{c['seed']}_{mode}.json").exists() else 'incomplete_or_unattempted'}
                for c in manifest['cases'] for mode in MODES]
            write(OUT/'progress.json', {'complete': all(r['status'] == 'completed' for r in statuses),
                'arms': statuses, 'stop_reason': stop, 'actual_new_accesses': len(lines(OUT/'acquisitions.jsonl'))})
    after = read('artifacts/resource_ledger_v2.json'); require(after['requests'] == before['requests'] == 200, 'No new inference')
    write('artifacts/study_v29/collection_accounting.json', {'charged_seconds': after['experiment_seconds']-before['experiment_seconds'],
        'cumulative_seconds': after['experiment_seconds'], 'new_model_calls': 0,
        'new_objective_acquisitions': len(lines(OUT/'acquisitions.jsonl')), 'active_since': after['active_since']})
    if stop: raise RuntimeError(stop)


if __name__ == '__main__': main()
