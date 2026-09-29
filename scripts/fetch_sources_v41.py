"""Archive primary admission evidence under existing download caps."""
import hashlib, json, shutil
from pathlib import Path
from download_guard import fetch
ROOT = Path(__file__).resolve().parents[1]
out = ROOT/'artifacts/study_v41'
out.mkdir(parents=True, exist_ok=True)
history = ROOT/'artifacts/history/v41_before_collection'
history.mkdir(parents=True, exist_ok=True)
for name in ('STATUS.md', 'artifacts/resource_ledger_v2.json', 'artifacts/download_ledger.json'):
    target = history/Path(name).name
    if not target.exists(): shutil.copy2(ROOT/name, target)
sources = [
    ('fse15.pdf', 'https://www.se.cs.uni-saarland.de/publications/docs/SGA%2B15.pdf'),
    ('deepperf.pdf', 'https://hongyujohn.github.io/DeepPerf.pdf'),
    ('fse15_supplement.html', 'https://www.se.cs.uni-saarland.de/projects/splconqueror/esecfse2015.php'),
]
records = []
for name, url in sources:
    path = ROOT/'artifacts/sources/v41'/name
    data = path.read_bytes() if path.exists() else fetch(url, path)
    if name.endswith('.pdf') and not data.startswith(b'%PDF'): raise ValueError('Expected PDF')
    records.append(dict(path=str(path.relative_to(ROOT)), url=url, sha256=hashlib.sha256(data).hexdigest(), bytes=len(data)))
(out/'sources.json').write_text(json.dumps(records, indent=2)+'\n')
print(json.dumps(records, indent=2))
