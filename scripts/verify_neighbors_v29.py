"""Independent Decimal source scoring for all V29 comparator/feedback gains."""
import csv, json
from decimal import Decimal, getcontext
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
getcontext().prec = 40


def read(name): return json.loads((ROOT/name).read_text(), parse_float=Decimal)
def avg(xs): return sum(xs, Decimal(0))/len(xs)
def check(a, b):
    if abs(a-b) > Decimal('1e-12'): raise ValueError(f'Mismatch: {a} vs {b}')


def main():
    result = read('results/v29_neighbors/summary.json'); manifest = read('data/manifest_v8.json')
    jobs = read('data/larger_probe_v22.json')['jobs']; metrics = {}; case_gains = {}; counts = 0
    for spec in manifest['datasets']:
        targets = []; seen = set()
        with (ROOT/spec['path']).open(newline='') as f:
            for row in csv.DictReader(f, delimiter=spec['delimiter']):
                if any(row[k] != str(v) for k, v in spec['filters'].items()): continue
                x = tuple(Decimal(row[k]) for k in spec['feature_names'])
                if x in seen: continue
                seen.add(x); targets.append(Decimal(row[spec['primary_objective']]))
        lo, hi = min(targets), max(targets)
        def quality(state):
            assert state['labels'] == [[targets[i]] for i in state['ids']]
            target = min(targets[i] for i in state['ids'])
            return target, (target-lo)/(hi-lo)
        for case in [c for c in manifest['cases'] if c['dataset'] == spec['id']]:
            key = f"{case['dataset']}_{case['seed']}"
            singles = []
            for condition in ('assigned_ids', 'reverse_display', 'reassigned_ids'):
                job = next(j for j in jobs if j['dataset'] == case['dataset'] and j['seed'] == case['seed'] and j['condition'] == condition)
                singles.append(quality(read(f"results/v22_larger/arms/{job['job_id']:02d}_llm.json")['state']))
            bases = {'full_classical': [quality(read(f'results/v6/classical/{key}.json')['arms']['centroid_nominal']['state'])],
                'static_rank': [quality(read(f'results/v8/static_rank/{key}.json')['state'])],
                'centroid_shortlist': [quality(read(f'results/v25_shortlist/arms/{key}.json')['state'])],
                'voting': [quality(read(f'results/v28_consensus/arms/{key}.json')['state'])],
                'single_assigned': [singles[0]], 'single_presentation_mean': singles}
            variants = {}
            for mode in ('batch_3nn', 'sequential_3nn'):
                target, loss = quality(read(f'results/v29_neighbors/arms/{key}_{mode}.json')['state'])
                variants[mode] = (target, loss)
                row = next(r for r in result['cases'] if r['dataset'] == case['dataset'] and r['seed'] == case['seed'] and r['arm'] == mode)
                check(target, row['target']); check(loss, row['loss'])
                for base, vs in bases.items():
                    for metric, value in [('normalized', avg([v[1]-loss for v in vs])), ('relative', avg([(v[0]-target)/v[0] for v in vs]))]:
                        check(value, row[base+'_'+metric+'_gain']); counts += 1
                        metrics.setdefault((mode, base, metric), {}).setdefault(spec['system_group'], []).append(value)
            b, s = variants['batch_3nn'], variants['sequential_3nn']
            case_gains[key] = {'system_group': spec['system_group'], 'normalized_gain': b[1]-s[1], 'relative_gain': (b[0]-s[0])/b[0]}
            saved = next(r for r in result['sequential_minus_batch_cases'] if r['dataset'] == case['dataset'] and r['seed'] == case['seed'])
            for field in ('normalized_gain', 'relative_gain'): check(case_gains[key][field], saved[field])
    for (mode, base, metric), families in metrics.items():
        values = [v for vs in families.values() for v in vs]
        summary = result['modes'][mode]['comparisons'][base][metric]
        check(avg([avg(vs) for vs in families.values()]), summary['equal_family_mean_gain'])
        assert summary['wins'] == sum(v > Decimal('1e-12') for v in values)
        assert summary['ties'] == sum(abs(v) <= Decimal('1e-12') for v in values)
        assert summary['losses'] == sum(v < Decimal('-1e-12') for v in values)
    for metric in ('normalized', 'relative'):
        family_means = [avg([r[metric+'_gain'] for r in case_gains.values() if r['system_group'] == g]) for g in {r['system_group'] for r in case_gains.values()}]
        check(avg(family_means), result['sequential_over_batch'][metric]['equal_family_mean_gain'])
    print(json.dumps({'verified': True, 'decimal_paired_metric_checks': counts, 'aggregate_comparisons_checked': len(metrics),
        'win_tie_loss_count_checks': 3*len(metrics), 'paired_feedback_metrics_checked': 2*len(case_gains),
        'source_labels_checked': True, 'new_model_calls': 0, 'new_objective_acquisitions': 0}, indent=2))


if __name__ == '__main__': main()
