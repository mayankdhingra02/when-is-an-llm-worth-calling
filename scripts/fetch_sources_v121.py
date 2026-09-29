"""Bounded owner-source retrieval; no objective conversion or upstream execution."""
import sys,json,hashlib,urllib.request,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];cfg=json.loads((ROOT/'configs/source_v121.json').read_text());out=ROOT/'artifacts/sources/v121'
def main():
    out.mkdir(exist_ok=False);total=0;rows=[]
    for e in cfg['files']:
        assert e['size']+total<=cfg['byte_cap'] and cfg['cumulative_prior_downloads']+total+e['size']<=cfg['cumulative_cap']
        url=f"https://raw.githubusercontent.com/{cfg['repo']}/{cfg['commit']}/{e['path']}"
        at=time.time();record={'url':url,'path':e['path'],'started_unix':at}
        with (out/'attempts.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
        with urllib.request.urlopen(url,timeout=cfg['timeout']) as response:body=response.read(e['size']+1)
        total+=len(body);assert len(body)==e['size']
        gitsha=hashlib.sha1(f'blob {len(body)}\0'.encode()+body).hexdigest();assert gitsha==e['sha']
        p=out/e['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(body)
        rows.append({**record,'saved_path':str(p.relative_to(ROOT)),'git_sha':gitsha,'sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body),'seconds':time.time()-at})
        (out/'manifest.json').write_text(json.dumps({'complete':len(rows)==len(cfg['files']),'files':rows,'total_bytes':total,'targets_parsed':False},indent=2)+'\n')
        print(e['path'],len(body),'verified',flush=True)
if __name__=='__main__':main()
