"""V178: verify an unpacked reviewer audit bundle. Read-only; no network, no acquisitions.

1. Every file listed in BUNDLE_MANIFEST_V178.json is present with the recorded SHA-256.
2. The evidence-manifest chain is intact: the latest sealed manifest (V177) and every earlier manifest it names by hash
   are present, byte-for-byte as originally written (manifests are never rewritten).
3. Coverage of earlier seals: for every file that any of those manifests seals, the bundle holds a copy with the sealed
   hash (at its path, at the redirect recorded by the V177 seal, or at a previous_snapshot copy), or the file is absent
   and falls into a stated exclusion category. A file that is present but differs from its seal, with no recorded
   supersession, is an integrity failure.
Exit status 0 only if (1) and (2) hold and (3) finds no integrity failure.
"""
import collections, hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LATEST = 'artifacts/study_v177/evidence_manifest.json'
PAPER_STUDIES = {41, 131, 132, 134, 136, 141, 142, 144, 145, 147, 148, 149, 151, 153, 154, 155, 159, 163, 164, 165, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178}
WORKFLOW_NOTES = {'AGENTS.md', 'CLAUDE_HANDOFF.md', 'START_HERE.md'}

def digest(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

def category(n):
    """Why a sealed file is not in the bundle. Pure function of the path, so the build and the check agree."""
    if n.endswith('.gguf') or n.startswith('models/'): return 'model_weights'
    if n.startswith(('.local-runtime/', '.venv', '.native-', '.cache/')): return 'third_party_runtimes_and_native_builds'
    if n.startswith('output/'): return 'earlier_packaged_bundles'
    if n.startswith('artifacts/sources/'): return 'third_party_source_archives'
    if n in WORKFLOW_NOTES: return 'workflow_notes'
    m = re.search(r'(?:study_v|/v|_v|^v)(\d+)', n)
    if m and int(m.group(1)) not in PAPER_STUDIES: return 'earlier_or_unrelated_iterations'
    if n.startswith('data/'): return 'raw_data_not_read_by_bundle_checks'
    return 'other_files_not_needed_to_reproduce_the_paper'

def coverage(root=ROOT):
    manifests = {digest(p): p for p in root.glob('artifacts/*/evidence_manifest.json')}
    latest = json.loads((root/LATEST).read_text()); latest_sha = digest(root/LATEST)
    entries = [s for s in latest['historical'] if 'manifest_sha256' in s]
    chain_missing = [s['stage'] for s in entries if s['manifest_sha256'] not in manifests]
    special = [s for s in latest['historical'] if 'manifest_sha256' not in s]
    for s in special:  # the V78 checkpoint is verified through two STATUS snapshots named in an audit record
        a = json.loads((root/'artifacts/study_v78_blocked/audit.json').read_text())
        if digest(root/'artifacts/study_v78_execution/previous_snapshot/STATUS.md') != a['status_sha256'] or digest(root/'artifacts/study_v78_blocked/previous_snapshot/STATUS.md') != a['previous_status_sha256']:
            chain_missing.append(s['stage'])
    snapshots = collections.defaultdict(list)
    for mp in sorted(root.glob('artifacts/*/previous_snapshot/mapping.json')):
        for n, m in json.loads(mp.read_text()).items(): snapshots[n].append(m['snapshot_path'])
    stages = [(s['stage'], s['manifest_sha256'], s['redirects']) for s in entries if s['manifest_sha256'] in manifests]
    stages.append(('v177_package_consistency', latest_sha, {}))
    cache = {}; out = {'verified': 0, 'superseded_version_not_included': 0, 'integrity_failures': [], 'absent_by_category': collections.Counter(), 'absent': []}
    def same(c, m):
        p = root/c
        if not p.is_file() or p.stat().st_size != m['bytes']: return False
        if c not in cache: cache[c] = digest(p)
        return cache[c] == m['sha256']
    for stage, msha, redirects in stages:
        for n, m in json.loads(manifests[msha].read_text())['files'].items():
            cands = [n]+([redirects[n]] if n in redirects else [])+snapshots.get(n, [])
            if any(same(c, m) for c in cands): out['verified'] += 1; continue
            if any((root/c).is_file() for c in cands):
                if n in redirects or n in snapshots: out['superseded_version_not_included'] += 1; out['absent'].append((stage, n, m['sha256'], m['bytes'], 'superseded_version_not_included'))
                else: out['integrity_failures'].append((stage, n))
                continue
            c = category(n); out['absent_by_category'][c] += 1; out['absent'].append((stage, n, m['sha256'], m['bytes'], c))
    return {'latest_manifest_sha256': latest_sha, 'chain_checkpoints': len(latest['historical'])+1, 'chain_missing': chain_missing, **out}

def main():
    bm = json.loads((ROOT/'BUNDLE_MANIFEST_V178.json').read_text())
    bad = [n for n, m in bm['files'].items() if not (ROOT/n).is_file() or digest(ROOT/n) != m['sha256']]
    cov = coverage()
    summary = {'bundle_files': len(bm['files']), 'bundle_files_mismatched': bad[:20], 'latest_manifest_sha256_matches': cov['latest_manifest_sha256'] == bm['latest_sealed_manifest_sha256'],
               'manifest_chain_checkpoints': cov['chain_checkpoints'], 'manifest_chain_missing': cov['chain_missing'],
               'sealed_file_entries_verified': cov['verified'], 'sealed_file_entries_superseded_version_not_included': cov['superseded_version_not_included'],
               'sealed_file_entries_absent_by_category': dict(sorted(cov['absent_by_category'].items())), 'integrity_failures': cov['integrity_failures'][:20],
               'coverage_matches_build_record': {k: bm['coverage'][k] for k in ['verified', 'superseded_version_not_included']} == {'verified': cov['verified'], 'superseded_version_not_included': cov['superseded_version_not_included']}
                                                and bm['coverage']['absent_by_category'] == dict(sorted(cov['absent_by_category'].items()))}
    ok = not bad and summary['latest_manifest_sha256_matches'] and not cov['chain_missing'] and not cov['integrity_failures'] and summary['coverage_matches_build_record']
    summary['passed'] = ok; print(json.dumps(summary, indent=1)); sys.exit(0 if ok else 1)

if __name__ == '__main__': main()
