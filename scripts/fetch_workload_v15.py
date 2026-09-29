"""Pin a small real source-code workload from the CPython owner; execute no code."""
import hashlib,io,json,tarfile
from pathlib import Path
from download_guard import fetch
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/sources/live_v15/cpython';OUT.mkdir(parents=True,exist_ok=True)

def get(url,path):return path.read_bytes() if path.exists() else fetch(url,path)
head=json.loads(get('https://api.github.com/repos/python/cpython/commits/v3.10.13',OUT/'head.json'))
commit=head['sha'];records=[]
for name in ['LICENSE','Objects/unicodeobject.c','Python/ceval.c','Modules/_ssl.c']:
 url=f'https://raw.githubusercontent.com/python/cpython/{commit}/{name}'
 raw=get(url,OUT/name)
 if len(raw)>2*1024**2:raise ValueError('Source file exceeds workload bound')
 records.append({'name':name,'path':str((OUT/name).relative_to(ROOT)),'url':url,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
workload=OUT/'workload.tar'
with tarfile.open(workload,'w',format=tarfile.USTAR_FORMAT) as archive:
 for row in records:
  if row['name']=='LICENSE':continue
  raw=(ROOT/row['path']).read_bytes();info=tarfile.TarInfo(row['name']);info.size=len(raw);info.mode=0o644;info.mtime=0;info.uid=info.gid=0;info.uname=info.gname=''
  archive.addfile(info,io.BytesIO(raw))
assert workload.stat().st_size<=2*1024**2
manifest={'source_owner':'python/cpython','tag':'v3.10.13','commit':commit,'files':records,
 'workload_path':str(workload.relative_to(ROOT)),'workload_sha256':hashlib.sha256(workload.read_bytes()).hexdigest(),'workload_bytes':workload.stat().st_size,
 'construction':'USTAR in listed source-file order, LICENSE excluded, uid/gid/mtime0, mode0644, empty owner names; real source files, no repetition or synthetic payload',
 'scope':'single source-code archive for development measurement feasibility; not a representative production corpus'}
(ROOT/'artifacts/study_v15/workload_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({k:manifest[k] for k in ['commit','workload_bytes','workload_sha256']}))
