"""Read-only completion checks across actual pilot stages. No inference or writes."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(p): return json.loads((ROOT / p).read_text())
def lines(p): return [json.loads(x) for x in (ROOT / p).read_text().splitlines() if x]
def sha(p): return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
def require(ok, message):
    if not ok: raise ValueError(message)

def main():
    checks = {}
    evidence = read('artifacts/study_v22/executed_evidence.json')['sha256']
    historical_v22 = {'STATUS.md', 'README.md', 'REPRODUCE.md',
                      'reports/next_experiment_v22.md', 'artifacts/resource_ledger_v2.json'}
    for name, expected in evidence.items():
        archived = 'artifacts/history/v23_before_analysis/' + name
        matched = sha(name) == expected
        if not matched and name in historical_v22 and (ROOT / archived).exists():
            matched = sha(archived) == expected
        require(matched, name)
    checks['unchanged_v22_evidence_files'] = len(evidence)
    sources = read('artifacts/source_manifest.json')['sources']
    for entry in sources: require(sha(entry['path']) == entry['sha256'], entry['path'])
    checks['retained_primary_source_files'] = len(sources)
    refs = 0
    for path in (ROOT / 'reports').glob('*.freeze.json'):
        for name, expected in read(path)['sha256'].items():
            require(sha(name) == expected, name); refs += 1
    checks['scientific_frozen_references'] = refs
    runs = lines('results/v3/classical/runs.jsonl')
    require(len(runs) == 30, '30 corrected classical arms')
    require({r['seed'] for r in runs} == {11,23,37,53,71}, 'Fixed smoke seeds')
    require(len({r['system_group'] for r in runs}) == 3, 'Three smoke systems')
    for row in runs:
        require(row['status'] == 'completed' and len(row['ids']) == len(set(row['ids'])) == 20, 'Smoke budget')
        require(row['logical_evaluations'] == row['actual_new_accesses'] == 20, 'Smoke accounting')
        prefix = read(f"results/v3/classical/prefixes/{row['dataset']}_{row['seed']}.json")['state']
        require(len(prefix['ids']) == 10, 'Checkpoint ten')
        if row['method'] != 'random': require(row['ids'][:10] == prefix['ids'], 'Smoke prefix')
    checks['corrected_classical_arms'] = 30
    all_specs = read('data/manifest_v6.json')['datasets']
    specs = [d for d in all_specs if d['selected']]
    require(len(specs) == 6, 'Six prospectively selected families; unused admissions excluded')
    splits = {}
    for spec in all_specs:
        splits.setdefault(spec['system_group'], set()).add(spec['split'])
        require(sha(spec['path']) == spec['sha256'], spec['path'])
    require(all(len(x) == 1 for x in splits.values()), 'Group isolation')
    seal = read('results/v6/router_seal.json')
    require(seal['test_outcomes_used'] is False, 'Router seal')
    require(set(seal['benefit']['training_groups']) == {d['system_group'] for d in specs if d['split'] == 'development'}, 'Development fit')
    for name, expected in seal['development_files'].items(): require(sha(name) == expected, name)
    journal = lines('results/v6/acquisitions.jsonl')
    require(len(journal) == 1800, 'Acquisition count')
    heldout = {d['id'] for d in specs if d['split'] == 'test'}
    require(all(r['at'] > seal['at'] for r in journal if r['dataset'] in heldout), 'Seal before held-out acquisition')
    for spec in specs:
        for seed in [11,23,37,53,71]:
            key = f"{spec['id']}_{seed}"
            prefix = read(f'results/v6/prefixes/{key}.json')['state']
            classic = read(f'results/v6/classical/{key}.json')['arms']['centroid_nominal']['state']
            paired = read(f'results/v6/paired/{key}.json')['state']
            for arm in [classic, paired]:
                require(len(arm['ids']) == len(set(arm['ids'])) == 20, 'Paired budget')
                require(arm['ids'][:10] == prefix['ids'] and arm['labels'][:10] == prefix['labels'], 'Paired prefix')
    checks['v6_pairs_with_identical_prefix_and_budget'] = 30
    checks['v6_group_split_and_seal_before_test_acquisitions'] = True
    with (ROOT / 'results/v6/policies.csv').open() as stream: policies = list(csv.DictReader(stream))
    require({r['policy'] for r in policies} == {'never','always','benefit','uncertainty','random_development_rate','random_matched_realized_rate_diagnostic','hindsight_oracle_diagnostic'}, 'Required policies')
    require(all(int(r['cases']) == 15 for r in policies), 'Policy denominator')
    require(next(r for r in policies if r['policy'] == 'hindsight_oracle_diagnostic')['nondeployable'] == 'True', 'Oracle label')
    checks['required_routing_policy_rows'] = 7
    requests = lines('results/v6/requests.jsonl')
    require(len(requests) == 32 and sum(r['namespace'] == 'measured_v6' for r in requests) == 30, 'Real requests and synthetic separation')
    checks['real_v6_requests_measured_only'] = 30
    checks['scope'] = 'Saved-evidence checks, complementing prior numerical/token replay; no inference, acquisitions or fresh-machine reproduction'
    print(json.dumps(checks, indent=2))

if __name__ == '__main__': main()
