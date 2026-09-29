"""Seal V78 real execution and verify older checkpoints via exact snapshots."""
import argparse
import json
from datetime import datetime, timezone
from seal_v78_failure_checks import ROOT, sha, read, history as older_history

ART = ROOT / 'artifacts/study_v78_execution'

def history():
    prior = older_history()
    manifest = ROOT / 'artifacts/study_v78_failure_checks/evidence_manifest.json'
    assert sha(manifest) == '0254302037b3d8ac548bbea8f5ac8e44ed119c850594b751da4d916015675999'
    mapping = read(ART / 'previous_snapshot/mapping.json')
    redirects = {}
    files = read(manifest)['files']
    for name, meta in files.items():
        path = ROOT / name
        if path.exists() and sha(path) == meta['sha256']:
            continue
        if name == 'STATUS.md':
            path = ROOT / 'artifacts/study_v78_blocked/previous_snapshot/STATUS.md'
        else:
            assert name in mapping, name
            path = ROOT / mapping[name]['snapshot_path']
        assert sha(path) == meta['sha256'] and path.stat().st_size == meta['bytes'], name
        redirects[name] = str(path.relative_to(ROOT))
    audit = read(ROOT / 'artifacts/study_v78_blocked/audit.json')
    assert sha(ART / 'previous_snapshot/STATUS.md') == audit['status_sha256']
    assert sha(ROOT / 'artifacts/study_v78_blocked/previous_snapshot/STATUS.md') == audit['previous_status_sha256']
    return prior + [{'stage': 'v78_failure_checks', 'manifest_sha256': sha(manifest),
                     'verified_files': len(files), 'redirects': redirects},
                    {'stage': 'v78_blocked_checkpoint', 'audit_status_verified': True}]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    hist = history()
    freeze = ROOT / 'reports/protocol_v78.freeze.json'
    assert sha(freeze) == '59766c399b902a0e9f9eb5f785e2eb5350e383810e368de53467fce3a3bdd440'
    pins = read(freeze)['sha256']
    for name, digest in pins.items():
        assert sha(ROOT / name) == digest, name
    supplementary = read(ROOT / 'artifacts/study_v78_failure_checks/supplementary_code_pins.json')
    for name, digest in supplementary['sha256'].items():
        assert sha(ROOT / name) == digest, name
    manifest = ART / 'evidence_manifest.json'
    if args.verify_only:
        data = read(manifest)
        for name, meta in data['files'].items():
            path = ROOT / name
            assert sha(path) == meta['sha256'] and path.stat().st_size == meta['bytes'], name
        print(json.dumps({'verified': True, 'files': len(data['files']),
                          'manifest_sha256': sha(manifest), 'frozen_collection_unchanged': True,
                          'historical': hist}, indent=2))
        return
    assert not manifest.exists(), 'Never overwrite a seal'
    names = ['STATUS.md', 'README.md', 'reports/next_experiment.md', 'reports/kanzi_v78.md',
             'scripts/seal_v78_execution.py', 'scripts/report_kanzi_v78.py', 'scripts/diagnose_kanzi_v78.py',
             'scripts/verify_blocked_v78.py', 'reports/protocol_v78.freeze.json',
             'artifacts/study_v78_failure_checks/evidence_manifest.json',
             'artifacts/study_v78_failure_checks/supplementary_code_pins.json']
    paths = {ROOT / name for name in names + list(pins) + list(supplementary['sha256'])}
    for directory in [ART, ROOT / 'artifacts/study_v78_blocked',
                      ROOT / 'results/v78_kanzi_paired', ROOT / 'results/v78_kanzi_analysis',
                      ROOT / 'results/v78_preset_diagnostic']:
        paths.update(path for path in directory.rglob('*') if path.is_file())
    paths = {p for p in paths if p != manifest and p.name not in ['seal_creation.log', 'seal_verification.json']
             and '__pycache__' not in p.parts}
    manifest.write_text(json.dumps({'scope': 'V78 actual real-model/native paired collection and explicitly post-hoc descriptive diagnostics',
        'sealed_at': datetime.now(timezone.utc).isoformat(), 'historical': hist,
        'files': {str(p.relative_to(ROOT)): {'sha256': sha(p), 'bytes': p.stat().st_size} for p in sorted(paths)}}, indent=2) + '\n')
    print(json.dumps({'files': len(paths), 'manifest_sha256': sha(manifest)}))

if __name__ == '__main__':
    main()
