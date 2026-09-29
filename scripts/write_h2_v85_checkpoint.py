"""Checkpoint prepared scope, retaining exact older evidence."""
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    art=ROOT/'artifacts/study_v85';snap=art/'previous_snapshot';snap.mkdir(exist_ok=False);mapping={}
    for n in ['STATUS.md','README.md','reports/next_experiment.md']:
        dest=snap/n;dest.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(ROOT/n,dest);mapping[n]={'snapshot_path':str(dest.relative_to(ROOT)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
    (snap/'mapping.json').write_text(json.dumps(mapping,indent=2)+'\n')
    scope=json.loads((art/'approval_scope.json').read_text());digest=scope['frozen_scope_sha256'];assert digest=='e8ac5ce395f5d36a5f319ecc496a76a7fa54c14a3a972a30bf8d90b5db8f1e17'
    text=f'''# V85 readiness: real local H2 model comparison prepared

The implementation and prospective analysis are frozen. **No V85 model answer or native H2 result has been collected.** The previous allowance is exhausted; the runner rejects execution before startup without a new explicit grant. Preparation advanced the research infrastructure but does not establish a positive optimization/router result or journal readiness.

## Concrete proposed batch

Use the installed SmolLM3-3B-Q4_K_M model and all five saved V84 H2 prefixes. Collect at most **35 real generation requests and 115 new native trials**, capped at **1,800 seconds**, with **USD0 spending and no downloads**. Compare LLM and fresh RF continuations plus the fixed cheap predicate-index prior while the model is resident. The paired arms get10historical prefix +7new search +3charged confirmations; prior gets3fresh trials. Logical planned charges215, physical new115, historical prefix50. Stop on errors/caps; zero retries and no fabricated fallback.

Read [frozen protocol](protocol_v85.md), `configs/study_v85.json`, `src/escalation/h2_v85.py`, `scripts/run_h2_v85.py`, and `scripts/analyze_h2_v85.py`. The prompt includes exact query/data context and only current-arm acquired timings. The finite grammar excludes illegal or already-observed configurations. The analysis checks every model proposal, RF choice, prefix, native answer, order and budget, and separates observed collection cost from modeled deployment cost.

## What actually ran

- Owner-provenance model/runtime pins rechecked against the earlier frozen assets. Nothing downloaded.
- Real local server loaded for health/template/tokenization only. All five actual prefix prompts fit:637–643input tokens. An explicitly synthetic16-observation structure-stress fixture used777tokens. Output reserve64tokens; context4096. The fixture is not a model response or measured benchmark result. Every dynamic prompt will be checked again.
- Preflight used16HTTP calls, **zero generations and zero objective evaluations**,0.890seconds inside runtime accounting, with sampled server peak1,403,027,456bytes. It shut down with exit0; no process remains running. Initial sandbox process-inspection denial preceded startup and is retained at `artifacts/study_v85/prompt_preflight_denied/`; the identical preflight then ran with permission.
- Full explicit suite **619passed**, including synthetic complete-collector budget/isolation coverage, malformed-response abort, failed-transport charging, zero-generation preflight enforcement, paid-endpoint refusal and missing/mismatched approval rejection. Synthetic tests use isolated temporary paths and never enter measured aggregates.
- Actual execution command with the correct scope hash but no grant exited1 with the expected authorization error; it created no collection directory or grant. Receipt: `artifacts/study_v85/authorization_gate_check.json`.

No real end-to-end V85 generation/native collection or real-output analyzer run has occurred. Prompt fit does not establish model quality, grammar-engine correctness for these new prompts, future context fit, or experiment completion. Resource caps may still stop a real batch. V84's executed classical finding remains unchanged:165valid trials, no10%gain over the cheap baseline.

## Exact permission and resume action

AGENTS.md says **“Do not silently increase limits.”** The last explicit V80 inference allowance was fully consumed. A new grant must specifically cover35calls/115trials/30minutes/$0/no-downloads; an unavailable grant is a permission blocker, not unavailable hardware or a request for paid access.

After explicit user approval, create `artifacts/study_v85_execution/user_approval.json` containing `granted:true`, `frozen_scope_sha256:"{digest}"`, `max_generation_requests:35`, `max_physical_trials:115`, `max_stage_seconds:1800`, `max_new_download_bytes:0`, `max_external_spend_usd:0`, the actual user message and timestamp. Do not fabricate that record from a synthetic fixture or an automatic goal continuation. The record is intentionally outside the sealed preparation directory.

Run `{scope['command']}` with required process/loopback permission. Then run `scripts/analyze_h2_v85.py` only if actual collection completes; preserve partial denominators otherwise. Update the cost ledger and STATUS from real receipts. Do not change frozen inputs or reuse V84's model-free continuation timings as fresh controls. Current preparation integrity check: `.venv/bin/python scripts/seal_h2_v85.py --verify-only`.

Cumulative counts unchanged:2,156real model calls;184H2physical trials (183valid,one historical failure);4,817,487,882artifact download bytes with551,221,238remaining under5GiB. External spendingUSD0. Broader gaps remain independent-group generalization, stronger-model robustness, practical utility, clean-machine replication and defensible novelty. This is a preparation checkpoint, not Q2 completion.
'''
    (ROOT/'reports/readiness_v85.md').write_text(text)
    status=f'''# STATUS — V85 real-model H2 comparison prepared; new allowance needed

## Resume here

Read `reports/readiness_v85.md` and frozen `reports/protocol_v85.md`. Implementation, bounded runtime, prompts, tests, analysis and authorization gate are prepared. **No V85 model answers or H2 measurements exist.** Do not present synthetic tests or tokenizer outputs as LLM research results. No process is running. The research goal remains active and unproved; no Q2-readiness claim.

Proposed exact scope: **35 new local SmolLM3 calls,115 new native trials,30minutes maximum,USD0,no downloads**. All five saved V84 prefixes, fresh RF and LLM continuations, and fresh fixed-prior measurements while the model is resident. Paired arms each20logical evaluations including three confirmations; fixed prior only3. The last V80 allowance is exhausted and no new grant is recorded.

## Actual completed work and evidence

Full explicit suite:619tests passed (`artifacts/study_v85/tests_all.log`). Synthetic complete-collector and malformed-response fixtures are isolated and excluded from measurements. Model/runtime hashes verified. Real local prompt preflight: five actual prefix prompts637–643tokens; synthetic structure-stress777;4096context with64reserved output tokens.16HTTP health/template/tokenize calls,zero generations,zero native trials. Preflight runtime0.890seconds, sampled peak1.403GB; server exited0. Initial sandbox `ps` denial was before model startup and is retained separately.

Actual unapproved execution gate test passed: expected exit1, no collection directory, no approval record, no generation/native call. Source and receipts: `src/escalation/h2_v85.py`, `scripts/runtime_h2_v85.py`, `scripts/run_h2_v85.py`, `scripts/analyze_h2_v85.py`, `artifacts/study_v85/`. End-to-end real V85 output validation remains untested because no V85 output exists.

Frozen scope SHA256: `{digest}`. Exact limits/command in `artifacts/study_v85/approval_scope.json`. Verify current evidence/history with `.venv/bin/python scripts/seal_h2_v85.py --verify-only`. Old root docs preserved at `artifacts/study_v85/previous_snapshot/`; never rewrite frozen history.

## Single most important next action

Obtain explicit approval for the concrete35-call/115-trial/30-minute/$0/no-download batch, then execute it unchanged. The reason is AGENTS.md's “Do not silently increase limits” rule and the consumed V80 inference allowance. Real model access is available locally; no payment, cloud, new download or account access is needed.

Only after the user approves, create `artifacts/study_v85_execution/user_approval.json` with the exact scope and actual authorization message, as specified in `reports/readiness_v85.md`. Do not infer a grant from automated goal messages or synthetic tests. Run the command in `approval_scope.json`; follow with the frozen analyzer if complete. Keep failed/unattempted denominators on interruption. The prepared study has a generated workload and one exposed family, so even completion alone will not establish generalizable routing.

## Retained actual finding and costs

V84:165/165valid native trials across five seeds,683.521seconds; zero10%improvements over the cheap indexed baseline for eitherRF or random. Mean query times were0.69%worse forRF and0.30%worse for random. Full trace replay and portable reconstruction passed. See `reports/h2_v84.md`; archive `output/h2_v84_outcome_reconstruction.zip` (3,426,268bytes; SHA256040ffd81bb67741aa5d595fa073b21ad9c44b58b15401a098bc1475a63bb0fa3). These are classical results, not H2LLM evidence.

No new generation/native collection/download spending this turn. Cumulative model calls2,156;H2physical184(183valid+one historical validation failure),eight historical unattempted; Kanzi1,265/RocksDB350physical trials and26,358recorded-table acquisitions unchanged. Artifact downloads4,817,487,882bytes;551,221,238remain under5GiB. External spendingUSD0; electricity/hardware unknown. No publishing,push,contact or cloud authorized. V80 remains a bounded negative real-model result versus its cheap preset.

Remaining research gaps: real H2LLM comparison, sufficient independent held-out paired benefit evidence, stronger-model robustness, practical utility, clean-machine native replication and a defensible contribution against close prior work (`reports/novelty_boundary_v84.md`). Do not fit a claimed generalizable gate to these five seeds.
'''
    (ROOT/'STATUS.md').write_text(status)
    p=ROOT/'README.md';s=p.read_text();anchor='A reproducible, bounded pilot on cost- and reliability-aware escalation in software-configuration optimization.';s=s.replace(anchor,anchor+'\n\n**Prepared V85:** [Real local H2 comparison](reports/readiness_v85.md),35calls/115trials/30minutes/$0/no-downloads;619tests and actual zero-generation prompt preflight passed. Execution awaits a new explicit allowance. No V85model or native result exists.');p.write_text(s)
    (ROOT/'reports/next_experiment.md').write_text('''# Next research action after V85 preparation

The bounded real-model H2 experiment is concrete and frozen. Read `reports/readiness_v85.md` and `reports/protocol_v85.md`; limits and command are in `artifacts/study_v85/approval_scope.json`. Obtain the new explicit35-call/115-trial/30-minute/$0/no-download grant before execution. The previous inference allowance is consumed; do not silently extend it or treat automatic goal messages as approval.

After approval, run the frozen collection, preserving failures and unattempted cases, and independently replay genuine results. Fresh RF and prior controls must run with the model resident; do not substitute model-free V84 continuations. No prompt/prefix tuning on V85 outcomes. Then assess whether any model benefit survives both controls and its measured cost; no one-family router/generalization claim follows.

If the model still adds no benefit, retain that negative result and reassess the scientific contribution before spending on further small-model repetitions. Independent realistic workloads, model-capacity robustness, clean-machine replication and a novelty audit address broader gaps; additional seeds or legal-output success alone do not. Current evidence does not certify Q2 readiness.
''')
if __name__=='__main__':main()
