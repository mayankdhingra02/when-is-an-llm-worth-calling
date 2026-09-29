# Status — 2026-09-24 America/New_York: V25 new classical experiment complete

## Resume here

[Current report](reports/shortlist_v25.md): **15 new adaptive-shortlist classical arms completed**, with150 new charged recorded-label accesses and no new model calls. Restricting the classical optimizer to the LLM's exact20-candidate shortlist improves its average loss over the original full-space classical baseline, but it still trails the LLM average. The prior static-shortlist rule ends only0.00001851 normalized loss behind the LLM mean; this is not equivalence or a practical cost-benefit guarantee.

All15 development prefixes were retained: MySQL/lrzip/Brotli × seeds11,23,37,53,71. Same10-label checkpoint,10 new evaluations,20 inclusive budget. The fixed shortlist is acquired-label/feature-derived; sequential updates and tie-breaking use only acquired labels and original seeded order. No hidden targets or display IDs enter selection.

## Actual result

Equal-family mean losses: original full-space classical0.01558039;static shortlist0.01133746;new adaptive shortlist0.01314247;LLM three-presentation mean0.01131896. Lower is better.

New arm versus original classical: mean gain+0.00243792;3 wins,11 ties,1 loss;one gain and one harm exceed0.02. New arm versus LLM mean: mean gain-0.00182351;8 wins,4 ties,3 losses,one material harm. It is no worse than all three tested LLM presentations in12/15 cases,strictly better than all three in0/15. Choosing the favorable method per family after these outcomes would be hindsight.

The LLM mean versus static rank:3 wins,4 ties,8 losses;one material gain,zero material harms;net mean gain+0.00001851. All per-case and per-family results remain reported,including MySQL/11 where the new arm harms performance.

## What ran and validation

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python -u scripts/run_shortlist_v25.py
.venv/bin/python scripts/analyze_shortlist_v25.py
.venv/bin/python scripts/analyze_shortlist_v25.py --verify-only
.venv/bin/python scripts/render_shortlist_v25.py
```

**177 tests passed in1.19seconds.** Independent Python modal-centroid/distance replay verified all150 sequential choices,source row/target identities,15 final states and20/10 budgets;45 saved LLM metrics recomputed. Read-only replay passed. Synthetic tests remain separate. All15 intended arms completed,no collection/evaluation failure or omission.

216 protocol/source/input references were frozen before new acquisitions,after prior development exposure. This is a separately bounded exploratory classical-only stage,not an alteration of V22 or an inference-cap increase. Selection and full-table scoring remain separate. Original plot labels were crowded; a separate presentation-only script produced a readable figure,visually inspected. Initial plot and frozen analyzer remain unchanged.

## Evidence

- [Report](reports/shortlist_v25.md), [full summary](results/v25_shortlist/summary.json), [case CSV](results/v25_shortlist/cases.csv), [readable figure](results/v25_shortlist/comparison_readable.png).
- Raw new collection: results/v25_shortlist/arms/,checkpoints/,acquisitions.jsonl,started.json,progress.json.
- Fixed protocol/code/tests/data: reports/protocol_v25_shortlist.md and .freeze.json.
- Logs,tests,replay,independent verification and three accounting receipts: artifacts/study_v25/.
- Underlying real LLM outputs remain results/v22_larger/;static controls remain results/v8/static_rank/;prefixes/full-space classical remain results/v6/.
- Previous mutable docs and exact ledger: artifacts/history/v25_before_execution/. Its STATUS preserves V24; earlier histories preserve V22/V23. PDF/ZIP remain V21 historical snapshots.

## Costs and limits

New collection charged150 label accesses even when targets had appeared in historical branches. These are recorded-table evaluations,not new live software measurements. Historical totals now7058 recorded-label accesses and1134 separate physical trials. Branch loops summed0.238948seconds;full collection0.957621seconds,analysis0.612506seconds,readable rendering0.454216seconds,total2.024344 experimental seconds. Setup/verification overhead is included in the stage total,not the branch loop sum.

Requests unchanged200/200 follow-up (300 including initial stage). Current runtime2252.612712/3600seconds,remaining1347.387288seconds;active_since null. No new inference,downloads,physical trials,spending,cloud,credentials,contact,push or publication. No workers or queued campaign. Preserve guards and ledgers. A hypothetical15-case deployment of the new classical arm uses300 logical evaluations andzero model calls; research-collection cost is separate.

## Limits and next action

Three exposed development families only. New algorithm has sequential label feedback;LLM selects one batch. This is a practical equal-budget alternative,not isolation of model intelligence or proof of generalization. Static/adaptive/LLM outcomes depend on case;near-equal aggregate values do not establish equivalence. SNAP2 remains an adaptation,not exact artifact replication. Original smoke/policy comparisons and all prior failures are preserved.

Untested: untouched-family learned routing,application-grounded utility/cost thresholds,broader model/prompt robustness,live deployment,fresh-host reproduction and peak memory.

**Single next action:** review the matched-control evidence with Tim and agree on a practical benefit/cost threshold and untouched task families before a new model/router campaign. [Priorities](reports/next_experiment_v25.md). Further inference needs a separate bounded allowance; no campaign is queued.
