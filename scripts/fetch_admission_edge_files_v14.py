"""Check two raw-looking inventory leads; read only, no benchmark execution."""
import hashlib,json
from pathlib import Path
from download_guard import fetch
ROOT=Path(__file__).resolve().parents[1]
source=next(s for s in json.loads((ROOT/'artifacts/study_v14/source_inventory.json').read_text()) if s['repo']=='inikep/lzbench')
tree={x['path']:x for x in json.loads((ROOT/source['tree_path']).read_text())['tree']}
records=[]
for p in ['lz/zstd/tests/regression/results.csv','misc/density/src/benchmark.log']:
 item=tree[p];assert item['size']<1000000
 target=ROOT/'artifacts/sources/admission_v14/inikep__lzbench'/p
 url=f'https://raw.githubusercontent.com/inikep/lzbench/{source["commit"]}/{p}'
 data=target.read_bytes() if target.exists() else fetch(url,target)
 blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert blob==item['sha']
 records.append({'path':str(target.relative_to(ROOT)),'upstream_path':p,'url':url,'git_blob_sha1':blob,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
(ROOT/'artifacts/study_v14/source_edge_files.json').write_text(json.dumps(records,indent=2)+'\n')
print('Verified two raw-looking inventory files; no benchmark executed.')
