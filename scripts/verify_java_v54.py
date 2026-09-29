"""Independent audit of physical logs, charged sources and classical decisions."""
import collections
import hashlib
import itertools
import json
import random
import re
import statistics
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestRegressor
ROOT = Path(__file__).resolve().parents[1]


def read(path): return json.loads((ROOT / path).read_text())
def lines(path): return [json.loads(s) for s in (ROOT / path).read_text().splitlines()]
def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(65536), b''): h.update(b)
    return h.hexdigest()


def main():
    for seal in ['reports/protocol_v53_java_feasibility.freeze.json', 'reports/protocol_v54_java_screen.freeze.json']:
        for p, expected in read(seal)['files'].items(): assert sha(ROOT / p) == expected, p
    physical = 'results/v54_java_physical/'
    rows = lines(physical + 'trials.jsonl'); starts = lines(physical + 'starts.jsonl')
    schedule = read(physical + 'schedule.json')
    assert len(rows) == len(starts) == len(schedule) == 144
    grid = list(itertools.product([1, 2, 4, 8], [1, 2, 4, 8], [2, 4, 8]))
    expected_schedule = []
    for r in range(3):
        order = list(range(48)); random.Random(54000 + r).shuffle(order)
        expected_schedule.extend(order)
    measured = collections.defaultdict(list)
    for i, (r, start, planned) in enumerate(zip(rows, starts, schedule)):
        assert r['trial'] == start['trial'] == planned['trial'] == i
        assert r['config_id'] == expected_schedule[i] and r['round'] == i // 48
        assert r['configuration'] == list(grid[r['config_id']])
        assert r['status'] == 'passed' and r['exit_code'] == 0 and r['termination_reason'] is None
        assert r['output_bytes'] == 23901000 and r['output_sha256'] == '4c72b92f00eca08f8bda35e2734124f92fbfd01884c3bf259f2f5d005e98bddb'
        log = ROOT / physical / f'trial_{i}.log'
        assert sha(log) == r['log_sha256']
        text = log.read_text()
        assert re.findall(r'xalan PASSED in (\d+) msec', text) == [str(r['final_ms'])]
        assert re.findall(r'completed warmup 1 in (\d+) msec', text) == [str(r['warmup_ms'])]
        validation = (ROOT / physical / f'validation_{i}.txt').read_text()
        assert validation.count('0xd31deba48b76595f822b43217afefd6fec3aefb9') == 2
        assert validation.count('0xda39a3ee5e6b4b0d3255bfef95601890afd80709') == 2
        assert r['command'] == start['command']
        assert not set(r['command']) & {'--no-validation', '--ignore-validation', '--no-digest-output'}
        for flag, val in zip(['-XX:ParallelGCThreads=', '-XX:NewRatio=', '-XX:SurvivorRatio='], grid[r['config_id']]):
            assert flag + str(val) in r['command']
        for flag, value in [('-t', '1'), ('-n', '2'), ('-s', 'default')]:
            assert r['command'][r['command'].index(flag) + 1] == value
        measured[r['config_id']].append(r['final_ms'])
    folder = 'results/v54_java_screen/'
    table = read(folder + 'table.json'); seal = read(folder + 'table_seal.json')
    assert sha(ROOT / folder / 'table.json') == seal['sha256']
    assert sha(ROOT / physical / 'trials.jsonl') == seal['physical_trials_sha256']
    for r in table:
        assert len(measured[r['config_id']]) == 3
        assert statistics.median(measured[r['config_id']]) == r['median_ms']
    events = lines(folder + 'acquisitions.jsonl'); assert len(events) == 200
    seen = set(); steps = 0
    x = np.array([[np.log2(a)/3, np.log2(b)/3, (np.log2(c)-1)/2] for a,b,c in grid])
    def expected_choice(obs, method, seed, rng):
        ids = [a['config_id'] for a in obs]; candidates = [c for c in range(48) if c not in ids]
        if method == 'random': return rng.choice(candidates)
        y = np.array([a['value_ms'] for a in obs])
        if method == 'nn':
            values = []
            for c in candidates:
                nearest = sorted(range(len(ids)), key=lambda j: float(np.abs(x[c] - x[ids[j]]).mean()))[:3]
                values.append(float(y[nearest].mean()))
        else:
            fit = RandomForestRegressor(n_estimators=64, min_samples_leaf=1, max_features=1.,
                                        bootstrap=True, n_jobs=1, random_state=seed*100 + len(obs))
            fit.fit(x[ids], y)
            values = []
            # Batch tree prediction matches sklearn input precision; no hidden labels.
            predictions = np.array([t.predict(x[candidates]) for t in fit.estimators_])
            values = predictions.mean(0) - predictions.std(0)
        return candidates[min(range(len(candidates)), key=lambda i: values[i])]
    for seed in [11,23,37,53,71]:
        prefix = read(folder + f'prefix_{seed}.json'); assert len(prefix) == 10
        assert [o['config_id'] for o in prefix[:4]] == random.Random(seed).sample(range(48),4)
        for n in range(4,10):
            assert prefix[n]['config_id'] == expected_choice(prefix[:n], 'nn', seed, None); steps += 1
        for method in ['random','nn','rf_lcb']:
            arm = read(folder + f'arm_{seed}_{method}.json'); obs = arm['observations']
            assert obs[:10] == prefix and len(obs) == len({r['config_id'] for r in obs}) == 20
            assert arm['prefix_sha256'] == sha(ROOT / folder / f'prefix_{seed}.json')
            rng = random.Random(seed+1000)
            for n in range(10,20):
                assert obs[n]['config_id'] == expected_choice(obs[:n],method,seed,rng); steps += 1
            for n, o in enumerate(obs):
                e = events[o['source_event_id']]; seen.add(e['event_id'])
                assert e['case'] == seed and e['arm'] == ('prefix' if n < 10 else method)
                assert e['inclusive_step'] == n+1 and e['config_id'] == o['config_id']
                assert e['value_ms'] == o['value_ms'] == table[o['config_id']]['median_ms']
    assert seen == set(range(200))
    summary = read(folder + 'summary.json')
    optimum = min(r['median_ms'] for r in table)
    noise = 100 * statistics.median(statistics.stdev(v)/statistics.mean(v) for v in measured.values())
    threshold = max(5., 2*noise)
    assert summary['table_minimum_ms'] == optimum
    assert summary['gate_threshold_percent'] == threshold
    gates = 0
    for c in summary['cases']:
        seed = c['seed']
        best = {m: min(o['value_ms'] for o in read(folder + f'arm_{seed}_{m}.json')['observations'])
                for m in ['random','nn','rf_lcb']}
        assert c['best_ms'] == best
        value = min(best.values())
        headroom = 100*(value-optimum)/value
        assert c['portfolio_headroom_percent'] == headroom
        assert c['gate_met'] == (headroom >= threshold)
        gates += headroom >= threshold
    assert summary['gate_case_count'] == gates and summary['gate_passed'] == (gates >= 2)
    print(f'PASS:144 physical trials/288 iterations, all output and log receipts,200 charged vectors,15 arms,180 replayed choices ({steps}).')


if __name__ == '__main__': main()
