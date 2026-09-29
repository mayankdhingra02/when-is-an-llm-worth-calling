"""Persistent payload caps for subsequent owner-file downloads, no credentials."""
import fcntl,hashlib,json,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class DownloadCap(RuntimeError):pass

def load_ledger(root=ROOT):
    p=root/'artifacts/download_ledger.json'
    if p.exists():return json.loads(p.read_text())
    accounting=root/'artifacts/download_accounting.json'
    if accounting.exists():
        a=json.loads(accounting.read_text());return {'accounted_bytes':int(a['accounted_upper_estimate_bytes']),'model_bytes':a['model_exact_bytes'],'basis':'prior measured payloads plus conservative metadata reserve; pip sizes rounded','transfers':[]}
    return {'accounted_bytes':512*1024**2,'model_bytes':0,'basis':'512 MiB reserve for pinned dependency wheels/metadata; source/model payloads counted below','transfers':[]}

def save_ledger(d,root=ROOT):
    p=root/'artifacts/download_ledger.json';p.parent.mkdir(exist_ok=True);tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(d,indent=2));tmp.replace(p)

def available(d,model=False):
    remaining=5*1024**3-d['accounted_bytes']
    return min(remaining,4*1024**3-d['model_bytes']) if model else remaining

def fetch(url,target,model=False,expected=None):
    target=Path(target);target.parent.mkdir(parents=True,exist_ok=True)
    if expected and target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()==expected:return target.read_bytes()
    (ROOT/'artifacts').mkdir(exist_ok=True)
    with (ROOT/'artifacts/download.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);d=load_ledger();started=time.monotonic()
        if available(d,model)<=0:raise DownloadCap('persistent download cap exhausted')
        save_ledger(d);partial=target.with_suffix(target.suffix+'.partial')
        with urllib.request.urlopen(url,timeout=60) as response,partial.open('wb') as out:
            size=int(response.headers.get('Content-Length',0))
            if size>available(d,model):raise DownloadCap('declared payload exceeds remaining download cap')
            entry={'url':url,'bytes_received':0,'complete':False};d['transfers'].append(entry)
            while True:
                budget=available(d,model)
                if budget<=0:raise DownloadCap('persistent download cap reached')
                if time.monotonic()-started>600:raise DownloadCap('download time limit')
                chunk=response.read(min(1024*1024,budget))
                if not chunk:break
                d['accounted_bytes']+=len(chunk)
                if model:d['model_bytes']+=len(chunk)
                entry['bytes_received']+=len(chunk);save_ledger(d);out.write(chunk)
        data=partial.read_bytes()
        if expected and hashlib.sha256(data).hexdigest()!=expected:raise ValueError('download hash mismatch')
        partial.replace(target);entry['complete']=True;save_ledger(d);return data
