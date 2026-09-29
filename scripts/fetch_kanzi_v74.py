"""Bounded owner/registry retrieval; inspect files before running any code."""
import argparse,hashlib,json,time,urllib.request
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/sources/v74';CAP=32*1024**2
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('name');p.add_argument('url');a=p.parse_args()
    if Path(a.name).name!=a.name:raise ValueError('Basename required')
    if urlparse(a.url).hostname not in ['api.github.com','raw.githubusercontent.com','github.com','codeload.github.com','repo.maven.apache.org']:raise ValueError('Owner/registry only')
    OUT.mkdir(parents=True,exist_ok=True);manifest=OUT/'manifest.json';ledger=json.loads(manifest.read_text()) if manifest.exists() else {'entries':[],'failures':[]}
    target=OUT/a.name
    if target.exists():raise FileExistsError('No overwrite')
    remaining=CAP-sum(x['bytes'] for x in ledger['entries']);start=time.monotonic()
    try:
        request=urllib.request.Request(a.url,headers={'User-Agent':'llm-escalation-study'})
        with urllib.request.urlopen(request,timeout=45) as response:
            if int(response.headers.get('Content-Length',0))>remaining:raise ValueError('Download cap')
            body=response.read(remaining+1)
            if len(body)>remaining:raise ValueError('Download cap')
            url=response.url
        target.write_bytes(body);item={'file':a.name,'url':a.url,'final_url':url,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'at':datetime.now(timezone.utc).isoformat(),'seconds':time.monotonic()-start};ledger['entries'].append(item);print(json.dumps(item))
    except Exception as e:ledger['failures'].append({'url':a.url,'error':repr(e)});raise
    finally:manifest.write_text(json.dumps(ledger,indent=2)+'\n')
