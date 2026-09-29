"""Bounded acquisition for fixed consensus plans. No model provider/evaluator."""
import hashlib, os, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT/'src')); os.chdir(ROOT)
from escalation.io import read, write, append, lines, digest, now
from escalation.core import State
from escalation.config import load_config
from escalation.resources import Resources
from escalation.larger_v22 import authorization_config, require
from escalation.finite_v6 import load_candidates, LazyOracle
from escalation.consensus_v28 import select, continue_branch
OUT = Path('results/v28_consensus')


def main():
    require(not OUT.exists(), 'Preserve started/completed transaction; no automatic restart')
    for name, h in read('reports/protocol_v28_consensus.freeze.json')['sha256'].items():
        require(hashlib.sha256(Path(name).read_bytes()).hexdigest() == h, 'Changed frozen input: '+name)
    plans = read('data/consensus_v28.json')['cases']; manifest = read('data/manifest_v8.json')
    require(len(plans) == 15, 'All15 intended cases')
    cfg = authorization_config(load_config('configs/followup_v3.yaml'), read('configs/authorization_v22.json'))
    before = read('artifacts/resource_ledger_v2.json'); stop = None
    with Resources(cfg, 'artifacts/resource_ledger_v2.json') as resource:
        require(resource.remaining() > 60, '60-second reserve'); deadline = time.monotonic()+60
        write(OUT/'started.json', {'at': now(), 'intended_arms': 15, 'intended_new_accesses': 150, 'baseline_ledger': before})
        try:
            for plan in plans:
                key = f"{plan['dataset']}_{plan['seed']}"
                p = read(f'results/v6/prefixes/{key}.json')['state']
                require(digest(p) == plan['prefix_hash'], 'Frozen prefix')
                require(select(plan['pool'], plan['ballots'])['selected'] == plan['selected'], 'Fixed vote rule')
                spec = next(d for d in manifest['datasets'] if d['id'] == plan['dataset'])
                candidates = load_candidates(spec)
                ctx = {k: plan[k] for k in ('dataset', 'seed', 'system_group', 'prefix_hash')}
                ctx.update(split='development', namespace='measured_v28', arm='cached_real_response_consensus')
                oracle = LazyOracle(spec, candidates, prefix=p, journal=lambda e: append(OUT/'acquisitions.jsonl', {**ctx, **e, 'at': now()}))
                def acquire(row):
                    resource.check(); require(time.monotonic() < deadline, '60-second stage deadline')
                    return oracle.acquire(row)
                start = time.perf_counter()
                state = continue_branch(State(**p), plan['selected'], candidates.directions, acquire,
                    lambda s: write(OUT/'checkpoints'/f'{key}.json', s.record()))
                write(OUT/'arms'/f'{key}.json', {**ctx, 'status': 'completed', 'state': state.record(),
                    'actual_new_accesses': oracle.new_accesses, 'logical_evaluations': 20,
                    'branch_seconds': time.perf_counter()-start, 'source_request_ids': [r['request_id'] for r in plan['sources']]})
                print(key, 'completed', flush=True)
        except Exception as e:
            stop = f'{type(e).__name__}: {e}'
        finally:
            statuses = [{'dataset': p['dataset'], 'seed': p['seed'], 'status': 'completed' if (OUT/'arms'/f"{p['dataset']}_{p['seed']}.json").exists() else 'incomplete_or_unattempted'} for p in plans]
            write(OUT/'progress.json', {'complete': all(r['status'] == 'completed' for r in statuses),
                'arms': statuses, 'stop_reason': stop, 'actual_new_accesses': len(lines(OUT/'acquisitions.jsonl'))})
    after = read('artifacts/resource_ledger_v2.json'); require(after['requests'] == before['requests'] == 200, 'No new model calls')
    write('artifacts/study_v28/collection_accounting.json', {'charged_seconds': after['experiment_seconds']-before['experiment_seconds'],
        'cumulative_seconds': after['experiment_seconds'], 'new_model_calls': 0,
        'new_objective_acquisitions': len(lines(OUT/'acquisitions.jsonl')), 'active_since': after['active_since']})
    if stop: raise RuntimeError(stop)


if __name__ == '__main__': main()
