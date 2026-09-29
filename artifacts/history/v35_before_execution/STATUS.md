# STATUS — V34 concrete result complete

Updated 2026-09-25. Resume here and from [V34 report](reports/constrained_v34.md), [frozen protocol](reports/protocol_v34_constrained.md), and relevant code. Do not reread the entire initial literature report. Prior STATUS/README/resource ledgers are preserved under `artifacts/history/v34_before_execution/`.

**Result:** Real cached 1.5B assigned-ID selections have **−0.3015%** mean feasible-runtime gain versus size-aware shortlist3NN (1 win,6 ties,3 harms). They beat static ranking by +1.3495%, but lose to full-domain joint3NN (−1.6470%) and runtime3NN (−2.6023%). Across all three presentations versus runtime3NN:0 wins,19 ties,11 harms. This is a concrete control-sensitive result, not successful generalizable routing.

## Actual execution

- Ten shared prefixes: Brotli0.3.0 and lrzip530, five fixed seeds each.
- Seven continuations per prefix; **70/70 complete**,20 distinct configurations per arm inclusive of10-prefix.
- **800 new recorded runtime/size-vector accesses** (100 prefix +700 continuation), all charged and logged; no new model calls/physical trials/downloads.
- Thirty real V22 response selections reused with original runtime-only prompts; this is retrospective constrained evaluation, **not size-aware LLM inference**.
- Acquired-prefix fastest row supplies the size cap; same V11/V12 default, not application-approved quality.
- Two adaptive size-aware controls plus static/runtime controls; all decisions replayed. All full-domain joint3NN traces match V12.
- **233 tests passed in1.24s**;224 frozen inputs;800 ordered raw entries verified;120 paired comparisons and240 Decimal gains checked;60 original model provenance records replayed;2,736 frozen historical/current references passed. Figure inspected.

## Commands and evidence

Executed preparation: `.venv/bin/python scripts/prepare_constrained_v34.py`.
Executed collection: `.venv/bin/python scripts/run_constrained_v34.py`.
Executed analysis: `.venv/bin/python scripts/analyze_constrained_v34.py`.
Read-only replay: `.venv/bin/python scripts/analyze_constrained_v34.py --verify-only`.
Tests: `.venv/bin/python -m pytest -q`.
Provenance: `.venv/bin/python scripts/verify_report_larger_v22.py --verify-only`.
Historical integrity: `.venv/bin/python scripts/audit_history_v30.py`.

- Report: `reports/constrained_v34.md`; prospective priorities: `reports/next_experiment_v34.md`.
- Protocol/freeze: `reports/protocol_v34_constrained.md` and `.freeze.json`.
- Source/version/action manifest: `data/constrained_v34.json`.
- Raw: `results/v34_constrained/acquisitions.jsonl`, `prefixes/`, `arms/`, `checkpoints/`, `progress.json`.
- Numbers: `results/v34_constrained/summary.json`, `comparisons.csv`, `arms.csv`, `reliability.csv`.
- Figures: `results/v34_constrained/constrained_gains.png` and `.svg`.
- Logs/accounting/verification/final receipt: `artifacts/study_v34/`.

Collection and analysis completed without experiment failures. No active/scheduled job. No publication,push,contact,cloud use or external spending. Existing V26 reconstruction ZIP unchanged and remains a V25 snapshot, not a complete V34 bundle.

## Limits and retained findings

V34 is exploratory on two exposed families. Runtime-only model prompts cannot answer a new size-aware prompt counterfactual. No fresh physical correctness, per-row noise, unseen-system generalization, learned-router benefit or actual deployment savings tested here. All three presentations and weaker/stronger controls are reported; no favorable presentation selected.

Earlier verified findings remain: original SNAP2 artifact unlocated, implementations labeled adaptations; corrected V3 smoke; V6 sealed group-aware router with no held-out advantage; V22 real1.5B model with presentation sensitivity; V29 stronger runtime3NN average advantage; V30/V31 fresh classical transfer and low shortlist headroom; V32 timing-reliability sign changes; V33 hypothetical request-cost recovery,not real deployment savings. Historical evidence map is in README.

## Remaining allowance

Cumulative experiment runtime **2281.347753/3600s**; remaining **1318.652247s**. V34 added **4.229261s**. Read-only checks and software development are outside this experiment ledger.

Follow-up model requests **200/200**,300 including initial stage; generic continuation does not expand the allowance. Recorded accesses **9,108**; physical trials **1,274**. Downloads remain4,518,268,306bytes total /4,098,574,535model bytes. External spendUSD0.

**Single next action:** freeze an application-grounded prospective protocol (quality bound,practical gain margin,strong controls,untouched groups) before fresh size-aware paired inference. Fresh inference is blocked by the exhausted request allowance; it requires an explicit bounded local-call extension or a genuinely compatible provenance-checked cache. Additional exposed-case variants are not a route to credible generalization.
