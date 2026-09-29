"""Independent, read-only reproduction of V52 feature counts and evidence seals."""
import collections
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    for seal in ['reports/protocol_v52_admission.freeze.json',
                 'artifacts/study_v52/execution.freeze.json']:
        for p, expected in json.loads((ROOT / seal).read_text())['files'].items():
            assert digest(ROOT / p) == expected, p
    saved = json.loads((ROOT / 'results/v52_admission/summary.json').read_text())
    registry = json.loads((ROOT / 'data/registry_v5.json').read_text())['datasets']
    d = next(x for x in registry if x['dataset_id'] == 'MOOT/dconvert')
    contracts = collections.defaultdict(set)
    fixed = [f for f in d['schema']['feature_names'] if f != 'threads']
    with (ROOT / d['path']).open(newline='') as f:
        for r in csv.DictReader(f):
            # No objective cell is indexed, converted or used in a branch.
            contracts[tuple(float(r[k]) for k in fixed)].add(float(r['threads']))
    result = saved['computed_feature_checks']['dconvert']
    assert len(contracts) == result['utility_contracts']
    assert sum(map(len, contracts.values())) == result['unique_configurations']
    assert max(map(len, contracts.values())) == result['largest_contract_configurations']
    assert dict(collections.Counter(map(len, contracts.values()))) == {
        int(k): v for k, v in result['contract_size_histogram'].items()}
    reserved = {'mongodb', 'redis', 'storm'}
    assert len(saved['families']) == 8
    for family in saved['families']:
        for gate in family['gates'].values():
            for evidence in gate['evidence']:
                assert (ROOT / evidence).is_file(), evidence
        expected = all(g['status'] == 'verified' for g in family['gates'].values())
        assert family['eligible'] == expected
        assert (family['split_reservation'] == 'future_evaluation') == (family['group'] in reserved)
    assert saved['eligible_families'] == []
    assert saved['recorded_objective_acquisitions'] == saved['physical_trials'] == saved['model_requests'] == 0
    print('PASS: both freezes, source references, independent feature counts, all8 gates/splits; zero objective acquisitions.')


if __name__ == '__main__':
    main()
