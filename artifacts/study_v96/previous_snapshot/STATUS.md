# STATUS — V94 and bounded V95 finished; verified negative-result candidate

**Concrete result:** On two fresh native-engine groups, fixed non-thinking Qwen3 lost to sequential3NN by mean10.21% (SuperLU) and9.69% (HiGHS), with zero >=5% wins in ten pairs. Owner-informed native sampling on development data produced one >=5% win, but cheap batch3NN did better in that case. Bounded thinking produced no valid final answers. This strengthens a scoped negative-result paper candidate; it does NOT demonstrate the proposed benefit predictor or establish Q2 readiness. Read `reports/research_readiness_v95.md` first.

## What ran this continuation

- **V94:** two new software-engine groups, five fixed seeds each, B20/checkpoint10.100 shared-prefix +400 continuation acquisitions =500 native configuration labels.485 valid;15 charged SuperLU worker crashes. Physical journal:1,474 starts,1,459 returns;26 planned repeats never started and15 started solves did not return. All1,455 vectors from successful workers independently recertified. All250 HiGHS acquisitions valid. Native collection272.823s.
- **V94 real model:**100 requests/100 valid responses,100 generated tokens,70,620 summed full-context /7,152 reported actual prefill tokens. Lifecycle37.449s; peakRSS6,721,028,096bytes; exit0. No retries.
- **V94 router addendum:** fitted only on six older development groups and sealed after prefixes but BEFORE continuation outcomes. Both benefit and uncertainty thresholds select never-call. No >=5% benefit missed in the two new groups, but no learned advantage over never/random/uncertainty. The addendum timing and small-group limitations are explicit.
- **V95/V95b:**36 intended development conditions (18 old prefixes ×thinking/non-thinking), owner-informed sampling, native decoding and explicit thinking-control prefixes. Original preflight failed BEFORE generation and is preserved. Corrected V95b made25 requests/24 responses:12 valid non-thinking outputs;12 thinking outputs exhausted2,048 tokens; one thinking HTTP timeout at120s. Five thinking and six non-thinking conditions unattempted. Stop rule respected; no retry or replacement output.
- **V95 outcomes:**360 additional recorded-table reads charged, including explicit fallback arms for failed/unattempted conditions. One non-thinking case beat sequential3NN by5.0046%, but batch3NN beat that same reference by5.2326%; none of the valid model selections beat both controls by>=5%. Thinking-policy quality is entirely fallback quality, not model achievement. Full intended-cohort gains are−2.58% thinking+fallback and−2.75% non-thinking+fallback; do not treat these as completed-case model means.
- **V95 costs:**1,459.030s amended lifecycle +1.148s original preflight, within shared1,800s. PeakRSS7,374,618,624bytes (<8GiB), server exit0.24,816 generated tokens in returned responses; final server log independently reports another2,048 for the missing response, giving26,864 observable output tokens. Returned prefill30,490 plus server-only3,304. Raw timed-out answer remains unavailable.
- **Validation:**755 repository tests passed in21.76s. Independent V94 budgets/decisions/solution checks passed; V95 replay reproduced36 branches/360 saved cells with zero new labels/calls. Both figures visually checked. No experiment or model server remains running. External spendingUSD0; electricity/hardware cost unknown.

## Evidence and exact commands

Raw native requests, vectors, crashes and charges: `results/v94_native/`. Qwen3 fixed-policy traces: `results/v94_qwen/`. Original/amended thinking records: `results/v95_reasoning/`, `results/v95b_reasoning/`. Tables, policies, coverage, cost/noise audits and PNG/SVG: `results/v94_analysis/`, `results/v95_analysis/`.

Reports: `reports/numerical_v94.md`, `reports/router_numerical_v94.md`, `reports/reasoning_v95.md`, `reports/research_readiness_v95.md`. Frozen protocols: `reports/protocol_v94.freeze.json`, `reports/protocol_v95.freeze.json`, `reports/protocol_v95b.freeze.json`, `reports/protocol_v95_analysis.freeze.json`. Dataset/source manifests: `artifacts/study_v94/`, `artifacts/sources/v94/`. Source/hardware audit was completed before native timings; previously exposed records were checked.

Saved-evidence replay (safe; zero new inference):
```
.venv/bin/python scripts/analyze_numerical_v94.py
.venv/bin/python scripts/evaluate_router_numerical_v94.py
.venv/bin/python scripts/cost_noise_numerical_v94.py
.venv/bin/python scripts/synthesize_numerical_v94.py
.venv/bin/python scripts/verify_reasoning_v95.py
.venv/bin/python scripts/audit_transport_usage_v95.py
.venv/bin/python scripts/report_reasoning_v95.py
.venv/bin/python -m pytest tests -q
.venv/bin/python scripts/seal_reasoning_v95.py --verify-only
```
Do NOT rerun `analyze_reasoning_v95.py` into existing outputs: it is the once-only charged acquisition stage. Do not reopen exhausted inference batches implicitly. For a faithful new collection use a separate predeclared replication workspace/configuration; preserve these original outputs.

V94 seal verified3,122files and32historical checkpoints; SHA528a32723e5da822c6c307040f7e10018a94496dad587a5c8fd4ead7563e940c. V95 has its own final manifest and verification receipt in `artifacts/study_v95/`. Root snapshots preserve V93→V94→V95 history. Historical standalone seals that reference changed root docs require the newest snapshot-aware sealer.

## Cumulative limits and next action

Real-model requests **3,843**. Recorded-table acquisitions **27,018**. V94 additionally collected500 native configuration labels (SuperLU250, HiGHS250); keep physical-solve counts separate. Earlier native counts remain unchanged (DuckDB78physical, H2299, Kanzi1265, RocksDB350). Total downloads9,870,205,044bytes /10GiB; **867,213,196 remaining**. Model payload9,126,358,023 /9GiB;537,318,393remaining. V95 added zero downloads. No paid/cloud/credential use, publishing, push, author contact or paper submission.

**Single highest-priority next action: independently replicate the frozen V94 comparison on a second configured machine.** No second machine is connected here. Preserve all configurations/failures, seeds and thresholds. Native crash causality, clean-machine portability, further independent groups and longer/final-answer-reserved reasoning remain untested. The current bounded batch stopped on its declared HTTP timeout rule; all independent analysis/test/report work is finished. Do not chase a positive score or claim a journal tier from these results.
