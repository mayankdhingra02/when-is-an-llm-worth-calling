# Status — 2026-09-24 America/New_York: V24 exact opportunity result complete

## Resume here

[Current report](reports/opportunity_v24.md): even perfect hindsight routing yields at most **0.00023694 mean normalized-loss gain over first-displayed-ten selection**, using4/15 calls in the empirical average-presentation scenario. Random escalation at the same rate yields0.00005113 expected gain. Using each prefix's minimum gain across the three observed presentations, best hindsight gain is **zero**, achieved with zero calls. Hindsight knows counterfactual outcomes and is not deployable.

This answers a new question beyond V23: how much quality improvement could routing possibly recover at each call budget? It does not show that predecision features predict the good cases or that the gain justifies inference costs.

## What actually ran

All15 saved development cases,4 baselines,2 presentation scenarios and16 budgets(k=0..15). Exhaustively enumerated32768 subsets per comparison,262144 allocations total. Independently checked sorted-gain maxima and exact random allocation expectations. No model calls,new objective accesses,physical trials,downloads or external spending.

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/analyze_opportunity_v24.py
.venv/bin/python scripts/analyze_opportunity_v24.py --verify-only
```

**171 tests passed in1.42seconds.** All128 frontier rows independently reconstructed from V22 CSV using Decimal gains, including selected sets and binomial subset counts. Read-only replay passed. Figure visually inspected. A seven-file analysis freeze preceded new computation, after V22/V23 exposure; this is explicitly post-hoc development analysis. No failed V24 commands/tests or incomplete denominators.

## Evidence

- [Report](reports/opportunity_v24.md), [all curves and selected-case usage](results/v24_opportunity/summary.json), [CSV](results/v24_opportunity/frontiers.csv), [figure](results/v24_opportunity/frontiers.png).
- Fixed plan/code/tests/inputs: reports/protocol_v24_opportunity.md and .freeze.json.
- Execution/tests/replay/independent checks/costs: artifacts/study_v24/analysis.log,tests.log,replay.log,verification.json,accounting.json.
- Actual underlying model provenance: results/v22_larger/requests.jsonl,request_starts.jsonl,arms/,acquisitions.jsonl and model manifests. V23 saved per-case gains feed V24; no fabricated outputs substituted.
- Pre-V24 mutable documents and exact ledger: artifacts/history/v24_before_analysis/. Prior STATUS preserves all V23 details. Older PDF/ZIP remain V21 snapshots; do not present them as current.

## Costs and interpretation

The four-case average-presentation hindsight choice corresponds to28.3981 request-seconds,6192 input tokens and80 output tokens, using averages of the recorded three presentations. This is retrospective one-branch usage, not predicted/deployed cost; excludes startup,training and historical collection. A15-case deployment scenario has300 logical evaluations. No dollar savings or arbitrary quality/time utility claimed.

V24 added0.914865seconds charged computation/plotting. Current requests200/200 follow-up (300 including initial stage),cumulative runtime2250.588368/3600seconds,remaining1349.411632seconds;active_since null. Historical6908 recorded-label accesses and1134 physical trials remain counted. Download caps4GiB/5GiB unchanged;USD0. No active workers or queued campaign. Preserve completed-output guards and all ledgers.

The maximum average-case oracle gain versus classical is0.00499637 with6/15 calls, substantially more than versus first-display selection. The first-display bound improves on always-escalate's0.00019175 by only0.00004519. The oracle ceiling is a property of these saved cases and treatment, not a universal limit on LLMs or a policy recommendation.

## Prior work and limits

V3 corrected classical smoke completed three systems × five seeds at20/10 budgets. V6 implemented all requested policy comparisons with grouped development/held-out data; no useful router advantage. V22 completed60 real1.5B calls and90 controls;V23 found0/15 prefixes consistently better than first-display across three tested presentations. All historic results, failures, source caveats and costs preserved. SNAP2 code was not located in the bounded primary-source search; adaptations are labeled.

Only three exposed families; seeds/presentations are not independent systems. Untested: sufficient independent held-out routing,practical utility/cost thresholds,robustness beyond tested presentations,successful live deployment,fresh-machine reproduction and peak memory. No claim of novelty,significance,non-inferiority or model-size causality. Exact allocation distributions are not confidence intervals or p-values.

**Single next action:** review the control-adjusted V22–V24 evidence with Tim and agree whether it warrants a new application-grounded study. [Priorities](reports/next_experiment_v24.md). New inference would require its own bounded allowance; no paid/cloud spend,contact,push or publication occurred.
