"""Bounded registry/owner retrieval; no objective or model execution."""
import hashlib, json, time, urllib.request, urllib.parse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'artifacts/sources/v166'
def main():
    cfg=json.loads((ROOT/'configs/study_v166.json').read_text())
    assert not (A/'receipt.json').exists()
    started=time.monotonic(); rows=[]; received=0; retained=0; error=None
    hosts={'pypi.org','files.pythonhosted.org','raw.githubusercontent.com','archive.ics.uci.edu'}
    class Redirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            if urllib.parse.urlparse(newurl).hostname not in hosts: raise ValueError('Unapproved redirect')
            return super().redirect_request(req,fp,code,msg,headers,newurl)
    opener=urllib.request.build_opener(Redirect)
    def fetch(name,url,expected=None):
        nonlocal received,retained
        remaining=cfg['new_download_bytes_cap']-received
        seconds=cfg['source_seconds_cap']-(time.monotonic()-started)
        assert remaining>0 and seconds>0 and urllib.parse.urlparse(url).hostname in hosts
        with opener.open(urllib.request.Request(url,headers={'User-Agent':'bounded-local-research/1.0'}),timeout=min(60,seconds)) as r:
            assert int(r.headers.get('Content-Length','0'))<=remaining
            chunks=[]
            while True:
                assert time.monotonic()-started<cfg['source_seconds_cap']
                b=r.read(min(1048576,remaining+1)); received+=len(b); remaining-=len(b)
                if remaining<0: raise ValueError('Download cap')
                if not b: break
                chunks.append(b)
        body=b''.join(chunks); digest=hashlib.sha256(body).hexdigest()
        if expected and digest!=expected:raise ValueError('Registry digest mismatch')
        (A/name).write_bytes(body);retained+=len(body)
        rows.append({'path':str((A/name).relative_to(ROOT)),'url':url,'bytes':len(body),'sha256':digest})
        print(name,len(body),flush=True);return body
    try:
        for package,version in cfg['versions'].items():
            meta=json.loads(fetch(package+'.json',f'https://pypi.org/pypi/{package}/{version}/json'))
            wheels=[x for x in meta['urls'] if x['filename'].endswith('.whl') and ('macosx' in x['filename'] and 'arm64' in x['filename'] or 'py3-none-any' in x['filename'])]
            assert len(wheels)==1,[x['filename'] for x in wheels]
            w=wheels[0];fetch(w['filename'],w['url'],w['digests']['sha256'])
        fetch('polars_LICENSE','https://raw.githubusercontent.com/pola-rs/polars/py-1.35.2/LICENSE')
        fetch('xgboost_LICENSE','https://raw.githubusercontent.com/dmlc/xgboost/v3.1.1/LICENSE')
        fetch('xgboost_parameter.rst','https://raw.githubusercontent.com/dmlc/xgboost/v3.1.1/doc/parameter.rst')
        fetch('covertype_page.html','https://archive.ics.uci.edu/dataset/31/covertype')
        fetch('covertype.zip','https://archive.ics.uci.edu/static/public/31/covertype.zip')
    except Exception as exc:error=repr(exc)
    finally:
        (A/'receipt.json').write_text(json.dumps({'files':rows,'response_content_bytes_received':received,'retained_http_bytes':retained,'seconds':time.monotonic()-started,'error':error,'caps':cfg},indent=2)+'\n')
    if error:raise RuntimeError(error)
if __name__=='__main__':main()
