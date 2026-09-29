"""Separate retrospective evaluator. Never imported by the selection runner."""
import csv
import hashlib
import os
import sys
from pathlib import Path
from statistics import mean
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src')); os.chdir(ROOT)
from escalation.io import read, write, lines
from escalation.config import load_config
from escalation.resources import Resources
from escalation.larger_v22 import authorization_config, require

OUT = Path('results/v22_larger')


def main():
    cfg = authorization_config(load_config('configs/followup_v3.yaml'), read('configs/authorization_v22.json'))
    require(not (OUT / 'summary.json').exists(), 'Preserve completed analysis')
    require((OUT / 'progress.json').exists(), 'Actual execution required')
    for name, expected in read('reports/protocol_v22_larger.freeze.json')['sha256'].items():
        require(hashlib.sha256(Path(name).read_bytes()).hexdigest() == expected, 'Frozen input changed:' + name)
    with Resources(cfg, 'artifacts/resource_ledger_v2.json') as resource:
        resource.check()
        from escalation.finite_v6 import load_candidates
        from escalation.study_v6 import retrospective_labels
        from escalation.evaluator import evaluate
        jobs = read('data/larger_probe_v22.json')['jobs']; progress = read(OUT / 'progress.json')
        manifest = read('data/manifest_v8.json'); null = read('results/v9_analysis/summary.json')['records']
        requests = lines(OUT / 'requests.jsonl'); records = []
        for spec in manifest['datasets']:
            resource.check()
            candidates = load_candidates(spec); labels = retrospective_labels(spec, candidates)
            for job in [j for j in jobs if j['dataset'] == spec['id']]:
                key = f"{job['dataset']}_{job['seed']}"
                path = OUT / 'arms' / f"{job['job_id']:02d}_llm.json"
                row = {'dataset': job['dataset'], 'system_group': job['system_group'], 'seed': job['seed'],
                       'condition': job['condition'], 'job_id': job['job_id'], 'status': 'incomplete'}
                if path.exists():
                    state = read(path)['state']
                    classic = read(f'results/v6/classical/{key}.json')['arms']['centroid_nominal']['state']
                    control_job = (next(j for j in jobs if j['dataset'] == job['dataset'] and j['seed'] == job['seed']
                                       and j['condition'] == 'assigned_ids') if job['condition'] == 'assigned_ids_repeat' else job)
                    def loss(s): return evaluate(labels, candidates.directions, s['ids'])['loss']
                    row.update(status='completed', llm_loss=loss(state), classical_loss=loss(classic))
                    row['uniform_expected_loss'] = next(r['uniform_expected_loss'] for r in null
                                                       if r['dataset'] == job['dataset'] and r['seed'] == job['seed'])
                    for arm in ['first_display', 'lowest_ids']:
                        control = read(OUT / 'arms' / f"{control_job['job_id']:02d}_{arm}.json")
                        row[arm + '_loss'] = loss(control['state'])
                        row[arm + '_exact_set_match'] = set(state['ids'][10:]) == set(control['state']['ids'][10:])
                records.append(row)
        repeats = []
        for job in [j for j in jobs if j['condition'] == 'assigned_ids']:
            repeat = next(j for j in jobs if j['dataset'] == job['dataset'] and j['seed'] == job['seed']
                          and j['condition'] == 'assigned_ids_repeat')
            a = next((r for r in requests if r['job_id'] == job['job_id'] and r['status'] == 'response'), None)
            b = next((r for r in requests if r['job_id'] == repeat['job_id'] and r['status'] == 'response'), None)
            repeats.append({'dataset': job['dataset'], 'seed': job['seed'], 'available': a is not None and b is not None,
                            'exact_output_match': a['raw_output'] == b['raw_output'] if a and b else None})
        primary = None; group_effects = []
        if progress['complete']:
            for group in sorted({r['system_group'] for r in records}):
                unique = [r for r in records if r['system_group'] == group and r['condition'] != 'assigned_ids_repeat']
                require(len(unique) == 15, 'Five seeds times three presentations per family')
                group_effects.append({'system_group': group, **{baseline: mean(r[baseline] - r['llm_loss'] for r in unique)
                    for baseline in ['classical_loss', 'uniform_expected_loss', 'first_display_loss', 'lowest_ids_loss']}})
            primary = {baseline: mean(g[baseline] for g in group_effects)
                       for baseline in ['classical_loss', 'uniform_expected_loss', 'first_display_loss', 'lowest_ids_loss']}
        summary = {'scope': 'Adaptive development-only feasibility study; no unseen-system/router/generalization claim',
                   'complete': progress['complete'], 'intended_requests': 60, 'records': records, 'repeated_conditions': repeats,
                   'family_mean_gains': group_effects, 'primary_family_equal_mean_gain_excluding_repeat': primary,
                   'interpretation': 'Positive gain favors LLM. Uniform is a cached retrospective expectation, not a newly deployed arm. No aggregate efficacy claim if intended experiment incomplete.',
                   'collection': {'model_attempts': len(lines(OUT / 'request_starts.jsonl')),
                       'new_objective_acquisitions': len(lines(OUT / 'acquisitions.jsonl')),
                       'requests_missing_usage': sum(r.get('input_tokens') is None or r.get('output_tokens') is None for r in requests),
                       'input_tokens_observed': sum(r.get('input_tokens') or 0 for r in requests),
                       'output_tokens_observed': sum(r.get('output_tokens') or 0 for r in requests),
                       'request_wall_seconds': sum(r['wall_seconds'] for r in requests), 'external_spend_usd': 0},
                   'deployment_scenario': {'status': 'modeled separately from collection', 'one_presentation_per_case_logical_evaluations': 300,
                                           'always_escalate_model_requests': 15, 'repeated_conditions_not_free': True}}
        write(OUT / 'summary.json', summary)
        columns = sorted({k for r in records for k in r})
        with (OUT / 'outcomes.csv').open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=columns); writer.writeheader(); writer.writerows(records)
        resource.check()
    print('Saved full intended denominator, quality comparisons, repeat agreement and costs.')


if __name__ == '__main__':
    main()
