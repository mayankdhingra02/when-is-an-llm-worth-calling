# Status — V27 metric sensitivity completed

## Resume here

**New concrete result:** LLM versus static shortlist changes sign across quality metrics on the same saved outcomes. Normalized-loss gain is +0.00001850685; equal-family mean relative recorded-target reduction is **−0.3394419%**. Original classical comparison remains +2.2406761%; adaptive shortlist comparison +0.8704683%. This is an exploratory sensitivity analysis, not a new held-out evaluation or a change to the primary metric.

Read [report](reports/metric_sensitivity_v27.md), [frozen protocol](reports/protocol_v27_metric_sensitivity.md) and relevant code. No need to reread the original literature report. All 15 exposed development prefixes, three families, five seeds and three unique V22 presentations retained. Each of three fixed classical comparators yields 45 paired observations:135 comparisons. Saved acquired labels only; no oracle/provider calls. Exact repeated prompts excluded from efficacy but retained in historical cost.

## What actually ran

- New analyzer: scripts/analyze_metric_sensitivity_v27.py; math: src/escalation/metric_sensitivity_v27.py.
- 133 input references frozen before calculation, after earlier outcome exposure.
- 190 tests passed in1.33seconds; log artifacts/study_v27/tests.log.
- Separate Decimal verification:135 paired ratios,9 family means,3 overall means,9 family-exclusion means,48 margin counts. scripts/verify_metric_sensitivity_v27.py.
- Read-only replay passed; figure visually inspected; historical audit passed all1670 frozen references.
- Actual new computation/plotting:0.462316792 seconds. No new model requests, objectives, physical trials, downloads or spending.

Commands actually executed:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/analyze_metric_sensitivity_v27.py
.venv/bin/python scripts/analyze_metric_sensitivity_v27.py --verify-only
.venv/bin/python scripts/verify_metric_sensitivity_v27.py
.venv/bin/python scripts/audit_goal_completion.py
```

Analysis refuses existing output; verifier commands are read-only. No failed or omitted comparisons. A few initial filename lookups used nonexistent names; no experiment command failed or retried.

## Artifacts

- results/v27_metric_sensitivity/summary.json:every case,family,margin and family-exclusion diagnostic.
- results/v27_metric_sensitivity/comparisons.csv:135 raw paired target/metric comparisons.
- results/v27_metric_sensitivity/relative_gain.png and.svg:reproducible figure.
- artifacts/study_v27/:actual logs,tests,Decimal verification,accounting,historical integrity.
- Prior mutable docs/ledger:artifacts/history/v27_before_analysis/.
- V26 ZIP remains unchanged:output/llm_escalation_v25_reproduction.zip. SHA256747d21658e3ef143f7e1388e2a3677153143a2676a2cfa2ad2e7481dd4e11e1e. It reconstructs V25 and does not include V27. V26's standalone command still runs after extraction:python3 -I -S scripts/verify_reproduction_v26.py.

## Interpretation and remaining limits

Relative reductions describe recorded target values, not end-to-end runtime savings or money. Changing denominators changes aggregate weighting; individual comparison signs agree. Against static rank,only1/15 prefixes improves across all three presentations by more than1%,and0/15 by more than5%. All tested thresholds are descriptive defaults,not application-approved quality gates. Choosing the metric,family or controller after seeing results cannot establish generalization.

Unproven:successful benefit-aware held-out routing,practical cost/benefit utility,unseen-system effects,unobserved formatting risk,new-host/fresh-inference reproduction. No new model or prompt tuning. The exact SNAP2 artifact was not located; implementations remain adaptations. Earlier negative and mixed results are preserved.

Ledger:2253.075028421/3600 experimental seconds;1346.924971579 remaining;active_since:null. Calls200/200 follow-up (300 total including initial stage);7058 recorded-label accesses and1134 separate physical trials unchanged. No new inference allowance inferred. No workers or queued campaign;no email,publication,push or external spending.

**Single next action:** agree on a prospective application-specific benefit/cost metric with Tim before new held-out collection,using this metric sign reversal and the static shortlist control as evidence. Do not replace the original normalized-loss outcome retroactively.
