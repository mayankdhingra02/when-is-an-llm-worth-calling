# Status — 2026-09-24 America/New_York: V23 concrete result completed

## Resume here

[Current report](reports/robustness_v23.md): **0/15 saved prefixes beat the first-displayed-ten control under all three tested presentations.** Four beat it at least once; none exceed the earlier0.02 normalized-loss margin against that control. Removing MySQL turns the average gain against all three cheap selection references negative. This is a completed post-hoc analysis of actual V22 measurements, not new inference or an independent confirmation.

V22's positive aggregate remains unchanged: +0.00426143 versus classical, +0.00019175 versus first-display selection. V23 shows that this small average does not establish a consistently useful LLM advantage. [V22 report](reports/larger_model_v22.md) and every raw run are preserved.

## What ran

All15 development prefixes (MySQL/lrzip/Brotli × five fixed seeds),45 unique presentations, four baseline comparisons. Calculated per-case min/mean/max paired gain, strict positive/sign-changing/material-gain counts, family summaries and leave-one-family-out means. Exact repeats excluded from efficacy but historical costs retained. No controller fitted or held-out family used.

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/analyze_robustness_v23.py
.venv/bin/python scripts/analyze_robustness_v23.py --verify-only
```

**164 tests passed in2.57seconds.** Actual-data checks passed:180 independent Decimal min/mean/max calculations,300 independently recomputed case predicates and unchanged four V22 aggregate means. Read-only replay passed. Figure visually inspected. V23 adds an eight-file freeze before new computation, explicitly after V22 exposure. Original scientific code/results unchanged.

## Evidence and reproducibility

- [V23 result](reports/robustness_v23.md), [full summary](results/v23_robustness/summary.json), [all case envelopes](results/v23_robustness/case_envelopes.csv), [figure](results/v23_robustness/gain_envelopes.png).
- Plan and fixed analysis inputs/code: reports/protocol_v23_robustness.md and .freeze.json.
- Executed analysis, tests, independent verification and accounting: artifacts/study_v23/.
- Source real-model outputs: results/v22_larger/requests.jsonl, request_starts.jsonl, arms/, acquisitions.jsonl, summary.json and outcomes.csv.
- Pre-V23 docs and exact ledger: artifacts/history/v23_before_analysis/. The prior STATUS preserves the full V22 resume information.

scripts/audit_goal_completion.py now resolves only five explicitly archived V22 mutable files when checking the older evidence snapshot; all scientific bytes still require exact original hashes. No ledger reset or evidence overwrite occurred. The older PDF/ZIP remain V21 snapshots and exclude V22/V23.

## Concrete numerical result

Against classical: gain in every presentation3/15, any6/15; material gain in every1/15,any2/15. Against first displayed: every0/15,any4/15;material every0/15,any0/15. Ties count as no strict gain, not as harm. Mean of per-case minimum gains versus first displayed is-0.00014152; original average+0.00019175; mean maximum+0.00071677. These are envelopes over three observed presentations, not guarantees or confidence intervals. Their endpoints require hindsight presentation selection and are not deployable policies.

With MySQL omitted, average gain is+0.00018400 versus classical,-0.00006553 versus first displayed,-0.00011211 versus uniform expectation,-0.00010193 versus lowest IDs. Preserve all families; this is concentration analysis, not an exclusion rule.

## Costs and limits

V23 added0.684720seconds of charged analysis/plotting. New model calls,objective acquisitions,physical trials,downloads and external spending:all0. Historical totals unchanged:200/200 follow-up calls (300 including initial stage),6908 recorded-label accesses and1134 separate physical trials. Cumulative experiment runtime2249.673503/3600seconds;remaining1350.326497seconds;active_since null. Original download caps remain4GiB model/5GiB total. No further model calls authorized. No active experiment or scheduled work.

No V23 execution/test/verification failure. No new source/model retrieval. The previous stage includes retained initial schema errors and provider warnings; do not remove historical failures or mix superseded runs. No paid/cloud inference,push,publication or external contact.

## Scope and next action

The original classical smoke and all requested policies were implemented/executed; V6 group-held-out routing showed no useful learned-router advantage. V22 collected60 real larger-model calls and90 controls. V23 supplies the next concrete result about presentation-dependent quality. Scientific honesty takes precedence over obtaining a positive result.

Untested: robust improvement across arbitrary presentations,application-grounded utility/cost thresholds,independent held-out generalization,successful deployment routing,fresh-host reproduction and peak memory. Three exposed families and repeated seeds/presentations are not many independent systems.

**Single next action:** review the V22/V23 control-adjusted evidence with Tim and agree whether it justifies a prospectively specified held-out study with a practical benefit/cost threshold. [Prioritized plan](reports/next_experiment_v23.md). No new campaign is queued. Do not select a favorable presentation after seeing its outcomes and call it a policy.
