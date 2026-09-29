"""Replay saved acquired targets under two declared metrics; no new acquisition."""
import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
from statistics import mean
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
os.chdir(ROOT)
os.environ['MPLCONFIGDIR'] = str(ROOT/'.cache/matplotlib')
from escalation.io import read, write
from escalation.config import load_config
from escalation.larger_v22 import authorization_config, require
from escalation.resources import Resources
from escalation.metric_sensitivity_v27 import relative_gain, summarize

OUT = Path('results/v27_metric_sensitivity')
BASELINES = {'full_classical': 'full_classical_loss', 'static_rank': 'static_rank_loss',
             'adaptive_shortlist': 'restricted_loss'}


def terminal(state, prefix):
    require(len(state['ids']) == len(set(state['ids'])) == len(state['labels']) == 20, 'Arm budget')
    require(state['ids'][:10] == prefix['ids'] and state['labels'][:10] == prefix['labels'], 'Shared prefix')
    require(all(len(y) == 1 and math.isfinite(y[0]) and y[0] > 0 for y in state['labels']), 'Positive scalar targets')
    return min(y[0] for y in state['labels'])


def calculate():
    for name, digest in read('reports/protocol_v27_metric_sensitivity.freeze.json')['sha256'].items():
        require(hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest, 'Frozen input: '+name)
    manifest = read('data/manifest_v8.json')
    old = read('results/v25_shortlist/summary.json')['cases']
    records = read('results/v22_larger/summary.json')['records']
    require(len(old) == 15 and len(manifest['cases']) == 15, 'Fifteen cases')
    require(len(manifest['datasets']) == 3 and all(d['direction'] == '-' for d in manifest['datasets']), 'Three minimization systems')
    by_baseline = {b: [] for b in BASELINES}
    comparisons = []
    for c in old:
        key = f"{c['dataset']}_{c['seed']}"
        prefix = read(f'results/v6/prefixes/{key}.json')['state']
        require(len(prefix['ids']) == len(prefix['labels']) == 10, 'Ten-prefix')
        states = {
            'full_classical': read(f'results/v6/classical/{key}.json')['arms']['centroid_nominal']['state'],
            'static_rank': read(f'results/v8/static_rank/{key}.json')['state'],
            'adaptive_shortlist': read(f'results/v25_shortlist/arms/{key}.json')['state']}
        presentations = [r for r in records if r['dataset'] == c['dataset'] and r['seed'] == c['seed'] and r['condition'] != 'assigned_ids_repeat']
        require(len(presentations) == 3 and {r['condition'] for r in presentations} == {'assigned_ids', 'reverse_display', 'reassigned_ids'}, 'Three unique presentations')
        require(math.isclose(mean(r['llm_loss'] for r in presentations), c['llm_mean_loss'], abs_tol=1e-12), 'Prior efficacy mean')
        for b, field in BASELINES.items():
            target = terminal(states[b], prefix)
            gains = []
            for r in presentations:
                candidate = terminal(read(f"results/v22_larger/arms/{r['job_id']:02d}_llm.json")['state'], prefix)
                gain = relative_gain(target, candidate)
                normalized_gain = c[field] - r['llm_loss']
                require((gain > 1e-12) == (normalized_gain > 1e-12) and (gain < -1e-12) == (normalized_gain < -1e-12), 'Individual gain sign mismatch')
                gains.append(gain)
                comparisons.append({'baseline': b, 'dataset': c['dataset'], 'system_group': c['system_group'],
                                    'seed': c['seed'], 'condition': r['condition'], 'job_id': r['job_id'],
                                    'baseline_target': target, 'llm_target': candidate,
                                    'relative_gain': gain, 'normalized_gain': normalized_gain})
            by_baseline[b].append({k: c[k] for k in ('dataset', 'system_group', 'seed')} |
                                 {'relative_gains': gains, 'mean_normalized_gain': c[field] - c['llm_mean_loss']})
    require(len(comparisons) == 135, 'Complete comparison denominator')
    summaries = {b: summarize(rows) for b, rows in by_baseline.items()}
    require(all(len(s['families']) == 3 and all(g['cases'] == 5 for g in s['families']) for s in summaries.values()), 'Family/seed denominator')
    return {'scope': 'Exploratory metric sensitivity on exposed development systems; no new efficacy trial',
            'comparisons': comparisons, 'baselines': summaries,
            'new_model_calls': 0, 'new_objective_acquisitions': 0,
            'interpretation': 'Relative reductions in recorded primary target, not measured end-to-end runtime savings; no application utility established'}


def render(result):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(11, 4.4))
    names = ['Original classical', 'Static shortlist', 'Adaptive shortlist']
    for ax, (b, s), name in zip(axes, result['baselines'].items(), names):
        labels = [r['system_group'].replace('_family', '') for r in s['families']] + ['Equal-family\nmean']
        values = [r['mean_relative_gain']*100 for r in s['families']] + [s['equal_family_mean_relative_gain']*100]
        ax.bar(range(4), values, color=['#176b93' if v >= 0 else '#b55b3d' for v in values])
        ax.axhline(0, color='black', linewidth=.7)
        ax.set_xticks(range(4), labels, fontsize=8, rotation=20)
        ax.set_title('LLM versus '+name, fontsize=10)
        ax.set_ylabel('Relative recorded-target reduction (%)')
        ax.grid(axis='y', alpha=.15)
    fig.suptitle('V27: does the comparison depend on the quality metric?')
    fig.text(.5, .018, 'Positive favors LLM. Three exposed families; five seeds; three presentations. Separate panel scales.', ha='center', fontsize=8)
    fig.tight_layout(rect=[0, .06, 1, .94])
    for ext in ['png', 'svg']:
        fig.savefig(OUT/('relative_gain.'+ext), dpi=180)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    if args.verify_only:
        require(calculate() == read(OUT/'summary.json'), 'Saved summary differs')
        print('All 135 relative/normalized comparisons and summaries replayed.')
        return
    require(not OUT.exists(), 'Preserve started/completed V27 result')
    before = read('artifacts/resource_ledger_v2.json')
    cfg = authorization_config(load_config('configs/followup_v3.yaml'), read('configs/authorization_v22.json'))
    with Resources(cfg, 'artifacts/resource_ledger_v2.json') as resource:
        require(resource.remaining() > 30, 'Analysis reserve')
        result = calculate()
        write(OUT/'summary.json', result)
        with (OUT/'comparisons.csv').open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(result['comparisons'][0]))
            writer.writeheader(); writer.writerows(result['comparisons'])
        render(result)
        resource.check()
    after = read('artifacts/resource_ledger_v2.json')
    require(after['requests'] == before['requests'] == 200, 'No inference allowed')
    write('artifacts/study_v27/accounting.json', {
        'charged_seconds': after['experiment_seconds'] - before['experiment_seconds'],
        'cumulative_seconds': after['experiment_seconds'], 'remaining_seconds': 3600-after['experiment_seconds'],
        'new_model_calls': 0, 'new_objective_acquisitions': 0, 'new_physical_trials': 0,
        'external_spend_usd': 0, 'active_since': after['active_since']})
    print(json.dumps({b: {k: v for k, v in s.items() if k != 'cases'} for b, s in result['baselines'].items()}, indent=2))


if __name__ == '__main__':
    main()
