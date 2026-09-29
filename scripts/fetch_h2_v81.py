"""Bounded retrieval from Maven Central and pinned H2 owner source; no installers."""
import hashlib,json,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE='https://repo.maven.apache.org/maven2/com/h2database/h2/2.3.232/'
FILES={'h2-2.3.232.jar':BASE+'h2-2.3.232.jar','h2-2.3.232.jar.sha1':BASE+'h2-2.3.232.jar.sha1','h2-2.3.232.pom':BASE+'h2-2.3.232.pom','DbSettings.java':'https://raw.githubusercontent.com/h2database/h2database/version-2.3.232/h2/src/main/org/h2/engine/DbSettings.java','LICENSE.txt':'https://raw.githubusercontent.com/h2database/h2database/version-2.3.232/LICENSE.txt'}
def main():
    art=ROOT/'artifacts/study_v81';source=ROOT/'artifacts/sources/v81';total=0;receipts=[];limit=8*1024**2
    for name,url in FILES.items():
        p=source/name;assert not p.exists();r={'name':name,'url':url,'started_unix':time.time(),'bytes':0};receipts.append(r)
        try:
            with urllib.request.urlopen(url,timeout=45) as response,p.open('xb') as f:
                r['resolved_url']=response.url
                while True:
                    b=response.read(min(65536,limit-total+1))
                    if not b:break
                    total+=len(b);r['bytes']+=len(b);assert total<=limit;f.write(b)
            r['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();r['status']='downloaded'
        finally:(art/'download_ledger.json').write_text(json.dumps({'new_download_bytes':total,'cumulative_download_bytes':4814795101+total,'remaining_download_bytes':553914019-total,'receipts':receipts},indent=2)+'\n')
    jar=source/'h2-2.3.232.jar';assert hashlib.sha1(jar.read_bytes()).hexdigest()==(source/'h2-2.3.232.jar.sha1').read_text().strip()
    print(json.dumps({'verified_registry_sha1':True,'download_bytes':total}))
if __name__=='__main__':main()
