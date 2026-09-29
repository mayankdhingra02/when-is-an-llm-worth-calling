"""Bounded, credential-free primary metadata retrieval; project-local runtime and benchmark; never fetch target tables."""
import datetime
import fcntl
import hashlib
import json
import sys
import urllib.request
from pathlib import Path
from download_guard import ROOT, available, load_ledger, save_ledger

OUT = ROOT / 'artifacts/sources/v55'
MANIFEST = OUT / 'manifest.json'
CAP = 64 * 1024**2


def fetch(name, url):
    OUT.mkdir(parents=True, exist_ok=True)
    records = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else []
    target = OUT / name
    if target.exists():
        record = next(r for r in records if r['path'] == str(target.relative_to(ROOT)))
        assert record['url'] == url
        assert hashlib.sha256(target.read_bytes()).hexdigest() == record['sha256']
        return target.read_bytes()
    # Check public endpoint allowlist, with no ambient credentials or installers.
    assert url.startswith(('https://api.github.com/repos/', 'https://raw.githubusercontent.com/',
                           'https://github.com/', 'https://www.fast-downward.org/', 'https://codeload.github.com/', 'https://api.adoptium.net/', 'https://sourceforge.net/', 'https://downloads.sourceforge.net/', 'https://download.dacapobench.org/'))
    with (ROOT / 'artifacts/download.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        ledger = load_ledger()
        used = sum(r['bytes_received'] for r in ledger['transfers'] if r.get('study') == 'v55')
        allowance = min(CAP - used, available(ledger))
        if allowance <= 0:
            raise RuntimeError('V55 download cap exhausted')
        entry = {'study': 'v55', 'url': url, 'bytes_received': 0, 'complete': False}
        ledger['transfers'].append(entry)
        save_ledger(ledger)
        partial = target.with_suffix(target.suffix + '.partial')
        with urllib.request.urlopen(url, timeout=30) as response, partial.open('wb') as dest:
            if int(response.headers.get('Content-Length', 0)) > allowance:
                raise RuntimeError('source exceeds remaining cap')
            while allowance > 0:
                chunk = response.read(min(32768, allowance))
                if not chunk:
                    break
                dest.write(chunk)
                allowance -= len(chunk)
                entry['bytes_received'] += len(chunk)
                ledger['accounted_bytes'] += len(chunk)
                save_ledger(ledger)
            if allowance == 0:
                raise RuntimeError('source reached cap; retained partial, not admitted')
        partial.replace(target)
        entry['complete'] = True
        save_ledger(ledger)
    data = target.read_bytes()
    records.append({'path': str(target.relative_to(ROOT)), 'url': url,
                    'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data),
                    'retrieved_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()})
    MANIFEST.write_text(json.dumps(records, indent=2) + '\n')
    return data


if __name__ == '__main__':
    print(len(fetch(sys.argv[1], sys.argv[2])))
