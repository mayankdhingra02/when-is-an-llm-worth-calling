"""Record current v4 analysis/report evidence hashes, without collection."""
import hashlib,json
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[1]
files=[root/'reports/protocol_v4.freeze.json',root/'data/registry_v4.json',root/'configs/study_v4.json']
files+=list((root/'results/v4_projection_diagnostic').rglob('*'))
files += [root/p for p in ['scripts/verify_projection_v4.py','scripts/analyze_projection_v4.py','scripts/report_v4.py',
                          'scripts/record_v4_manifest.py','reports/pilot_report_v4.md','reports/registry_audit_v4.md',
                          'artifacts/resource_ledger_v2.json','artifacts/download_ledger.json',
                          'artifacts/registry_v4/tests_final.txt','artifacts/registry_v4/projection_verification.json',
                          'artifacts/registry_v4/preflight.json']]
manifest={'recorded_at':datetime.now(timezone.utc).isoformat(),
          'scope':'post-run v4 evidence/analysis hashes; frozen collection code/input hashes remain in protocol_v4.freeze.json',
          'sha256':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(files)) if p.is_file()}}
(root/'artifacts/registry_v4/evidence_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Recorded',len(manifest['sha256']),'v4 evidence files')
