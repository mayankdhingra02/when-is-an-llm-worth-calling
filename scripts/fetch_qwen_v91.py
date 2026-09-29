"""Approved bounded owner-file transfer; stream hashes, retain partial charges."""
import hashlib,json,time,urllib.request,urllib.parse,shutil
from pathlib import Path
from check_resources_v91 import ROOT,validate
ART=ROOT/'artifacts/study_v91';OUT=ROOT/'artifacts/sources/v91';MODEL=ROOT/'models/Qwen3-8B-Q4_K_M/Qwen3-8B-Q4_K_M.gguf'
def read(p):return json.loads(p.read_text())
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(v,indent=2)+'\n');tmp.replace(p)
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024**2),b''):h.update(b)
    return h.hexdigest()
def allowed(url):
    p=urllib.parse.urlsplit(url);h=p.hostname or ''
    if p.scheme!='https' or p.username or p.password or not (h=='huggingface.co' or h.endswith('.huggingface.co') or h.endswith('.hf.co')):raise ValueError('Non-owner redirect')
class Redirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):allowed(newurl);return super().redirect_request(req,fp,code,msg,headers,newurl)
def main():
    proposal=ROOT/'configs/resource_proposal_v91.json';cfg=read(proposal);validate(cfg,read(ART/'approval.json'),sha(proposal));OUT.mkdir(parents=True,exist_ok=True)
    ledger_path=ART/'downloads.json';ledger=read(ledger_path) if ledger_path.exists() else {'bytes':0,'model_bytes':0,'transfers':[]};started=time.monotonic();opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),Redirect())
    def fetch(url,path,limit,expected=None,size=None,model=False):
        allowed(url)
        previous=[e for e in ledger['transfers'] if e['path']==str(path.relative_to(ROOT))]
        if path.exists():
            assert previous and previous[-1]['status']=='complete' and sha(path)==previous[-1]['sha256']
            if expected:assert sha(path)==expected
            return
        if any(e['bytes']>0 for e in previous):raise RuntimeError('Partial transfer retained; no implicit retry')
        if model:assert shutil.disk_usage(ROOT).free>limit+2*1024**3
        path.parent.mkdir(parents=True,exist_ok=True);partial=path.with_suffix(path.suffix+'.partial');entry={'url':url,'path':str(path.relative_to(ROOT)),'bytes':0,'status':'started','started_unix':time.time()};ledger['transfers'].append(entry);write(ledger_path,ledger);h=hashlib.sha256();t=time.monotonic()
        try:
            remaining=cfg['download_timeout_seconds']-(time.monotonic()-started);assert remaining>0
            with opener.open(url,timeout=min(30,remaining)) as response,partial.open('wb') as out:
                if response.headers.get('Content-Length'):assert int(response.headers['Content-Length'])<=limit
                while True:
                    assert time.monotonic()-started<cfg['download_timeout_seconds']
                    b=response.read(min(1024**2,limit-entry['bytes']+1))
                    if not b:break
                    entry['bytes']+=len(b);ledger['bytes']+=len(b)
                    if model:ledger['model_bytes']+=len(b)
                    write(ledger_path,ledger)
                    assert entry['bytes']<=limit and ledger['bytes']<=cfg['stage_download_cap_bytes']
                    assert cfg['previous_total_download_bytes']+ledger['bytes']<=cfg['proposed_total_download_cap_bytes']
                    assert cfg['previous_model_download_bytes']+ledger['model_bytes']<=cfg['proposed_model_download_cap_bytes']
                    h.update(b);out.write(b)
                    if model and entry['bytes']%(256*1024**2)==0:print('downloaded model MiB',entry['bytes']//1024**2,flush=True)
            if expected:assert h.hexdigest()==expected,'hash mismatch'
            if size:assert entry['bytes']==size,'size mismatch'
            partial.replace(path);entry.update(status='complete',sha256=h.hexdigest())
        except Exception as e:entry.update(status='failed',error=repr(e));raise
        finally:entry['seconds']=time.monotonic()-t;write(ledger_path,ledger)
    base='https://huggingface.co/'+cfg['model_repo']+'/raw/'+cfg['revision']+'/'
    for name in ['LICENSE','README.md',cfg['filename']]:fetch(base+name,OUT/(name if name!=cfg['filename'] else 'model.pointer'),512*1024)
    pointer=(OUT/'model.pointer').read_text();assert ('oid sha256:'+cfg['model_sha256']) in pointer and ('size '+str(cfg['model_file_bytes'])) in pointer
    assert 'Apache License' in (OUT/'LICENSE').read_text() and 'Version 2.0' in (OUT/'LICENSE').read_text()
    fetch('https://huggingface.co/'+cfg['model_repo']+'/resolve/'+cfg['revision']+'/'+cfg['filename'],MODEL,cfg['model_file_bytes'],cfg['model_sha256'],cfg['model_file_bytes'],True)
    write(ART/'model_manifest.json',{'model_repo':cfg['model_repo'],'revision':cfg['revision'],'path':str(MODEL.relative_to(ROOT)),'sha256':sha(MODEL),'bytes':MODEL.stat().st_size,'license_sha256':sha(OUT/'LICENSE'),'readme_sha256':sha(OUT/'README.md'),'download_bytes':ledger['bytes'],'external_spend_usd':0});print('model verified',flush=True)
if __name__=='__main__':main()
