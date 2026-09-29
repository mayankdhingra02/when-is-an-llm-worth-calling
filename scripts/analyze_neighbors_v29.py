"""Separate source scorer; independent vectorized distance/recommendation replay."""
import argparse, csv, hashlib, json, os, sys
from decimal import Decimal, localcontext
from pathlib import Path
from statistics import mean
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT/'src')); os.chdir(ROOT)
os.environ['MPLCONFIGDIR'] = str(ROOT/'.cache/matplotlib')
from escalation.io import read, write, lines
from escalation.config import load_config
from escalation.resources import Resources
from escalation.larger_v22 import authorization_config, require
from verify_reproduction_v26 import observe
OUT = Path('results/v29_neighbors')
MODES = ('batch_3nn', 'sequential_3nn')
BASES = ('full_classical', 'static_rank', 'centroid_shortlist', 'single_assigned', 'single_presentation_mean', 'voting')


def reference_rank(x, state, pool):
    available = [i for i in state['order'] if i in pool and i not in state['ids']]
    distances = (x[available, None, :] != x[state['ids']][None, :, :]).sum(axis=2)
    neighbors = np.argsort(distances, axis=1, kind='stable')[:, :3]
    with localcontext() as context:
        context.prec = 40
        predicted = [sum((Decimal(str(state['labels'][int(j)][0])) for j in near), Decimal(0))/3 for near in neighbors]
        order = sorted(range(len(available)), key=lambda j: (predicted[j], j))
        return [{'row_id': available[j], 'neighbor_ids': [state['ids'][int(k)] for k in neighbors[j]],
                 'predicted_target': str(predicted[j])} for j in order]


def describe(rows, field):
    values = [r[field] for r in rows]
    families = sorted({r['system_group'] for r in rows})
    return {'equal_family_mean_gain': mean(mean(r[field] for r in rows if r['system_group'] == g) for g in families),
            'wins': sum(v > 1e-12 for v in values), 'ties': sum(abs(v) <= 1e-12 for v in values),
            'losses': sum(v < -1e-12 for v in values)}


def calculate():
    for name, h in read('reports/protocol_v29_neighbors.freeze.json')['sha256'].items():
        require(hashlib.sha256(Path(name).read_bytes()).hexdigest() == h, 'Changed input: '+name)
    manifest = read('data/manifest_v8.json'); jobs = read('data/larger_probe_v22.json')['jobs']
    progress = read(OUT/'progress.json'); require(progress['complete'] and len(progress['arms']) == 30, 'Complete intended denominator')
    journal = lines(OUT/'acquisitions.jsonl'); require(len(journal) == 300, '300 new acquisitions')
    rows = []; prediction_checks = 0
    for spec in manifest['datasets']:
        xs = []; targets = []; source_lines = []; seen = set()
        with Path(spec['path']).open(newline='') as f:
            for line, row in enumerate(csv.DictReader(f, delimiter=spec['delimiter']), 2):
                if any(row[k] != str(v) for k, v in spec['filters'].items()): continue
                x = tuple(float(row[k]) for k in spec['feature_names'])
                if x in seen: continue
                seen.add(x); xs.append(x); targets.append(float(row[spec['primary_objective']])); source_lines.append(line)
        x = np.asarray(xs); lo, hi = min(targets), max(targets)
        require(len(targets) == spec['rows'] and spec['direction'] == '-', 'Schema/minimization')
        def quality(state):
            require(len(state['ids']) == len(set(state['ids'])) == len(state['labels']) == 20, 'Twenty unique labels')
            require(state['ids'][:10] == prefix['ids'] and state['labels'][:10] == prefix['labels'], 'Identical prefix')
            require(state['labels'] == [[targets[i]] for i in state['ids']], 'Original source labels')
            target = min(targets[i] for i in state['ids'])
            return target, (target-lo)/(hi-lo) if hi > lo else 0.
        for case in [c for c in manifest['cases'] if c['dataset'] == spec['id']]:
            key = f"{case['dataset']}_{case['seed']}"; prefix = read(f'results/v6/prefixes/{key}.json')['state']
            pool = case['pool']['ranked']
            states = {'full_classical': read(f'results/v6/classical/{key}.json')['arms']['centroid_nominal']['state'],
                'static_rank': read(f'results/v8/static_rank/{key}.json')['state'],
                'centroid_shortlist': read(f'results/v25_shortlist/arms/{key}.json')['state'],
                'voting': read(f'results/v28_consensus/arms/{key}.json')['state']}
            bases = {b: [quality(s)] for b, s in states.items()}
            singles = []
            for condition in ('assigned_ids', 'reverse_display', 'reassigned_ids'):
                js = [j for j in jobs if j['dataset'] == case['dataset'] and j['seed'] == case['seed'] and j['condition'] == condition]
                require(len(js) == 1, 'One frozen job per condition')
                singles.append(quality(read(f"results/v22_larger/arms/{js[0]['job_id']:02d}_llm.json")['state']))
            bases.update(single_assigned=[singles[0]], single_presentation_mean=singles)
            for mode in MODES:
                arm = read(OUT/'arms'/f'{key}_{mode}.json'); state = json.loads(json.dumps(prefix))
                events = [e for e in journal if e['dataset'] == case['dataset'] and e['seed'] == case['seed'] and e['arm'] == mode]
                require(len(events) == len(arm['trace']) == arm['actual_new_accesses'] == 10, 'Ten new acquisitions/trace')
                batch = reference_rank(x, prefix, pool)[:10]
                for step, event in enumerate(events):
                    expected = batch[step] if mode == 'batch_3nn' else reference_rank(x, state, pool)[0]
                    require(arm['trace'][step] == {'step': step, **expected}, 'Independent prediction/neighbor replay')
                    i = expected['row_id']
                    require(event['row_id'] == i and event['source_line'] == source_lines[i] and float(event['raw_target']) == targets[i], 'Journal source identity')
                    observe(state, i, targets[i], '-'); prediction_checks += 1
                require(state == arm['state'], 'Independent final state')
                target, loss = quality(state)
                row = {'dataset': case['dataset'], 'seed': case['seed'], 'system_group': spec['system_group'],
                    'arm': mode, 'target': target, 'loss': loss, 'branch_seconds': arm['branch_seconds']}
                for b, values in bases.items():
                    row[b+'_loss'] = mean(v[1] for v in values)
                    row[b+'_normalized_gain'] = mean(v[1]-loss for v in values)
                    row[b+'_relative_gain'] = mean((v[0]-target)/v[0] for v in values)
                rows.append(row)
    require(len(rows) == 30 and prediction_checks == 300, 'Full denominator')
    modes = {}
    for mode in MODES:
        cases = [r for r in rows if r['arm'] == mode]
        groups = sorted({r['system_group'] for r in cases})
        families = [{'system_group': g, 'mean_loss': mean(r['loss'] for r in cases if r['system_group'] == g)} for g in groups]
        modes[mode] = {'families': families, 'equal_family_mean_loss': mean(g['mean_loss'] for g in families),
                      'comparisons': {b: {'normalized': describe(cases, b+'_normalized_gain'), 'relative': describe(cases, b+'_relative_gain')} for b in BASES}}
    paired = []
    for batch in [r for r in rows if r['arm'] == 'batch_3nn']:
        sequential = next(r for r in rows if r['arm'] == 'sequential_3nn' and r['dataset'] == batch['dataset'] and r['seed'] == batch['seed'])
        paired.append({'dataset': batch['dataset'], 'seed': batch['seed'], 'system_group': batch['system_group'],
            'normalized_gain': batch['loss']-sequential['loss'], 'relative_gain': (batch['target']-sequential['target'])/batch['target']})
    return {'scope': 'Exploratory fixed batch/sequential nearest-neighbor controls; no model calls or held-out study',
        'complete': True, 'cases': rows, 'modes': modes, 'sequential_minus_batch_cases': paired,
        'sequential_over_batch': {k: describe(paired, k+'_gain') for k in ('normalized', 'relative')},
        'independent_predictions_and_labels_verified': prediction_checks,
        'new_objective_acquisitions': 300, 'new_model_calls': 0,
        'deployment_per_mode': {'cases': 15, 'logical_objective_evaluations': 300, 'model_requests': 0}}


def render(result):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(11, 4))
    for ax, g in zip(axes, sorted({r['system_group'] for r in result['cases']})):
        rows = [r for r in result['cases'] if r['system_group'] == g]
        values = [mean(r['static_rank_loss'] for r in rows), mean(r['single_assigned_loss'] for r in rows)]
        values += [mean(r['loss'] for r in rows if r['arm'] == mode) for mode in MODES]
        ax.bar(range(4), values, color=['#7b8b96', '#b55b3d', '#74a7bb', '#176b93'])
        ax.set_xticks(range(4), ['Static\nrank', 'Single\nLLM', 'Batch\n3NN', 'Sequential\n3NN'], fontsize=8)
        ax.set_title(g); ax.set_ylabel('Normalized loss (lower is better)')
    fig.suptitle('V29: same shortlist, direct acquired-label prediction')
    fig.text(.5, .015, '20 objective evaluations per arm. Fixed k=3; no tuning. Three exposed families; separate panel scales.', ha='center', fontsize=8)
    fig.tight_layout(rect=[0, .05, 1, .95])
    for ext in ('png', 'svg'): fig.savefig(OUT/('comparison.'+ext), dpi=180)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--verify-only', action='store_true'); args = parser.parse_args()
    if args.verify_only:
        require(calculate() == read(OUT/'summary.json'), 'Saved result differs')
        print('All30 arms/300 nearest-neighbor decisions and source labels replayed.'); return
    require(not (OUT/'summary.json').exists(), 'Preserve completed analysis')
    cfg = authorization_config(load_config('configs/followup_v3.yaml'), read('configs/authorization_v22.json'))
    before = read('artifacts/resource_ledger_v2.json')
    with Resources(cfg, 'artifacts/resource_ledger_v2.json') as resource:
        resource.check(); result = calculate(); write(OUT/'summary.json', result)
        with (OUT/'cases.csv').open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(result['cases'][0])); writer.writeheader(); writer.writerows(result['cases'])
        render(result); resource.check()
    after = read('artifacts/resource_ledger_v2.json')
    write('artifacts/study_v29/analysis_accounting.json', {'charged_seconds': after['experiment_seconds']-before['experiment_seconds'],
        'cumulative_seconds': after['experiment_seconds'], 'remaining_seconds': 3600-after['experiment_seconds'],
        'new_objective_acquisitions': 0, 'new_model_calls': 0, 'active_since': after['active_since']})
    print(json.dumps({k: v for k, v in result.items() if k not in ('cases', 'sequential_minus_batch_cases')}, indent=2))


if __name__ == '__main__': main()
