"""Download one author-hosted source paper under the persistent payload cap."""
import hashlib, json, time
from pathlib import Path
from download_guard import fetch
ROOT=Path(__file__).resolve().parents[1]
url='https://www.se.cs.uni-saarland.de/publications/docs/KMG%2B23.pdf'
path=ROOT/'artifacts/sources/v30/performance_evolution_author.pdf'
start=time.monotonic()
payload=path.read_bytes() if path.exists() else fetch(url,path)
if not payload.startswith(b'%PDF'):raise ValueError('Expected owner PDF')
record={'url':url,'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(payload).hexdigest(),
        'bytes':len(payload),'retrieval_seconds':time.monotonic()-start,
        'source':'Kaltenecker,Muehlbauer,Grebhahn,Siegmund,Apel; author-hosted Performance Evolution manuscript',
        'support':'Table2 page10:Opus encoding time,z3 solving time; sections3.2/3.3; footer links exact owner repository',
        'published_doi':'10.1007/s10664-023-10338-3',
        'scope':'Direction/workload admission only; paper results do not substitute for experimental outcomes'}
(ROOT/'artifacts/study_v30/source.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
