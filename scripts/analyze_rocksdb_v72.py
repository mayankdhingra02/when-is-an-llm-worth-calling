"""Fixed descriptive analysis of paired live continuations; no router fitting."""
import csv
import json
import os
import statistics
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT/'.cache/matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    source = ROOT/'results/v72_rocksdb_paired'
    summary = json.loads((source/'summary.json').read_text())
    assert summary['complete'], 'Do not silently drop incomplete intended cases'
    out = ROOT/'results/v72_rocksdb_analysis'; out.mkdir(exist_ok=False)
    methods = ['rf_lcb', 'domain_prior', 'llm']; rows = []; comparisons = []
    for case in summary['cases']:
        medians = {}
        for method in methods:
            values = [o['value_ms'] for o in case['confirmation'][method]]
            median = statistics.median(values); medians[method] = median
            cid = case['selected_config_ids'][method]
            index = next(i for i, o in enumerate(case['arms'][method]) if o['config_id'] == cid)
            origin = 'historical_prefix' if index < 10 else method
            if method == 'llm' and index >= 10 and index-9 in case['fallback_steps']: origin = 'rf_fallback'
            rows.append({'seed': case['seed'], 'method': method, 'selected_config_id': cid,
                'selected_origin': origin, 'confirmation_ms': values, 'confirmed_median_ms': median,
                'confirmation_cv': statistics.stdev(values)/statistics.mean(values), 'inclusive_budget': 20})
        for control in ['rf_lcb', 'domain_prior']:
            pct = 100*(medians[control]-medians['llm'])/medians[control]
            same = case['selected_config_ids'][control] == case['selected_config_ids']['llm']
            comparisons.append({'seed': case['seed'], 'control': control, 'llm_improvement_percent': pct,
                'same_configuration': same, 'gain_above_5pct_different_setting': pct > 5 and not same,
                'harm_above_5pct_different_setting': pct < -5 and not same})
    decisions = [json.loads(p.read_text()) for p in source.glob('v72_seed*/decision.json')]
    usage = {}
    for key in ['tokens_predicted', 'tokens_evaluated']:
        values = [d.get('usage', {}).get(key) if d.get('usage') is not None else None for d in decisions]
        usage[key] = {'observed_sum': sum(v for v in values if v is not None), 'unknown_requests': sum(v is None for v in values)}
    costs = [json.loads(line) for line in (source/'selection_costs.jsonl').read_text().splitlines()]
    result = {'scope': 'Exploratory one-family paired study; no held-out or router claim',
        'rows': rows, 'comparisons': comparisons, 'mean_confirmed_median_ms': {m: statistics.mean(r['confirmed_median_ms'] for r in rows if r['method']==m) for m in methods},
        'observed_usage': usage, 'decision_seconds_by_method': {m: sum(c['seconds'] for c in costs if c['arm']==m) for m in methods},
        'request_seconds': sum(d['wall_seconds'] for d in decisions), 'valid_model_responses': sum(d['valid'] for d in decisions),
        'median_confirmation_cv': statistics.median(r['confirmation_cv'] for r in rows),
        'actual_new_physical_evaluations': 150, 'historical_shared_prefix_evaluations': 50,
        'logical_evaluations': 300, 'independent_families': 1, 'ledger': summary['ledger'],
        'hindsight_oracle_mean_ms_non_deployable': statistics.mean(min(r['confirmed_median_ms'] for r in rows if r['seed']==seed and r['method'] in ['rf_lcb','llm']) for seed in [11,23,37,53,71])}
    (out/'summary.json').write_text(json.dumps(result, indent=2)+'\n')
    with (out/'incumbents.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    labels = {'rf_lcb': 'RF-LCB', 'domain_prior': 'Cheap domain prior', 'llm': 'Local LLM (+ fallback if needed)'}
    for offset, method in enumerate(methods):
        subset = [r for r in rows if r['method']==method]
        ax.errorbar([i+(offset-1)*.19 for i in range(5)], [r['confirmed_median_ms'] for r in subset],
            yerr=[[r['confirmed_median_ms']-min(r['confirmation_ms']) for r in subset], [max(r['confirmation_ms'])-r['confirmed_median_ms'] for r in subset]],
            fmt='o', capsize=3, label=labels[method])
    ax.set_xticks(range(5), [11,23,37,53,71]); ax.set_xlabel('Seed (one software family)')
    ax.set_ylabel('Confirmed verified-loop time (ms)'); ax.set_title('V72: paired continuations, median and range of three confirmations')
    ax.legend(frameon=False); ax.spines[['top','right']].set_visible(False)
    fig.text(.5,.01,'Exploratory. Ranges are not confidence intervals. 10 shared prefix + 7 search + 3 confirmation.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.04,1,1]); fig.savefig(out/'paired_incumbents.png',dpi=160); fig.savefig(out/'paired_incumbents.svg'); plt.close(fig)
    print(json.dumps({k:v for k,v in result.items() if k not in ['rows','comparisons','ledger']}, indent=2))


if __name__ == '__main__': main()
