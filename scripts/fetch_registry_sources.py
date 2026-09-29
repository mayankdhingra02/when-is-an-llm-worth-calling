"""Fetch pinned owner tables for feature/schema audit; do not print outcomes."""
import hashlib,json
from pathlib import Path
from download_guard import fetch
ROOT=Path(__file__).resolve().parents[1]
COMMIT='90803be51b00f881305db45aa0cf6a3b5340804f'
tree=json.loads((ROOT/'artifacts/sources/moot_tree.json').read_text())
assert tree['sha']==COMMIT and not tree['truncated']
entries=[]
for item in tree['tree']:
    path=item['path']
    wanted=(path.startswith(('optimize/config/','optimize/systems/')) and path.endswith(('.csv','README.md'))) or path=='docs/cited_by.md'
    if not wanted:continue
    target=ROOT/'data/registry_raw'/path
    if target.exists():payload=target.read_bytes()
    else:payload=fetch(f'https://raw.githubusercontent.com/timm/moot/{COMMIT}/{path}',target)
    blob=hashlib.sha1(b'blob '+str(len(payload)).encode()+b'\0'+payload).hexdigest()
    if blob!=item['sha']:raise ValueError(f'Pinned Git blob mismatch: {path}')
    entries.append({'upstream_path':path,'path':str(target.relative_to(ROOT)),'git_blob_sha1':blob,'sha256':hashlib.sha256(payload).hexdigest(),'bytes':len(payload),'url':f'https://raw.githubusercontent.com/timm/moot/{COMMIT}/{path}'})
    print(path,len(payload),'hash verified',flush=True)
(ROOT/'artifacts/registry_v4/sources.json').write_text(json.dumps({'commit':COMMIT,'tree_sha256':hashlib.sha256((ROOT/'artifacts/sources/moot_tree.json').read_bytes()).hexdigest(),'files':entries},indent=2)+'\n')
