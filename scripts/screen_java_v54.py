"""Build sealed medians, collect saved classical decisions, then score separately."""
import collections
import hashlib
import itertools
import json
import random
import statistics
import sys
import time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from escalation.classical_java_v54 import RecordedOracle, choose, encode
from run_java_feasibility_v53 import digest


def write(path, obj):
    path.write_text(json.dumps(obj, indent=2) + '\n')


def main():
    started = time.monotonic()
    for p, expected in json.loads((ROOT / 'reports/protocol_v54_java_screen.freeze.json').read_text())['files'].items():
        assert digest(ROOT / p) == expected, p
    physical = ROOT / 'results/v54_java_physical'
    summary = json.loads((physical / 'summary.json').read_text())
    assert summary['attempted'] == summary['passed'] == 144
    rows = [json.loads(s) for s in (physical / 'trials.jsonl').read_text().splitlines()]
    by_config = collections.defaultdict(list)
    grid = list(itertools.product([1, 2, 4, 8], [1, 2, 4, 8], [2, 4, 8]))
    for r in rows:
        assert r['status'] == 'passed' and list(grid[r['config_id']]) == r['configuration']
        by_config[r['config_id']].append(r)
    out = ROOT / 'results/v54_java_screen'; out.mkdir(exist_ok=False)
    table = []
    for cid, config in enumerate(grid):
        entries = by_config[cid]
        assert sorted(r['round'] for r in entries) == [0, 1, 2]
        values = [r['final_ms'] for r in entries]
        table.append({'config_id': cid, 'configuration': config, 'median_ms': statistics.median(values),
                      'repetition_ms': values, 'trial_ids': [r['trial'] for r in entries],
                      'cv': statistics.stdev(values) / statistics.mean(values)})
    write(out / 'table.json', table)
    write(out / 'table_seal.json', {'sha256': digest(out / 'table.json'),
                                  'physical_trials_sha256': digest(physical / 'trials.jsonl')})
    oracle = RecordedOracle([r['median_ms'] for r in table])
    x = encode(grid)
    cases = []
    for seed in [11, 23, 37, 53, 71]:
        if time.monotonic() - started > 120: raise TimeoutError('offline screen cap')
        prefix = []
        for cid in random.Random(seed).sample(range(48), 4):
            prefix.append(oracle.acquire(cid, prefix, seed, 'prefix'))
        while len(prefix) < 10:
            prefix.append(oracle.acquire(choose(x, prefix, 'nn', seed), prefix, seed, 'prefix'))
        path = out / f'prefix_{seed}.json'; write(path, prefix)
        arms = {}
        for method in ['random', 'nn', 'rf_lcb']:
            observed = [dict(r) for r in prefix]
            rng = random.Random(seed + 1000)
            while len(observed) < 20:
                cid = choose(x, observed, method, seed, rng)
                observed.append(oracle.acquire(cid, observed, seed, method))
            write(out / f'arm_{seed}_{method}.json', {'prefix_sha256': digest(path), 'observations': observed})
            arms[method] = observed
        cases.append({'seed': seed, 'prefix': prefix, 'arms': arms})
    (out / 'acquisitions.jsonl').write_text(''.join(json.dumps(e) + '\n' for e in oracle.events))
    assert len(oracle.events) == 200
    # Full-table scoring starts only after all choices/acquisition logs are saved.
    optimum = min(r['median_ms'] for r in table)
    noise_percent = 100 * statistics.median(r['cv'] for r in table)
    threshold = max(5., 2 * noise_percent)
    scored = []
    for case in cases:
        best = {m: min(r['value_ms'] for r in observations) for m, observations in case['arms'].items()}
        prefix_best = min(r['value_ms'] for r in case['prefix'])
        portfolio = min(best.values())
        headroom = 100 * (portfolio - optimum) / portfolio
        scored.append({'seed': case['seed'], 'prefix_best_ms': prefix_best, 'best_ms': best,
                       'prefix_headroom_percent': 100 * (prefix_best - optimum) / prefix_best,
                       'portfolio_headroom_percent': headroom, 'gate_met': headroom >= threshold,
                       'gain_over_random_percent': {m: 100 * (best['random'] - best[m]) / best['random'] for m in ['nn', 'rf_lcb']}})
    result = {'family': 'javagc', 'workload': 'DaCapo9.12-MR1/Xalan default, fresh Temurin17 adaptation',
              'independent_families': 1, 'seeds': 5, 'arms': 15, 'recorded_acquisitions': 200,
              'total_evaluations_per_arm': 20, 'checkpoint': 10,
              'table_minimum_ms': optimum, 'median_configuration_cv_percent': noise_percent,
              'gate_threshold_percent': threshold, 'gate_case_count': sum(c['gate_met'] for c in scored),
              'gate_passed': sum(c['gate_met'] for c in scored) >= 2, 'cases': scored,
              'runtime_seconds': time.monotonic() - started, 'model_requests': 0,
              'external_spend_usd': 0, 'source_table_sha256': digest(out / 'table.json'),
              'scope': 'Development headroom only; portfolio/oracle non-deployable; no LLM benefit measured.'}
    write(out / 'summary.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
