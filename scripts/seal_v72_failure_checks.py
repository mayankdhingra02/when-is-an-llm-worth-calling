"""Read-only verification of V72 plus subsequent synthetic failure checks."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from seal_evidence_v72 import history
from seal_evidence_v67 import ROOT, read, sha

ART = ROOT/'artifacts/study_v72_failure_checks'


def historical():
    previous = history(); seal = ROOT/'artifacts/study_v72/evidence_manifest.json'
    assert sha(seal) == '7a0eda82544ca48ebf41861de2ac31f325d91f1faa5aca1be570f3fe87382a11'
    mapping = read(ART/'previous_snapshot/mapping.json'); redirects = {}
    for name, meta in read(seal)['files'].items():
        path = ROOT/name
        if path.exists() and sha(path) == meta['sha256']: continue
        assert name in mapping, name
        path = ROOT/mapping[name]['snapshot_path']; assert sha(path) == meta['sha256'], name
        redirects[name] = str(path.relative_to(ROOT))
    return previous+[{'stage': 'v72_preparation', 'manifest_sha256': sha(seal), 'verified_files': len(read(seal)['files']), 'snapshot_redirects': redirects}]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--verify-only', action='store_true'); args = parser.parse_args()
    hist = historical(); manifest = ART/'evidence_manifest.json'
    if args.verify_only:
        record = read(manifest)
        for name, meta in record['files'].items():
            path = ROOT/name; assert sha(path) == meta['sha256'] and path.stat().st_size == meta['bytes'], name
        print(json.dumps({'verified': True, 'files': len(record['files']), 'manifest_sha256': sha(manifest), 'historical': hist}, indent=2))
    else:
        assert not manifest.exists()
        paths = {ROOT/'STATUS.md', ROOT/'tests/synthetic/test_runner_v72_failure_paths.py', Path(__file__)}
        paths.update(p for p in ART.rglob('*') if p.is_file() and p.name not in ['seal_creation.log', 'seal_verification.json'])
        record = {'scope': 'Synthetic orchestration validation only; no research calls', 'at': datetime.now(timezone.utc).isoformat(), 'historical': hist,
                  'files': {str(p.relative_to(ROOT)): {'sha256': sha(p), 'bytes': p.stat().st_size} for p in sorted(paths)}}
        manifest.write_text(json.dumps(record, indent=2)+'\n'); print(json.dumps({'files': len(paths), 'manifest_sha256': sha(manifest)}, indent=2))
