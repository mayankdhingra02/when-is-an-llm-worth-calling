"""Seal executed V72 evidence and verify prior snapshots without changing them."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT/'artifacts/study_v72_execution'
PRIOR = {
    'study_v58': '0382297f307b192585d78696446ecd10ae15f014da95f82670a57a50232b4be2',
    'study_v59': '041edb1cf956540e8b73ea6a21fe109017d652bbfedf4a84e74361defb434890',
    'study_v65': 'd93e0f5ecf6d35c5a471ddafb9b45f82e70111772d975a089a499e3e42f227f3',
    'study_v67': '1a5f15214c4698476a1647997793a5342443f778bf93600311c6204a0d05b10f',
    'study_v68': '8bf33a61e9164379bd07bf710b8a9f30d0ec704fa5292d634cd9db5804aab8ad',
    'study_v69': '5daedbc21c1d3a918d078d332b77a73d9e754bdf33c6cf70deda094f5c6c04f5',
    'study_v71': '6e2a6d6c3b84d31c17a90323eebdba9f3311f85443ad5882ee8375cfa0e313f6',
    'study_v72': '7a0eda82544ca48ebf41861de2ac31f325d91f1faa5aca1be570f3fe87382a11',
    'study_v72_failure_checks': '4ca53f476f751cf28a7ddfefc36a5c96b09580eb139cc695c3d8235cdc793125',
}

def read(path): return json.loads(path.read_text())
@lru_cache(maxsize=None)
def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for data in iter(lambda: f.read(1024*1024), b''): h.update(data)
    return h.hexdigest()


def history():
    candidates = {}
    for mapping in (ROOT/'artifacts').glob('*/previous_snapshot/mapping.json'):
        for name, meta in read(mapping).items():
            if isinstance(meta, dict) and 'snapshot_path' in meta:
                candidates.setdefault(name, []).append(ROOT/meta['snapshot_path'])
    candidates.setdefault('STATUS.md', []).append(ROOT/'artifacts/study_v72_blocked/previous_STATUS.md')
    histories = []
    for stage, digest in PRIOR.items():
        manifest = ROOT/f'artifacts/{stage}/evidence_manifest.json'
        assert sha(manifest) == digest, str(manifest)
        redirects = {}; files = read(manifest)['files']
        for name, meta in files.items():
            actual = ROOT/name
            if actual.exists() and sha(actual) == meta['sha256']: continue
            matches = [p for p in candidates.get(name, []) if p.exists() and sha(p) == meta['sha256']]
            assert matches, f'No exact historical content: {stage}: {name}'
            redirects[name] = str(matches[0].relative_to(ROOT))
        histories.append({'stage': stage, 'manifest_sha256': digest, 'verified_files': len(files), 'redirects': redirects})
    audit = read(ROOT/'artifacts/study_v72_blocked/audit.json')
    assert sha(ART/'previous_snapshot/STATUS.md') == audit['current_status_sha256']
    return histories


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--verify-only', action='store_true'); args = parser.parse_args()
    hist = history(); manifest = ART/'evidence_manifest.json'
    if args.verify_only:
        record = read(manifest)
        for name, meta in record['files'].items():
            p = ROOT/name; assert p.stat().st_size == meta['bytes'] and sha(p) == meta['sha256'], name
        print(json.dumps({'verified': True, 'files': len(record['files']), 'manifest_sha256': sha(manifest), 'historical': hist}, indent=2))
    else:
        assert not manifest.exists()
        paths = {ROOT/n for n in ['STATUS.md', 'README.md', 'THIRD_PARTY.md', 'reports/next_experiment.md']}
        for pattern in ['artifacts/study_v72_execution/**/*', 'results/v72*/**/*', 'scripts/*v72*.py',
                        'src/escalation/*v72*.py', 'tests/**/*v72*.py', 'reports/*v72*', 'configs/*v72*', 'artifacts/study_v72_blocked/*']:
            paths.update(p for p in ROOT.glob(pattern) if p.is_file())
        for freeze in ROOT.glob('reports/*v72.freeze.json'): paths.update(ROOT/n for n in read(freeze)['sha256'])
        paths.update(ROOT/f'artifacts/{stage}/evidence_manifest.json' for stage in PRIOR)
        paths = {p for p in paths if '__pycache__' not in p.parts and p != manifest and p.name not in ['seal_creation.log','seal_verification.json']}
        record = {'study': 'v72_executed_paired_local_model', 'sealed_at_utc': datetime.now(timezone.utc).isoformat(), 'historical': hist,
                  'files': {str(p.relative_to(ROOT)): {'sha256': sha(p), 'bytes': p.stat().st_size} for p in sorted(paths)}}
        manifest.write_text(json.dumps(record, indent=2)+'\n')
        print(json.dumps({'files': len(paths), 'manifest_sha256': sha(manifest)}, indent=2))
