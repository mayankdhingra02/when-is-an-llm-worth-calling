"""Separate source evaluator and independent replay of fresh transfer prefixes."""
import argparse, csv, hashlib, json, math, os, random, sys
from pathlib import Path
from statistics import mean
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT/'src')); os.chdir(ROOT)
os.environ['MPLCONFIGDIR'] = str(ROOT/'.cache/matplotlib')
from escalation.io import read, write, lines, digest
from escalation.config import load_config
from escalation.resources import Resources
from escalation.larger_v22 import authorization_config, require
from escalation.transfer_v30 import MODES
from verify_reproduction_v26 import ranked, observe
from analyze_neighbors_v29 import reference_rank
OUT = Path('results/v30_transfer')


def calculate():
    for name, h in read('reports/protocol_v30_transfer.freeze.json')['sha256'].items():
        require(hashlib.sha256(Path(name).read_bytes()).hexdigest() == h, 'Changed frozen input: '+name)
    manifest = read('data/manifest_v30.json'); progress = read(OUT/'progress.json')
    require(progress['complete'] and len(progress['arms']) == 50, 'Complete intended denominator')
    journal = lines(OUT/'acquisitions.jsonl'); require(len(journal) == 600, '600 charged acquisitions')
    rows = []; checked = 0
    for spec in manifest['datasets']:
        features = []; targets = []; source_lines = []; seen = set()
        with Path(spec['path']).open(newline='') as f:
            for line, row in enumerate(csv.DictReader(f, delimiter=spec['delimiter']), 2):
                if any(row[k] != str(v) for k, v in spec['filters'].items()): continue
                x = tuple(float(row[k]) for k in spec['feature_names'])
                if x in seen: continue
                seen.add(x); features.append(x); targets.append(float(row[spec['primary_objective']])); source_lines.append(line)
        require(len(targets) == spec['rows'] and all(math.isfinite(v) and v > 0 for v in targets), 'Source schema and positive target domain')
        lo, hi = min(targets), max(targets); x = np.asarray(features)
        for seed in manifest['seeds']:
            key = f"{spec['id']}_{seed}"; p = read(OUT/'prefixes'/f'{key}.json')
            order = list(range(len(targets))); random.Random(seed).shuffle(order)
            prefix = {'order': order, 'ids': [], 'labels': [], 'best': [], 'rest': []}
            def replay_event(state, selected, event):
                nonlocal checked
                require(event['row_id'] == selected and event['source_line'] == source_lines[selected] and float(event['raw_target']) == targets[selected], 'Journal identity')
                observe(state, selected, targets[selected], '-'); checked += 1
            events = [e for e in journal if e['dataset'] == spec['id'] and e['seed'] == seed and e['arm'] == 'prefix']
            require(len(events) == 10, 'Ten charged prefix labels')
            for event in events: replay_event(prefix, ranked(features, prefix)[0], event)
            require(prefix == p['state'] and digest(prefix) == p['prefix_hash'], 'Independent prefix state/hash')
            pool = ranked(features, prefix)[:20]; require(pool == p['pool']['ranked'], 'Independent acquired-only shortlist')
            for mode in MODES:
                arm = read(OUT/'arms'/f'{key}_{mode}.json'); state = json.loads(json.dumps(prefix))
                if mode == 'centroid_shortlist': state['order'] = [i for i in state['order'] if i in set(pool)|set(prefix['ids'])]
                events = [e for e in journal if e['dataset'] == spec['id'] and e['seed'] == seed and e['arm'] == mode]
                require(len(events) == arm['actual_new_accesses'] == 10 and arm['logical_evaluations'] == 20, 'Branch budget')
                batch = reference_rank(x, prefix, pool)[:10]
                for step, event in enumerate(events):
                    if mode in ('batch_3nn', 'sequential_3nn'):
                        expected = batch[step] if mode == 'batch_3nn' else reference_rank(x, state, pool)[0]
                        require(arm['trace'][step] == {'step': step, **expected}, 'Independent3NN trace')
                        selected = expected['row_id']
                    elif mode == 'static_rank': selected = pool[step]
                    else: selected = ranked(features, state)[0]
                    replay_event(state, selected, event)
                require(state == arm['state'] and arm['prefix_hash'] == p['prefix_hash'], 'Independent final branch state')
                require(len(state['ids']) == len(set(state['ids'])) == 20 and state['ids'][:10] == prefix['ids'] and state['labels'][:10] == prefix['labels'], 'Shared prefix and uniqueness')
                target = min(targets[i] for i in state['ids'])
                rows.append({'dataset': spec['id'], 'system_group': spec['system_group'], 'seed': seed, 'arm': mode,
                    'target': target, 'loss': (target-lo)/(hi-lo) if hi > lo else 0., 'branch_seconds': arm['branch_seconds']})
    require(len(rows) == 50 and checked == 600, 'Full completed denominator')
    families = [{'system_group': g, **{mode: mean(r['loss'] for r in rows if r['system_group'] == g and r['arm'] == mode) for mode in MODES}}
                for g in sorted({r['system_group'] for r in rows})]
    pairs = []; summaries = {}
    for base in MODES[:-1]:
        values = []
        for candidate in [r for r in rows if r['arm'] == 'sequential_3nn']:
            b = next(r for r in rows if r['dataset'] == candidate['dataset'] and r['seed'] == candidate['seed'] and r['arm'] == base)
            record = {'dataset': b['dataset'], 'system_group': b['system_group'], 'seed': b['seed'], 'comparator': base,
                      'normalized_gain': b['loss']-candidate['loss'], 'relative_gain': (b['target']-candidate['target'])/b['target']}
            values.append(record); pairs.append(record)
        groups = [{'system_group': g, **{m: mean(v[m] for v in values if v['system_group'] == g) for m in ('normalized_gain', 'relative_gain')}} for g in sorted({v['system_group'] for v in values})]
        summaries[base] = {'families': groups, 'equal_family_normalized_gain': mean(g['normalized_gain'] for g in groups),
            'equal_family_relative_gain': mean(g['relative_gain'] for g in groups),
            'wins': sum(v['normalized_gain'] > 1e-12 for v in values), 'ties': sum(abs(v['normalized_gain']) <= 1e-12 for v in values),
            'losses': sum(v['normalized_gain'] < -1e-12 for v in values)}
    return {'scope': 'Prospective classical transfer check on two previously unacquired families; no LLM/router evaluation',
            'complete': True, 'cases': rows, 'families': families,
            'equal_family_mean_losses': {mode: mean(g[mode] for g in families) for mode in MODES},
            'sequential_comparisons': summaries, 'paired_gains': pairs,
            'independent_acquisitions_replayed': checked, 'new_prefix_labels': 100, 'new_branch_labels': 500,
            'new_objective_acquisitions': 600, 'new_model_calls': 0,
            'logical_evaluations_all_arms': 1000, 'logical_deployment_evaluations_per_method': 200}


def render(result):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, family in zip(axes, result['families']):
        ax.bar(range(5), [family[m] for m in MODES], color=['#a5afb5', '#7b8b96', '#91afbd', '#74a7bb', '#176b93'])
        ax.set_xticks(range(5), ['Full\ncentroid', 'Static\nrank', 'Shortlist\ncentroid', 'Batch\n3NN', 'Sequential\n3NN'], fontsize=8)
        ax.set_title(family['system_group']); ax.set_ylabel('Normalized loss (lower is better)')
    fig.suptitle('V30: fixed classical methods on newly admitted families')
    fig.text(.5, .015, 'Two families × five seeds. 20 evaluations per arm; same 10-label prefix. No LLM calls. Separate panel scales.', ha='center', fontsize=8)
    fig.tight_layout(rect=[0, .06, 1, .95])
    for ext in ('png', 'svg'): fig.savefig(OUT/('comparison.'+ext), dpi=180)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--verify-only', action='store_true'); args = parser.parse_args()
    if args.verify_only:
        require(calculate() == read(OUT/'summary.json'), 'Saved summary differs')
        print('10 prefixes,50 arms,600 acquisitions/decisions independently replayed.'); return
    require(not (OUT/'summary.json').exists(), 'Preserve completed analysis')
    cfg = authorization_config(load_config('configs/followup_v3.yaml'), read('configs/authorization_v22.json'))
    before = read('artifacts/resource_ledger_v2.json')
    with Resources(cfg, 'artifacts/resource_ledger_v2.json') as resource:
        resource.check(); result = calculate(); write(OUT/'summary.json', result)
        for name, records in [('cases', result['cases']), ('paired_gains', result['paired_gains'])]:
            with (OUT/(name+'.csv')).open('w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=list(records[0])); writer.writeheader(); writer.writerows(records)
        render(result); resource.check()
    after = read('artifacts/resource_ledger_v2.json')
    write('artifacts/study_v30/analysis_accounting.json', {'charged_seconds': after['experiment_seconds']-before['experiment_seconds'],
        'cumulative_seconds': after['experiment_seconds'], 'remaining_seconds': 3600-after['experiment_seconds'],
        'new_objective_acquisitions': 0, 'new_model_calls': 0, 'active_since': after['active_since']})
    print(json.dumps({k: v for k, v in result.items() if k not in ('cases', 'paired_gains')}, indent=2))


if __name__ == '__main__': main()
