"""Seal V72 preparation and verify immutable V71 evidence through snapshots."""
import argparse
import json
from datetime import datetime, timezone
from seal_evidence_v71 import history as previous_history
from seal_evidence_v67 import sha, read, ROOT
ART = ROOT/'artifacts/study_v72'


def history():
    prior = previous_history(); seal = ROOT/'artifacts/study_v71/evidence_manifest.json'
    assert sha(seal) == '6e2a6d6c3b84d31c17a90323eebdba9f3311f85443ad5882ee8375cfa0e313f6'
    files = read(seal)['files']; mapping = read(ART/'previous_snapshot/mapping.json'); redirects = {}
    for name, meta in files.items():
        p = ROOT/name
        if p.exists() and sha(p) == meta['sha256']: continue
        assert name in mapping, name
        old = ROOT/mapping[name]['snapshot_path']; assert sha(old) == meta['sha256'], name
        redirects[name] = str(old.relative_to(ROOT))
    return prior+[{'stage': 71, 'manifest_sha256': sha(seal), 'verified_files': len(files), 'snapshot_redirects': redirects}]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--verify-only', action='store_true'); args = parser.parse_args()
    hist = history(); manifest = ART/'evidence_manifest.json'
    if args.verify_only:
        data = read(manifest)
        for name, meta in data['files'].items():
            p = ROOT/name; assert p.stat().st_size == meta['bytes'] and sha(p) == meta['sha256'], name
        print(json.dumps({'verified': True, 'files': len(data['files']), 'manifest_sha256': sha(manifest), 'historical': hist}, indent=2))
    else:
        assert not manifest.exists()
        paths = {ROOT/n for n in ['STATUS.md', 'README.md', 'THIRD_PARTY.md', 'reports/next_experiment.md', 'artifacts/study_v71/evidence_manifest.json']}
        for pattern in ['artifacts/study_v72/**/*', 'scripts/*v72.py', 'src/escalation/*v72.py', 'tests/**/*v72.py', 'reports/*v72*', 'configs/*v72*']:
            paths.update(p for p in ROOT.glob(pattern) if p.is_file())
        for freeze in ROOT.glob('reports/*v72.freeze.json'):
            paths.update(ROOT/n for n in read(freeze)['sha256'])
        paths = {p for p in paths if '__pycache__' not in p.parts and p != manifest and p.name not in ['seal_creation.log', 'seal_verification.json']}
        data = {'study': 'v72_preparation_no_new_inference', 'sealed_at_utc': datetime.now(timezone.utc).isoformat(), 'historical': hist,
                'files': {str(p.relative_to(ROOT)): {'sha256': sha(p), 'bytes': p.stat().st_size} for p in sorted(paths)}}
        manifest.write_text(json.dumps(data, indent=2)+'\n')
        print(json.dumps({'files': len(paths), 'manifest_sha256': sha(manifest)}, indent=2))
