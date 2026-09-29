"""Read-only, standard-library independent Fraction check of measured V38 scores.

The frozen analyzer separately verifies tokenizer/model provenance. This checker
does not import study code, acquire objectives, fit policies, or call a model.
"""
import csv
import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


def main():
    manifest = read('data/arithmetic_v36.json')
    summary = read('results/v38_size_prompt/summary.json')
    sources = {}
    for d in manifest['datasets']:
        values, seen = [], set()
        with (ROOT / d['path']).open(newline='') as stream:
            for row in csv.DictReader(stream, delimiter=d['delimiter']):
                if any(row[k] != str(v) for k, v in d['filters'].items()):
                    continue
                features = tuple(F(row[n]) for n in d['feature_names'])
                if features not in seen:
                    seen.add(features)
                    values.append((F(row['performance']), F(row['size'])))
        assert len(values) == d['rows']
        sources[d['id']] = values
    gains, diagnostics = {}, []
    for record in summary['records']:
        d, seed, condition = (record[k] for k in ('dataset', 'seed', 'condition'))
        key = f'{d}_{seed}'
        case = next(c for c in manifest['cases'] if (c['dataset'], c['seed']) == (d, seed))
        prefix, values = case['prefix'], sources[d]
        cap = F(prefix['size_cap'])
        new = read(f"results/v38_size_prompt/arms/{record['job_id']:02d}.json")
        old = read(f'results/v34_constrained/arms/{key}_cached_llm_{condition}.json')
        assert new['ids'][:10] == old['ids'][:10] == prefix['ids']
        assert len(new['ids']) == len(set(new['ids'])) == 20
        assert [(F(t), F(s)) for t, s in new['labels']] == [values[i] for i in new['ids']]

        def best(arm):
            return min(values[i][0] for i in arm['ids'] if values[i][1] <= cap)

        current = best(new)
        assert current == F(record['best_runtime']) == F(new['best_runtime'])
        for comparison in summary['comparisons']:
            if (comparison['dataset'], comparison['seed'], comparison['condition']) != (d, seed, condition):
                continue
            base = comparison['baseline']
            if base == 'runtime_only_llm':
                other = old
            elif base.startswith('exact_'):
                other = read(f'results/v36_arithmetic/arms/{key}_{base[6:]}.json')
            else:
                other = read(f'results/v34_constrained/arms/{key}_{base}.json')
            assert other['ids'][:10] == prefix['ids']
            gain = (best(other) - current) / best(other)
            assert abs(float(gain) - comparison['relative_gain']) < 1e-15
            assert best(other) == F(comparison['baseline_runtime'])
            gains[(d, seed, condition, base)] = gain
        diagnostics.append({
            'dataset': d, 'seed': seed, 'condition': condition,
            'selected_set_changed': set(new['ids'][10:]) != set(old['ids'][10:]),
            'new_infeasible': sum(values[i][1] > cap for i in new['ids'][10:]),
            'old_infeasible': sum(values[i][1] > cap for i in old['ids'][10:]),
            'new_unconstrained_best_infeasible': values[min(new['ids'], key=lambda i: values[i][0])][1] > cap,
            'old_unconstrained_best_infeasible': values[min(old['ids'], key=lambda i: values[i][0])][1] > cap,
        })
    assert len(diagnostics) == 30 and len(gains) == 150
    for s in summary['summaries']:
        rr = [v for (d, seed, c, b), v in gains.items() if (c, b) == (s['condition'], s['baseline'])]
        assert len(rr) == 10
        assert abs(float(sum(rr) / 10) - s['equal_family_mean_gain']) < 1e-15
        assert (sum(v > 0 for v in rr), sum(v == 0 for v in rr), sum(v < 0 for v in rr)) == (s['wins'], s['ties'], s['harms'])
    print(json.dumps({'verified_source_bound_arms': 30, 'verified_fraction_comparisons': 150,
                      'verified_summaries': 15, 'new_model_calls': 0, 'new_acquisitions': 0,
                      'diagnostics': diagnostics}, indent=2))


if __name__ == '__main__':
    main()
