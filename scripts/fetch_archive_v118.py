"""Bounded public-owner metadata fetcher. No performance table downloads."""
import argparse
import hashlib
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/sources/v118'
LIMIT = 1024**2
ALLOWED = {'https://zenodo.org/api/records/56238',
           'https://zenodo.org/records/56238/files/bo4co_dataset.zip?download=1',
           'https://zenodo.org/records/56238/files/bo4co_dataset.zip',
           'https://zenodo.org/api/records/56238/files/bo4co_dataset.zip/content'}


def check_url(url):
    if url not in ALLOWED:raise ValueError('Only original owner-linked record and named archive')


class Redirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(name, url):
    if Path(name).name != name or name in {'.', '..', 'manifest.json'}:
        raise ValueError('New non-reserved basename required')
    check_url(url)
    OUT.mkdir(parents=True, exist_ok=True)
    ledgerpath = OUT / 'manifest.json'
    ledger = json.loads(ledgerpath.read_text()) if ledgerpath.exists() else {'attempts': []}
    target = OUT / name
    if target.exists() or any(a['name'] == name for a in ledger['attempts']):
        raise FileExistsError('No overwrite or implicit retry')
    remaining = LIMIT - sum(a['bytes'] for a in ledger['attempts'])
    if remaining <= 0:
        raise ValueError('Stage download cap exhausted')
    entry = {'name': name, 'url': url, 'bytes': 0,
             'at': datetime.now(timezone.utc).isoformat(), 'status': 'started'}
    ledger['attempts'].append(entry)
    ledgerpath.write_text(json.dumps(ledger, indent=2) + '\n')
    start = time.monotonic()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'llm-escalation-study-admission'})
        with urllib.request.build_opener(Redirect).open(req, timeout=40) as response:
            check_url(response.url)
            entry['final_url'] = response.url
            length = response.headers.get('Content-Length')
            if length is not None and int(length) > remaining:
                raise ValueError('Declared body exceeds remaining cap')
            with target.open('xb') as out:
                while entry['bytes'] < remaining:
                    chunk = response.read(min(65536, remaining - entry['bytes']))
                    if not chunk:
                        break
                    out.write(chunk)
                    entry['bytes'] += len(chunk)
                    ledgerpath.write_text(json.dumps(ledger, indent=2) + '\n')
            if entry['bytes'] == remaining and (length is None or int(length) != remaining):
                raise ValueError('Cap reached; completeness unknown; partial body retained')
            if length is not None and entry['bytes'] != int(length):
                raise ValueError('Incomplete body')
        entry['status'] = 'complete'
    except Exception as error:
        entry.update(status='failed', error=repr(error))
        raise
    finally:
        if target.exists():
            entry['bytes'] = target.stat().st_size
            entry['sha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
        entry['seconds'] = time.monotonic() - start
        ledgerpath.write_text(json.dumps(ledger, indent=2) + '\n')
    return entry


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name')
    parser.add_argument('url')
    args = parser.parse_args()
    print(json.dumps(fetch(args.name, args.url)))
