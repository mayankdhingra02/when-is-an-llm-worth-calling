"""Independent Decimal verification from saved arm targets; read-only."""
import json
from decimal import Decimal, getcontext
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
getcontext().prec = 40


def read(path):
    return json.loads((ROOT/path).read_text(), parse_float=Decimal)


def average(values):
    return sum(values, Decimal(0))/len(values)


def check(a, b):
    if abs(a-b) > Decimal('1e-12'):
        raise ValueError(f'Decimal mismatch: {a} versus {b}')


def main():
    saved = read('results/v27_metric_sensitivity/summary.json')
    groups = {}
    for row in saved['comparisons']:
        key = f"{row['dataset']}_{row['seed']}"
        if row['baseline'] == 'full_classical':
            baseline = read(f'results/v6/classical/{key}.json')['arms']['centroid_nominal']['state']
        elif row['baseline'] == 'static_rank':
            baseline = read(f'results/v8/static_rank/{key}.json')['state']
        elif row['baseline'] == 'adaptive_shortlist':
            baseline = read(f'results/v25_shortlist/arms/{key}.json')['state']
        else:
            raise ValueError('Unknown baseline')
        llm = read(f"results/v22_larger/arms/{row['job_id']:02d}_llm.json")['state']
        b, c = [min(y[0] for y in state['labels']) for state in (baseline, llm)]
        gain = Decimal(1) - c/b
        check(b, row['baseline_target']); check(c, row['llm_target']); check(gain, row['relative_gain'])
        groups.setdefault(row['baseline'], {}).setdefault(row['system_group'], {}).setdefault(key, []).append(gain)
    predicate_checks = 0
    for baseline, families in groups.items():
        summary = saved['baselines'][baseline]
        means = {g: average([average(v) for v in seeds.values()]) for g, seeds in families.items()}
        check(average(list(means.values())), summary['equal_family_mean_relative_gain'])
        all_cases = [v for seeds in families.values() for v in seeds.values()]
        check(median([average(v) for v in all_cases]), summary['case_median_relative_gain'])
        for row in summary['families']:
            check(means[row['system_group']], row['mean_relative_gain'])
        for row in summary['leave_one_family_out']:
            check(average([v for g, v in means.items() if g != row['excluded_family']]), row['mean_relative_gain'])
        for row in summary['margins']:
            m, tolerance = row['margin_fraction'], Decimal('1e-12')
            expected = {
                'help_any_presentation': sum(any(v > m+tolerance for v in values) for values in all_cases),
                'help_all_presentations': sum(all(v > m+tolerance for v in values) for values in all_cases),
                'harm_any_presentation': sum(any(v < -m-tolerance for v in values) for values in all_cases),
                'harm_all_presentations': sum(all(v < -m-tolerance for v in values) for values in all_cases)}
            for k, value in expected.items():
                if row[k] != value:
                    raise ValueError('Margin predicate mismatch')
                predicate_checks += 1
    print(json.dumps({'verified': True, 'decimal_comparisons': len(saved['comparisons']),
                      'family_means': sum(len(f) for f in groups.values()),
                      'aggregate_means': len(groups), 'leave_one_family_out_means': 9,
                      'margin_count_checks': predicate_checks, 'new_model_calls': 0,
                      'new_objective_acquisitions': 0}, indent=2))


if __name__ == '__main__':
    main()
