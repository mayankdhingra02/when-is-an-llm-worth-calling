"""Seal completed V59 evidence and explicit, family-grouped data lineage once."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    artifact = ROOT / 'artifacts/study_v59'
    seal_path = artifact / 'evidence_manifest.json'
    if seal_path.exists():
        raise FileExistsError('Preserve the completed evidence seal')
    physical = ROOT / 'results/v59_workload_physical'
    screen = ROOT / 'results/v59_workload_screen'
    summary = read(physical / 'summary.json')
    assert summary['complete_table'] and summary['attempted'] == 576
    verification = read(artifact / 'verification.json')
    assert verification['verified'] and verification['charged_acquisitions'] == 800
    assert verification['arms'] == 60 and verification['reconstructed_choices'] == 720
    freeze_path = ROOT / 'reports/protocol_v59_workload_screen.freeze.json'
    freeze = read(freeze_path)
    for name, expected in freeze['sha256'].items():
        assert digest(ROOT / name) == expected, name
    approval = read(artifact / 'approval_receipt.json')
    assert approval == read(ROOT / 'configs/authorization_v59.json')
    assert approval['authorized'] and approval['protocol_freeze_sha256'] == digest(freeze_path)
    old_mapping = read(artifact / 'previous_snapshot/mapping.json')
    old_seal = read(ROOT / 'artifacts/study_v58/evidence_manifest.json')
    for name, entry in old_mapping.items():
        assert digest(ROOT / entry['snapshot_path']) == entry['historical_v58_sha256']
        assert old_seal['files'][name]['sha256'] == entry['historical_v58_sha256']
    metadata = read(ROOT / 'artifacts/study_v57/workload_metadata.json')
    sources = read(ROOT / 'artifacts/sources/v57/manifest.json')
    entries = []
    for workload in read(screen / 'summary.json')['workloads']:
        family, name = workload['family'], workload['workload']
        table = screen / f'{family}_{name}' / 'table.json'
        entries.append({
            'family_group': family, 'workload': name, 'split': 'development_only',
            'related_variants_and_seeds_are_one_group': True,
            'table_path': str(table.relative_to(ROOT)), 'table_sha256': digest(table),
            'configurations': 48, 'physical_repetitions': 3,
            'objective': ('median of three final harness milliseconds' if family == 'javagc'
                          else 'median of three whole-process exit-wall milliseconds'),
            'failure_penalty_ms': 120000 if family == 'javagc' else 60000,
            'utility': ('owner validation and predeclared repeated-reference output SHA256'
                        if family == 'javagc' else 'independently valid goal-achieving plan, cost105'),
        })
    lineage = {
        'study': 'v59', 'independent_family_groups': 2, 'held_out_groups': 0,
        'workloads': entries, 'predeclared_workload_metadata': metadata,
        'new_task_source_receipts_from_v57': sources,
        'all_runtime_source_input_pins': str(freeze_path.relative_to(ROOT)),
        'protocol_freeze_sha256': digest(freeze_path),
        'physical_raw_journal_sha256': digest(physical / 'trials.jsonl'),
        'physical_intended': 576, 'physical_attempted': summary['attempted'],
        'physical_valid': summary['valid'], 'recorded_acquisitions': 800,
        'prior_failed_admission': 'V57 p20: three CPU timeouts; not an LLM-negative result',
        'not_a_historical_timing_replication': True, 'new_model_requests': 0,
        'external_spend_usd': 0, 'dataset_redistribution_permission': 'unresolved; local only',
    }
    manifest_path = ROOT / 'data/live_manifest_v59.json'
    write(manifest_path, lineage)
    selected = set()
    for directory in [physical, screen, artifact]:
        selected.update(p for p in directory.rglob('*') if p.is_file()
                        and p.name not in ['evidence_manifest.json', 'evidence_manifest.sha256',
                                           'seal.log', 'seal_verification.json'])
    # Include frozen source/input files themselves, not just a transitive reference.
    selected.update(ROOT / name for name in freeze['sha256'])
    selected.update(ROOT / name for name in [
        'reports/protocol_v59_workload_screen.freeze.json', 'reports/workload_screen_v59.md',
        'configs/authorization_v59.json', 'data/live_manifest_v59.json',
        'scripts/progress_workloads_v59.py', 'scripts/verify_workloads_v59.py',
        'scripts/report_workloads_v59.py', 'scripts/manifest_workloads_v59.py',
        'STATUS.md', 'README.md', 'reports/next_experiment.md', 'THIRD_PARTY.md',
        'requirements.lock.txt',
    ])
    rows = read(physical / 'all_cases.json')
    selected.update(ROOT / r['retained_output_path'] for r in rows if r.get('output_retained'))
    obj = {'study': 'v59', 'sealed_at_utc': datetime.now(timezone.utc).isoformat(),
           'files': {str(p.relative_to(ROOT)): {'sha256': digest(p), 'bytes': p.stat().st_size}
                     for p in sorted(selected)}}
    write(seal_path, obj)
    seal_path.with_suffix('.sha256').write_text(digest(seal_path) + '\n')
    print(json.dumps({'files': len(obj['files']), 'manifest_sha256': digest(seal_path)}, indent=2))


if __name__ == '__main__':
    main()
