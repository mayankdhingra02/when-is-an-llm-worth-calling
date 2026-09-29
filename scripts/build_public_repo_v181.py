"""V181: build the public GitHub repository tree from the sealed V178 review bundle.

Starts from output/llm_escalation_audit_v178.zip, removes the 11 third-party tables whose redistribution is not clearly
permitted and the 8 source-extract files that copy their rows, and writes third_party/fetch_spec_v181.json so that
scripts/fetch_third_party_v181.py can restore all 19 files byte-for-byte from the owners' repositories. Adds the
V180/V181 manuscript and its figures, the public README (.github/README.md) and the fetch script. Refuses to finish if a
credential pattern, a private string, a file over 50 MB, or a verbatim row of a removed table remains.

    .venv/bin/python scripts/build_public_repo_v181.py --dest DIR [--private-string S ...]
"""
import argparse, hashlib, json, re, shutil, sys, zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_audit_bundle_v178 import SECRETS, REVIEWED

ROOT = Path(__file__).resolve().parents[1]
ZIP = ROOT/'output/llm_escalation_audit_v178.zip'; TOP = 'llm-escalation-audit-v178/'
OWNERS = {'data/registry_raw_v5/': ('registry_v5', None), 'artifacts/sources/v143/tuneful/':
          ('tuneful', 'https://raw.githubusercontent.com/ayat-khairy/tuneful-data/90ebfe3194a50cca00cf8524da26de21e93e6111/')}
EXTRA = {'.github/README.md': 'PUBLIC_README_V181.md', 'scripts/fetch_third_party_v181.py': 'scripts/fetch_third_party_v181.py',
         'scripts/build_public_repo_v181.py': 'scripts/build_public_repo_v181.py', 'scripts/figures_v180.py': 'scripts/figures_v180.py',
         'scripts/check_tables_v180.py': 'scripts/check_tables_v180.py', 'reports/external_audit_v178.md': 'reports/external_audit_v178.md',
         'paper/overleaf_v180/main.tex': 'paper/overleaf_v180/main.tex', 'paper/overleaf_v180/figures/design.pdf': 'paper/overleaf_v180/figures/design.pdf',
         'paper/overleaf_v180/figures/case_gains.pdf': 'paper/overleaf_v180/figures/case_gains.pdf',
         'paper/overleaf_v180/figures/draw_variability.pdf': 'paper/overleaf_v180/figures/draw_variability.pdf'}

def sha(b): return hashlib.sha256(b).hexdigest()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dest', type=Path, required=True); ap.add_argument('--private-string', action='append', default=[]); a = ap.parse_args()
    dest = a.dest.resolve(); assert not dest.exists() or not any(dest.iterdir()), 'destination must be empty'
    manifest = json.loads(zipfile.ZipFile(ZIP).read(TOP+'BUNDLE_MANIFEST_V178.json'))['files']
    registry = {e['path']: e for e in json.loads((ROOT/'artifacts/registry_v5/sources.json').read_text())}
    tables, extracts = [], []
    for n, m in manifest.items():
        for prefix, (kind, base) in OWNERS.items():
            if n.startswith(prefix):
                url = registry[n]['url'] if kind == 'registry_v5' else base+n[len(prefix):]
                if kind == 'registry_v5': assert registry[n]['sha256'] == m['sha256'], n
                tables.append({'path': n, 'url': url, 'sha256': m['sha256']})
    by_sha = {t['sha256']: t['path'] for t in tables}
    with zipfile.ZipFile(ZIP) as z:
        for n in sorted(k for k in manifest if '/source_extracts/' in k):
            d = json.loads(z.read(TOP+n)); src = by_sha[d['source_sha256']]
            extracts.append({'path': n, 'source': src, 'sha256': manifest[n]['sha256'], 'line_numbers': list(d['lines']),
                             'template': {k: (None if k == 'lines' else v) for k, v in d.items()}})
        removed = {t['path'] for t in tables} | {e['path'] for e in extracts}
        dest.mkdir(parents=True, exist_ok=True)
        for info in z.infolist():
            n = info.filename[len(TOP):]
            if not n or info.is_dir() or n in removed: continue
            out = dest/n; out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(z.read(info))
            if (info.external_attr >> 16) & 0o111: out.chmod(0o755)
    for n, src in EXTRA.items(): out = dest/n; out.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(ROOT/src, out)
    spec = {'status': 'V181 fetch specification: third-party tables not redistributed in the public repository, and the source extracts rebuilt from them',
            'tables': sorted(tables, key=lambda t: t['path']), 'extracts': extracts}
    (dest/'third_party').mkdir(exist_ok=True); (dest/'third_party/fetch_spec_v181.json').write_text(json.dumps(spec, indent=1)+'\n')
    for d in sorted({str(Path(p).parent) for p in removed}):  # keep fetched files out of commits
        names = sorted(Path(p).name for p in removed if str(Path(p).parent) == d)
        (dest/d).mkdir(parents=True, exist_ok=True); (dest/d/'.gitignore').write_text('# fetched by scripts/fetch_third_party_v181.py; not redistributed\n'+''.join(f'/{x}\n' for x in names))
    # checks: removed rows absent, no credentials, no private strings, no huge files
    rows = set()
    with zipfile.ZipFile(ZIP) as z:
        for t in tables: rows |= {l.strip() for l in z.read(TOP+t['path']).decode(errors='ignore').splitlines()[1:] if len(l.strip()) > 20}
    files = [p for p in dest.rglob('*') if p.is_file()]; leaks, hits, big, priv = [], [], [], {s: 0 for s in a.private_string}
    for p in files:
        b = p.read_bytes(); n = str(p.relative_to(dest))
        hits += [(n, pat.decode()) for pat in SECRETS if re.search(pat, b) and REVIEWED.get((n, pat)) != sha(b)]
        for s in priv: priv[s] += s.encode() in b
        if p.stat().st_size > 50_000_000: big.append(n)
        if p.suffix in ('.json', '.jsonl', '.csv', '.txt', '.md', '.log'):
            txt = b.decode(errors='ignore'); cands = set(l.strip() for l in txt.splitlines()) | set(re.findall(r'"((?:[^"\\]|\\.){20,2000})"', txt))
            if cands & rows: leaks.append(n)
    report = {'files': len(files), 'bytes': sum(p.stat().st_size for p in files), 'removed_tables': len(tables), 'removed_extracts': len(extracts),
              'files_with_verbatim_rows_of_removed_tables': leaks, 'credential_pattern_hits': hits, 'files_over_50MB': big, 'private_string_hits_by_index': list(priv.values())}
    print(json.dumps(report, indent=1))
    if leaks or hits or big or any(priv.values()): sys.exit('public tree failed its checks; do not publish')

if __name__ == '__main__': main()
