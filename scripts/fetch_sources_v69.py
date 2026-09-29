"""Fetch pinned owner source only, at most 10 MiB including the installed wheel."""
import hashlib,json,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'artifacts/sources/v69'
base='https://raw.githubusercontent.com/rocksdict/RocksDict/350884b4e8f30df1f155261994f97f8768b64167/'
ycsb='https://raw.githubusercontent.com/brianfrankcooper/YCSB/4b19340e3bab5e4c88eda75ad56e83dc4d5cc503/'
urls={name:base+name for name in ['Cargo.toml','Cargo.lock','.gitmodules','LICENSE','README.md','src/options.rs']}
urls['ZipfianGenerator.java']=ycsb+'core/src/main/java/site/ycsb/generator/ZipfianGenerator.java'
urls['ScrambledZipfianGenerator.java']=ycsb+'core/src/main/java/site/ycsb/generator/ScrambledZipfianGenerator.java'
if __name__=='__main__':
 opener=urllib.request.build_opener(urllib.request.ProxyHandler({}));start=time.monotonic()
 for name,url in urls.items():
  p=OUT/name
  if p.exists():continue
  assert time.monotonic()-start<300
  remaining=10*1024**2-sum(q.stat().st_size for q in OUT.rglob('*') if q.is_file())
  with opener.open(url,timeout=30) as res: data=res.read(remaining+1)
  assert len(data)<=remaining
  p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 print(json.dumps({'elapsed_seconds':time.monotonic()-start,'downloaded_sources':list(urls)},indent=2))
