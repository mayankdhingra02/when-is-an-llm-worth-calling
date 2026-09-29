"""Bounded retrieval of two original SciPy sources, with byte provenance."""
import hashlib, json, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/sources/v96'
CAP = 65536

def main():
    OUT.mkdir(parents=True, exist_ok=False)
    total = 0
    for name in ['util.c', 'sp_ienv.c']:
        url = 'https://raw.githubusercontent.com/scipy/scipy/v1.13.1/scipy/sparse/linalg/_dsolve/SuperLU/SRC/' + name
        with urllib.request.urlopen(url, timeout=30) as response:
            assert response.url == url
            raw = response.read(CAP - total + 1)
        total += len(raw)
        (OUT / name).write_bytes(raw)
        with (OUT / 'fetch.jsonl').open('a') as f:
            f.write(json.dumps(dict(url=url, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
                at=datetime.now(timezone.utc).isoformat())) + '\n')
        if total > CAP:
            raise RuntimeError('Source download cap exceeded; stop')
        print(name, len(raw), flush=True)

if __name__ == '__main__':
    main()
