"""Current saved-evidence audit. Standard library only; never runs an experiment.

Checks hashes and recomputes selection mappings/arithmetic from existing records.
Does not replay inference, tokenizer decoding, optimization or controller fitting.
Historical verifiers remain untouched. Fails closed, including under python -O.
"""
import argparse
import csv
import hashlib
import json
import math
import re
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = Path('artifacts/history/review_handoff_before_update')
IDS = list('0123456789ABCDEFGHIJ')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads((ROOT / path).read_text())


def lines(path):
    return [json.loads(line) for line in (ROOT / path).read_text().splitlines() if line.strip()]


def checked_selections(jobs, requests, starts, outcomes):
    """Account for each intended job exactly once; independently map raw IDs."""
    def indexed(rows, key):
        result = {row[key]: row for row in rows}
        require(len(result) == len(rows), f'Duplicate {key}')
        return result

    job_map = indexed(jobs, 'job_id')
    response_map = indexed(requests, 'job_id')
    start_map = indexed(starts, 'job_id')
    outcome_map = indexed(outcomes, 'request_id')
    require(job_map.keys() == response_map.keys() == start_map.keys(), 'Missing/extra intended job')
    require(len(outcomes) == len(jobs), 'Outcome denominator mismatch')
    require({r['request_id'] for r in requests} == outcome_map.keys(), 'Request/outcome mismatch')
    checked = []
    for job_id, job in job_map.items():
        request, start = response_map[job_id], start_map[job_id]
        require(start['request_id'] == request['request_id'], 'Start/request mismatch')
        require(request['status'] == 'response' and request['retry'] == 0, 'Unexpected failure/retry')
        require(request['messages'] == job['messages'] == start['messages'], 'Prompt mismatch')
        require(request['mapping'] == job['mapping'], 'Mapping mismatch')
        selected = request['raw_output'].strip().splitlines()
        body = json.loads(job['messages'][-1]['content'].split('\n', 1)[1])
        displayed = [candidate['id'] for candidate in body['candidates']]
        require(len(displayed) == 20 and set(displayed) == set(IDS), 'Candidate IDs invalid')
        require(len(selected) == len(set(selected)) == 10, 'Ten distinct output IDs required')
        require(set(selected) <= set(displayed), 'Unknown output ID')
        rows = [job['mapping'][i] for i in selected]
        outcome = outcome_map[request['request_id']]
        require(outcome['status'] == 'completed', 'Outcome not completed')
        require(outcome['selected_ids'] == selected and outcome['selected_rows'] == rows, 'Raw/summary mismatch')
        require(request['revision'] == '7ae557604adf67be50417f59c2c2f167def9a775', 'Model revision mismatch')
        require(request['provider'] == 'local_transformers', 'Nonlocal response')
        require(request['parameters'] == {'do_sample': False, 'max_new_tokens': 20}, 'Parameter mismatch')
        require(request['input_tokens'] is not None and request['output_tokens'] == 20, 'Usage missing/changed')
        checked.append({'dataset': job['dataset'], 'condition': job['condition'],
                        'request_id': request['request_id'], 'selected_ids': selected,
                        'selected_rows': rows, 'display_prefix_match': selected == displayed[:10],
                        'lowest_ids_match': selected == IDS[:10]})
    return checked


def audit():
    started = time.perf_counter()
    ledger_path = ROOT / 'artifacts/resource_ledger_v2.json'
    ledger_hash = digest(ledger_path)
    freezes = {}
    for path in sorted((ROOT / 'reports').glob('*.freeze.json')):
        entries = json.loads(path.read_text())['sha256']
        for name, expected in entries.items():
            require(digest(ROOT / name) == expected, f'Freeze mismatch: {path.name}: {name}')
        freezes[path.name] = len(entries)
    relocations = {}
    snapshot = read('artifacts/study_v21/executed_evidence.json')['files']
    for name, record in snapshot.items():
        path = ROOT / name
        if digest(path) != record['sha256']:
            # Only mutable review documents may resolve to the explicit prior copy.
            require(name in ('README.md', 'REPRODUCE.md', 'STATUS.md', 'reports/decisions.md'),
                    f'Executed evidence changed: {name}')
            path = ROOT / ARCHIVE / name
            relocations[name] = str(path.relative_to(ROOT))
        require(digest(path) == record['sha256'] and path.stat().st_size == record['bytes'],
                f'Historical evidence mismatch: {name}')

    with (ROOT / 'results/v6/policies.csv').open() as handle:
        policies = {r['policy']: r for r in csv.DictReader(handle)}
    require(len(policies) == 7 and all(int(r['cases']) == 15 for r in policies.values()), 'V6 denominator')
    for policy in ('benefit', 'uncertainty', 'random_development_rate', 'random_matched_realized_rate_diagnostic'):
        require(int(policies[policy]['escalations']) == 0, f'V6 {policy} rate changed')
        require(policies[policy]['group_mean_loss'] == policies['never']['group_mean_loss'], 'V6 policy mismatch')
    require(float(policies['always']['group_mean_loss']) > float(policies['never']['group_mean_loss']), 'V6 direction')

    stages = {}
    for version, directory, data, key, count, first in (
        ('v19', 'v19_order_probe', 'order_probe_v19', 'outcomes', 9, 129),
        ('v21', 'v21_nonmonotone', 'nonmonotone_probe_v21', 'cases', 3, 138),
    ):
        base = f'results/{directory}'
        jobs = read(f'data/{data}.json')['jobs']
        requests = lines(f'{base}/requests.jsonl')
        summary = read(f'{base}/summary.json')
        require(len(jobs) == summary['intended'] == summary['completed'] == count, 'Stage denominator')
        require([r['request_id'] for r in requests] == list(range(first, first + count)), 'Request sequence')
        began = read(f'{base}/started.json')
        require(began['authorization']['granted'] and began['authorization']['recorded_at'] < began['at']
                < min(r['started'] for r in requests), 'Approval must precede inference')
        checked = checked_selections(jobs, requests, lines(f'{base}/request_starts.jsonl'), summary[key])
        require(sum(r['input_tokens'] for r in requests) == summary['input_tokens_observed'], 'Input usage')
        require(sum(r['output_tokens'] for r in requests) == summary['output_tokens_observed'], 'Output usage')
        require(math.isclose(sum(r['wall_seconds'] for r in requests), summary['request_wall_seconds']), 'Request time')
        stages[version] = checked

    require(sum(r['display_prefix_match'] for r in stages['v19']) == 9, 'V19 first displayed ten')
    for row in stages['v19'] + stages['v21']:
        original = next(r for r in stages['v19'] if r['dataset'] == row['dataset'] and r['condition'] == 'original')
        row['configuration_overlap_with_v19_original'] = len(set(row['selected_rows']) & set(original['selected_rows']))
        if row['condition'] in ('reverse_display', 'reverse_ids'):
            require(row['configuration_overlap_with_v19_original'] == (0 if row['condition'] == 'reverse_display' else 10),
                    'V19 intervention result')
    require([r['display_prefix_match'] for r in stages['v21']] == [True, False, False], 'V21 mixed prefix result')
    require([r['lowest_ids_match'] for r in stages['v21']] == [False, True, True], 'V21 mixed ID result')
    require([r['configuration_overlap_with_v19_original'] for r in stages['v21']] == [10, 5, 5], 'V21 overlap')
    ledger = read('artifacts/resource_ledger_v2.json')
    authorization = read('configs/authorization_v21.json')
    require(ledger['requests'] == authorization['request_cap'] == 140 and ledger['active_since'] is None, 'Current cap/state')
    require(ledger['experiment_seconds'] < 1800 and ledger['external_spend_usd'] == 0, 'Current runtime/spend')
    require('140 passed' in (ROOT / 'artifacts/study_v21/post_execution_tests.log').read_text(), 'Saved V21 tests')
    links = 0
    documents = ['README.md', 'REPRODUCE.md', 'STATUS.md', 'reports/review_note.md', 'reports/review_evidence.md']
    for name in documents:
        path = ROOT / name
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' in target or target.startswith('#'):
                continue
            require((path.parent / target.split('#', 1)[0]).exists(), f'Broken link: {name}: {target}')
            links += 1
    require(digest(ledger_path) == ledger_hash, 'Ledger modified by audit')
    return {'verified': True, 'at': datetime.now(timezone.utc).isoformat(),
            'scope': 'Saved-evidence consistency and raw ID mapping; no new inference or independent numerical/model replay',
            'scientific_freezes': freezes, 'frozen_references': sum(freezes.values()),
            'v21_snapshot_files': len(snapshot), 'historical_document_relocations': relocations,
            'v6_policy_csv_checked': True, 'v6_heldout_cases': 15, 'v6_heldout_families': 3,
            'raw_selection_checks': stages, 'local_links_checked': links,
            'saved_v21_tests_passed': 140, 'followup_requests': ledger['requests'],
            'experiment_seconds': ledger['experiment_seconds'], 'external_spend_usd': 0,
            'new_model_requests': 0, 'new_objective_acquisitions': 0,
            'ledger_unchanged_sha256': ledger_hash,
            'audit_wall_seconds_outside_experiment_ledger': time.perf_counter() - started}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Optional new JSON receipt; refuses overwrite')
    args = parser.parse_args()
    if args.output:
        require(not args.output.exists(), 'Preserve existing audit receipt; choose a new path')
    report = audit()
    payload = json.dumps(report, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as handle:
            handle.write(payload)
    print(payload)


if __name__ == '__main__':
    main()
