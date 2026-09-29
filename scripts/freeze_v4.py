"""Freeze v4 design/control before diagnostic collection; never overwrite."""
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
root=Path(__file__).resolve().parents[1]
target=root/'reports/protocol_v4.freeze.json'
if target.exists() or (root/'results/v4_projection_diagnostic').exists():
    raise RuntimeError('freeze/output exists; make a versioned amendment')
paths=['reports/protocol_v4.md','configs/study_v4.json','data/registry_v4.json',
       'data/manifest_v3.json','configs/followup_v3.yaml','requirements.lock.txt',
       'scripts/fetch_registry_sources.py','scripts/build_registry_v4.py','scripts/preflight_v4.py']
paths += [str(p.relative_to(root)) for p in (root/'src/escalation').glob('*.py')]
paths += [str(p.relative_to(root)) for p in (root/'results/v3/classical/prefixes').glob('*.json')]
record={'frozen_at':datetime.now(timezone.utc).isoformat(),
        'scope':'larger-study design and exposed-system projection diagnostic; not final larger collector',
        'sha256':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in sorted(paths)}}
target.write_text(json.dumps(record,indent=2)+'\n')
print('Frozen',len(paths),'inputs before diagnostic collection')
