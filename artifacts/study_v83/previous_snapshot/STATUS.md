# STATUS — V80 real-model comparison completed; no size benefit beyond preset

## Resume here

The user's “Continue” directly answered the exact 105-call/450-trial/30-minute/$0/no-download approval question. Approval is recorded separately at `artifacts/study_v80_execution/user_approval.json`. All **105 genuine local SmolLM3 requests and 450 physical trials completed**, with zero invalid responses, retries, fallbacks or application failures, in **784.759 seconds**. All model/native processes exited; no experiment remains running. V80's frozen collection code, prompt, seeds, workloads and limits were unchanged.

**Concrete finding:** versus the cheap preset, the LLM had **0 wins / 10 ties / 5 losses** across 15 workload/seed cases, adding **9.852 seconds of decision time per case** on average. Mean files were **1.720% larger on text, 1.465% larger on binary records, and 3.735% larger on XML**. Versus RF: 4 wins / 6 ties / 5 losses. Thus the observed gains versus RF do not survive this stronger cheap comparator. Even hindsight selection between preset and LLM cannot improve size over the preset in this finite sample. All requests were valid, so this negative optimization result is not explained by response parsing failures.

All three inputs are variants of ONE exposed Kanzi development family, using the V76 buffer-fix adaptation. No learned router was fitted; no generalization, universal model limitation, significance or Q2-readiness claim is established. Same-model RocksDB V72 remains separately negative against both controls; do not pool its milliseconds with these bytes.

## Evidence and actual verification

Read `reports/kanzi_v80.md` and `reports/reproduction_v80.md`. Raw prompts/responses/commands/logs/receipts: `results/v80_kanzi_paired/`. Verified JSON, per-case CSV, cost estimates and inspected figures: `results/v80_kanzi_analysis/`. Post-hoc proposal diagnostic: `results/v80_proposal_diagnostic/`. Approval, costs, audit and history records: `artifacts/study_v80_execution/`.

Frozen analyzer and supplementary verifier passed: every acquired-only choice/shared prefix/round order/budget/grammar/request/usage checked, plus all 900 exact native commands and resource receipts. All 135 confirmation sizes repeat within their own three-repetition sets. Stream checksum, header/settings and exact decompression passed during collection. Validated bulky payloads were removed per protocol; offline replay checks retained receipts rather than recreating removed bytes.

Pre-collection frozen suite: 594 tests passed. Additional actual isolated standard-library replay passed on Python 3.10.13 with `-I -S`; three synthetic corruptions (reported mean, arm budget, request denominator) were rejected after their hashes were updated. Fixtures are excluded from measured results. This is saved-outcome reconstruction, not full RF policy replay or clean-machine native/model remeasurement.

Local portable archive: `output/kanzi_v80_outcome_reconstruction.zip`, 3,236,610 bytes, SHA256 `464cfbd561ef170d80f6a67c180e9eed5f0de6c6afc0fa633f6ed649c65c0b8c`. It excludes corpus/model/runtime payloads and includes a report snapshot before the reproduction addendum. Extract and run `python3 -I -S scripts/replay_kanzi_v80_portable.py`. Nothing was published or pushed.

Current complete evidence/history check: `.venv/bin/python scripts/seal_v80_execution.py --verify-only`. Do not regenerate sealed artifacts in place; use a separate copy. Prior current documents are preserved in `artifacts/study_v80_execution/previous_snapshot/`.

## Executed commands and failures

Executed the frozen `.venv/bin/python scripts/run_kanzi_v80.py --approved-envelope-sha256 9369379ed6b74d19b5eb031875314ee27303d57027f7783fe525437e688d6814`. Initial sandbox `ps` denial happened before collection; exact command then ran with process-inspection permission. No experimental retry or extra model requests resulted from that preflight denial.

Completed `analyze_kanzi_v80.py`, `verify_kanzi_v80_addendum.py`, `report_kanzi_v80.py`, `diagnose_kanzi_v80.py`, `write_kanzi_v80_report.py`, `bundle_kanzi_v80.py` and `check_portable_kanzi_v80.py` using the project Python. Post-hoc diagnostics used acquired outcomes only: 69/105 valid proposals were in the preset transform/entropy family; ten final LLM incumbents were the same candidate439. This describes observed choices, not internal reasoning or causal mechanisms.

## Costs and remaining limits

105 new model requests; cumulative 2,156. 61,181 observed input tokens and 970 output tokens; no unknown usage. 319 HTTP requests including health/template/tokenization. 450 new physical trials (315 search,135 confirmation),900 native processes,900 logical charges including150 reused historical prefix trials. Recent V74–V80 Kanzi physical total1,265, retaining two earlier application failures. Prior RocksDB V71/V72 trials350 remain separate; recorded-table acquisitions26,358 unchanged.

V80 downloads0 and external spendingUSD0. Cumulative downloads4,814,795,101bytes;553,914,019bytes remain. Electricity/hardware costs unknown. Actual three-arm collection costs and modeled selected-branch costs are separate; deployment estimates exclude some prefix/controller overhead and are not production runtime measurements.

The explicit V80 allowance is fully consumed. No pending approval is required to finish this completed stage, and no future inference scope is implied. Broader source/admission/reproduction work can continue without new model calls. No cloud, paid API, credential use, publication, push or author contact is authorized.

## Single most important next action

Design a prospectively selected **additional independent software-family replication with a credible cheap domain baseline**, using metadata/correctness/resource criteria rather than selecting tasks for favorable LLM outcomes. Do not fit a benefit-aware gate on these seeds: there is zero observed size headroom beyond the preset, and only one Kanzi family. See `reports/next_experiment.md` for the research decision and remaining gaps. A stronger-model allowance or larger independent study, if justified later, requires its own concrete scope rather than repeated prompts on exposed outcomes.

Still untested: independent-family transfer of this baseline-adjusted finding, useful pre-decision routing on tasks with material genuine model benefit, clean-machine native V80 reproduction, and a practical cost/quality utility. The result is a credible bounded negative finding with a replayable artifact, not demonstrated Q2 readiness or a positive escalation controller.
