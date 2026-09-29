"""V172 authorized one-time owner-file transfer; pinned revision, streamed hash, byte caps, no retries."""
import hashlib, json, re, shutil, time, urllib.parse, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ART = ROOT/'artifacts/study_v172'; SRC = ROOT/'artifacts/sources/v172'

def read(p): return json.loads(Path(p).read_text())
def write(p, v):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True); tmp = p.with_suffix(p.suffix+'.tmp'); tmp.write_text(json.dumps(v, indent=1)+'\n'); tmp.replace(p)
def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
def allowed(url):
    p = urllib.parse.urlsplit(url); h = p.hostname or ''
    if p.scheme != 'https' or p.username or p.password or not (h == 'huggingface.co' or h.endswith('.huggingface.co') or h.endswith('.hf.co')):
        raise ValueError('Non-owner host: '+h)
class Redirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl): allowed(newurl); return super().redirect_request(req, fp, code, msg, headers, newurl)

def parse_pointer(text):
    oid = re.search(r'^oid sha256:([0-9a-f]{64})$', text, re.M); size = re.search(r'^size (\d+)$', text, re.M)
    if not (text.startswith('version https://git-lfs.github.com/spec/v1') and oid and size): raise ValueError('Not an LFS pointer')
    return oid.group(1), int(size.group(1))

def main():
    cfg = read(ROOT/'configs/study_v172.json'); auth = read(ART/'authorization.json'); d = cfg['download']
    assert auth['authorized']['retained_download_cap_bytes'] == d['authorized_retained_download_cap_bytes']
    assert auth['authorized']['model_payload_cap_bytes'] == d['authorized_model_payload_cap_bytes']
    assert auth['authorized']['one_time_download'] == {'repo': cfg['model_repo'], 'file': cfg['model_filename'], 'plus': ['LICENSE', 'README.md', 'LFS pointer']}
    model = ROOT/cfg['model_path']; ledger_path = ART/'downloads.json'
    if ledger_path.exists() or model.exists(): raise RuntimeError('Create-once transfer already started; no implicit retry')
    free = shutil.disk_usage(ROOT).free
    if free < cfg['min_free_disk_bytes_before_download']: raise RuntimeError(f'Disk gate failed: {free} bytes free')
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), Redirect()); started = time.monotonic()
    ledger = {'started_at_unix': time.time(), 'free_disk_bytes_before': free, 'bytes': 0, 'model_bytes': 0, 'transfers': []}; write(ledger_path, ledger)
    def fetch(url, limit, dest=None, is_model=False, expected=None, size=None):
        allowed(url); entry = {'url': url, 'bytes': 0, 'status': 'started', 'started_unix': time.time()}; ledger['transfers'].append(entry); write(ledger_path, ledger)
        h = hashlib.sha256(); buf = bytearray(); partial = None if dest is None else dest.with_suffix(dest.suffix+'.partial'); t = time.monotonic()
        try:
            remaining = d['download_timeout_seconds']-(time.monotonic()-started); assert remaining > 0
            if partial: partial.parent.mkdir(parents=True, exist_ok=True)
            out = partial.open('xb') if partial else None
            try:
                with opener.open(url, timeout=min(60, remaining)) as r:
                    entry['final_host'] = urllib.parse.urlsplit(r.geturl()).hostname
                    if r.headers.get('Content-Length'): assert int(r.headers['Content-Length']) <= limit, 'Declared size over limit'
                    while True:
                        assert time.monotonic()-started < d['download_timeout_seconds'], 'Download time cap'
                        b = r.read(min(1 << 20, limit-entry['bytes']+1))
                        if not b: break
                        entry['bytes'] += len(b); ledger['bytes'] += len(b)
                        if is_model: ledger['model_bytes'] += len(b)
                        assert entry['bytes'] <= limit and ledger['bytes'] <= d['stage_download_cap_bytes'], 'Stage byte cap'
                        assert d['previous_retained_download_bytes']+ledger['bytes'] <= d['authorized_retained_download_cap_bytes'], 'Retained-download cap'
                        assert d['previous_model_payload_bytes']+ledger['model_bytes'] <= d['authorized_model_payload_cap_bytes'], 'Model-payload cap'
                        h.update(b)
                        if out: out.write(b)
                        else: buf.extend(b)
                        if is_model and entry['bytes'] % (512 << 20) < len(b): write(ledger_path, ledger); print('model MiB', entry['bytes'] >> 20, round(time.monotonic()-t), 's', flush=True)
            finally:
                if out: out.close()
            if expected: assert h.hexdigest() == expected, 'SHA256 mismatch'
            if size is not None: assert entry['bytes'] == size, 'Size mismatch'
            if partial: partial.replace(dest)
            entry.update(status='complete', sha256=h.hexdigest())
        except Exception as e: entry.update(status='failed', error=repr(e)); raise
        finally: entry['seconds'] = time.monotonic()-t; write(ledger_path, ledger)
        return bytes(buf)
    api = json.loads(fetch(f"https://huggingface.co/api/models/{cfg['model_repo']}", 1 << 20)); revision = api['sha']; assert re.fullmatch(r'[0-9a-f]{40}', revision)
    blobs = json.loads(fetch(f"https://huggingface.co/api/models/{cfg['model_repo']}/revision/{revision}?blobs=true", 1 << 20))
    sib, = [s for s in blobs['siblings'] if s['rfilename'] == cfg['model_filename']]; api_sha, api_size = sib['lfs']['sha256'], sib['lfs']['size']
    base = f"https://huggingface.co/{cfg['model_repo']}/raw/{revision}/"
    for name in ['LICENSE', 'README.md']:
        (SRC/name).parent.mkdir(parents=True, exist_ok=True); (SRC/name).write_bytes(fetch(base+name, 1 << 20))
    pointer = fetch(base+cfg['model_filename'], 4096).decode(); (SRC/'model.pointer').write_text(pointer); p_sha, p_size = parse_pointer(pointer)
    assert (p_sha, p_size) == (api_sha, api_size), 'Pointer and API blob metadata disagree'
    lic = (SRC/'LICENSE').read_text(); assert 'Apache License' in lic and 'Version 2.0' in lic
    assert shutil.disk_usage(ROOT).free > p_size+8*(1 << 30), 'Insufficient disk margin for model'
    fetch(f"https://huggingface.co/{cfg['model_repo']}/resolve/{revision}/{cfg['model_filename']}", p_size, model, True, p_sha, p_size)
    assert sha(model) == p_sha and model.stat().st_size == p_size
    manifest = {'model_repo': cfg['model_repo'], 'revision': revision, 'path': cfg['model_path'], 'sha256': p_sha, 'bytes': p_size, 'license': 'Apache-2.0',
                'license_sha256': sha(SRC/'LICENSE'), 'readme_sha256': sha(SRC/'README.md'), 'pointer_sha256': sha(SRC/'model.pointer'),
                'download_bytes': ledger['bytes'], 'retained_download_bytes_after': d['previous_retained_download_bytes']+ledger['bytes'],
                'model_payload_bytes_after': d['previous_model_payload_bytes']+ledger['model_bytes'], 'external_spend_usd': 0, 'seconds': time.monotonic()-started}
    write(ART/'model_manifest.json', manifest); print(json.dumps(manifest, indent=1))

if __name__ == '__main__': main()
