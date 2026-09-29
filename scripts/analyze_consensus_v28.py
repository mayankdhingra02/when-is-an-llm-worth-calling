"""Separate full-table scorer and independent reconstruction of fixed vote arms."""
import argparse, csv, hashlib, json, math, os, sys
from pathlib import Path
from statistics import mean
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT/'src')); os.chdir(ROOT)
os.environ['MPLCONFIGDIR'] = str(ROOT/'.cache/matplotlib')
from escalation.io import read, write, lines
from escalation.config import load_config
from escalation.resources import Resources
from escalation.larger_v22 import authorization_config, require
from verify_reproduction_v26 import observe
OUT = Path('results/v28_consensus')
COMPARATORS = ('full_classical', 'static_rank', 'adaptive_shortlist', 'single_assigned', 'single_presentation_mean')


def calculate():
    for name, h in read('reports/protocol_v28_consensus.freeze.json')['sha256'].items():
        require(hashlib.sha256(Path(name).read_bytes()).hexdigest() == h, 'Changed frozen input: '+name)
    plans = read('data/consensus_v28.json')['cases']; manifest = read('data/manifest_v8.json')
    progress = read(OUT/'progress.json'); require(progress['complete'] and len(progress['arms']) == 15, 'Full completed denominator')
    journal = lines(OUT/'acquisitions.jsonl'); require(len(journal) == 150, '150 new acquisitions')
    rows = []; replayed = 0
    for spec in manifest['datasets']:
        features = []; y = []; source_lines = []; seen = set()
        with Path(spec['path']).open(newline='') as f:
            for line, row in enumerate(csv.DictReader(f, delimiter=spec['delimiter']), 2):
                if any(row[k] != str(v) for k, v in spec['filters'].items()): continue
                x = tuple(float(row[k]) for k in spec['feature_names'])
                if x in seen: continue
                seen.add(x); features.append(x); y.append(float(row[spec['primary_objective']])); source_lines.append(line)
        require(len(y) == spec['rows'] and spec['direction'] == '-', 'Source schema/direction')
        lo, hi = min(y), max(y)
        def terminal(state):
            require(len(state['ids']) == len(set(state['ids'])) == len(state['labels']) == 20, 'Arm budget')
            require(state['ids'][:10] == prefix['ids'] and state['labels'][:10] == prefix['labels'], 'Paired prefix')
            require(state['labels'] == [[y[i]] for i in state['ids']], 'Source labels')
            best = min(y[i] for i in state['ids'])
            return best, (best-lo)/(hi-lo) if hi > lo else 0.
        for plan in [p for p in plans if p['dataset'] == spec['id']]:
            key = f"{plan['dataset']}_{plan['seed']}"
            prefix = read(f'results/v6/prefixes/{key}.json')['state']
            state = json.loads(json.dumps(prefix))
            # Independent per-candidate membership sums, not production selector.
            ranked = sorted(enumerate(plan['pool']), key=lambda pair: (-sum(pair[1] in ballot for ballot in plan['ballots']), pair[0]))
            selected = [row for position, row in ranked[:10]]
            require(selected == plan['selected'], 'Independent vote selection')
            events = [e for e in journal if e['dataset'] == plan['dataset'] and e['seed'] == plan['seed']]
            require(len(events) == 10, 'Per-arm acquisition denominator')
            for row, event in zip(selected, events):
                require(event['row_id'] == row and event['source_line'] == source_lines[row] and float(event['raw_target']) == y[row], 'Journal/source label identity')
                observe(state, row, y[row], '-'); replayed += 1
            arm = read(OUT/'arms'/f'{key}.json')
            require(state == arm['state'] and arm['actual_new_accesses'] == 10 and arm['logical_evaluations'] == 20, 'Independent arm replay')
            e_target, e_loss = terminal(state)
            single = [terminal(read(f"results/v22_larger/arms/{r['job_id']:02d}_llm.json")['state']) for r in plan['sources']]
            base_states = {
                'full_classical': read(f'results/v6/classical/{key}.json')['arms']['centroid_nominal']['state'],
                'static_rank': read(f'results/v8/static_rank/{key}.json')['state'],
                'adaptive_shortlist': read(f'results/v25_shortlist/arms/{key}.json')['state']}
            bases = {b: [terminal(s)] for b, s in base_states.items()}
            bases.update(single_assigned=[single[0]], single_presentation_mean=single)
            record = {k: plan[k] for k in ('dataset', 'seed', 'system_group')}
            record.update(ensemble_loss=e_loss, ensemble_target=e_target,
                best_observed_single_loss=min(v[1] for v in single), worst_observed_single_loss=max(v[1] for v in single),
                strictly_beats_best_observed_single=e_loss < min(v[1] for v in single)-1e-12,
                ties_require_classical_rank=plan['tie_break_decides_membership'],
                equals_any_component_set=any(set(selected) == set(b) for b in plan['ballots']),
                equals_static_rank_set=set(selected) == set(plan['pool'][:10]),
                branch_seconds=arm['branch_seconds'])
            for b, values in bases.items():
                record[b+'_loss'] = mean(v[1] for v in values)
                record[b+'_normalized_gain'] = mean(v[1]-e_loss for v in values)
                record[b+'_relative_gain'] = mean((v[0]-e_target)/v[0] for v in values)
            rows.append(record)
    require(len(rows) == 15 and replayed == 150, 'Complete experiment')
    metrics = ['ensemble_loss'] + [b+s for b in COMPARATORS for s in ('_loss', '_normalized_gain', '_relative_gain')]
    families = [{'system_group': g, **{k: mean(r[k] for r in rows if r['system_group'] == g) for k in metrics}}
                for g in sorted({r['system_group'] for r in rows})]
    comparisons = {b: {'mean_normalized_gain': mean(f[b+'_normalized_gain'] for f in families),
        'mean_relative_gain': mean(f[b+'_relative_gain'] for f in families),
        'wins': sum(r[b+'_normalized_gain'] > 1e-12 for r in rows),
        'ties': sum(abs(r[b+'_normalized_gain']) <= 1e-12 for r in rows),
        'losses': sum(r[b+'_normalized_gain'] < -1e-12 for r in rows)} for b in COMPARATORS}
    usage = {}
    for scenario in ('ensemble', 'single_assigned', 'single_presentation_mean'):
        usage[scenario] = {'logical_objective_evaluations': 300, 'model_requests': 45 if scenario == 'ensemble' else 15}
        for k in ('input_tokens', 'output_tokens', 'wall_seconds'):
            usage[scenario][k] = sum(sum(r[k] for r in p['sources']) if scenario == 'ensemble' else
                p['sources'][0][k] if scenario == 'single_assigned' else mean(r[k] for r in p['sources']) for p in plans)
    return {'scope': 'Exploratory cached-real-response hybrid voting; no fresh inference or held-out evaluation',
        'complete': True, 'cases': rows, 'families': families, 'comparisons': comparisons,
        'ensemble_mean_loss': mean(f['ensemble_loss'] for f in families),
        'strictly_beats_best_observed_single_cases': sum(r['strictly_beats_best_observed_single'] for r in rows),
        'boundary_tie_cases': sum(r['ties_require_classical_rank'] for r in rows),
        'equals_component_set_cases': sum(r['equals_any_component_set'] for r in rows),
        'equals_static_rank_set_cases': sum(r['equals_static_rank_set'] for r in rows),
        'new_objective_acquisitions': 150, 'new_model_calls': 0, 'independent_journal_entries_verified': replayed,
        'deployment_usage_scenarios': usage,
        'usage_caveat': 'Historical observed request usage, not fresh measured ensemble-service latency; excludes startup, tie-break/control and objective execution overhead. All research collection retained separately.'}


def render(result):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fields = ['static_rank_loss', 'single_assigned_loss', 'single_presentation_mean_loss', 'ensemble_loss']
    labels = ['Static\nrank', 'One call\nassigned IDs', 'One call\npresentation mean', 'Three-call\nvoting']
    fig, axes = plt.subplots(1, 3, figsize=(11, 4.3))
    for ax, family in zip(axes, result['families']):
        ax.bar(range(4), [family[f] for f in fields], color=['#7b8b96', '#be9871', '#b55b3d', '#176b93'])
        ax.set_xticks(range(4), labels, fontsize=8, rotation=15); ax.set_title(family['system_group'])
        ax.set_ylabel('Normalized loss (lower is better)')
    fig.suptitle('V28: fixed voting over three saved real LLM presentations')
    fig.text(.5, .015, 'All arms: 20 objective evaluations. Voting scenario uses 3 calls; tie-break uses classical rank. Separate panel scales.', ha='center', fontsize=8)
    fig.tight_layout(rect=[0, .06, 1, .95])
    for ext in ('png', 'svg'): fig.savefig(OUT/('comparison.'+ext), dpi=180)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--verify-only', action='store_true'); args = parser.parse_args()
    if args.verify_only:
        require(calculate() == read(OUT/'summary.json'), 'Saved summary differs')
        print('15 consensus arms,150 labels,all comparisons/usage independently replayed.'); return
    require(not (OUT/'summary.json').exists(), 'Preserve completed analysis')
    cfg = authorization_config(load_config('configs/followup_v3.yaml'), read('configs/authorization_v22.json'))
    before = read('artifacts/resource_ledger_v2.json')
    with Resources(cfg, 'artifacts/resource_ledger_v2.json') as resource:
        resource.check(); result = calculate(); write(OUT/'summary.json', result)
        with (OUT/'cases.csv').open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(result['cases'][0])); writer.writeheader(); writer.writerows(result['cases'])
        render(result); resource.check()
    after = read('artifacts/resource_ledger_v2.json')
    write('artifacts/study_v28/analysis_accounting.json', {'charged_seconds': after['experiment_seconds']-before['experiment_seconds'],
        'cumulative_seconds': after['experiment_seconds'], 'remaining_seconds': 3600-after['experiment_seconds'],
        'new_objective_acquisitions': 0, 'new_model_calls': 0, 'active_since': after['active_since']})
    print(json.dumps({k: v for k, v in result.items() if k not in ('cases', 'families')}, indent=2))


if __name__ == '__main__': main()
