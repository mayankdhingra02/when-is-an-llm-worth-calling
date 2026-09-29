"""Actually exercise denial before model/native collection, without creating a grant."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    scope=json.loads((ROOT/'artifacts/study_v85/approval_scope.json').read_text())
    assert not (ROOT/'artifacts/study_v85_execution/user_approval.json').exists()
    assert not (ROOT/'results/v85_h2_paired').exists()
    command=[sys.executable,str(ROOT/'scripts/run_h2_v85.py'),'--approved-envelope-sha256',scope['frozen_scope_sha256']]
    r=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=30)
    assert r.returncode!=0 and 'No explicit new 35-request allowance recorded' in r.stderr
    assert not (ROOT/'results/v85_h2_paired').exists()
    report={'command':command,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'expected_denial_verified':True,'collection_directory_created':False,'grant_created':False,'new_generation_requests':0,'new_native_trials':0}
    (ROOT/'artifacts/study_v85/authorization_gate_check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['stderr','command']},indent=2))
if __name__=='__main__':main()
