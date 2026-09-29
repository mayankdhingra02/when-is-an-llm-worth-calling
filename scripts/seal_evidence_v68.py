"""Seal V68 and preserve V67 and earlier evidence with explicit redirects."""
import argparse
import json
from datetime import datetime, timezone
from seal_evidence_v67 import old_history, sha, read, ROOT

ART = ROOT / 'artifacts/study_v68'


def history():
    previous = old_history()
    seal = ROOT / 'artifacts/study_v67/evidence_manifest.json'
    assert sha(seal) == '1a5f15214c4698476a1647997793a5342443f778bf93600311c6204a0d05b10f'
    files = read(seal)['files']
    mapping = read(ART / 'previous_snapshot/mapping.json')
    redirects = {}
    for name, meta in files.items():
        path = ROOT / name
        if path.exists() and sha(path) == meta['sha256']: continue
        assert name in mapping, name
        archived = ROOT / mapping[name]['snapshot_path']
        assert sha(archived) == meta['sha256'], name
        redirects[name] = str(archived.relative_to(ROOT))
    return previous + [{'stage': 67, 'manifest_sha256': sha(seal),
        'verified_files': len(files), 'snapshot_redirects': redirects}]


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args(); hist = history()
    seal = ART / 'evidence_manifest.json'
    if args.verify_only:
        data = read(seal)
        for name, meta in data['files'].items():
            p = ROOT / name
            assert p.stat().st_size == meta['bytes'] and sha(p) == meta['sha256'], name
        print(json.dumps({'verified': True, 'files': len(data['files']),
            'manifest_sha256': sha(seal), 'historical': hist}, indent=2)); return
    assert not seal.exists()
    paths = {ROOT / name for name in ['STATUS.md', 'README.md', 'THIRD_PARTY.md',
        'reports/next_experiment.md', 'requirements.lock.txt', 'artifacts/study_v67/evidence_manifest.json']}
    for pattern in ['artifacts/study_v68/**/*', 'artifacts/sources/v68/**/*',
        'results/v68*/**/*', 'scripts/*v68.py', 'src/escalation/*v68.py',
        'tests/synthetic/*v68.py', 'reports/*v68*']:
        paths.update(p for p in ROOT.glob(pattern) if p.is_file())
    paths = {p for p in paths if '__pycache__' not in p.parts and p != seal
        and p.name not in ['seal_creation.log', 'seal_verification.json']}
    result = {'study': 'v68_source_admission_complete', 'historical': hist,
        'sealed_at_utc': datetime.now(timezone.utc).isoformat(),
        'files': {str(p.relative_to(ROOT)): {'sha256': sha(p), 'bytes': p.stat().st_size} for p in sorted(paths)}}
    seal.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'files': len(paths), 'manifest_sha256': sha(seal)}, indent=2))


if __name__ == '__main__': main()
