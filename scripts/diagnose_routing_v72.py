"""Post-hoc finite-policy bound on saved outcomes, not a deployable controller."""
import csv
import itertools
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = ROOT/'results/v72_rocksdb_paired'
    summary = json.loads((ROOT/'results/v72_rocksdb_analysis/summary.json').read_text())
    costs = [json.loads(line) for line in (source/'selection_costs.jsonl').read_text().splitlines()]
    seeds = [11, 23, 37, 53, 71]
    quality = {(r['seed'], r['method']): r['confirmed_median_ms'] for r in summary['rows']}
    overhead = {(s, m): sum(c['seconds'] for c in costs if c['seed']==s and c['arm']==m)
                for s in seeds for m in ['rf_lcb','llm']}
    never = statistics.mean(quality[s,'rf_lcb'] for s in seeds)
    rows = []
    for mask in itertools.product([0,1], repeat=5):
        selected = ['llm' if value else 'rf_lcb' for value in mask]
        rows.append({'mask_in_seed_order': ''.join(map(str, mask)), 'escalated_cases': sum(mask),
                     'mean_confirmed_ms': statistics.mean(quality[s,m] for s,m in zip(seeds,selected)),
                     'sum_observed_decision_seconds_selected_branches': sum(overhead[s,m] for s,m in zip(seeds,selected))})
    counts = []
    for k in range(6):
        subset = [r for r in rows if r['escalated_cases']==k]
        counts.append({'escalated_cases': k, 'number_of_masks': len(subset),
            'uniform_random_mask_expected_mean_ms': statistics.mean(r['mean_confirmed_ms'] for r in subset),
            'hindsight_best_mean_ms_non_deployable': min(r['mean_confirmed_ms'] for r in subset),
            'hindsight_worst_mean_ms_non_deployable': max(r['mean_confirmed_ms'] for r in subset),
            'uniform_random_mask_expected_decision_seconds': statistics.mean(r['sum_observed_decision_seconds_selected_branches'] for r in subset)})
    result = {'scope': 'Post-hoc descriptive enumeration of32 masks on five observed seeds from ONE family; no controller trained or evaluated',
        'never_mean_ms': never, 'strictly_worse_masks_than_never': sum(r['mean_confirmed_ms']>never for r in rows),
        'equal_masks_to_never': sum(r['mean_confirmed_ms']==never for r in rows), 'fixed_rate_diagnostics': counts,
        'cost_caveat': 'Selected-branch observed decision time only; excludes physical objective acquisition, prefix, controller and startup. Not actual total collection cost or verified production cost.',
        'uncertainty_caveat': 'Finite observed medians only; three confirmations and one family cannot establish true dominance or generalization.'}
    out = ROOT/'results/v72_routing_diagnostic'; out.mkdir(exist_ok=False)
    (out/'summary.json').write_text(json.dumps(result, indent=2)+'\n')
    with (out/'masks.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
