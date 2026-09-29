"""Preserve historical evidence through explicit snapshots and seal V60–V65."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'artifacts/study_v65'
def read(p): return json.loads(p.read_text())
def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''): h.update(b)
    return h.hexdigest()


def history():
    mappings = [read(ROOT / f'artifacts/study_v{v}/previous_snapshot/mapping.json') for v in [59, 60]]
    summary = []
    for stage, expected in [(58, '0382297f307b192585d78696446ecd10ae15f014da95f82670a57a50232b4be2'), (59, '041edb1cf956540e8b73ea6a21fe109017d652bbfedf4a84e74361defb434890')]:
        seal = ROOT / f'artifacts/study_v{stage}/evidence_manifest.json'
        assert sha(seal) == expected
        old = read(seal)['files']
        redirects = {}
        for name, meta in old.items():
            path = ROOT / name
            if path.exists() and sha(path) == meta['sha256']: continue
            matches = [ROOT / mapping[name]['snapshot_path'] for mapping in mappings if name in mapping and sha(ROOT / mapping[name]['snapshot_path']) == meta['sha256']]
            assert matches, f'Historical evidence changed without exact snapshot: {name}'
            redirects[name] = str(matches[0].relative_to(ROOT))
        summary.append({'stage': stage, 'seal_sha256': expected, 'verified_files': len(old), 'snapshot_redirects': redirects})
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    hist = history()
    manifest = ART / 'evidence_manifest.json'
    if args.verify_only:
        data = read(manifest)
        for name, meta in data['files'].items():
            assert sha(ROOT / name) == meta['sha256'], name
            assert (ROOT / name).stat().st_size == meta['bytes'], name
        print(json.dumps({'verified': True, 'files': len(data['files']), 'manifest_sha256': sha(manifest), 'historical': hist}, indent=2))
        return
    assert not manifest.exists(), 'Do not overwrite a seal'
    paths = {ROOT / p for p in ['STATUS.md', 'README.md', 'THIRD_PARTY.md', 'reports/next_experiment.md', 'requirements.lock.txt', 'data/live_manifest_v60_v63.json', 'data/live_manifest_v60_v65.json']}
    patterns = [
        'artifacts/study_v6[0-5]/**/*', 'artifacts/sources/v60/**/*', 'artifacts/sources/v62/**/*',
        'artifacts/synthetic_v61_reply_guard/**/*', 'data/generated_v6[23]/**/*',
        'results/v6[0-5]*/**/*', 'scripts/*v6[0-5].py', 'src/escalation/*v6[0-5].py',
        'tests/synthetic/*v6[0-5].py', 'reports/*v6[0-5]*', 'configs/study_v65.json',
    ]
    for pattern in patterns: paths.update(p for p in ROOT.glob(pattern) if p.is_file())
    for freeze in ROOT.glob('reports/protocol_v6[0-5]*.freeze.json'):
        paths.update(ROOT / name for name in read(freeze)['sha256'])
    paths = {p for p in paths if '__pycache__' not in p.parts and p != manifest and p.name not in ['seal_verification.json', 'seal_creation.log']}
    assert all(p.is_file() for p in paths)
    data = {'studies': 'v60_v65_complete', 'sealed_at_utc': datetime.now(timezone.utc).isoformat(), 'historical': hist, 'files': {str(p.relative_to(ROOT)): {'sha256': sha(p), 'bytes': p.stat().st_size} for p in sorted(paths)}}
    manifest.write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps({'files': len(paths), 'manifest_sha256': sha(manifest), 'historical': hist}, indent=2))


if __name__ == '__main__': main()
