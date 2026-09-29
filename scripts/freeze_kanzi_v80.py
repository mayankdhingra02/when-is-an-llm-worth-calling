"""Freeze prepared V80 after verified V79 prefixes; never starts inference."""
import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def main():
    assert json.loads((ROOT/'artifacts/study_v79/replay_verification.json').read_text())['verified']
    assert '594 passed' in (ROOT/'artifacts/study_v80/tests.log').read_text()
    pins=json.loads((ROOT/'reports/protocol_v78.freeze.json').read_text())['sha256'].copy()
    pins.update(json.loads((ROOT/'reports/protocol_v79.freeze.json').read_text())['sha256'])
    names=['src/escalation/kanzi_policy_v80.py','scripts/run_kanzi_v80.py','scripts/worker_kanzi_v80.py','scripts/analyze_kanzi_v80.py','configs/study_v80.json','tests/synthetic/test_kanzi_v80.py','reports/protocol_v80.md','artifacts/study_v80/tests.log','artifacts/study_v79/replay_verification.json','scripts/freeze_kanzi_v80.py']
    prefixes=sorted((ROOT/'results/v79_kanzi_classical').glob('prefix_*.json'));assert len(prefixes)==15
    names += [str(p.relative_to(ROOT)) for p in prefixes]
    for name in names:pins[name]=sha(ROOT/name)
    for name,d in pins.items():assert sha(ROOT/name)==d,name
    freeze=ROOT/'reports/protocol_v80.freeze.json';assert not freeze.exists()
    freeze.write_text(json.dumps({'frozen_at':datetime.now(timezone.utc).isoformat(),'status':'prepared; separate explicit105-request allowance required before inference','scope':'all15V79prefixes;105real local calls;450new trials;1800seconds;$0/zero downloads','sha256':pins},indent=2)+'\n')
    digest=sha(freeze)
    (ROOT/'artifacts/study_v80/approval_scope.json').write_text(json.dumps({'status':'not_yet_received','frozen_scope_sha256':digest,'max_generation_requests':105,'max_physical_trials':450,'max_stage_seconds':1800,'max_new_download_bytes':0,'max_external_spend_usd':0,'command':'.venv/bin/python scripts/run_kanzi_v80.py --approved-envelope-sha256 '+digest,'reason_new_allowance_required':'V78 requests consumed;105also exceeds initial100-call default; no silent increase permitted.'},indent=2)+'\n')
    print(digest)
if __name__=='__main__':main()
