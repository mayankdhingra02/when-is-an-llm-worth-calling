# V80: does a real local LLM improve over a cheap preset?

The approved batch completed **105 real local SmolLM3 requests and 450 new physical trials** on three fixed corpus inputs and five seeds. All trials passed validation; 0 invalid model responses and 0 fallback search slots were recorded. This is one exposed Kanzi development family, not a held-out learned-router evaluation.

Across the 15 repeated-search cases, LLM versus RF yielded **4 wins / 6 ties / 5 losses**; versus the cheap preset it yielded **0 wins / 10 ties / 5 losses**. These counts are descriptive; workloads and seeds are not independent software systems.

## Confirmed quality

Lower compressed byte count is better. Each case uses three charged confirmations. The means below average five seed medians within each workload; savings compares the ratio of those means. Positive savings favors the LLM. There is no pooled raw-byte statistic across workloads.

| Input | RF mean bytes | Preset mean bytes | LLM mean bytes | LLM saved vs RF | LLM saved vs preset |
|---|---:|---:|---:|---:|---:|
| dickens | 2,429,511.8 | 2,377,944.0 | 2,418,843.0 | +0.439% | -1.720% |
| sao | 4,704,659.6 | 4,681,324.0 | 4,749,925.6 | -0.962% | -1.465% |
| xml | 390,815.4 | 388,529.0 | 403,041.4 | -3.128% | -3.735% |

All cases, including losses:

| Input | Seed | RF bytes | Preset bytes | LLM bytes |
|---|---:|---:|---:|---:|
| dickens | 11 | 2,377,944 | 2,377,944 | 2,377,944 |
| dickens | 23 | 2,377,944 | 2,377,944 | 2,377,944 |
| dickens | 37 | 2,582,439 | 2,377,944 | 2,582,439 |
| dickens | 53 | 2,377,944 | 2,377,944 | 2,377,944 |
| dickens | 71 | 2,431,288 | 2,377,944 | 2,377,944 |
| sao | 11 | 4,681,324 | 4,681,324 | 4,681,324 |
| sao | 23 | 4,634,852 | 4,681,324 | 4,879,548 |
| sao | 37 | 4,779,056 | 4,681,324 | 4,826,108 |
| sao | 53 | 4,726,201 | 4,681,324 | 4,681,324 |
| sao | 71 | 4,701,865 | 4,681,324 | 4,681,324 |
| xml | 11 | 389,477 | 388,529 | 388,529 |
| xml | 23 | 388,529 | 388,529 | 388,529 |
| xml | 37 | 413,785 | 388,529 | 427,807 |
| xml | 53 | 388,529 | 388,529 | 421,813 |
| xml | 71 | 373,757 | 388,529 | 388,529 |

Prospective 1% descriptive margin (benefit / within margin / harm):

| Input | Comparator | LLM wins/ties/losses | 1% flags | Extra mean decision seconds |
|---|---|---|---|---:|
| dickens | rf_lcb | 1/4/0 | 1/4/0 | 9.660 |
| dickens | preset | 0/4/1 | 0/4/1 | 9.871 |
| sao | rf_lcb | 2/1/2 | 0/4/1 | 9.698 |
| sao | preset | 0/3/2 | 0/3/2 | 9.906 |
| xml | rf_lcb | 1/1/3 | 0/2/3 | 9.577 |
| xml | preset | 0/3/2 | 0/3/2 | 9.780 |

The 1% flag is a practical descriptive convention, not a significance test, risk bound, or dollar-valued utility. Mean paired percentages are also preserved in JSON and can differ from ratios of means. No threshold was fitted to these outcomes.

![Paired quality and selector time](../results/v80_kanzi_analysis/paired_results.png)

## Protocol, baseline and provenance

User's “Continue” answered the immediately preceding explicit 105-call/450-trial/30-minute/$0/no-download approval question. Receipt: `artifacts/study_v80_execution/user_approval.json`. Original freeze SHA256 `9369379ed6b74d19b5eb031875314ee27303d57027f7783fe525437e688d6814` is unchanged. Initial sandbox process-inspection denial occurred before collection; the exact command then ran with local execution permission. There was no experiment restart.

All three inputs and all five seeds were fixed, including unfavorable classical cases. Each saved V79 ten-label prefix was cloned into fresh RF, preset and LLM arms, each with seven search acquisitions and three charged incumbent confirmations. Thus 900 logical charges include 150 historical prefix trials shared across arms; 450 new physical trials comprise 315 search and 135 confirmation trials. No hidden terminal outcomes or unacquired labels entered decisions. Arm state was isolated and round order randomized as frozen. The model remained resident for every new arm; V79 model-free control timings were not substituted.

The preset is a V78-informed development choice: owner level-7 transform/entropy pair, descending block sizes, with acquired duplicates skipped and RF only after exhaustion of its fixed list. It is not a newly learned gate or a universal preset claim. The LLM prompt uses only fixed input category/size, configuration definitions and acquired observations; corpus filename is omitted. Public-corpus/model pretraining contamination nevertheless remains unknowable.

Same real model and runtime as V78: SmolLM3-3B-Q4_K_M, revision `4965cb60b150737b68a0408c36aeefb65078f894`, GGUF SHA256 `8334b850b7bd46238c16b0c550df2138f0889bf433809008cc17a8b05761863e`; llama.cpp b11146 offline/loopback, temperature 0, requested seed, 64 output-token cap. Cross-device determinism is not established. Kanzi uses the isolated V76 buffer-reference repair, an explicitly labeled adaptation, not an unmodified owner release. Input owner URLs, MD5 and SHA256 are preserved in the V79 manifest; no raw corpus redistribution rights are asserted.

## Actual collection versus hypothetical deployment cost

Actual wall time: **784.76 seconds**, within the 1,800-second cap; 900 native JVM processes. Generation requests: 105; all HTTP requests including health/template/tokenization: 319; retries: 0. Observed input tokens: 61,181 (0 requests unknown); output tokens: 970 (0 requests unknown). Startup: 0.771 seconds; sampled peak model-server RSS: 2,450,046,976 bytes.

Total continuation decision time across all 15 cases: rf_lcb 3.146 seconds, preset 0.031 seconds, llm 147.817 seconds. Native trial-supervision time is recorded separately. Zero new downloads or external spending; hardware and electricity costs are unknown.

`deployment_estimates.json` accounts for a hypothetical single chosen branch: recorded historical prefix process time plus the selected model-resident continuation and selection time. Model cold startup is separate. Prefix verification/I/O/selection and future router overhead are excluded. These estimates are not new production measurements, monetary valuations, or the actual amount collected: the experiment paid for all three continuations. Confirmed incumbent compression/decompression times are saved in `cases.csv`, separately from size and selector overhead.

## What this does and does not establish

Against rf_lcb, 1/15 cases exceeded the prespecified 1% LLM benefit flag. Against preset, 0/15 cases exceeded the prespecified 1% LLM benefit flag. **There is zero observed compressed-size routing headroom beyond the preset in this finite batch.** A hindsight preset/LLM selector gives exactly the preset result in every case, while actual LLM continuation adds decision cost. The four wins against RF therefore do not establish useful escalation beyond this stronger comparator. All requests were valid and no fallback occurred, so malformed responses do not explain this result.

A useful controller would have to identify such cases using only pre-decision information on independent systems; their existence alone does not establish predictability. If no material benefit remains against a strong cheap comparator, learning a gate cannot manufacture it.

Post-hoc observed-choice diagnostic: 69/105 valid proposals were in the preset transform/entropy family, and 10/15 LLM incumbents were candidate439 (the same 2MiB preset setting). This is an observed pattern, not proof of model reasoning, causal mechanism or unseen counterfactual outcomes. No additional calls were made for the diagnostic.

The JSON includes a hindsight better-of-control-and-LLM reference, explicitly nondeployable. No controller was fitted here. V72's same-model RocksDB comparison remains a separate negative result with a different objective; milliseconds and compression bytes are not pooled. Older router results and cross-platform bundles retain their historical scopes. Neither more seeds nor three Kanzi files creates independent software families. A broadly beneficial escalation result and Q2 readiness remain unestablished.

## Validation and reproducibility

All new trials passed stream checksum, independent header/settings checks and exact decompression at collection. All intended trials are retained in the denominator. Successful bulky outputs were removed only after validation under the frozen retention rule; hashes, raw headers, commands, logs and receipts remain. Offline replay validates those receipts rather than recreating deleted payloads.

The frozen analyzer replays acquired-only classical choices, legal model proposals, shared prefixes, chosen incumbents, round ordering, budgets and saved usage. The supplementary verifier independently checks exact native commands, request order, complete fallback tails, payload parameters and cost/resource counters. Both must pass before this report is generated. The pre-collection frozen suite had 594 passing tests. Synthetic tests are excluded from all measured aggregates.

Raw evidence: `results/v80_kanzi_paired/`. Verified tables/figures/JSON: `results/v80_kanzi_analysis/`. Approval/cost/audit records: `artifacts/study_v80_execution/`. Commands executed: frozen `scripts/run_kanzi_v80.py` with its approval digest, then `scripts/analyze_kanzi_v80.py`, `scripts/verify_kanzi_v80_addendum.py`, `scripts/report_kanzi_v80.py` and `scripts/write_kanzi_v80_report.py`, using `.venv/bin/python`.

A separate local portable bundle supports standard-library reconstruction of saved outcomes without model/runtime binaries or corpus payloads. Its execution and corruption-check receipts, if completed, are under `artifacts/reproduction_v80/`; the bundle is not fresh inference, full RF decision replay, native remeasurement or a clean-machine runtime replication. No publication or push is performed.

Remaining limitations: one exposed patched software family, three historical corpus files, one model and host, a fixed twenty-label budget, small repeated-seed sample, no held-out learned-router study or fresh cross-machine collection. Research conclusions follow all observed cases, not a search for a favorable subset.
