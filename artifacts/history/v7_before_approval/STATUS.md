# Status — 2026-09-24, v7 implemented; controls executed; LLM allowance pending

## Current state

Continued beyond v6 by implementing the next development-only prefix-copy exclusion experiment. **54 tests pass, 15 real-tokenizer checks pass, and all 15 matched no-model controls actually ran.** The 15-case real LLM arm is ready but has not run because it needs 15 calls and only two remain under the current cap.

An explicit approval question has been sent to the user: **raise the shared follow-up request cap 100 → 113**, allowing exactly 15 new requests from the current count of 98. This adds 13 permitted attempts to the two remaining. The **1,800-second cumulative runtime cap, USD 0 external spending, model and download limits stay unchanged**. There has been no reply/approval in the session so far. Do not interpret generic continuation or elapsed time as permission to raise the cap. `configs/authorization_v7.json` remains `granted:false`, cap 100.

Start with reports/pilot_report_v7.md, reports/protocol_v7.md and relevant v7 code. The latest completed real-LLM evidence remains reports/pilot_report_v6.md. Prior STATUS is preserved at artifacts/history/STATUS_v6_before_v7.md. No need to reread the initial research synthesis.

## Implemented and tested

- `grammar_v7.py`: feature-only dynamic decoding constraints exclude exactly the original ten prefix configurations. Remaining decisions still use real model logits; no objective values enter the constraint. Trailing constants and densely forbidden spaces are handled without a dead end. Repeated novel proposals within a batch remain allowed.
- Exact uniform sampling from the Cartesian-domain complement supplies a matched model-free control. It is not presented as LLM output.
- `provider_v7.py`: real local adapter with pinned original Qwen weights/revision and fixed CPU/float32 to match v6. The prompt payload must equal the corresponding original v6 prompt exactly; only decoding-time exclusion changes.
- `study_v7.py`: development-only collector, 15 intended cases, shared saved prefixes, inclusive 20-label budgets, durable acquisition journals, no retries, fallbacks/blocked cases retained, immutable earlier evidence. Full-arm preflight requires enough authorized requests before model loading. Interrupted started transactions fail closed for journal audit.
- `analyze_v7.py` and independent `scripts/verify_v7.py`: development-only comparison, replay, budget, source-label, grammar/token/provenance checks. No controller fit or new held-out claims.
- Frozen 97 code/test/protocol/input files before new labels in reports/protocol_v7.freeze.json. Existing v4/v5/v6 scientific freezes remain intact. Authorization is a separate record; no override is silently assumed.

## Actually executed

- Five fixed seeds [11,23,37,53,71] on MySQL, lrzip and Brotli development families.
- **15 uniform-prefix-excluded continuations**, each reusing its exact ten-label v6 prefix and acquiring ten new labels. **150 new charged objective accesses**. Zero v7 model requests.
- **54 synthetic tests passed in 0.96 s**. Tests are excluded from measured results.
- **15 real-tokenizer synthetic traversals**, zero inference. All excluded prefix strings avoided; prompts match their original v6 payloads.
- All 15 control states independently replayed and matched source labels, budgets, prefixes and projection choices. No held-out family entered the v7 collector or outcome analysis.
- Invoked the LLM entry point; it exited **2 as expected**, before model loading/request reservation: 15 pending calls exceed two available. Full intended branch denominator remains 15 controls + 15 blocked LLM continuations, not a selected subset.
- Generated controls-only report, machine tables and figure; visually inspected the figure. No new-model quality result exists yet.

Control mean losses (lower better): Brotli 0.000255, lrzip 0.001444, MySQL 0.046647. These are descriptive model-free outcomes, not evidence that prefix exclusion improves the LLM. Uniform sampling uses an exact complement distribution; sharing a seed does not mean identical draws to the original coordinate sampler.

## Evidence and actual commands

| Evidence | Location |
|---|---|
| Current report / frozen protocol | reports/pilot_report_v7.md; reports/protocol_v7.md |
| Scientific freeze / development inputs | reports/protocol_v7.freeze.json; data/manifest_v7.json |
| Approval gate | configs/authorization_v7.json |
| New raw labels and controls | results/v7/acquisitions.jsonl; results/v7/uniform_excluded/ |
| All intended branches / blocked cases | results/v7/progress.json |
| Tests / tokenizer / refusal / verification | artifacts/study_v7/ |
| Controls-only comparison and figure | results/v7/summary.json; outcomes.csv; comparison.png, .svg |
| Source snapshot and baseline ledger | results/v7/source_snapshot/; manifest.json |

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/prepare_v7.py
PYTHONPATH=src .venv/bin/python -m escalation.study_v7 controls
PYTHONPATH=src .venv/bin/python -m escalation.study_v7 llm
# Above returned 2 with no requests, as required by the current allowance.
PYTHONPATH=src .venv/bin/python -m escalation.analyze_v7
.venv/bin/python scripts/verify_v7.py
.venv/bin/python scripts/report_v7.py
```

The scientific freeze refuses overwrite. Completed controls are reused without reacquisition. No model worker or background job remains.

## Remaining limits and interpretation

Shared ledger: **98/100 attempts**, two remaining. Cumulative experiment runtime **1,473.0097/1,800 seconds**, **326.9903 seconds remaining**, inactive. New v7 collection/analysis so far cost about 1.902 seconds. Historical objective acquisitions: **3,608** (3,458 before v7 + 150). Historical attempts including v1: **198**. Downloads unchanged, USD 0 spending, no packages/weights downloaded, no cloud/credentials/remote publish/contact.

The full v7 ablation would add 150 more objective acquisitions and 15 real calls. Its execution is capped by actual remaining runtime even if request allowance is granted; completion is not guaranteed. No runtime increase is requested.

V6 remains negative: LLM helped materially in 2/15 held-out cases and harmed in 3/15, both controllers chose zero calls, and 279/300 proposals copied original prefix configurations. V7 was chosen after that observation and is explicitly exploratory. Zero prefix copies under the new constraint is enforced, not proof of useful model insight. No generalization, empirical nonbinary-domain performance or improved routing is established.

## Single next action / exact resume

**Obtain an explicit answer to the pending cap-113 approval, then run the prepared LLM arm if approved.** If approved, update only configs/authorization_v7.json with `granted:true`, `request_cap:113`, and the exact user authorization; do not change older frozen configs or reset counts. Then:

```sh
PYTHONPATH=src .venv/bin/python -u -m escalation.study_v7 llm
PYTHONPATH=src .venv/bin/python -m escalation.analyze_v7
.venv/bin/python scripts/verify_v7.py
.venv/bin/python scripts/report_v7.py
```

After actual collection, update this status and report. If permission is declined or absent, leave inference blocked. Nothing is scheduled outside the active session.
