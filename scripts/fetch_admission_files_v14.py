"""Retrieve only inventoried primary files for source/schema review; execute none."""
import hashlib
import json
from pathlib import Path
from download_guard import fetch
ROOT = Path(__file__).resolve().parents[1]
SELECT = {
 'nk2242696/compression-codec-benchmark': [
  'configs/codecs.toml','docs/methodology.md','src/codec_bench/codecs.py','src/codec_bench/engine.py',
  'docs/results/standard-2026-07/manifest.json','docs/results/standard-2026-07/raw.csv'],
 'nschorgh/PDS-Throughput': ['prepfiles.cmd','prepfiles_other.cmd','timecompress.cmd'],
 'inikep/lzbench': ['doc/lzbench.7.txt','bench/lzbench.cpp'],
}
records=[]
for source in json.loads((ROOT/'artifacts/study_v14/source_inventory.json').read_text()):
 repo=source['repo'];commit=source['commit']
 tree={x['path']:x for x in json.loads((ROOT/source['tree_path']).read_text())['tree']}
 for p in SELECT[repo]:
  item=tree[p]
  if item.get('size',0)>1000000:raise ValueError('metadata review per-file size limit')
  target=ROOT/'artifacts/sources/admission_v14'/repo.replace('/','__')/p
  url=f'https://raw.githubusercontent.com/{repo}/{commit}/{p}'
  data=target.read_bytes() if target.exists() else fetch(url,target)
  blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  assert blob==item['sha'],p
  records.append({'repo':repo,'commit':commit,'upstream_path':p,'path':str(target.relative_to(ROOT)),
                  'url':url,'git_blob_sha1':blob,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
  (ROOT/'artifacts/study_v14/source_files.json').write_text(json.dumps(records,indent=2)+'\n')
  print(repo,p,len(data),'verified',flush=True)
