"""Pin metadata from identified public primary artifact owners; no code execution."""
import hashlib,json
from pathlib import Path
from download_guard import fetch
ROOT=Path(__file__).resolve().parents[1]
REPOS=['DeepPerf/DeepPerf','se-sic/SPLConqueror','ChristianKaltenecker/PerformanceEvolution_Website','anonymous12138/multiobj']
manifest=[]
for repo in REPOS:
    out=ROOT/'artifacts/sources/registry_v5'/repo.replace('/','__');out.mkdir(parents=True,exist_ok=True)
    def get(url,path):return path.read_bytes() if path.exists() else fetch(url,path)
    head=json.loads(get(f'https://api.github.com/repos/{repo}/commits/HEAD',out/'head.json'))
    commit=head['sha'];tree=json.loads(get(f'https://api.github.com/repos/{repo}/git/trees/{commit}?recursive=1',out/'tree.json'))
    if tree.get('truncated'):raise ValueError('truncated inventory')
    files=[]
    for item in tree['tree']:
        if '/' not in item['path'] and item['path'].lower().startswith(('readme','license','.gitmodules')):
            payload=get(f'https://raw.githubusercontent.com/{repo}/{commit}/{item["path"]}',out/item['path'])
            assert hashlib.sha1(b'blob '+str(len(payload)).encode()+b'\0'+payload).hexdigest()==item['sha']
            files.append({'path':str((out/item['path']).relative_to(ROOT)),'sha256':hashlib.sha256(payload).hexdigest()})
    manifest.append({'repo':repo,'commit':commit,'tree_path':str((out/'tree.json').relative_to(ROOT)),
                     'tree_sha256':hashlib.sha256((out/'tree.json').read_bytes()).hexdigest(),'files':files})
    print(repo,commit,len(tree['tree']),flush=True)
(ROOT/'artifacts/registry_v5/metadata.json').write_text(json.dumps(manifest,indent=2)+'\n')
