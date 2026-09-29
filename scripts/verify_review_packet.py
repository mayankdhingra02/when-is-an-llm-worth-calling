"""Read-only consistency audit of review claims; no inference or label acquisition."""
import csv
import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return json.loads((ROOT / name).read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ledger_path = ROOT / 'artifacts/resource_ledger_v2.json'
    ledger_hash = digest(ledger_path)
    freezes = {}
    for path in sorted((ROOT / 'reports').glob('*.freeze.json')):
        entries = json.loads(path.read_text())['sha256']
        for name, expected in entries.items():
            assert digest(ROOT / name) == expected, f'Freeze mismatch: {path.name}: {name}'
        freezes[path.name] = len(entries)

    with (ROOT / 'results/v6/policies.csv').open() as handle:
        policies = {row['policy']: row for row in csv.DictReader(handle)}
    for name in ('benefit', 'uncertainty'):
        assert int(policies[name]['escalations']) == 0
        assert policies[name]['group_mean_loss'] == policies['never']['group_mean_loss']
    assert all(int(row['cases']) == 15 for row in policies.values())
    assert float(policies['never']['group_mean_loss']) < float(policies['always']['group_mean_loss'])

    exact = read('results/v9_analysis/summary.json')
    assert len(exact['records']) == 15
    assert all(row['exact_first_half_sequence_match'] for row in exact['records'])
    assert all(row['probability_random_no_worse_than_observed'] >= .5 for row in exact['records'])
    assert all(row['subsets_enumerated'] == math.comb(20, 10) for row in exact['records'])
    assert all(row['formula_matches_all_subsets'] for row in exact['verification'])

    controls = read('results/v12_controls/summary.json')
    assert controls['complete'] and len(controls['records']) == 10
    groups = {}
    for group in ('brotli', 'lrzip'):
        rows = [r for r in controls['records'] if r['system_group'] == group]
        assert len(rows) == 5
        for row in rows:
            calculated = (row['random_runtime'] - row['joint_3nn_runtime']) / row['random_runtime']
            assert math.isclose(calculated, row['joint_3nn_gain_over_random'], abs_tol=1e-12)
        groups[group] = mean(row['joint_3nn_gain_over_random'] for row in rows)
    groups['all_two_groups'] = mean(groups.values())
    for row in controls['summaries']:
        assert math.isclose(groups[row['group']], row['mean_relative_gain_over_random'], abs_tol=1e-12)
    assert [round(100 * groups[g], 2) for g in ('lrzip', 'brotli', 'all_two_groups')] == [4.82, -2.79, 1.01]
    count = sum(bool(line.strip()) for line in (ROOT / 'results/v12_controls/acquisitions.jsonl').read_text().splitlines())
    assert count == controls['new_vector_accesses'] == 300
    replay = read('artifacts/study_v12/verification.json')
    assert replay['verified'] and replay['branches'] == 20 and replay['joint_vector_acquisitions'] == count
    assert '95 passed' in (ROOT / 'artifacts/study_v12/tests.log').read_text()
    ledger = read('artifacts/resource_ledger_v2.json')
    assert ledger['requests'] == 128 and ledger['active_since'] is None
    assert ledger['experiment_seconds'] < 1800 and ledger['external_spend_usd'] == 0

    documents = ['README.md', 'STATUS.md', 'REPRODUCE.md', 'reports/decision_brief.md', 'reports/next_experiment.md']
    links = 0
    for name in documents:
        path = ROOT / name
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' in target or target.startswith('#'):
                continue
            target = target.split('#', 1)[0]
            assert (path.parent / target).exists(), f'Broken local link in {name}: {target}'
            links += 1
    assert digest(ledger_path) == ledger_hash, 'Audit changed ledger'
    report = {
        'at': datetime.now(timezone.utc).isoformat(),
        'verified': True,
        'scope': 'Saved-evidence consistency, not new experiments or independent numerical replay',
        'scientific_freezes': freezes,
        'v6_heldout_cases': 15,
        'v8_first_half_matches': 15,
        'v9_recorded_subset_checks_per_case': math.comb(20, 10),
        'v12_recomputed_mean_relative_gains': groups,
        'v12_journal_vectors': count,
        'latest_saved_tests_passed': 95,
        'local_document_links_checked': links,
        'ledger_unchanged_sha256': ledger_hash,
        'new_model_requests': 0,
        'new_objective_acquisitions': 0,
    }
    destination = ROOT / 'artifacts/review_packet/verification.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
