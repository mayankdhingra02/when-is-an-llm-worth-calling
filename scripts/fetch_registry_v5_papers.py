"""Save primary author-hosted audit papers and hashes; do not execute content."""
import json,hashlib
from pathlib import Path
from download_guard import fetch
root=Path(__file__).resolve().parents[1];out=root/'artifacts/sources/registry_v5/papers';out.mkdir(parents=True,exist_ok=True)
urls={'veer.pdf':'https://www.se.cs.uni-saarland.de/publications/docs/PKS%2B23.pdf',
      'flash.pdf':'https://www.se.cs.uni-saarland.de/publications/docs/NYM%2B18tse.pdf',
      'moconfig.pdf':'https://gu-youngfeng.github.io/paper/2019_APSEC_MultiObjective.pdf',
      'hsmgp_study.pdf':'https://www.infosun.fim.uni-passau.de/cl/publications/docs/KSK%2B18.pdf'}
records=[]
for name,url in urls.items():
    path=out/name;payload=path.read_bytes() if path.exists() else fetch(url,path)
    records.append({'url':url,'path':str(path.relative_to(root)),'sha256':hashlib.sha256(payload).hexdigest(),'bytes':len(payload)})
(root/'artifacts/registry_v5/papers.json').write_text(json.dumps(records,indent=2)+'\n')
print('Pinned',len(records),'primary paper payloads')
