import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    assert '608 passed' in (R/'artifacts/study_v84/tests_all.log').read_text()
    pins=json.loads((R/'reports/protocol_v83.freeze.json').read_text())['sha256']
    for n in ['scripts/run_h2_v84.py','scripts/analyze_h2_v84.py','scripts/freeze_h2_v84.py','src/escalation/h2_v84.py','tests/synthetic/test_h2_v84.py','reports/protocol_v84.md','artifacts/study_v84/tests_all.log','requirements.lock.txt']:pins[n]=sha(R/n)
    out=R/'reports/protocol_v84.freeze.json';assert not out.exists();out.write_text(json.dumps({'frozen_at':datetime.now(timezone.utc).isoformat(),'sha256':pins,'scope':'165native trials maximum;1800seconds;no model calls'},indent=2)+'\n');print(sha(out))
if __name__=='__main__':main()
