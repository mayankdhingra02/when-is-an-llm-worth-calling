"""Pin upstream lineage metadata, never execute repository code."""
import json,hashlib
from pathlib import Path
from download_guard import fetch
root=Path(__file__).resolve().parents[1];out=root/'artifacts/registry_v4'
meta=out/'promisetune_head.json'
raw=meta.read_bytes() if meta.exists() else fetch('https://api.github.com/repos/ideas-labo/PromiseTune/commits/main',meta)
commit=json.loads(raw)['sha']
readme=out/'promisetune_README.md'
body=readme.read_bytes() if readme.exists() else fetch(f'https://raw.githubusercontent.com/ideas-labo/PromiseTune/{commit}/README.md',readme)
(out/'lineage.json').write_text(json.dumps({'repository':'https://github.com/ideas-labo/PromiseTune','commit':commit,'readme_url':f'https://github.com/ideas-labo/PromiseTune/blob/{commit}/README.md','readme_sha256':hashlib.sha256(body).hexdigest(),'status':'metadata and system catalogue inspected; no upstream execution or row-level equivalence established'},indent=2)+'\n')
print(commit)
