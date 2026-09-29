# STATUS — H2 V81–V83 native feasibility completed

## Resume here

Read `reports/h2_v83.md` and frozen `reports/protocol_v83.md`. H2 source admission, original JDBC harness and actual trials are complete. **19 physical charges;18 validated,one retained V81 validation failure;eight V81 slots unattempted.** V82/V83 each nine correct trials. V83 **passes the coarse same-host precision screen**. No new LLM calls; no process remains running. H2 is one exposed development family, distinct from prior Kanzi/RocksDB. This stage does not establish a positive routing result or Q2 readiness.

## Evidence and commands

Raw commands,settings,index metadata,exact answers,times and receipts: `results/v81_h2_feasibility/`, `results/v82_h2_feasibility/`, `results/v83_h2_feasibility/`. Revalidated summaries and inspected figures: `results/v82_h2_analysis/`, `results/v83_h2_analysis/`. Source audit `reports/source_audit_v81.md`; third-party attribution `reports/third_party_v81.md`; source receipts `artifacts/study_v81/download_ledger.json`. Each protocol/compiled harness/runtime is pinned before its measurements. V81 failed because H2 omitted a metadata field; V82 verifies the engine flag directly. V82 timings violated the precision floor/spread; V83 lengthened fixed warm-up and measurement prospectively, without changing configurations. Preserve all stages.

Executed fetch/prepare/run H2 scripts V81–V83 and `analyze_h2_v82.py` for82/83. Full explicit suite:604passed (`artifacts/study_v83/tests_all.log`). Synthetic wrong-answer/index/reuse fixtures excluded from research data. Initial sandbox network/process denials were preflight-only; reruns had required permission. V82 missing build-directory parent fixed before freeze. All native application processes exited0; V81 validation still counted as failure. No model retry, fabricated output or paid request.

Current evidence/history check: `.venv/bin/python scripts/seal_h2_v83.py --verify-only`. Previous root docs preserved at `artifacts/study_v83/previous_snapshot/`; never rewrite frozen old evidence. Timing criteria and limitations are explicit in the report. Saved-output verification is not a clean-machine rerun.

## Costs and prior result

New native H2 trials19; native valid18; native validation failures1. Runner-measured total75.104297s excludes initial pin checks/Python oracle and analysis. Model calls0new,2156cumulative. Download2692781newbytes,4817487882cumulative,551221238remaining under5GiB. USD0external spend; electricity/hardware unknown. Recent Kanzi physical trials1265 and RocksDB350 remain separate; recorded-table acquisitions26358 unchanged. H2 querytime excludes setup/index-build; deployment utility is untested.

V80 remains a credible bounded negative result:105realSmolLM3calls,450validtrials;0wins/10ties/5lossesvscheap preset,4/6/5vsRF;9.852seconds extra decisiontime/case. Three inputs are one Kanzi family. See `reports/kanzi_v80.md`, `reports/reproduction_v80.md` and portable ZIP. V80 inference allowance is consumed; no new model batch defined. Read-only/source/classical/reproduction work remains authorized within limits; no paid/cloud/push/contact.

## Single most important next action

Freeze a classical-only H2 comparison with the predicate-index prior, a deterministic optimizer, five fixed seeds,20 evaluations/checkpoint10, and independent final confirmations; include index-building amortization and predeclare a practically relevant gain threshold. Do not add model calls before that baseline check.

Remaining untested: H2 classical budgeted optimization, real model continuation on H2, baseline-adjusted transfer to independent untouched software groups, useful learned routing, practical deployment utility, and clean-machine native/model replication. Scientific honesty takes priority over a positive outcome.
