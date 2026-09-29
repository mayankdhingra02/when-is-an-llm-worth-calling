"""Bounded owner metadata retrieval only; never downloads objective tables."""
import argparse
import hashlib
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'artifacts/sources/v73'
LIMIT = 10*1024**2

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name'); parser.add_argument('url'); args = parser.parse_args()
    if Path(args.name).name != args.name: raise ValueError('Basename required')
    if urlparse(args.url).hostname not in ['zenodo.org', 'api.github.com', 'raw.githubusercontent.com']:
        raise ValueError('Only selected owner/repository metadata hosts')
    OUT.mkdir(parents=True, exist_ok=True)
    ledgerpath = OUT/'manifest.json'
    ledger = json.loads(ledgerpath.read_text()) if ledgerpath.exists() else {'entries': [], 'failed_requests': []}
    target = OUT/args.name
    if target.exists(): raise FileExistsError('No overwrite')
    remaining = LIMIT-sum(e['bytes'] for e in ledger['entries'])
    start = time.monotonic()
    try:
        request = urllib.request.Request(args.url, headers={'User-Agent': 'llm-escalation-study-source-audit', 'Accept': 'application/json' if args.url.startswith('https://api.github.com') else '*/*'})
        with urllib.request.urlopen(request, timeout=40) as response:
            if int(response.headers.get('Content-Length', 0)) > remaining: raise ValueError('Stage download cap')
            body = response.read(remaining+1)
            if len(body)>remaining: raise ValueError('Stage download cap')
            final_url = response.url
        target.write_bytes(body)
        ledger['entries'].append({'name': args.name, 'url': args.url, 'final_url': final_url,
            'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(), 'at': datetime.now(timezone.utc).isoformat(), 'seconds': time.monotonic()-start})
        print(json.dumps(ledger['entries'][-1]))
    except Exception as error:
        ledger['failed_requests'].append({'name': args.name, 'url': args.url, 'error': repr(error), 'at': datetime.now(timezone.utc).isoformat()})
        raise
    finally: ledgerpath.write_text(json.dumps(ledger, indent=2)+'\n')
