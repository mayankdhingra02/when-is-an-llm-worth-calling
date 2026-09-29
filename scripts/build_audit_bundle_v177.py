"""V177: build the offline reviewer audit bundle (output/llm_escalation_audit_v177.zip).

Selection = files the bundle's own command suite reads (artifacts/study_v177/traced_inputs.json, from
trace_inputs_v177.py) + all project code, configs, reports, the manuscript, every evidence manifest, freeze record and
previous_snapshot, the small artifact/result directories of the studies behind the paper, and a few licence files.
Hard exclusions: model weights, credentials, runtimes and native build trees (except ALLOWED_HIDDEN), earlier bundles,
caches and agent workflow notes. The build aborts if any staged file matches a credential pattern.

    .venv/bin/python scripts/build_audit_bundle_v177.py --scratch DIR [--private-string S ...]

--private-string values (e.g. an e-mail address) are only counted, never written anywhere.
"""
import argparse, hashlib, json, os, re, shutil, sys, zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from trace_inputs_v177 import ALLOWED_HIDDEN
from reproduce_bundle_v177 import TESTS
import verify_bundle_v177 as vb

ROOT = Path(__file__).resolve().parents[1]
NAME = 'llm-escalation-audit-v177'; ZIP = ROOT/'output/llm_escalation_audit_v177.zip'; ART = ROOT/'artifacts/study_v177'
TREES = ['scripts', 'src', 'configs', 'reports', 'paper/overleaf_v173', 'artifacts/history']
TOP = ['README.md', 'THIRD_PARTY.md', 'SOURCES.md', 'RESEARCH_BRIEF.md', 'REPRODUCE.md', 'STATUS.md', 'pyproject.toml', 'requirements.lock.txt', '.gitignore',
       'BUNDLE_V177_README.md', 'TABLE_MAP_V177.md']
STUDIES = sorted(vb.PAPER_STUDIES)
RESULT_DIRS = ['v141_analysis', 'v141_models', 'v142_smollm', 'v144_models', 'v144_spark', 'v145_models', 'v145_spark', 'v148_hadoop', 'v148_models', 'v151_router',
               'v153_models', 'v154_controllers', 'v155_gp', 'v159_models', 'v163_models', 'v164_models', 'v168_models', 'v171_audit', 'v172_analysis', 'v172_eval',
               'v172_models', 'v173_analysis', 'v173_eval', 'v173_models', 'v174_revision', 'v175_revision',
               # complete native measurement records, including logs whose verifiers need runtimes not in the bundle
               'v131_proposals', 'v132_router', 'v134_attribution', 'v136_feedback',
               'v41_transfer', 'v153_native', 'v159_native', 'v163_native', 'v164_native', 'v165_headroom', 'v168_native', 'v169_ezr', 'v170_ezr']
EXTRA = ['artifacts/study_v78_blocked/audit.json', 'artifacts/sources/ezr_LICENSE.md']
SMALL = 5_000_000
HARD_EXCLUDE = ('models/', 'output/', '.git/', '.venv', '.cache/', '.claude/', '.pytest_cache/')
SECRETS = [rb'sk-or-v1-[0-9a-f]{16,}', rb'sk-(?:proj-|ant-)?[A-Za-z0-9_-]{40,}', rb'hf_[A-Za-z0-9]{30,}', rb'AKIA[0-9A-Z]{16}', rb'-----BEGIN [A-Z ]*PRIVATE KEY-----',
           rb'gh[pousr]_[A-Za-z0-9]{36}', rb'xox[baprs]-[A-Za-z0-9-]{10,}', rb'Bearer [A-Za-z0-9._-]{20,}']
# Reviewed false positives, pinned by path, pattern and exact file hash: CPython 3.10.13's ssl docs show a PEM layout
# whose key body is the placeholder "... (private key in base64 encoding) ...". Any other hit aborts the build.
REVIEWED = {('.native-v160/search_corpus/Doc/library/ssl.rst', rb'-----BEGIN [A-Z ]*PRIVATE KEY-----'): '5303055924284cf02a064d3197b604ce613220479fff4856f2227e893d918746'}

def digest(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

def allowed(n):
    if n.startswith(HARD_EXCLUDE) or n.endswith(('.gguf', '.pyc')) or '__pycache__' in n or n.endswith('.DS_Store') or n in vb.WORKFLOW_NOTES: return False
    if n.startswith(('.local-runtime/', '.native-')): return any(n == a or n.startswith(a+'/') for a in ALLOWED_HIDDEN)
    return not n.startswith('.') or n == '.gitignore'

def select(traced):
    files = set(traced['reads'])
    for t in TREES: files |= {str(p.relative_to(ROOT)) for p in (ROOT/t).rglob('*') if p.is_file()}
    files |= {f'tests/synthetic/{t}' for t in TESTS+['test_ezr_v169.py']} | set(TOP) | set(EXTRA)
    files |= {str(p.relative_to(ROOT)) for p in ROOT.glob('artifacts/*/evidence_manifest.json')}
    files |= {str(p.relative_to(ROOT)) for p in ROOT.glob('artifacts/*/previous_snapshot/**/*') if p.is_file()}
    files |= {str(p.relative_to(ROOT)) for p in ROOT.glob('artifacts/*/**/*freeze*') if p.is_file()}
    latest = json.loads((ROOT/vb.LATEST).read_text())  # every earlier-version copy the latest seal redirects to (old STATUS/README snapshots)
    files |= {r for s in latest['historical'] for r in s.get('redirects', {}).values()}
    for v in STUDIES:
        for d in ROOT.glob(f'artifacts/study_v{v}'):
            files |= {str(p.relative_to(ROOT)) for p in d.rglob('*') if p.is_file() and p.stat().st_size <= SMALL}
    for r in RESULT_DIRS: files |= {str(p.relative_to(ROOT)) for p in (ROOT/'results'/r).rglob('*') if p.is_file()}
    for a in ALLOWED_HIDDEN:
        p = ROOT/a
        if p.is_file(): files.add(a)
    files |= {str(p.relative_to(ROOT)) for p in ROOT.glob('artifacts/sources/v146/**/*') if p.is_file() and re.search(r'licen[cs]e|copying', p.name, re.I)}
    skip = {'artifacts/study_v177/bundle_receipt.json', 'artifacts/study_v177/evidence_manifest.json', 'artifacts/study_v177/BUNDLE_MANIFEST_V177.json',
            'artifacts/study_v177/EXCLUDED_FROM_BUNDLE_V177.tsv', 'artifacts/study_v177/requirements-bundle-v177.txt'}
    # records about the bundle itself (receipt, test result, seal) live outside it
    return sorted(n for n in files if allowed(n) and (ROOT/n).is_file() and n not in skip and not n.startswith(('artifacts/study_v177/seal', 'artifacts/study_v177/bundle_', 'artifacts/study_v177/all_tests')))

def requirements(traced):
    lock = dict(l.strip().split('==') for l in (ROOT/'requirements.lock.txt').read_text().splitlines() if '==' in l)
    pins = dict(traced['distributions']); pins.update({k: lock[k] for k in ['contourpy', 'fonttools'] if k in lock})
    return '# Python 3.10 (the study used 3.10.13). Exactly the distributions the offline reproduction imports (traced), plus two\n' \
           '# matplotlib dependencies, pinned to the versions used in the study. Installing them is the only step that needs the network.\n' + \
           ''.join(f'{k}=={v}\n' for k, v in sorted(pins.items(), key=lambda x: x[0].lower()))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--scratch', type=Path, required=True); ap.add_argument('--private-string', action='append', default=[]); a = ap.parse_args()
    traced = json.loads((ART/'traced_inputs.json').read_text())
    assert not [c for c in traced['commands'] if c['returncode']] and not traced['network_events'], 'trace must be clean'
    files = select(traced); stage = a.scratch.resolve()/'bundle_stage_v177'/NAME; assert ROOT not in stage.parents
    if stage.parent.exists(): shutil.rmtree(stage.parent)
    for n in files: (stage/n).parent.mkdir(parents=True, exist_ok=True); os.link(ROOT/n, stage/n)
    hits = []; private = {s: 0 for s in a.private_string}; homes = 0
    for n in files:
        b = (ROOT/n).read_bytes()
        hits += [(n, pat.decode()) for pat in SECRETS if re.search(pat, b) and REVIEWED.get((n, pat)) != hashlib.sha256(b).hexdigest()]
        for s in private: private[s] += s.encode() in b
        homes += bool(re.search(rb'/Users/[A-Za-z0-9._-]+/', b))
    if hits: sys.exit(f'credential-like pattern found, bundle not built: {hits[:10]}')
    (stage/'requirements-bundle-v177.txt').write_text(requirements(traced))
    cov = vb.coverage(stage); assert not cov['chain_missing'] and not cov['integrity_failures'], (cov['chain_missing'], cov['integrity_failures'][:5])
    tsv = 'stage\tpath\tsealed_sha256\tbytes\tcategory\n'+''.join('\t'.join(map(str, r))+'\n' for r in sorted(cov['absent']))
    (stage/'EXCLUDED_FROM_BUNDLE_V177.tsv').write_text(tsv)
    listed = sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file())
    manifest = {'bundle': NAME, 'status': 'V177 offline reviewer audit bundle; private review copy (see BUNDLE_V177_README.md, Licensing)',
                'latest_sealed_manifest': vb.LATEST, 'latest_sealed_manifest_sha256': cov['latest_manifest_sha256'], 'allowed_runtime_files': ALLOWED_HIDDEN,
                'coverage': {'chain_checkpoints': cov['chain_checkpoints'], 'verified': cov['verified'], 'superseded_version_not_included': cov['superseded_version_not_included'],
                             'absent_by_category': dict(sorted(cov['absent_by_category'].items()))},
                'files': {n: {'sha256': digest(stage/n), 'bytes': (stage/n).stat().st_size} for n in listed}}
    (stage/'BUNDLE_MANIFEST_V177.json').write_text(json.dumps(manifest, indent=1)+'\n')
    ZIP.parent.mkdir(exist_ok=True); tmp = ZIP.with_suffix('.zip.partial')
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for n in sorted(listed+['BUNDLE_MANIFEST_V177.json']):
            zi = zipfile.ZipInfo(f'{NAME}/{n}', date_time=(1980, 1, 1, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = (0o100755 if os.access(stage/n, os.X_OK) else 0o100644) << 16
            with open(stage/n, 'rb') as f: z.writestr(zi, f.read(), compresslevel=6)
    tmp.replace(ZIP)
    for n in ['BUNDLE_MANIFEST_V177.json', 'EXCLUDED_FROM_BUNDLE_V177.tsv', 'requirements-bundle-v177.txt']: shutil.copyfile(stage/n, ART/n)
    receipt = {'zip': str(ZIP.relative_to(ROOT)), 'zip_sha256': digest(ZIP), 'zip_bytes': ZIP.stat().st_size, 'files': len(listed)+1,
               'uncompressed_bytes': sum(m['bytes'] for m in manifest['files'].values()), 'bundle_manifest_sha256': digest(stage/'BUNDLE_MANIFEST_V177.json'),
               'coverage': manifest['coverage'], 'credential_pattern_hits': 0, 'files_with_home_directory_paths': homes,
               'private_string_hits_by_index': [private[s] for s in a.private_string], 'executables_included': sorted(n for n in listed if os.access(stage/n, os.X_OK) and not n.endswith(('.py', '.sh')))}
    (ART/'bundle_receipt.json').write_text(json.dumps(receipt, indent=1)+'\n'); print(json.dumps(receipt, indent=1))

if __name__ == '__main__': main()
