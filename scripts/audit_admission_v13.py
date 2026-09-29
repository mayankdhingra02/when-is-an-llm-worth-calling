"""Execute the frozen metadata audit without reading objective-table contents."""
import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from escalation.admission_v13 import audit_registry, exposed_groups, validate_prospective_split


def read(name):
    return json.loads((ROOT / name).read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ledger = ROOT / 'artifacts/resource_ledger_v2.json'
    before = sha(ledger)
    # V13 metadata only. Older freezes are verified by the separate review audit;
    # this entry point never opens a CSV objective table, even just for hashing.
    freeze = read('reports/protocol_v13_admission.freeze.json')
    for name, expected in freeze['sha256'].items():
        assert not name.endswith('.csv'), 'Objective CSV access prohibited by this audit'
        assert sha(ROOT / name) == expected, f'Frozen input changed: {name}'
    registry = read('data/registry_v5.json')
    evidence = read('data/admission_evidence_v13.json')
    for entry in evidence.values():
        assert sha(ROOT / entry['readme']) == entry['sha256']
    exposed = exposed_groups(read('data/manifest_v3.json'), read('data/manifest_v6.json'))
    report = audit_registry(registry, exposed, evidence, read('configs/task_contract_v13.json'))
    # Check the conservative grouping independently against the four source rows.
    size_rows = [r for r in report['records'] if r['has_size_metadata']]
    assert len(report['records']) == 81
    assert len(size_rows) == 4
    assert {r['system_group'] for r in size_rows} == {'brotli', 'lrzip', 'libvpx'}
    assert all(r['system_group'] in exposed for r in size_rows)
    assert report['summary']['prospective_ready_families'] == []
    for group in ('brotli', 'lrzip', 'libvpx'):
        try:
            validate_prospective_split([{'system_group': group, 'split': 'test'}], exposed, {group})
        except ValueError as error:
            assert 'Previously exposed' in str(error)
        else:
            raise AssertionError('Exposure guard failed')
    assert sha(ledger) == before
    out = ROOT / 'results/v13_admission'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'summary.json').write_text(json.dumps(report, indent=2) + '\n')
    with (out / 'checklist.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=['dataset_id', 'system_group', 'size_column', 'unexposed_family', 'prospective_ready', 'blockers'])
        writer.writeheader()
        for row in report['records']:
            writer.writerow({'dataset_id': row['dataset_id'], 'system_group': row['system_group'],
                             'size_column': row['has_size_metadata'],
                             'unexposed_family': row['checks']['family_unexposed'],
                             'prospective_ready': row['prospective_evaluation_ready'],
                             'blockers': ';'.join(row['blockers'])})
    verification = {'verified': True, 'frozen_files': len(freeze['sha256']),
                    'summary': report['summary'], 'no_objective_csv_opened': True,
                    'ledger_unchanged_sha256': before,
                    'new_model_requests': 0, 'new_objective_acquisitions': 0,
                    'scope': 'metadata admission and split guard; no optimizer or model experiment'}
    destination = ROOT / 'artifacts/study_v13/verification.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(verification, indent=2) + '\n')
    print(json.dumps(verification, indent=2))


if __name__ == '__main__':
    main()
