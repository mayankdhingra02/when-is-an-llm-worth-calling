"""Snapshot audit/prototype artifacts; never authorize or execute collection."""
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
root=Path(__file__).resolve().parents[1];target=root/'reports/registry_v5.freeze.json'
if target.exists():raise RuntimeError('snapshot exists; use a versioned amendment')
paths=['data/registry_v5.json','reports/registry_v5.md','reports/finite_domain_v5_notes.md',
       'src/escalation/registry_v5.py','src/escalation/finite_domain.py',
       'scripts/build_registry_v5.py','scripts/verify_registry_v5.py','scripts/fetch_registry_v5_metadata.py',
       'scripts/fetch_registry_v5_data.py','scripts/fetch_registry_v5_papers.py',
       'tests/synthetic/test_registry_v5.py','artifacts/registry_v5/admission_review.json',
       'artifacts/registry_v5/metadata.json','artifacts/registry_v5/sources.json','artifacts/registry_v5/papers.json',
       'artifacts/registry_v5/verification.json','artifacts/registry_v5/tests_final.log',
       'artifacts/registry_v5/reproducibility.log']
record={'frozen_at':datetime.now(timezone.utc).isoformat(),'scope':'Outcome-blind registry and finite-domain prototype snapshot; no admitted experiment or model adapter',
        'collection_admitted':False,'new_model_requests':0,'new_label_accesses':0,
        'sha256':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths}}
target.write_text(json.dumps(record,indent=2)+'\n');print('V5 audit/preparation snapshot saved')
