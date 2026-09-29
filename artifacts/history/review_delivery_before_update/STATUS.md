# Status — 2026-09-24, current evidence audit and review handoff completed

## Resume here

Start with [the current evidence guide](reports/review_evidence.md) and [discussion note](reports/review_note.md). The bounded research pilot and approved V21 extension are complete. No useful LLM optimization or benefit-router advantage is established. The model allowance is exhausted; no new experiment is queued.

## Latest continuation: reproducibility repair, no new experiment

Added `scripts/verify_review_current.py` and seven synthetic corruption/mapping tests. Fixed README/REPRODUCE instructions that still pointed at the historical128-call verifier and stale116-test/runtime counts. Prior review documents are preserved byte-for-byte in `artifacts/history/review_handoff_before_update/`; scientific freezes and measured outputs remain unchanged.

Actually ran the full suite: **147 passed in1.34seconds**, captured in `artifacts/review_handoff/tests.json`. The new standard-library audit passed: **19 scientific freezes /1171 references**, all79 V21 executed-index entries (explicit archived document relocations), V6 policy CSV, and all12 actual V19/V21 request/output mappings, usage totals, denominators and approval timing. Receipt: `artifacts/review_handoff/verification.json`. Current review/source hashes: `artifacts/review_handoff/manifest.json`.

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/verify_review_current.py
```

Optional `--output` saves a new receipt and refuses overwrite. This verifies saved-evidence consistency; it does not rerun model generation, tokenizer decoding, objective evaluation, controller fitting or physical measurement. No failures occurred in these checks. Review-audit runtime is separately recorded; experiment ledger unchanged. New model calls/objective acquisitions/downloads/spend: all0. This continuation adds no positive research finding.

The earlier user reply “Continue” directly authorized the fixed V21 three-call extension only (cap137→140,1800seconds,USD0). All3/3 real calls completed in the preceding execution, summarized below.

## Latest actual result

Interleaved IDs0,J,1,I,…,9,A, same original feature/display order and acquired observations:

- MySQL returned0,J,1,I,2,H,3,G,4,F: first ten displayed,10/10 configurations overlapping V19 original.
- lrzip and Brotli returned0–9: display positions1,3,5,…,19,each5/10 configurations overlapping V19 original.

Thus display-prefix prediction matches1/3, endpoint-sequence and lowest-ID predictions match2/3. Each simple rule fails at least one case. Endpoint-sequence and lowest-ID explanations still coincide for the two matching responses. V19's observed first-display-ten result on nine monotone-ID conditions is preserved, but a universal first-ten explanation is falsified by two new responses. This is not a discovered internal algorithm, selection-quality result or useful benefit router.

No fresh original-condition repeats were budgeted in V21, so V19 configuration comparisons are across sessions. Cases remain exposed development data, one response per case, no significance/generalization claim. No new candidate objective was acquired/scored.

## What ran / evidence

All3/3 requests138–140 succeeded,0 retries/failures/timeouts/fallbacks/unattempted cases. Existing pinned Qwen2.5-0.5B-Instruct revision7ae557604adf67be50417f59c2c2f167def9a775,CPUfloat32,greedy,four threads,unchanged V19 provider/V8 grammar. Actual model hashes,prompts,token IDs/grammar traces,counts and mappings verified. Separate independent feature-preserving relabel/approval/request-ID checks pass. **140 tests passed after execution**, figure visually inspected.

```sh
.venv/bin/python scripts/run_nonmonotone_v21.py
.venv/bin/python scripts/analyze_nonmonotone_v21.py
.venv/bin/python scripts/render_verify_nonmonotone_v21.py
PYTHONPATH=src .venv/bin/python -m pytest -q
```

All commands succeeded. Preserve completed guards/results; no automatic rerun or ledger reset. Sample-only configuration warnings with greedy generation remain in logs; they are not failed responses.

- Actual prompts,raw outputs,tokens/usage: results/v21_nonmonotone/requests.jsonl, request_starts.jsonl.
- All cases/selected configuration IDs: outcomes/,progress.json,response_table.csv,summary.json in results/v21_nonmonotone/.
- Actual plot: results/v21_nonmonotone/interleaved_selection.png/.svg.
-27-file pre-inference scientific freeze: reports/protocol_v21_nonmonotone.freeze.json; prepared inputs data/nonmonotone_probe_v21.json. The frozen protocol's pending wording is historical.
- Approval before inference: configs/authorization_v21.json, results/v21_nonmonotone/started.json.
- Logs/tests/independent checks/costs: artifacts/study_v21/inference.log,analysis.log,render_verification.log,post_execution_tests.log,execution_verification.json,executed_accounting.json.
- Historical pending review/permission/index: artifacts/history/v21_before_execution/.

## Current costs and bounds

New3 requests:4788 input/60 output tokens,missing usage0;request wall6.4575s. Startup4.0899s includes0.6839s model load; whole inference session11.6498s. This turn incl.analysis/render14.3014s; V21 incl.preparation17.0909s. No new objective/physical acquisitions/downloads/spending.

**140/140 follow-up calls exhausted**,240 historical including initial stage. Cumulative runtime **1790.6854/1800seconds**, **9.3146seconds left**,active_since null. Totals5408 recorded objective acquisitions +1134 physical trials, distinct cost types. Downloads1415316681bytes/model999602607bytes unchanged;USD0 external spend. No active workers/scheduled tasks, install, paid/cloud inference, credentials, remote contact/push/publication or system change.

## Earlier results and overall interpretation

V6 three held-out families: benefit/uncertainty policies select0 escalation; no demonstrated useful router. V8 all15 responses IDs0–9. V9 random-subset reference matches/beats every original model score with probability≥0.5 (conditional diagnostic,not p-values). V19 all9 fresh monotone-ID responses first displayed ten; reverse display changedall10 configurations, ID reversal heldall10. V20 showed display-prefix and endpoint-sequence rules both fitall24 previous outputs. V21 now separates them and finds mixed behavior. Preserve all versions rather than rewriting earlier measurements.

V17/V18 actual compression/classical work showed little recorded headroom even from the reference; no useful optimizer/LLM benefit established. These are small adaptations, not SNAP2 numerical replication or broad generalization. All prior sources/failures/freezes retained.

## Single next action / untested

**Review the full V19–V21 evidence with Tim before proposing a larger, prospectively specified study.** reports/review_note.md is ready for that discussion; nothing was sent. Stop rules are satisfied. Remaining calls are zero and remaining runtime is insufficient for the prepared model-stage reserve. Generic continuation is not further resource approval; no new experiment is queued.

Untested: more arbitrary permutations/repetitions, stronger models/prompts, untouched systems, unique internal mechanism, selection-quality consequences, application utility and live routing benefit. No further automated work continues outside this session.
