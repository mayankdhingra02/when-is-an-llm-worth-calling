# Status — 2026-09-24, nine-call mechanism probe ready; request permission pending

## Resume here

Read **reports/order_probe_v19.md** and **reports/protocol_v19_order.md**. Independent implementation/preparation is complete; **no V19 model inference has run**. The actual runner and preflight both stopped before model loading because the128-request cap is exhausted. Do not start another audit or grid merely to avoid this concrete resource blocker.

## Next action: explicit bounded allowance

Request permission for **nine additional local attempts, cumulative cap128→137**, with **1800seconds andUSD0 unchanged**. configs/authorization_v19.json is still granted=false/request_cap128. If the user explicitly approves this precise request, record approval text/time, set granted=true/request_cap137, retain additional_requests9/runtime1800/spend0, and execute:

```sh
.venv/bin/python scripts/run_order_v19.py
.venv/bin/python scripts/analyze_order_v19.py
```

Then inspect all response/token provenance and report every condition/failure, update costs/STATUS. Do not infer cap increases from generic continuation. Never reset the ledger. Started probes refuse automatic rerun; stop after nine attempts regardless of outcomes. The analyzer and new worker remain untested end-to-end with real responses.

## Prepared design

Three V8 development families, first fixed seed11 (MySQL, lrzip, Brotli); each has original/fresh baseline, reversed display with IDs retained, and reversed ID assignment with feature order retained. Latin-rotated execution order, unchanged archived acquired prefix/candidate feature set, existing Qwen2.5-0.5B-Instruct pinned revision, CPUfloat32, greedy/four threads, unchanged distinct-ID grammar. Tests whether selection follows IDs/display position; no hidden candidate targets or objective acquisitions. Not an optimization quality/router/generalization experiment.

Nine requests maximum,20 output tokens each,eight-second request timeout,no retries.40-second model/work polling stage plus bounded cleanup, existing1800-second global limit,45-second reserve required at preflight. Model files checked by provider before launch. All paid/cloud endpoints remain disabled. No new model/download/install.

## What actually ran and evidence

- Nine transformed prompts prepared from hash-checked archived V8 messages and pools. Real pinned tokenizer validation passed;1402/1615/1771 input tokens per family/condition,20-token grammar,ten choices with20→11 allowed IDs. No model logits were computed.
- **134 tests passed** (artifacts/study_v19/tests.log), including transformation semantics, permission rejection, malformed-response rejection and deadline-before-reservation. Compilation checks passed.
- Both --preflight and actual unapproved run returned expected status2 with no model loading or measured output directory; logs artifacts/study_v19/preflight.log and denied_run_check.log. This is the project request limit, not an automatic approval-review rejection.
-25-file scientific freeze: reports/protocol_v19_order.freeze.json. Exact prompts/mappings: data/order_probe_v19.json. Authorization deliberately outside freeze and remains denied.
- Prepared runner/provider/analyzer: scripts/run_order_v19.py, src/escalation/provider_v19.py, scripts/analyze_order_v19.py. Synthetic tests remain under tests/synthetic, excluded from measured results.
- Reports/review docs before updates: artifacts/history/v19_before_order_probe/.

```sh
.venv/bin/python scripts/prepare_order_v19.py
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/run_order_v19.py --preflight
.venv/bin/python scripts/run_order_v19.py
```

These commands actually ran; the last two were correctly blocked. Preparation refuses overwrite. The real inference and analyzer commands await permission, not missing code.

## Current resources

Requests128/128 unchanged,228 historical attempts including initial stage. Runtime **1746.9059/1800seconds**, **53.0941seconds left**, active_since null. This preparation charged2.7051seconds;0 model requests,0 optimizer acquisitions,0 physical trials,0 downloads,USD0 external spend. Cumulative1134 physical trials +5408 recorded-vector objective accesses, separate cost types. Downloads1415316681bytes,999602607 model bytes. No running worker, scheduled task, external contact, publishing/push or system change.

## Prior conclusions and remaining limits

No demonstrated useful LLM selection or benefit-router advantage. V6 three held-out families: selected benefit/uncertainty rates0; matched-rate policies degenerate there. V8 all15 actual outputs selected IDs0–9; grammar did not force this, but causal ID/display effects remain untested. V9 uniform subset reference matches/beats each observed score with probability≥0.5 (conditional diagnostic, not p-values).

V17 physical846/846 exact roundtrips and30 classical arms completed. V18 all30 V16/V17 cases show the expanded grid's initial-reference opportunity is only2.929%/0.987%/0% in recorded medians. Full-table bounds are retrospective, not router features. All prior evidence/freezes retained; complete audit/report at reports/checkpoint_opportunity_v18.md.

Still untested: V19 real responses, stronger models, application-grounded utility, realistic workloads, precise measurement uncertainty, enough independent untouched families, live deployment benefit. Original bounded pilot is complete; this finite mechanism follow-up requires the explicit nine-call allowance. No work continues automatically outside this session.
