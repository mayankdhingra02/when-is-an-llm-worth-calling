"""Freeze reviewable H2 model study after zero-generation preflight."""
import hashlib,json
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    assert '619 passed' in (ROOT/'artifacts/study_v85/tests_all.log').read_text()
    pre=json.loads((ROOT/'artifacts/study_v85/prompt_preflight/summary.json').read_text());assert pre['complete'] and pre['new_model_generations']==pre['new_objective_evaluations']==0
    pins=json.loads((ROOT/'reports/protocol_v84.freeze.json').read_text())['sha256'].copy()
    old=json.loads((ROOT/'reports/protocol_v78.freeze.json').read_text())['sha256']
    pins.update({n:d for n,d in old.items() if n.startswith(('models/SmolLM3','.local-runtime/llama-')) or n=='artifacts/study_v78/runtime_plan.json'})
    names=['configs/study_v85.json','src/escalation/h2_v85.py','src/escalation/legal_proposals_v66.py','scripts/run_h2_v85.py','scripts/runtime_h2_v85.py','scripts/analyze_h2_v85.py','scripts/preflight_h2_v85.py','scripts/freeze_h2_v85.py','tests/synthetic/test_h2_v85.py','reports/protocol_v85.md','artifacts/study_v85/tests_all.log','results/v84_h2_classical/acquisitions.json']
    names += [f'results/v84_h2_classical/prefix_{seed}.json' for seed in [11,23,37,53,71]]
    names += [str(p.relative_to(ROOT)) for p in (ROOT/'artifacts/study_v85/prompt_preflight').iterdir() if p.is_file()]
    for n in names:pins[n]=sha(ROOT/n)
    for n,d in pins.items():assert sha(ROOT/n)==d,n
    freeze=ROOT/'reports/protocol_v85.freeze.json';assert not freeze.exists();freeze.write_text(json.dumps({'frozen_at':datetime.now(timezone.utc).isoformat(),'status':'prepared; separate explicit allowance required','scope':'35 new real local calls;115new native trials;1800seconds;$0;no downloads','sha256':pins},indent=2)+'\n');digest=sha(freeze)
    scope={'status':'not_yet_received','frozen_scope_sha256':digest,'max_generation_requests':35,'max_physical_trials':115,'max_stage_seconds':1800,'max_new_download_bytes':0,'max_external_spend_usd':0,'model':'SmolLM3-3B-Q4_K_M','command':'.venv/bin/python scripts/run_h2_v85.py --approved-envelope-sha256 '+digest,'required_record':'artifacts/study_v85_execution/user_approval.json','reason':'V80 inference allowance consumed; no silent extension; explicit user grant required.'}
    (ROOT/'artifacts/study_v85/approval_scope.json').write_text(json.dumps(scope,indent=2)+'\n');print(digest)
if __name__=='__main__':main()
