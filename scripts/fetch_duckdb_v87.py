"""Bounded owner/registry downloads only; never execute fetched source."""
import hashlib,json,time,urllib.request,urllib.parse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/sources/v87';CAP=64*1024**2
ALLOWED={'pypi.org','files.pythonhosted.org','api.github.com','raw.githubusercontent.com','extensions.duckdb.org'}
class Redirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        p=urllib.parse.urlparse(newurl)
        if p.scheme!='https' or p.hostname not in ALLOWED:raise ValueError('Unapproved redirect')
        return super().redirect_request(req,fp,code,msg,headers,newurl)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fetch(url,name,limit=8*1024**2):
    OUT.mkdir(parents=True,exist_ok=True);ledger=OUT/'downloads.json';rows=json.loads(ledger.read_text()) if ledger.exists() else []
    path=OUT/name
    if path.exists():
        old=next(r for r in rows if r['name']==name and r['status']=='complete');assert sha(path)==old['sha256'];return path
    parts=urllib.parse.urlparse(url);assert parts.scheme=='https' and parts.hostname in ALLOWED
    spent=sum(r['bytes'] for r in rows);assert spent<CAP
    row={'url':url,'name':name,'started_unix':time.time(),'bytes':0,'status':'started'};rows.append(row)
    def save():ledger.write_text(json.dumps(rows,indent=2)+'\n')
    save();partial=OUT/(name+'.partial');assert not partial.exists();start=time.monotonic()
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'llm-escalation-research-local','Accept':'application/json' if parts.hostname in ['pypi.org','api.github.com'] else '*/*'})
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),Redirect())
        with opener.open(req,timeout=30) as r,partial.open('xb') as f:
            length=r.headers.get('Content-Length')
            if length:assert int(length)<=min(limit,CAP-spent)
            row['final_url']=r.url
            while True:
                b=r.read(min(65536,min(limit,CAP-spent)-row['bytes']+1))
                if not b:break
                row['bytes']+=len(b);f.write(b);save();assert row['bytes']<=limit and spent+row['bytes']<=CAP and time.monotonic()-start<60
        partial.rename(path);row.update(status='complete',sha256=sha(path));return path
    except Exception as e:row.update(status='failed',error=repr(e));raise
    finally:row['seconds']=time.monotonic()-start;save()
def main():
    metadata=json.loads(fetch('https://pypi.org/pypi/duckdb/1.4.4/json','pypi.json').read_text());assert metadata['info']['version']=='1.4.4'
    candidates=[f for f in metadata['urls'] if 'cp310-cp310-macosx' in f['filename'] and f['filename'].endswith('arm64.whl')];assert len(candidates)==1
    item=candidates[0];p=fetch(item['url'],item['filename'],32*1024**2);assert sha(p)==item['digests']['sha256'] and p.stat().st_size==item['size']
    fetch('https://raw.githubusercontent.com/duckdb/duckdb/v1.4.4/LICENSE','DUCKDB_LICENSE')
    fetch('https://api.github.com/repos/duckdb/duckdb/contents/extension/tpch?ref=v1.4.4','tpch_tree.json')
    (ROOT/'artifacts/study_v87/wheel.json').write_text(json.dumps(item,indent=2)+'\n');print(json.dumps({'wheel':str(p.relative_to(ROOT)),'sha256':sha(p),'downloaded_bytes':sum(r['bytes'] for r in json.loads((OUT/'downloads.json').read_text()))}))
if __name__=='__main__':main()
