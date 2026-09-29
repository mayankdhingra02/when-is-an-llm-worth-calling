"""Seal V178 (guard bootstrap with self-verification, environment labelling, repeat-plan feedback correction, Data Availability environment note, V178 audit bundle and its offline test)."""
import argparse, json
from collect_smollm_v47 import ROOT, read, write, sha, now
ART = ROOT/'artifacts/study_v178'; SNAP = ART/'previous_snapshot'
PREV = 'artifacts/study_v177/evidence_manifest.json'; PREV_SHA = 'c11f1318270309e5131ea1c4fe980a5a80bebefc1fc71ff5bb7a2cefeed5cb7e'
def history():
    old = ROOT/PREV; assert sha(old) == PREV_SHA
    stages = read(old)['historical']+[{'stage': 'v177_package_consistency', 'manifest_sha256': PREV_SHA, 'redirects': {}}]
    manifests = {sha(p): p for p in (ROOT/'artifacts').glob('*/evidence_manifest.json')}; mapping = read(SNAP/'mapping.json'); cache = {}; done = []
    def matches(p, m):
        if not p.exists() or p.stat().st_size != m['bytes']: return False
        if p not in cache: cache[p] = sha(p)
        return cache[p] == m['sha256']
    for s in stages:
        if 'manifest_sha256' not in s:
            assert s == {'stage': 'v78_blocked_checkpoint', 'audit_status_verified': True}; a = read(ROOT/'artifacts/study_v78_blocked/audit.json')
            assert sha(ROOT/'artifacts/study_v78_execution/previous_snapshot/STATUS.md') == a['status_sha256'] and sha(ROOT/'artifacts/study_v78_blocked/previous_snapshot/STATUS.md') == a['previous_status_sha256']; done.append(s); continue
        f = manifests[s['manifest_sha256']]; files = read(f)['files']; redirects = {}
        for n, m in files.items():
            ps = [ROOT/n]
            if n in s['redirects']: ps.append(ROOT/s['redirects'][n])
            if n in mapping: ps.append(ROOT/mapping[n]['snapshot_path'])
            match = next((p for p in ps if matches(p, m)), None); assert match is not None, (s['stage'], n)
            if match != ROOT/n: redirects[n] = str(match.relative_to(ROOT))
        done.append({'stage': s['stage'], 'manifest_sha256': sha(f), 'verified_files': len(files), 'redirects': redirects})
    return done
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--verify-only', action='store_true'); args = ap.parse_args(); hist = history(); dest = ART/'evidence_manifest.json'
    from collect_v173 import verify_freeze
    verify_freeze()
    from common_v172 import frozen_hashes
    for n, h in frozen_hashes().items(): assert sha(ROOT/n) == h, n
    for n, m in read(SNAP/'mapping.json').items(): assert sha(ROOT/m['snapshot_path']) == m['sha256'], n
    if args.verify_only:
        d = read(dest)
        for n, m in d['files'].items(): assert sha(ROOT/n) == m['sha256'] and (ROOT/n).stat().st_size == m['bytes'], n
        print(json.dumps({'verified': True, 'files': len(d['files']), 'manifest_sha256': sha(dest), 'historical_checkpoints': len(hist)})); return
    assert not dest.exists(); names = ['.gitignore', 'STATUS.md', 'README.md', 'THIRD_PARTY.md', 'CLAUDE_HANDOFF.md', 'reports/next_experiment.md', 'BUNDLE_V178_README.md', 'TABLE_MAP_V178.md',
                                       'output/llm_escalation_audit_v178.zip', PREV]; paths = {ROOT/n for n in names}
    for folder in ['scripts', 'reports', 'configs', 'tests/synthetic']: paths.update(p for p in (ROOT/folder).glob('*v178*') if p.is_file())
    for folder in ['artifacts/study_v178', 'paper/overleaf_v173']: paths.update(p for p in (ROOT/folder).rglob('*') if p.is_file())
    paths = {p for p in paths if p != dest and p.name not in ['seal_creation.log', 'seal_verification.json'] and '__pycache__' not in p.parts and p.suffix != '.gguf'}
    write(dest, {'at': now(), 'scope': 'V178: offline guard moved to a bootstrap that installs and self-verifies the guard in every command process (the V176/V177 sitecustomize route can be shadowed by a host start-up module); runner environment labelling (reference vs non-reference) and child-process logging; repeat-plan revision 3 (loop arms use their own labels as round-by-round feedback); one Data Availability sentence on exact vs numerical reproduction; V178 audit bundle and its offline tests, including a shadowing-host test. Zero acquisitions, model requests or dataset/model downloads.',
                 'historical': hist, 'files': {str(p.relative_to(ROOT)): {'sha256': sha(p), 'bytes': p.stat().st_size} for p in sorted(paths)}})
    print(json.dumps({'files': len(paths), 'manifest_sha256': sha(dest), 'historical_checkpoints': len(hist)}))
if __name__ == '__main__': main()
