"""Freeze protocol, admission, dependencies and code before measured outcomes."""
import hashlib, json
from pathlib import Path
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parents[1]
target = ROOT/'reports/protocol_v41_transfer.freeze.json'
if target.exists() or (ROOT/'results/v41_transfer').exists(): raise ValueError('Preserve freeze and outcomes')
paths = list(ROOT.glob('src/escalation/*.py')) + list(ROOT.glob('scripts/*v41*.py')) + list(ROOT.glob('tests/*v41*.py'))
paths += [ROOT/p for p in ('reports/protocol_v41_transfer.md', 'reports/source_audit_v41.md',
    'data/manifest_v41.json', 'artifacts/study_v41/exposure_audit.json', 'artifacts/study_v41/sources.json',
    'results/v6/router_seal.json', 'configs/followup_v3.yaml', 'configs/authorization_v22.json', 'configs/authorization_v38.json',
    'artifacts/model_manifest.json', 'artifacts/model_manifest_v22.json')]
manifest = json.loads((ROOT/'data/manifest_v41.json').read_text())
for d in manifest['datasets']:
    paths += [ROOT/d['path']] + [ROOT/p for p in d['evidence']]
paths += list(ROOT.glob('requirements*.txt')) + list(ROOT.glob('pyproject.toml'))
result = {'at': datetime.now(timezone.utc).isoformat(), 'stage': 'before objective acquisition; model extension ungranted',
          'sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths))}}
target.write_text(json.dumps(result, indent=2)+'\n')
print('Frozen', len(result['sha256']), 'inputs')
