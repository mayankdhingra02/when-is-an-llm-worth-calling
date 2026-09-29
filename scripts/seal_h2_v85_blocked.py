"""Record the third verified permission blocker without modifying frozen science."""
import argparse,json,shutil,subprocess,sys
from datetime import datetime,timezone
from seal_h2_v85_validation import ROOT,sha,read,history as older_history
ART=ROOT/'artifacts/study_v85_blocked'
def history():
    hist=older_history();m=ROOT/'artifacts/study_v85_validation/evidence_manifest.json';assert sha(m)=='6ebe56c4cc5a0fc6690b0b82cb611be78a31df57b33ed6026585269169490355'
    mapping=read(ART/'previous_snapshot/mapping.json');redirects={};files=read(m)['files']
    for n,meta in files.items():
        p=ROOT/n
        if p.exists() and sha(p)==meta['sha256'] and p.stat().st_size==meta['bytes']:continue
        assert n in mapping,n
        p=ROOT/mapping[n]['snapshot_path'];assert sha(p)==meta['sha256'] and p.stat().st_size==meta['bytes'],n;redirects[n]=str(p.relative_to(ROOT))
    return hist+[{'stage':'v85_synthetic_analyzer_validation','verified_files':len(files),'manifest_sha256':sha(m),'redirects':redirects}]
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args();manifest=ART/'evidence_manifest.json'
    if args.verify_only:
        hist=history();data=read(manifest)
        for n,m in data['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
        print(json.dumps({'verified':True,'files':len(data['files']),'manifest_sha256':sha(manifest),'historical':hist},indent=2));return
    assert not ART.exists();assert not (ROOT/'artifacts/study_v85_execution/user_approval.json').exists();assert not (ROOT/'results/v85_h2_paired').exists()
    previous=read(ROOT/'artifacts/study_v85_validation/gate_recheck.json');assert previous['consecutive_goal_turns_with_this_permission_blocker']==2
    scope=read(ROOT/'artifacts/study_v85/approval_scope.json');command=[sys.executable,str(ROOT/'scripts/run_h2_v85.py'),'--approved-envelope-sha256',scope['frozen_scope_sha256']]
    r=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=30);assert r.returncode==1 and 'No explicit new 35-request allowance recorded' in r.stderr;assert not (ROOT/'results/v85_h2_paired').exists()
    ART.mkdir();snap=ART/'previous_snapshot';snap.mkdir();shutil.copyfile(ROOT/'STATUS.md',snap/'STATUS.md')
    (snap/'mapping.json').write_text(json.dumps({'STATUS.md':{'snapshot_path':str((snap/'STATUS.md').relative_to(ROOT)),'sha256':sha(snap/'STATUS.md')}},indent=2)+'\n')
    (ART/'audit.json').write_text(json.dumps({'at':datetime.now(timezone.utc).isoformat(),'consecutive_goal_turns_with_same_blocker':3,'blocker':'Explicit new 35-call/115-trial/1800-second/USD0/no-download allowance absent; prior allowance exhausted.','previous_turn_classification':'progress: six independent analyzer tests completed','current_turn_classification':'no further substantive unblocked progress; permission gate revalidated','required_next_goal_status':'blocked','objective_achieved':False,'approval_exists':False,'real_collection_exists':False,'new_real_generations':0,'new_native_trials':0,'command':command,'exit_code':r.returncode,'stderr':r.stderr,'scope':scope},indent=2)+'\n')
    (ROOT/'STATUS.md').write_text('''# STATUS — blocked on the explicit V85 inference allowance

## Resume here

The same permission blocker has been revalidated for three consecutive goal turns. The research objective is **not complete** and Q2 readiness is unproved. No benchmark/model process is running. The automatic goal continuation is not an explicit allowance extension.

**Required next input:** approval of the prepared batch: **35 local SmolLM3 calls, up to115new H2 trials, at most30minutes, USD0spending and no downloads**. The previous V80 allowance is consumed; AGENTS.md says “Do not silently increase limits.” Local model access is available. No paid/cloud/account resource is needed.

Read `reports/readiness_v85.md`, `reports/protocol_v85.md`, and `reports/validation_v85.md`. Exact scope/command: `artifacts/study_v85/approval_scope.json`. The immutable protocol hash remains `e8ac5ce395f5d36a5f319ecc496a76a7fa54c14a3a972a30bf8d90b5db8f1e17`. Only after explicit user approval, record the actual grant in `artifacts/study_v85_execution/user_approval.json` with the matching limits/hash and message, then run the prepared command. Do not create a grant from synthetic fixtures or automated goal messages.

## Completed preparation and retained results

The local model loaded successfully for template/tokenization checks only: five actual prefix prompts637–643tokens, synthetic stress fixture777; zero generated answers or native trials. Server shut down. The prepared collector, grammar, acquired-only prompts, model/runtime pins and analyzer are frozen. Independent synthetic tests checked full analysis and rejected five corrupted-record cases. Full suite625passed; the original619-test preparation log is unchanged. These fixtures are not measured LLM outcomes.

The real collector was rechecked with its correct scope hash and no grant: expected exit1, no real collection directory, no model/native calls. Three-turn audit: `artifacts/study_v85_blocked/audit.json`. Meaningful independent preparation/validation for this next batch is complete; further bookkeeping or synthetic traces cannot supply the missing real paired evidence.

Latest actual experiment remains V84:165/165valid H2 native trials, five seeds,683.521seconds. RF/random each had20logical evaluations versus the standalone prior's3. Neither achieved the predeclared10%gain over the cheap baseline. Mean query times were0.69%worse forRF and0.30%worse forrandom. See `reports/h2_v84.md`. Saved-outcome archive `output/h2_v84_outcome_reconstruction.zip` passed isolated replay and corruption checks; it is not a fresh native rerun. V80 retains105real model calls and450valid native trials with0wins/10ties/5lossesagainstitscheap preset.

## Costs, integrity and remaining scientific gaps

No new real generation, native measurement, download or external spending in this blocker check. Cumulative model calls2,156; H2physical184(183valid,one historical failure),eight historical unattempted; Kanzi1,265/RocksDB350physical trials;26,358recorded-table acquisitions. Artifact downloads4,817,487,882bytes;551,221,238bytes remain under5GiB. Electricity/hardware costs unknown. No cloud,publish,push or contact authorized.

Verify current evidence/history with `.venv/bin/python scripts/seal_h2_v85_blocked.py --verify-only`. Previous STATUS preserved in `artifacts/study_v85_blocked/previous_snapshot/`; all prior frozen artifacts remain unchanged.

Still missing: real H2LLM continuation, sufficient independent held-out paired benefit evidence, stronger-model robustness, practical utility, clean-machine native replication and defensible novelty. Approval enables the next experiment, not a guarantee of a positive result or journal acceptance.
''')
    hist=history();paths={ROOT/'STATUS.md',ROOT/'scripts/seal_h2_v85_blocked.py',ROOT/'artifacts/study_v85_validation/evidence_manifest.json'};paths.update(p for p in ART.rglob('*') if p.is_file())
    manifest.write_text(json.dumps({'scope':'third verified permission blocker; no new research measurements','historical':hist,'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}},indent=2)+'\n');print(json.dumps({'files':len(paths),'manifest_sha256':sha(manifest)}))
if __name__=='__main__':main()
