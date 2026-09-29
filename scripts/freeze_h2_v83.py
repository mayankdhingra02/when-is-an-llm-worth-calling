import hashlib,json
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    assert '604 passed' in (R/'artifacts/study_v83/tests_all.log').read_text()
    out=R/'reports/protocol_v83.freeze.json';assert not out.exists()
    pins=json.loads((R/'configs/runtime_v83.lock.json').read_text())['sha256']
    for n in ['scripts/run_h2_v83.py','src/escalation/h2_v83.py','scripts/freeze_h2_v83.py','scripts/prepare_h2_v83.py','src/escalation/bounded_process_v57.py','src/escalation/receipts_v70.py','scripts/run_planning_v55.py','reports/protocol_v83.md','configs/runtime_v83.lock.json','tests/synthetic/test_h2_v83.py','artifacts/study_v83/tests_all.log']:pins[n]=sha(R/n)
    out.write_text(json.dumps({'frozen_at':datetime.now(timezone.utc).isoformat(),'sha256':pins,'scope':'9 new native feasibility trials;600seconds;no model calls; V81 failure retained'},indent=2)+'\n');print(sha(out))
if __name__=='__main__':main()
