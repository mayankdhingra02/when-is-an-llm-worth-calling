"""Download pinned owner-published artifacts; no credentials or shell installers."""
import hashlib
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/study_v46'

def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

def main():
    cfg = json.loads((ROOT / 'configs/local_feasibility_v46.json').read_text())
    model = json.loads((OUT / 'model_metadata.json').read_text())
    runtime = json.loads((OUT / 'runtime_build.json').read_text())
    mf = next(x for x in model['siblings'] if x['rfilename'] == 'SmolLM3-Q4_K_M.gguf')
    rf = next(x for x in runtime['assets'] if x['name'] == 'llama-b11146-bin-macos-arm64.tar.gz')
    specs = [
        (f"https://huggingface.co/ggml-org/SmolLM3-3B-GGUF/resolve/{model['sha']}/{mf['rfilename']}", ROOT/'models/SmolLM3-3B-Q4_K_M'/mf['rfilename'], mf['size'], mf['lfs']['sha256']),
        (rf['browser_download_url'], OUT/rf['name'], rf['size'], rf['digest'].removeprefix('sha256:')),
    ]
    ledger_path = OUT/'downloads.json'
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {'metadata_reserve_bytes': 1048576, 'transferred_bytes': 0, 'files': []}
    for url, path, size, sha in specs:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and sha256(path) == sha:
            continue
        if ledger['transferred_bytes'] + size + ledger['metadata_reserve_bytes'] > cfg['max_additional_download_bytes']:
            raise RuntimeError('Download allowance exhausted')
        partial = path.with_suffix(path.suffix+'.partial')
        if partial.exists():
            raise RuntimeError('Preserve partial download; no implicit retry')
        start = time.monotonic()
        result = subprocess.run(['curl', '-fL', '--retry', '0', '--connect-timeout', '20', '--max-time', '600', '--max-filesize', str(size), '-o', str(partial), url])
        actual = partial.stat().st_size if partial.exists() else 0
        ledger['transferred_bytes'] += actual
        rec = {'url': url, 'path': str(path.relative_to(ROOT)), 'bytes_received': actual, 'expected_bytes': size, 'expected_sha256': sha, 'exit_code': result.returncode, 'seconds': time.monotonic()-start}
        # Streaming hash works on the project's Python 3.10 as well.
        h = hashlib.sha256()
        if partial.exists():
            with partial.open('rb') as f:
                for chunk in iter(lambda: f.read(1024*1024), b''): h.update(chunk)
        rec['sha256'] = h.hexdigest()
        rec['verified'] = result.returncode == 0 and actual == size and h.hexdigest() == sha
        ledger['files'].append(rec)
        ledger_path.write_text(json.dumps(ledger, indent=2)+'\n')
        if not rec['verified']: raise RuntimeError('Download incomplete or hash mismatch')
        partial.rename(path)
        print('Verified', path.name, flush=True)

if __name__ == '__main__':
    main()
