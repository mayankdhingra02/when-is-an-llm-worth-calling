"""Fresh-prefix, five-arm classical transfer collection with explicit caps."""
import hashlib, os, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT/'src')); os.chdir(ROOT)
from escalation.io import read, write, append, lines, digest, now
from escalation.core import initial_state
from escalation.finite_domain import recommend
from escalation.finite_v6 import load_candidates, LazyOracle
from escalation.selection_v8 import shortlist
from escalation.transfer_v30 import validate_admission, branch, MODES
from escalation.config import load_config
from escalation.resources import Resources
from escalation.larger_v22 import authorization_config, require
OUT = Path('results/v30_transfer')


def main():
    require(not OUT.exists(), 'Preserve started/completed transfer run')
    freeze = read('reports/protocol_v30_transfer.freeze.json')
    for name, h in freeze['sha256'].items():
        require(hashlib.sha256(Path(name).read_bytes()).hexdigest() == h, 'Changed frozen input: '+name)
    m = read('data/manifest_v30.json'); validate_admission(m['datasets'], m['historical_exposed_groups'])
    cfg = authorization_config(load_config('configs/followup_v3.yaml'), read('configs/authorization_v22.json'))
    before = read('artifacts/resource_ledger_v2.json'); stop = None; acquired = 0
    with Resources(cfg, 'artifacts/resource_ledger_v2.json') as resource:
        require(resource.remaining() > 120, '120-second reserve'); deadline = time.monotonic()+120
        write(OUT/'started.json', {'at': now(), 'intended_prefixes': 10, 'intended_arms': 50,
                                 'maximum_new_accesses': 600, 'baseline_ledger': before})
        try:
            for spec in m['datasets']:
                candidates = load_candidates(spec)
                for seed in m['seeds']:
                    key = f"{spec['id']}_{seed}"
                    ctx = {'dataset': spec['id'], 'seed': seed, 'system_group': spec['system_group'],
                           'split': 'prospective_transfer', 'namespace': 'measured_v30', 'arm': 'prefix'}
                    def make_oracle(prefix=None):
                        return LazyOracle(spec, candidates, prefix=prefix,
                            journal=lambda e: append(OUT/'acquisitions.jsonl', {**ctx, **e, 'at': now()}))
                    oracle = make_oracle()
                    def acquire(row):
                        nonlocal acquired
                        resource.check(); require(time.monotonic() < deadline, '120-second stage limit')
                        require(acquired < 600, '600 acquisitions cap'); acquired += 1
                        return oracle.acquire(row)
                    prefix = initial_state(candidates, seed); start = time.perf_counter()
                    for _ in range(10):
                        row = recommend(candidates, prefix)
                        prefix.observe(row, acquire(row), candidates.directions)
                        write(OUT/'prefix_checkpoints'/f'{key}.json', prefix.record())
                    prefix_hash = digest(prefix.record()); pool = shortlist(candidates, prefix, seed)
                    write(OUT/'prefixes'/f'{key}.json', {'state': prefix.record(), 'prefix_hash': prefix_hash,
                        'pool': pool, 'actual_new_accesses': oracle.new_accesses, 'prefix_seconds': time.perf_counter()-start, 'at': now()})
                    for mode in MODES:
                        ctx.update(arm=mode, prefix_hash=prefix_hash); oracle = make_oracle(prefix.record()); start = time.perf_counter()
                        final, trace = branch(candidates, prefix, pool['ranked'], mode, acquire,
                            lambda s, t: write(OUT/'checkpoints'/f'{key}_{mode}.json', {'state': s.record(), 'trace': t}))
                        write(OUT/'arms'/f'{key}_{mode}.json', {**ctx, 'status': 'completed', 'state': final.record(),
                            'trace': trace, 'logical_evaluations': 20, 'actual_new_accesses': oracle.new_accesses,
                            'branch_seconds': time.perf_counter()-start})
                        print(key, mode, 'completed', flush=True)
        except Exception as e:
            stop = f'{type(e).__name__}: {e}'
        finally:
            statuses = [{'dataset': d['id'], 'seed': seed, 'arm': mode,
                'status': 'completed' if (OUT/'arms'/f"{d['id']}_{seed}_{mode}.json").exists() else 'incomplete_or_unattempted'}
                for d in m['datasets'] for seed in m['seeds'] for mode in MODES]
            write(OUT/'progress.json', {'complete': all(r['status'] == 'completed' for r in statuses),
                'arms': statuses, 'stop_reason': stop, 'actual_new_accesses': len(lines(OUT/'acquisitions.jsonl'))})
    after = read('artifacts/resource_ledger_v2.json'); require(after['requests'] == before['requests'] == 200, 'No new inference')
    write('artifacts/study_v30/collection_accounting.json', {'charged_seconds': after['experiment_seconds']-before['experiment_seconds'],
        'cumulative_seconds': after['experiment_seconds'], 'new_objective_acquisitions': len(lines(OUT/'acquisitions.jsonl')),
        'new_model_calls': 0, 'active_since': after['active_since']})
    if stop: raise RuntimeError(stop)


if __name__ == '__main__': main()
