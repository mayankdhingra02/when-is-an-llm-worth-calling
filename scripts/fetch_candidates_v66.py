"""Bounded owner/registry source retrieval. No benchmark or model requests."""
import hashlib,json,urllib.request,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/sources/v66'
CAP=80*1024**2

def main():
    OUT.mkdir(exist_ok=True)
    manifest=OUT/'manifest.json'
    records=json.loads(manifest.read_text()) if manifest.exists() else []
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    total=sum(r['bytes'] for r in records)
    def get(name,url):
        nonlocal total
        path=OUT/name
        old=[r for r in records if r['name']==name]
        if old:
            assert len(old)==1 and old[0]['url']==url and hashlib.sha256(path.read_bytes()).hexdigest()==old[0]['sha256']
            return path.read_bytes()
        assert not path.exists()
        req=urllib.request.Request(url,headers={'User-Agent':'llm-escalation-study-source-audit'})
        with opener.open(req,timeout=45) as response:
            chunks=[]
            while True:
                b=response.read(min(1024**2,CAP-total+1))
                if not b:break
                total+=len(b)
                if total>CAP:raise RuntimeError('80MiB source cap')
                chunks.append(b)
        data=b''.join(chunks);path.write_bytes(data)
        records.append({'name':name,'url':url,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
        manifest.write_text(json.dumps(records,indent=2)+'\n')
        print(name,len(data),flush=True)
        return data
    meta=json.loads(get('duckdb_pypi_1.3.2.json','https://pypi.org/pypi/duckdb/1.3.2/json'))
    wheel=next(u for u in meta['urls'] if u['filename']=='duckdb-1.3.2-cp310-cp310-macosx_12_0_arm64.whl')
    data=get(wheel['filename'],wheel['url']);assert hashlib.sha256(data).hexdigest()==wheel['digests']['sha256']
    for name,url in [
        ('duckdb_README.md','https://raw.githubusercontent.com/duckdb/duckdb/v1.3.2/README.md'),
        ('duckdb_LICENSE','https://raw.githubusercontent.com/duckdb/duckdb/v1.3.2/LICENSE'),
        ('duckdb_settings.cpp','https://raw.githubusercontent.com/duckdb/duckdb/v1.3.2/src/main/settings/custom_settings.cpp'),
        ('openjpeg_tag.json','https://api.github.com/repos/uclouvain/openjpeg/git/ref/tags/v2.5.3'),
        ('coreutils-9.7.tar.xz','https://ftp.gnu.org/gnu/coreutils/coreutils-9.7.tar.xz'),
        ('coreutils-9.7.tar.xz.sig','https://ftp.gnu.org/gnu/coreutils/coreutils-9.7.tar.xz.sig'),
    ]:get(name,url)
    ref=json.loads((OUT/'openjpeg_tag.json').read_text())['object']
    if ref['type']=='tag':ref=json.loads(get('openjpeg_tag_object.json',ref['url']))['object']
    assert ref['type']=='commit'
    get('openjpeg-'+ref['sha']+'.tar.gz','https://codeload.github.com/uclouvain/openjpeg/tar.gz/'+ref['sha'])
    print(json.dumps({'source_bytes':total,'remaining_persistent_bytes':597246548-total}))
if __name__=='__main__':main()
