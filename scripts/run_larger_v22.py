"""One authorized V22 transaction; stops on failure, never silently resumes."""
import argparse
import hashlib
import os
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src')); os.chdir(ROOT)
from escalation.io import read, write, lines, append, digest, now
from escalation.config import load_config
from escalation.larger_v22 import authorization_config, controls, require
from escalation.resources import Resources
from escalation.order_probe_v19 import StageResources, inspect_response

OUT = Path('results/v22_larger')


def preflight():
    ledger = read('artifacts/resource_ledger_v2.json'); reasons = []
    try:
        cfg = authorization_config(load_config('configs/followup_v3.yaml'), read('configs/authorization_v22.json'))
    except (PermissionError, ValueError) as error:
        cfg = None; reasons.append(str(error))
    if ledger['active_since'] is not None: reasons.append('Experiment ledger is active')
    if cfg and 200 - ledger['requests'] < 60: reasons.append('Full60-attempt reservation required')
    if cfg and 3600 - ledger['experiment_seconds'] < 1000: reasons.append('1000seconds reserve required for900-second work stage and analysis')
    if not Path('artifacts/model_manifest_v22.json').exists(): reasons.append('Pinned larger model not downloaded')
    elif not read('artifacts/model_manifest_v22.json')['complete']: reasons.append('Model download incomplete')
    if (OUT / 'started.json').exists(): reasons.append('Prior V22 transaction retained; no automatic restart')
    result = {'ready': not reasons, 'blocked_reasons': reasons, 'requests_used': ledger['requests'],
              'current_runtime_seconds': ledger['experiment_seconds'], 'intended_model_requests': 60,
              'intended_control_arms': 90, 'maximum_new_objective_acquisitions': 1500, 'new_model_requests': 0}
    write('artifacts/study_v22/preflight.json', result)
    return cfg, result


def branch(job, arm, proposals, resource):
    # Candidate loader parses only features; LazyOracle charges every new target.
    from escalation.finite_v6 import load_candidates, LazyOracle
    from escalation.core import State
    spec = next(d for d in read('data/manifest_v8.json')['datasets'] if d['id'] == job['dataset'])
    prefix = read(f"results/v6/prefixes/{job['dataset']}_{job['seed']}.json")
    require(prefix['prefix_hash'] == job['prefix_hash'] == digest(prefix['state']), 'Shared prefix changed')
    state = State(**prefix['state']).clone(); candidates = load_candidates(spec)
    context = {'job_id': job['job_id'], 'dataset': job['dataset'], 'seed': job['seed'],
               'system_group': job['system_group'], 'split': 'development', 'condition': job['condition'],
               'arm': arm, 'namespace': 'measured_v22', 'prefix_hash': job['prefix_hash']}
    require(len(proposals) == len(set(proposals)) == 10 and not set(proposals) & set(state.ids), 'Ten new rows required')
    oracle = LazyOracle(spec, candidates, prefix=prefix['state'],
                        journal=lambda e: append(OUT / 'acquisitions.jsonl', {**context, **e, 'at': now()}))
    for row in proposals:
        resource.check()
        state.observe(row, oracle.acquire(row), candidates.directions)
        write(OUT / 'checkpoints' / f"{job['job_id']:02d}_{arm}.json", {**context, 'state': state.record()})
    result = {**context, 'status': 'completed', 'state': state.record(), 'selected_rows': proposals,
              'actual_new_accesses': oracle.new_accesses, 'logical_budget': 20}
    write(OUT / 'arms' / f"{job['job_id']:02d}_{arm}.json", result)
    return result


def progress(jobs, stop):
    requests = {r['job_id']: r for r in lines(OUT / 'requests.jsonl')}
    entries = []
    for job in jobs:
        for arm in (['llm'] if job['condition'] == 'assigned_ids_repeat' else ['first_display', 'lowest_ids', 'llm']):
            path = OUT / 'arms' / f"{job['job_id']:02d}_{arm}.json"
            request = requests.get(job['job_id']) if arm == 'llm' else None
            checkpoint = OUT / 'checkpoints' / f"{job['job_id']:02d}_{arm}.json"
            status = 'completed' if path.exists() else ('failed_or_incomplete' if request or checkpoint.exists() else 'unattempted')
            entries.append({'job_id': job['job_id'], 'arm': arm, 'status': status, 'reason': None if path.exists() else stop})
    write(OUT / 'progress.json', {'intended_model_requests': 60, 'intended_control_arms': 90,
          'complete': all(r['status'] == 'completed' for r in entries), 'arms': entries,
          'actual_request_attempts': len(lines(OUT / 'request_starts.jsonl')),
          'actual_new_objective_acquisitions': len(lines(OUT / 'acquisitions.jsonl')), 'stop_reason': stop})


def run():
    cfg, check = preflight()
    if not check['ready']:
        print(check); return 2
    for name, expected in read('reports/protocol_v22_larger.freeze.json')['sha256'].items():
        require(hashlib.sha256(Path(name).read_bytes()).hexdigest() == expected, 'Frozen input changed:' + name)
    jobs = read('data/larger_probe_v22.json')['jobs']
    require(len(jobs) == 60 and all(digest(j['messages']) == j['prompt_hash'] for j in jobs), 'Prepared prompt mismatch')
    stop = None
    with Resources(cfg, 'artifacts/resource_ledger_v2.json') as base:
        require(200 - base.d['requests'] >= 60 and not (OUT / 'started.json').exists(), 'Reservation changed')
        write(OUT / 'started.json', {'at': now(), 'authorization': read('configs/authorization_v22.json'),
              'baseline_ledger': read('artifacts/resource_ledger_v2.json'), 'intended_model_requests': 60})
        resource = StageResources(base, 900)
        try:
            for job in jobs:
                if job['condition'] != 'assigned_ids_repeat':
                    for arm, proposals in controls(job).items(): branch(job, arm, proposals, resource)
            from escalation.provider_v22 import LargerProvider
            with LargerProvider(cfg, resource, OUT / 'requests.jsonl') as provider:
                for job in jobs:
                    resource.check()
                    context = {k: v for k, v in job.items() if k != 'messages'}
                    response = provider.request(job['messages'], dict(context, namespace='measured_v22',
                        prompt_version='larger_v22', grammar_mode='candidate_order_v19', retry=0))
                    require(response['status'] == 'response', response.get('error', 'Provider failure'))
                    parsed = inspect_response(response['raw_output'], job)
                    branch(job, 'llm', parsed['selected_rows'], resource)
                    print(job['job_id'], job['dataset'], job['seed'], job['condition'], flush=True)
        except Exception as error:
            stop = f'{type(error).__name__}: {error}'
        finally:
            progress(jobs, stop)
    print(read(OUT / 'progress.json'))
    return 1 if stop else 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--preflight', action='store_true'); args = parser.parse_args()
    if args.preflight:
        _, result = preflight(); print(result); raise SystemExit(0 if result['ready'] else 2)
    raise SystemExit(run())
