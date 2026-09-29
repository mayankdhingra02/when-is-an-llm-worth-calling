"""Record analyzer-only checks without modifying sealed experiment inputs."""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];ART=ROOT/'artifacts/study_v85_validation'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    assert '625 passed' in (ART/'tests_all.log').read_text()
    scope=json.loads((ROOT/'artifacts/study_v85/approval_scope.json').read_text())
    assert not (ROOT/'artifacts/study_v85_execution/user_approval.json').exists()
    command=[sys.executable,str(ROOT/'scripts/run_h2_v85.py'),'--approved-envelope-sha256',scope['frozen_scope_sha256']]
    r=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=30)
    assert r.returncode!=0 and 'No explicit new 35-request allowance recorded' in r.stderr
    assert not (ROOT/'results/v85_h2_paired').exists()
    (ART/'gate_recheck.json').write_text(json.dumps({'command':command,'exit_code':r.returncode,'stderr':r.stderr,'expected_denial':True,'real_approval_exists':False,'real_collection_exists':False,'new_real_generations':0,'new_native_trials':0,'pending_permission':'35 local requests/115trials/1800seconds/USD0/no downloads','consecutive_goal_turns_with_this_permission_blocker':2,'previous_goal_turn_classification':'progress: frozen preparation and actual zero-generation preflight','current_goal_turn_classification':'progress: independent analyzer acceptance/rejection tests'},indent=2)+'\n')
    snap=ART/'previous_snapshot';snap.mkdir(exist_ok=False);mapping={}
    for n in ['STATUS.md','README.md']:
        dest=snap/n;shutil.copyfile(ROOT/n,dest);mapping[n]={'snapshot_path':str(dest.relative_to(ROOT)),'sha256':sha(dest)}
    (snap/'mapping.json').write_text(json.dumps(mapping,indent=2)+'\n')
    report='''# Independent V85 analyzer validation

Six additional isolated synthetic tests now exercise the frozen analyzer itself. The complete fixture covers five prefixes, 35 simulated proposals, 115 simulated native records and the full paired/standalone budget structure. Java count/sum outputs are fixture values derived from the deterministic formulas, not an executed database. The analyzer validates these records, replays classical decisions and checks every synthetic scored query answer.

Five semantic changes were each rejected: changed physical-charge denominator; mismatched LLM prefix; extra hidden information in a prompt; an already-acquired/illegal proposal; and a wrong SQL aggregate answer. The positive fixture uses plausible internally bounded timing values but all model/native timings and responses are synthetic. No substantive performance conclusion can be drawn from it. Temporary roots are explicitly named SYNTHETIC_H2_ANALYZER_ONLY; nothing is written to the real V85 collection directory.

Actual command `.venv/bin/python -m pytest tests -q` passed **625 tests**, including the six new checks. The original frozen preparation suite remains619; none of its source, protocol, model, runtime, prefix or test-log pins was changed. No amendment to the proposed inference scope is needed. Model grammar enforcement and the whole real-model/native integration remain untested for V85 until the real batch executes.

The exact real collector command was tried again with the correct frozen hash but without a grant. It rejected startup as intended, created no collection directory and made no model/native calls. `gate_recheck.json` records this permission check. The automated goal continuation is not an explicit new inference allowance.

No real generation, native evaluation, download, model load or external spending occurred in this validation turn. The prior local preflight already established model availability; the only immediate execution blocker is approval of35localcalls/115trials/30minutes/USD0/no downloads. AGENTS.md says “Do not silently increase limits”; the V80 allowance is consumed. This is the second consecutive goal turn encountering that condition, so the goal remains active pending the required input. Additional same-scope bookkeeping or synthetic tests are not a substitute for obtaining real paired outcomes.

Evidence: `tests/synthetic/test_h2_v85_analyzer.py`, `artifacts/study_v85_validation/tests_all.log`, `artifacts/study_v85_validation/gate_recheck.json`. Verify complete evidence/history with `.venv/bin/python scripts/seal_h2_v85_validation.py --verify-only`. The original experiment remains frozen at e8ac5ce395f5d36a5f319ecc496a76a7fa54c14a3a972a30bf8d90b5db8f1e17.
'''
    (ROOT/'reports/validation_v85.md').write_text(report)
    p=ROOT/'STATUS.md';s=p.read_text();needle='## Actual completed work and evidence';insert='''## Subsequent independent analyzer check

Read `reports/validation_v85.md`. Six new isolated synthetic analyzer tests passed, including rejection of altered budgets, mismatched prefixes, leaked prompt information, illegal responses and incorrect query answers. Full suite: **625 passed**. These fixtures are not real LLM/native results. All frozen V85 inputs and the619-test preparation log are unchanged.

The exact collector still rejects the absent grant before startup. No real V85 output directory exists; zero new model/native calls or downloads. This is the second consecutive goal turn encountering the same permission blocker; the goal remains active. The next substantive action is the already-prepared real batch, not more synthetic or bookkeeping work. Current evidence/history check: `.venv/bin/python scripts/seal_h2_v85_validation.py --verify-only`. Prior root docs are preserved in `artifacts/study_v85_validation/previous_snapshot/`.

''';s=s.replace(needle,insert+needle);p.write_text(s)
    p=ROOT/'README.md';s=p.read_text();anchor='A reproducible, bounded pilot on cost- and reliability-aware escalation in software-configuration optimization.';s=s.replace(anchor,anchor+'\n\n[Independent V85 analyzer checks](reports/validation_v85.md) passed;625tests total. All new traces were explicitly synthetic; the real35-call/115-trial batch still awaits its allowance.');p.write_text(s)
if __name__=='__main__':main()
