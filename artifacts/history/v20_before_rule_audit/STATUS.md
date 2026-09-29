# Status — 2026-09-24, nine real model calls complete; display-order result verified

## Resume here

Read **reports/order_probe_v19.md** and **reports/review_note.md**. The user replied “continue” directly to the explicit nine-call approval request; that was recorded as approval for cap128→137 only. The fixed V19 probe has now completed and its stop rule is reached. No further calls, model/grids or limits were authorized.

## Actual new result

**All9 actual local-model responses selected exactly the first ten displayed candidates, in display order.** On each of MySQL/lrzip/Brotli seed11:

- Reversing display order, keeping IDs bound to configurations, changed all10 selected configurations (overlap0/10).
- Reassigning IDs, keeping feature/display order, retained all10 selected configurations (overlap10/10).
- Fresh original responses matched the archived V8 originals (3/3).

This is controlled evidence of display-position sensitivity for the evaluated model/prompt on three development cases. It is not generalization, an exclusive internal explanation, measured optimization benefit, or a useful benefit router. A first-ten rule exactly reproduces these9 selections. No candidate objective outcomes were newly acquired/scored.

## What ran and evidence

All9/9 requests completed,IDs129–137;0 failures/timeouts/retries/fallbacks/unattempted cases. Existing pinned Qwen2.5-0.5B-Instruct revision7ae557604adf67be50417f59c2c2f167def9a775,CPUfloat32,greedy,four threads. V8 grammar unchanged with20→11 allowable IDs across ten choices. Provider model hashes, frozen prompts, token traces, rendered hashes and usage verified.134 tests passed after execution; figure visually checked.

```sh
.venv/bin/python scripts/run_order_v19.py
.venv/bin/python scripts/analyze_order_v19.py
.venv/bin/python scripts/render_verify_order_v19.py
PYTHONPATH=src .venv/bin/python -m pytest -q
```

These commands succeeded. Old denied preflights and134 pre-execution tests remain preserved. Harmless warnings about inactive sample-only generation settings are in inference.log; no failed requests were suppressed. Completed-run guards prevent reruns. No ledger reset is authorized.

- Actual full requests/raw outputs/usage: results/v19_order_probe/requests.jsonl and request_starts.jsonl.
- Selections/full denominator: results/v19_order_probe/outcomes/, progress.json, response_table.csv, summary.json.
- Reproducible figure: results/v19_order_probe/selection_order.png/.svg.
- Source25-file freeze: reports/protocol_v19_order.freeze.json; prepared prompts data/order_probe_v19.json. Frozen protocol retains its pre-authorization wording; later approval is recorded separately.
- Approval and baseline: configs/authorization_v19.json; results/v19_order_probe/started.json.
- Logs, post-run tests, independent checks and accounting: artifacts/study_v19/ (executed_accounting.json, execution_verification.json, post_execution_tests.log).
- Pending-state review docs/approval/index retained: artifacts/history/v19_before_execution/.

## Costs and limits

New calls9; usage14364 input/180 output tokens,usage missing0. Request wall18.3699s; startup4.2211s includes model load0.8716s. Overall inference session23.6912s; this turn including analysis/render26.6799s. V19 plus tokenizer preparation29.3851s.

**137/137 follow-up attempts exhausted**,237 historical including initial stage. Cumulative experiment runtime **1773.5859/1800seconds**, **26.4141seconds remaining**, active_since null. No new objective acquisitions/physical trials/downloads; totals remain5408 recorded accesses +1134 physical trials, separate types. Download ledger1415316681bytes/model999602607bytes unchanged;external spendUSD0. No active worker, scheduled followup, package install, credentials, paid/cloud inference, remote contact/push/publication or system change.

## Prior conclusions retained

No demonstrated useful LLM optimization or benefit-router advantage. V6 three held-out families: development-fitted benefit/uncertainty rates0, so matched-rate policies coincide. V8 all15 outputs first10; V9 uniform subset reference matches/beats each observed score with probability≥0.5 (conditional diagnostic,not p-values). V19 now supplies controlled display/ID interventions for3 of those development cases.

V17 completed846 physical trials and30 classical arms. V18 audited all30 V16/V17 cases: expanded grid's initial-reference improvement ceiling2.929%/0.987%/0% using recorded medians. Those are retrospective finite-table bounds, not router features or true-runtime guarantees. All prior source freezes/data/failures retained. Adaptation, not SNAP2 numerical replication.

## Single next action / remaining untested

**Review the controlled display-order finding with Tim to decide whether a small methodological report is worthwhile before more inference.** Use reports/review_note.md; nothing was sent. Stop after the nine-call probe regardless of result. A request to continue alone is not permission for another cap increase; the just-completed approval was specifically a reply to the nine-call proposal.

Untested: stronger models, other prompts/grammars, more order permutations/repeated responses, untouched-system generalization, quality consequences of these new selections, application-grounded tasks and live deployment/router benefit. The implemented bounded pilot now has a concrete selection-behavior result, not a successful escalation controller. Nothing continues automatically outside this session.
