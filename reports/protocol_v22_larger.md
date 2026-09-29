# V22: larger local model with formatting and repetition controls

**Prepared, not authorized or executed.** No V22 model output or optimization result exists. This is an adaptive development follow-up motivated by V6-V21, not a new held-out evaluation. Freeze these instructions, inputs and code before downloading weights or observing V22 outputs. The larger model is not assumed to be stronger at this task.

## Question and intended denominator

Can a larger local model select useful configurations after the same ten-label classical prefixes, beyond simple candidate-order/ID rules and an exact uniform-selection reference? Does changing presentation change the selected configurations, and are exact repeats stable?

Use all15 existing V8 development cases: MySQL, lrzip, Brotli; seeds11,23,37,53,71. No outcome-based subset selection. No held-out V6 family enters this study. Every case has the existing feature/acquired-label-only20-row shortlist and saved10-label prefix. Preserve the historical adaptive classical20-label continuation as the paired baseline.

Four real calls per case,60 intended calls:

1. **assigned_ids:** preserve V8 feature/display order; apply a deterministic pseudorandom nonmonotone permutation of the20 IDs.
2. **reverse_display:** reverse those candidate entries without changing ID-to-configuration mapping.
3. **reassigned_ids:** preserve feature/display order; independently permute the IDs.
4. **assigned_ids_repeat:** byte-identical messages to condition1, repeated in the final block.

The first three conditions follow a fixed Latin rotation over15 cases, balancing five cases of each condition per round. The repeat block is last, so repeat disagreement can include session/order drift; it does not isolate its cause. Permutations are derived from SHA-256 of version,dataset,seed,tag and Python's pinned random implementation, without objective values. Actual messages and mappings are fixed in data/larger_probe_v22.json. Rule predictions are not model responses.

## Model and provenance

Official owner: [Qwen/Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct/tree/989aa7980e4cf806f80c7fef2b1adb7bc71aa306), revision989aa7980e4cf806f80c7fef2b1adb7bc71aa306, Apache-2.0. Owner metadata and download plan are retained under artifacts/study_v22/. Model card reports1.54B parameters. Nine needed files total3,098,971,928bytes; the weight file is3,087,467,144bytes, owner SHA-256 dd924a11b4c220f385b51ffa522daea7c9f3d850e31b162bb5661df483c6d3ee. Non-LFS files must match pinned Git blob hashes; all local files receive SHA-256. No account, credentials, remote code, service terms or paid API.

Current hardware check:18GiB total RAM, approximately32GiB free disk. CPUfloat32 weights alone need approximately6.2GB; peak working memory, model-load success and throughput remain unmeasured. No MPS/device change or dependency upgrade is proposed. Existing pinned torch/transformers are reused. Owner card warns against transformers before4.37; the retained dependency lock is authoritative.

Use the unchanged V19 worker: local-files-only, CPUfloat32,four threads,greedy decoding; V8 ten-distinct-ID grammar;20 generated tokens maximum. Grammar/tokenizer incompatibility, provenance failure or load failure stops execution. LargerProvider binds logs/cache keys to the new actual model/revision; it does not inherit the old0.5B cache identity. Preserve prompts, tokens, choice traces, usage, timestamps, errors and request starts. No retries, repair prompts or fabricated fallback responses.

## Paired controls and label accounting

Before LLM collection, execute two deterministic controls for each of45 unique case/presentation combinations: first ten displayed IDs and canonical lowest ten IDs. Their configurations may coincide; retain and charge both arms. Each starts from the identical saved10-label prefix and acquires10 more outcomes via LazyOracle. This is90 control arms and900 new charged recorded-label accesses. Repeat-A reuses its identical A control outcomes with explicit attribution.

Each of60 LLM responses selects10 unevaluated rows; its own independent continuation acquires10 outcomes, up to600 further charged accesses. Maximum new recorded-label accesses:1,500; inclusive budget20 per completed arm. Prefixes and historical classical baselines are provenance-checked reused data, not newly acquired labels. The ledger and response logs retain partial/failing runs. No physical compression trial is proposed.

Only the separate retrospective analyzer reads complete targets for final normalized loss. Selection code sees feature candidates and saved acquired labels. The cached V9 exact uniform ten-of-twenty expectation is invariant to presentation and is used only as a retrospective reference; it is not a new deployed random arm or a fresh independent experiment.

## Analysis fixed before V22 outputs

Report all60 intended calls,90 intended control arms, all failed/incomplete/unattempted statuses and actual costs. For every completed model branch report loss against the same classical continuation, first-display control, lowest-ID control and uniform expectation. Positive gain means baseline loss minus LLM loss. Keep exact repeat agreement and selection-rule matches separate from quality gains.

Primary descriptive summaries exclude the repeated A condition: average the three unique presentations and five seeds within each family, then weight the three families equally. Show every family and condition, not only the aggregate. The repeat is a reliability diagnostic and its actual cost is always included. If any intended arm is incomplete, suppress aggregate efficacy summaries; retain available per-case results explicitly labeled incomplete. Do not fit a benefit router or tune thresholds here.

Continuous gains are descriptive. This pilot cannot establish significance, non-inferiority, generalization, novelty, an internal model algorithm, or improvement caused specifically by model size. Historical0.5B results used different conditions/sessions and are contextual only. Stop and report regardless of sign; do not search alternative prompts, models or permutations under this permission.

## Exact resource request and stop rules

Separate authorization file configs/authorization_v22.json is currently denied. Proposed permission:

-60 additional local attempts, follow-up cap140->200 (historical overall maximum300 including initial100).
-30 additional minutes of cumulative experimental runtime, cap1800->3600seconds. This includes control acquisition, model verification/load, inference and analysis. At launch require1000seconds remaining; the runner work stage has a900-second limit,90-second model-load poll and30-second per-request timeout, bounded by remaining stage/global time.
-One official3.099GB model download. Existing cumulative download caps remain4GiB model files and5GiB all payloads. Projected totals after successful download:4,098,574,535 model bytes and4,514,296,954 total bytes, using the current owner-metadata ledger. No other download/model is included.
-USD0 external spending, no cloud, no publication/contact, no system installation, one model worker. Downloader has a separate600-second wall deadline and charges every received byte including partial transfers. Download time is reported separately, not represented as inference time.

Stop after the first inference failure/malformed response, any data/provenance error, or resource limit. Preserve started/progress/partial journals and require explicit audit before any restart. No silent retries. Every normal timeout terminates/reaps the worker using existing bounded cleanup. A model-startup failure may occur after control-label acquisition; those900 accesses remain actual collection cost.

## Commands after explicit authorization

```sh
.venv/bin/python scripts/fetch_model_v22.py
.venv/bin/python scripts/run_larger_v22.py --preflight
.venv/bin/python scripts/run_larger_v22.py
.venv/bin/python scripts/analyze_larger_v22.py
```

Preflight is safe now and must return blocked. The downloader and runner check authorization before large downloads or model loading. Read-only source audit and the feature-only preparation ran under existing authority; preparation runtime was charged to the unchanged1800-second ledger. Tests use separate synthetic fixtures. Real larger-model execution, download and its tokenizer compatibility remain untested pending approval.
