"""Authorized, streamed owner download with byte caps and upstream digest checks."""
import fcntl
import hashlib
import json
import os
import sys
import time
import urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src')); os.chdir(ROOT)
from download_guard import load_ledger, save_ledger, available
from escalation.config import load_config
from escalation.io import read, write
from escalation.larger_v22 import authorization_config, MODEL_ID, REVISION, require


def check_file(path, expected):
    size = path.stat().st_size
    require(size == expected['size'], 'Owner file size mismatch')
    sha = hashlib.sha256(); git = hashlib.sha1(f'blob {size}\0'.encode())
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            sha.update(chunk); git.update(chunk)
    if 'lfs' in expected:
        require(sha.hexdigest() == expected['lfs']['sha256'], 'Owner LFS SHA256 mismatch')
    else:
        require(git.hexdigest() == expected['blobId'], 'Owner Git blob digest mismatch')
    return {'file': expected['rfilename'], 'bytes': size, 'sha256': sha.hexdigest(),
            'owner_digest_verified': True}


def main():
    authorization_config(load_config('configs/followup_v3.yaml'), read('configs/authorization_v22.json'))
    # Verify the proposal and downloader before any large download.
    for name, expected in read('reports/protocol_v22_larger.freeze.json')['sha256'].items():
        require(hashlib.sha256(Path(name).read_bytes()).hexdigest() == expected, 'Frozen input changed: ' + name)
    plan = read('artifacts/study_v22/model_download_plan.json')
    require(plan['model_id'] == MODEL_ID and plan['revision'] == REVISION, 'Pinned owner plan required')
    target = Path('models/Qwen2.5-1.5B-Instruct'); target.mkdir(parents=True, exist_ok=True)
    records = []; begin = time.monotonic()
    with Path('artifacts/download.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        ledger = load_ledger()
        pending = sum(r['size'] for r in plan['files'] if not (target / r['rfilename']).exists())
        require(pending <= available(ledger, model=True), 'Download allowance insufficient')
        for expected in plan['files']:
            name = expected['rfilename']; path = target / name
            if not path.exists():
                partial = path.with_suffix(path.suffix + '.partial')
                require(not partial.exists(), 'Interrupted download needs explicit audit; no silent restart')
                url = f'https://huggingface.co/{MODEL_ID}/resolve/{REVISION}/{name}'
                entry = {'url': url, 'bytes_received': 0, 'complete': False}
                ledger['transfers'].append(entry); save_ledger(ledger)
                with urllib.request.urlopen(url, timeout=60) as response, partial.open('xb') as stream:
                    while entry['bytes_received'] < expected['size']:
                        require(time.monotonic() - begin < 600, 'Whole-download10-minute deadline')
                        remaining = min(available(ledger, model=True), expected['size'] - entry['bytes_received'])
                        require(remaining > 0, 'Download cap exhausted')
                        chunk = response.read(min(1024 * 1024, remaining))
                        require(bool(chunk), 'Truncated owner payload')
                        ledger['accounted_bytes'] += len(chunk); ledger['model_bytes'] += len(chunk)
                        entry['bytes_received'] += len(chunk); save_ledger(ledger); stream.write(chunk)
                check_file(partial, expected)
                partial.replace(path); entry['complete'] = True; save_ledger(ledger)
            record = check_file(path, expected)
            record['url'] = f'https://huggingface.co/{MODEL_ID}/resolve/{REVISION}/{name}'
            records.append(record)
            write('artifacts/model_manifest_v22.json', {'model_id': MODEL_ID, 'revision': REVISION,
                  'license': 'Apache-2.0', 'files': records, 'complete': len(records) == len(plan['files'])})
            print(name, record['bytes'], flush=True)
    write('artifacts/study_v22/download_execution.json', {'download_wall_seconds': time.monotonic() - begin,
          'model_manifest': 'artifacts/model_manifest_v22.json', 'new_model_requests': 0,
          'scope': 'Download wall time tracked separately from experiment execution'})


if __name__ == '__main__':
    main()
