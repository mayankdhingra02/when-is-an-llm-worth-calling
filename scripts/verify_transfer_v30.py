"""Independent standard-library Decimal scoring and temporal checks; no acquisitions."""
import csv
import json
from datetime import datetime
from decimal import Decimal, getcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
getcontext().prec = 40
def read(path): return json.loads((ROOT/path).read_text(), parse_float=Decimal)
def avg(values): return sum(values, Decimal(0))/len(values)
def check(a, b):
    if abs(a-b) > Decimal('1e-12'): raise ValueError(f'{a} != {b}')

def main():
    result = read('results/v30_transfer/summary.json')
    manifest = read('data/manifest_v30.json')
    frozen = datetime.fromisoformat(read('reports/protocol_v30_transfer.freeze.json')['created_at'])
    journal = [json.loads(s) for s in (ROOT/'results/v30_transfer/acquisitions.jsonl').read_text().splitlines()]
    assert len(journal) == 600 and all(datetime.fromisoformat(e['at']) > frozen for e in journal)
    scores = {}; label_checks = 0; pair_checks = 0; family_checks = 0
    for spec in manifest['datasets']:
        targets = []; seen = set()
        with (ROOT/spec['path']).open(newline='') as stream:
            for row in csv.DictReader(stream, delimiter=spec['delimiter']):
                if any(row[k] != str(v) for k, v in spec['filters'].items()): continue
                features = tuple(Decimal(row[k]) for k in spec['feature_names'])
                if features in seen: continue
                seen.add(features); targets.append(Decimal(row[spec['primary_objective']]))
        assert len(targets) == spec['rows']
        lo, hi = min(targets), max(targets)
        for seed in manifest['seeds']:
            key = f"{spec['id']}_{seed}"
            prefix = read(f'results/v30_transfer/prefixes/{key}.json')
            events = [e for e in journal if e['dataset'] == spec['id'] and e['seed'] == seed]
            assert max(datetime.fromisoformat(e['at']) for e in events if e['arm'] == 'prefix') <= datetime.fromisoformat(prefix['at'])
            assert all(datetime.fromisoformat(e['at']) >= datetime.fromisoformat(prefix['at']) for e in events if e['arm'] != 'prefix')
            for row in [r for r in result['cases'] if r['dataset'] == spec['id'] and r['seed'] == seed]:
                arm = read(f"results/v30_transfer/arms/{key}_{row['arm']}.json")
                state = arm['state']; assert arm['prefix_hash'] == prefix['prefix_hash']
                assert state['labels'] == [[targets[i]] for i in state['ids']]
                label_checks += len(state['ids'])
                target = min(targets[i] for i in state['ids']); loss = (target-lo)/(hi-lo)
                check(target, row['target']); check(loss, row['loss'])
                scores[(spec['id'], seed, row['arm'])] = (target, loss)
    gains = {}
    for row in result['paired_gains']:
        base = scores[(row['dataset'], row['seed'], row['comparator'])]
        seq = scores[(row['dataset'], row['seed'], 'sequential_3nn')]
        values = {'normalized_gain': base[1]-seq[1], 'relative_gain': (base[0]-seq[0])/base[0]}
        for metric, value in values.items(): check(value, row[metric]); pair_checks += 1
        gains.setdefault(row['comparator'], {}).setdefault(row['system_group'], []).append(values)
    for comparator, groups in gains.items():
        saved = result['sequential_comparisons'][comparator]
        for metric in ('normalized_gain', 'relative_gain'):
            means = []
            for group, rows in groups.items():
                value = avg([r[metric] for r in rows]); means.append(value)
                check(value, next(g for g in saved['families'] if g['system_group'] == group)[metric]); family_checks += 1
            check(avg(means), saved['equal_family_'+metric])
        values = [r['normalized_gain'] for rows in groups.values() for r in rows]
        assert saved['wins'] == sum(v > Decimal('1e-12') for v in values)
        assert saved['ties'] == sum(abs(v) <= Decimal('1e-12') for v in values)
        assert saved['losses'] == sum(v < Decimal('-1e-12') for v in values)
    for mode, value in result['equal_family_mean_losses'].items():
        means = []
        for group in result['families']:
            rows = [r for r in result['cases'] if r['arm'] == mode and r['system_group'] == group['system_group']]
            computed = avg([scores[(r['dataset'], r['seed'], mode)][1] for r in rows])
            check(computed, group[mode]); means.append(computed)
        check(avg(means), value)
    print(json.dumps({'verified': True, 'source_label_checks_including_shared_prefixes': label_checks,
        'paired_metric_checks': pair_checks, 'family_gain_checks': family_checks, 'aggregate_gain_checks': 8,
        'win_tie_loss_checks': 12, 'family_loss_checks': 10, 'aggregate_loss_checks': 5,
        'freeze_before_all_600_acquisitions': True, 'saved_prefix_before_all_branches': True,
        'new_model_calls': 0, 'new_objective_acquisitions': 0}, indent=2))

if __name__ == '__main__': main()
