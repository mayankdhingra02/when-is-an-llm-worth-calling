"""Verify unchanged V72 preparation and its blocked-status checkpoint."""
import json
from seal_v72_failure_checks import historical
from seal_evidence_v67 import ROOT, read, sha

if __name__ == '__main__':
    previous = historical()
    art = ROOT/'artifacts/study_v72_blocked'
    audit = read(art/'audit.json')
    manifest = ROOT/'artifacts/study_v72_failure_checks/evidence_manifest.json'
    assert sha(manifest) == audit['prior_seal_sha256']
    files = read(manifest)['files']
    for name, meta in files.items():
        path = art/'previous_STATUS.md' if name == 'STATUS.md' else ROOT/name
        assert sha(path) == meta['sha256'] and path.stat().st_size == meta['bytes'], name
    assert sha(ROOT/'STATUS.md') == audit['current_status_sha256']
    assert sha(art/'previous_STATUS.md') == audit['previous_status_sha256']
    print(json.dumps({'verified': True, 'latest_files': len(files), 'historical': previous,
                      'blocked_audit': audit}, indent=2))
