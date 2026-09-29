# Status — 2026-09-24, checkpoint opportunity audit complete

## Resume here

Read **reports/checkpoint_opportunity_v18.md** and **reports/review_note.md**. The implemented pilot still has no demonstrated useful LLM escalation/router advantage. Latest continuation executed a post-hoc audit of30 saved development cases, not another model/grid campaign.

## New finding and actual execution

The reference itself leaves little recorded opportunity. Full-table feasible improvement over the reference:

- V17 expanded grid: **2.929% Zstandard,0.987% LZ4,0% zlib**.
- V16 small grid: **2.510% Zstandard,0.025% LZ4,0% zlib**.

Because every arm retains the feasible reference incumbent, even perfect selection cannot exceed those relative savings in the recorded problem. The prior10% diagnostic was impossible before optimization began. This is an arithmetic bound over recorded medians, not a bound on true runtime or a deployable router signal. Do not weaken a reference or change a metric merely to force a positive result.

Analyzed all30 V16/V17 saved joint3NN cases. Verified source vectors, reference-size cap, shared10-prefix, unique20-arm budgets and additive decomposition of pre-checkpoint savings, continuation savings and remaining hindsight opportunity. Second --verify-only run reproduced all results. **127 tests passed**; standalone decomposition PNG/SVG visually checked. No physical trial, new optimizer acquisition, model inference or download occurred.

All cases are already-exposed development families; two grids and repeated seeds do not increase independent-system count. Single small source archive, timing noise/CLI overhead, three repetitions and research-default utility still limit interpretation. V8 first-ten selection exactly reproduces observed choices, but its causal dependence on order was never tested by new model permutations; review wording corrected.

## Commands and evidence

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/audit_checkpoint_v18.py
.venv/bin/python scripts/audit_checkpoint_v18.py --verify-only
```

All ran successfully. First command is test infrastructure; last two charge runtime but no outcomes. Initial analysis refuses overwrite. Prior collectors/analyses retain their guards; no ledger reset authorized.

- Report: reports/checkpoint_opportunity_v18.md; discussion note: reports/review_note.md.
- All30 rows, summary and figures: results/v18_checkpoint_audit/.
- Protocol/formula/source freeze: reports/protocol_v18_checkpoint.md/.freeze.json (71 files; explicitly post-hoc).
- Tests, execution logs and accounting: artifacts/study_v18/.
- Older mutable docs preserved: artifacts/history/v18_before_checkpoint_audit/.
- Prior actual physical data: results/v15_measurements/ and results/v17_measurements/; actual compressed bytes artifacts/sources/live_v15/outputs/ and live_v17/outputs/ (Git ignored).
- Prior paired prefixes/arms/acquisitions: results/v16_classical/ and results/v17_classical/.

## Costs and limits

New: **0 physical trials,0 optimizer acquisitions,0 model requests,0.3939 charged seconds,0 downloads,USD0 external spend**.

Cumulative:1134 physical trials +5408 recorded-vector optimizer accesses, distinct cost types. Follow-up requests128/128 exhausted;228 historical attempts including initial stage. Runtime **1744.2008/1800seconds**, **55.7992seconds remaining**, active_since null. Downloads1415316681bytes;model bytes999602607. No installation, credentials, paid/cloud inference, remote contact/push/publication, system changes or ongoing workers.

## Earlier measured results unchanged

V3 corrected three-system/five-seed smoke used real local Qwen. V6 three held-out families: benefit/uncertainty select0 escalations, no router advantage. V8 all15 outputs choose IDs0–9; V9 uniform subsets match/beat each observed score with probability≥0.5 (conditional diagnostic, not p-values). V15 collected288 physical trials; V16 ran30 classical arms/450 accesses. V17 collected846 physical trials, all exact roundtrips passed, then30 classical arms/450 accesses; mean final hindsight headroom0.537%/0.197%/0%. All earlier failures, source/admission audits and freezes retained. Adaptation, not SNAP2 numerical replication.

## Single next action / untested

**Agree on an application-grounded task and utility that allow meaningful improvement over a credible reference before another campaign.** Use reports/review_note.md for discussion with Tim; nothing was sent. Current grid stop rules are satisfied, and leftover runtime does not justify repeated outcome-driven expansion.

Untested: stronger-model/candidate-order causal tests, application utility, broad workloads, precise measurement uncertainty, enough untouched families for routing generalization, live deployment costs/benefit. New inference requires an explicit bounded allowance beyond128; generic continuation is not a cap increase. The bounded pilot is ready for review. No automatic work continues after this session.
