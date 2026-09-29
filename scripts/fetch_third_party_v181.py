"""V181: restore the third-party measurement tables that the public repository does not redistribute.

Some tables used by the study come from repositories that declare no licence (DeepPerf, Tuneful) or a licence we do
not want to relicense (Performance Evolution, GPL-2.0). The public repository therefore omits:
  - the 11 raw tables, which are downloaded here from their owners' repositories at the exact commits the study used;
  - 8 "source extract" files (the header plus the rows the study acquired), which are rebuilt here from those tables.
Every downloaded and rebuilt file must match the SHA-256 recorded in the project's sealed manifests, or nothing is
written. Needs network access to raw.githubusercontent.com (about 11 MB). Run once, before the offline reproduction:

    python scripts/fetch_third_party_v181.py
"""
import hashlib, json, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT/'third_party/fetch_spec_v181.json'

def sha(b): return hashlib.sha256(b).hexdigest()

def download(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'llm-escalation-study replication fetch'})
    with urllib.request.urlopen(req, timeout=120) as r: return r.read()

def main():
    spec = json.loads(SPEC.read_text()); tables = {}
    for t in spec['tables']:
        dest = ROOT/t['path']
        if dest.exists() and sha(dest.read_bytes()) == t['sha256']:
            tables[t['path']] = dest.read_bytes(); print(f"ok (already present)  {t['path']}"); continue
        data = download(t['url'])
        if sha(data) != t['sha256']:
            sys.exit(f"hash mismatch for {t['url']}: the owner's file differs from the one the study used; nothing written")
        tables[t['path']] = data
    for p, data in tables.items():  # write only after every table verified
        dest = ROOT/p; dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists(): dest.write_bytes(data); print(f"fetched  {p}")
    for e in spec['extracts']:
        lines = tables[e['source']].decode().splitlines(); tpl = e['template']
        obj = {k: ({n: lines[int(n)-1] for n in e['line_numbers']} if k == 'lines' else v) for k, v in tpl.items()}
        text = (json.dumps(obj, indent=2)+'\n').encode()
        if sha(text) != e['sha256']: sys.exit(f"rebuilt extract {e['path']} does not match its sealed hash; nothing written for it")
        dest = ROOT/e['path']; dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(text); print(f"rebuilt  {e['path']}")
    print(json.dumps({'tables': len(spec['tables']), 'extracts': len(spec['extracts']), 'all_hashes_match': True}))

if __name__ == '__main__': main()
