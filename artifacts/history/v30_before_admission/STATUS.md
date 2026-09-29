# Status — 2026-09-25: V29 fixed nearest-neighbor controls completed

## Resume here

**New concrete result:** sequential3NN beats the fixed single-call LLM on both metrics on the exposed development sample:normalized gain+0.0005355608,relative target reduction+0.8721339%,6 wins/8 ties/1 loss. It also improves on three-call voting and all listed cheap comparators on average. This is an exploratory positive result for a cheap baseline,not achieved benefit-aware routing or generalized LLM inferiority.

Read [report](reports/neighbors_v29.md), [frozen protocol](reports/protocol_v29_neighbors.md) and relevant code. Do not reread the full literature report. k=3 and nominal mismatch distance are fixed from the earlier V12 control;no parameter search. Both modes use the same20-row LLM shortlist and ten-label prefix. Batch selects ten rows from original prefix predictions;sequential recomputes after each new acquisition. Ranking sees only acquired labels and feature values.

## Actual execution

- 30 new arms:15 cases × batch/sequential3NN.300 additional charged recorded-label accesses;each arm inclusive20-evaluation budget and identical10-prefix.
- All30 completed;no failures,retries,omitted cases or model calls.
- 176 input references frozen before acquisition,after prior outcome exposure.
- 205 tests passed in1.22seconds. Test log:artifacts/study_v29/tests.log.
- Independent acquired-only replay checked300 decisions,neighbor IDs,predictions,source journal labels and30 final states.
- Separate Decimal verification checked360 paired metric values,24 aggregate comparisons,72 win/tie/loss counts,30 feedback-pair metrics.
- Read-only replay passed;figure visually inspected;all1999 frozen historical/current references passed integrity audit.

Executed commands:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/run_neighbors_v29.py
.venv/bin/python scripts/analyze_neighbors_v29.py
.venv/bin/python scripts/analyze_neighbors_v29.py --verify-only
.venv/bin/python scripts/verify_neighbors_v29.py
.venv/bin/python scripts/audit_goal_completion.py
```

Collection and analysis refuse completed outputs;verification is read-only. No job remains live or scheduled.

## Evidence

- results/v29_neighbors/:raw arms,prediction traces,checkpoints,acquisitions.jsonl,progress.json,summary.json,cases.csv,comparison.png/svg.
- artifacts/study_v29/:actual collection/analysis logs,tests,Decimal/source verification,cost receipts,historical audit.
- src/escalation/neighbors_v29.py:fixed acquired-only predictor.
- reports/neighbors_v29.md:full result,all comparator summaries,limits,costs and next action.
- Prior docs/ledger:artifacts/history/v29_before_execution/.
- V26 standalone ZIP unchanged;reconstructs V25,not V27–V29.

## Findings and limitations

Mean normalized loss:batch3NN0.0105921231;sequential3NN0.0093010538;fixed single LLM0.0098366147;voting0.0096586743. Sequential versus batch:3 wins,12 ties,0 losses;relative mean improvement0.7783335%. Batch alone loses to fixed single LLM under normalized loss,so sequential feedback matters and this is not a pure intelligence comparison.

One sequential3NN harm versus single LLM:MySQL/53,1.1940% higher target. Retained in all results. The exposed families and repeated adaptive analyses prevent an unbiased generalization claim. Model-free controls are labeled classical;real LLM comparisons retain V22 provenance. Relative percentages are recorded target changes,not deployment speedups. Fresh inference,new-host reproduction,unseen-system effects,practical utility and successful learned routing remain untested. No new hypothesis test or equivalence claim.

## Accounting and next action

Actual added collection/analysis runtime2.120370417seconds. New labels300;historical recorded accesses7508. Physical trials1134 unchanged. Model requests200/200 follow-up (300 including initial stage);no new allowance inferred. Ledger2258.334693048/3600seconds;1341.665306952 remaining;active_since:null. No downloads,external spend,cloud,push,publication or contact.

**Single next action:** freeze this stronger cheap comparator into a prospectively specified paired study on untouched software families,with an application quality/cost metric and separate bounded inference allowance. Do not tune3NN further on these already exposed outcomes.
