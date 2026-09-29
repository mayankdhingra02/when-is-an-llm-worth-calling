# Reproducing and auditing this pilot

**Standalone V26 reconstruction is now tested:** extract `output/llm_escalation_v25_reproduction.zip`, then run `python3 -I -S scripts/verify_reproduction_v26.py` from that extracted root. This independently reconstructs the V25 numerical result from included source tables and raw model traces without project imports,third-party packages or inference. Actual Python3.10.13 and3.12.14 isolated runs passed. [Instructions](BUNDLE_V26_README.md), [actual evidence](reports/reproduction_v26.md). This is same-host saved-result reconstruction, not fresh model generation or a full new-machine experiment. Older fresh-host limitations below remain.

**Current V25 addition:** `.venv/bin/python scripts/analyze_shortlist_v25.py --verify-only` independently replays all15 restricted-classical branches,150 sequential choices/source labels,and45 saved LLM metrics without new acquisitions or ledger writes. [Report](reports/shortlist_v25.md).177 tests pass;current runtime2252.612712/3600seconds,calls200/200;7058 recorded-label accesses plus1134 physical trials. Prior instructions and exact ledger are preserved under artifacts/history/v25_before_execution/. Older accounting below is historical.

**Current V24 addition:** `.venv/bin/python scripts/analyze_opportunity_v24.py --verify-only` independently re-enumerates all262144 allocations and compares the saved summary, without inference, objective acquisition or ledger writes. [Report](reports/opportunity_v24.md).171 tests pass;current cumulative runtime2250.588368/3600seconds,calls200/200. Older stage accounting below is historical. Pre-V24 instructions are preserved under artifacts/history/v24_before_analysis/.

**Current V23 addition:** run `.venv/bin/python scripts/analyze_robustness_v23.py --verify-only` for a read-only replay of the observed-presentation gain analysis. [Report](reports/robustness_v23.md), [post-hoc frozen plan](reports/protocol_v23_robustness.md). 164 tests pass. Current runtime is2249.673503/3600seconds; calls remain200/200. V22 counts below describe its preserved historical snapshot. Full prior instructions are archived under artifacts/history/v23_before_analysis/.

Start with [the current evidence guide](reports/review_evidence.md) and [discussion note](reports/review_note.md). The current workspace includes the pinned environment, downloaded inputs, frozen scientific code, and all raw measured outputs. Python3.10.13 and exact package versions in `requirements.lock.txt` were used. Model identity/revision and every local model file hash are in `artifacts/model_manifest.json`; dataset URLs/commits/schema hashes are in the versioned data manifests.

## Verify the supplied evidence without inference

From the project directory:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/verify_report_larger_v22.py --verify-only
```

The current V22 audit reconstructs token decoding, cache identity, all 150 paired arms, source-label journals, scalar losses and aggregates. It requires the local Qwen1.5B tokenizer and retained source tables but performs no inference, new acquisitions or ledger writes. The authoritative model manifest is `artifacts/model_manifest_v22.json`; current evidence is `reports/larger_model_v22.md` and `artifacts/study_v22/`. `scripts/verify_review_current.py` targets the historical 140-call snapshot, and earlier verifiers also have obsolete live-ledger assumptions. Preserve their successful historical receipts; do not reset the ledger to satisfy them.

V22 completed 60/60 model calls and 90 controls. The approved allowance is exhausted at 200/200 follow-up calls; runtime is 2,248.9888/3,600 seconds. A fresh inference campaign needs a separate prospective protocol, output namespace and bounded allowance. The old PDF/archive remain V21 snapshots. Full fresh-host reproduction and an independent repeat experiment are untested.

The sections below retain the chronology of actual preparation, execution and analysis. Pending-state statements under earlier headings are historical snapshots, superseded by the later completed sections. Do not rerun collection commands at the exhausted cap or reset ledgers. Independent fresh-host reproduction remains untested.

## Regenerate the V9 exact-reference figure

```sh
.venv/bin/python scripts/render_selection_null_v9.py
```

This presentation-only command reads saved V9 numerical results and records its runtime in the persistent experiment ledger. It does not change data, policies, model responses or results. Output is `results/v9_analysis/exact_reference.png` and `.svg`.

## Numerical method and reruns

`scripts/analyze_selection_null_v9.py` contains the executable exact-reference analysis. For each of15 saved cases it computes a uniform ten-of-twenty terminal-loss distribution and independently enumerates all184756 subsets to verify it. Tests independently check hand-sized cases, ties and incumbent clipping. The completed-output guard refuses to overwrite the existing numerical evidence. To perform a new numerical reproduction, create a separately named output/version and charge its computation in the existing resource ledger; do not delete historical evidence merely to make a command run.

Historical V3–V8 source snapshots and their freeze maps retain the precise executed code. Old V6/V7 verifiers contain stage-specific request-count assertions, so the unified audit supplies their preserved historical ledger snapshots only to those assertions, checks their raw data, and independently checks the current cumulative ledger. It does not roll back live counts. Standalone old version verifiers should not be interpreted as current cumulative-budget checks.

## Environment or input restoration

A new project-local environment can be installed with Python3.10 and:

```sh
python3.10 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
```

This is a reconstruction instruction, not a claim that a second clean environment was tested. No container/OS image is pinned. Numerical generation can differ across devices/library builds; V6–V8 explicitly used CPU/float32 and greedy decoding. The earlier V3 MPS run is a separate treatment.

Raw third-party tables, model weights and source archives are Git-ignored. Preserve them when transferring this local research workspace for a fully offline audit. Their owner URLs and hashes support restoration; downloads remain subject to the existing caps and licensing notes in THIRD_PARTY.md. `scripts/fetch_sources.py` handles the original pinned MOOT/EZR inputs; `scripts/fetch_model.py` handles pinned Qwen files; V5 owner data uses pinned entries in `artifacts/registry_v5/sources.json` and `metadata.json` with `scripts/fetch_registry_v5_data.py`. That script requires the saved pinned repository inventories referenced by metadata. Do not resolve a fresh HEAD and call it the same experiment. Some source web/API archival bytes may change formatting even at a stable content revision; a mismatch must be reported rather than silently updating a frozen hash.

## Fresh real inference is a new experiment

Existing collectors reuse complete outputs, refuse interrupted transactions without audit, and enforce inclusive20-label arm budgets. The approved follow-up allowance is exhausted at128/128 attempts. A new local-model reproduction needs an explicitly bounded allowance and separate result namespace; it must retain prior counts. Do not reset ledgers or delete outputs. Paid APIs/cloud remain disabled. No clean-machine repeated model experiment, reordered-prompt experiment or stronger-model replication is claimed.

## Latest V10–V12 scope and review checks

```sh
.venv/bin/python scripts/verify_review_packet.py
```

This read-only check hashes every versioned scientific freeze, verifies headline arithmetic from saved V6/V9/V12 results, checks V12 acquisition counts and current accounting, and validates the local links in the review documents. It writes only `artifacts/review_packet/verification.json`; it makes no requests, acquires no labels and does not modify the ledger. It is a review consistency check, not a replacement for numerical replay.

V10–V12 already executed these analyses/replays; their logs remain under `artifacts/study_v10/`, `artifacts/study_v11/` and `artifacts/study_v12/`:

```sh
.venv/bin/python scripts/verify_headroom_v10.py
.venv/bin/python scripts/verify_quality_v11.py
.venv/bin/python scripts/analyze_verify_quality_controls_v12.py
```

The V12 command independently recomputes the deterministic acquired-only choices and source values, verifies all 20 branches and 300 joint-vector accesses, and regenerates its summary. Repeating analysis may rewrite derived reports and charges runtime to the existing ledger; do not confuse it with a no-write historical audit. For preservation, inspect the already executed replay log first. The latest saved suite result is 95 passing tests. V12 collection used `scripts/run_quality_controls_v12.py`; rerunning it is unnecessary for review and completed outputs must not be deleted to force fresh collection.

Mutable documents before this consolidation are preserved in `artifacts/history/v12_before_review_cleanup/`. Historical stage indexes describe those earlier snapshots; the final review document index is `artifacts/review_packet/evidence.json`. Scientific freezes and raw results are unchanged.

## Prospective metadata admission (V13.1)

```sh
.venv/bin/python scripts/audit_admission_v13_1.py
PYTHONPATH=src .venv/bin/python -m pytest -q
```

Executed successfully: all 81 registry tables audited without opening objective CSVs, 102 tests passed. The metadata audit leaves the resource ledger unchanged and regenerates only its separate JSON/CSV/check artifacts. The first V13 pass omitted the historical `heldout_smoke` spelling; V13.1 corrects it, preserving the original files. Use V13.1 for current exposure/admission decisions. See reports/admission_v13.md; no new optimization/model result is implied.

## External metadata coverage (V14)

```sh
.venv/bin/python scripts/audit_external_admission_v14.py
PYTHONPATH=src .venv/bin/python -m pytest -q
```

Executed successfully: 540 published metadata rows, 90 contexts, zero contexts with20 distinct settings;108 tests passed. The audit requires the pinned source files listed in artifacts/study_v14/source_inventory.json and source_files.json. It makes no model calls, does not analyze runtime/size values and leaves the experiment ledger unchanged. Owner-file fetch scripts use retained commit inventories and the persistent download ledger. To restore elsewhere, carry the saved inventories/head records; do not resolve fresh HEAD and claim the same version. Later edge-file inspection is separately recorded in source_edge_files.json. No upstream script or benchmark is executed.

## Live measurements and paired controls (V15–V16)

The executed workload, local binary/extension/library hashes, source provenance, random order and raw compressed artifacts are recorded under artifacts/study_v15/, artifacts/sources/live_v15/ and results/v15_measurements/. This is an actual local measurement campaign;116 tests now pass after the paired-control stage. Physical timing is not deterministic across reruns/machines. No complete OS image or second clean-machine reconstruction is claimed.

```sh
.venv/bin/python scripts/render_live_v15.py
PYTHONPATH=src .venv/bin/python -m pytest -q
```

The renderer reads saved numerical evidence, uses project-local caches, and charges computation to the existing ledger. It does not generate new measurements. `scripts/collect_live_v15.py` has been invoked again to verify completed-output reuse with zero extra physical trials. Do not delete output guards: new collection requires its own namespace/accounting and prospective protocol.

V16 collection and independent replay already ran:

```sh
.venv/bin/python scripts/run_classical_v16.py
.venv/bin/python scripts/analyze_verify_classical_v16.py
```

They preserve completed/start markers rather than silently rerun or overwrite. Inspect saved logs in artifacts/study_v16/ for a no-write review. The replay checks every source vector, seeded prefix, acquired-only decision and inclusive20-label budget. For a separate numerical reproduction, retain frozen input/source bytes and use a new output namespace while accounting runtime; do not reset the resource ledger. New compressed-source-file restoration uses scripts/fetch_workload_v15.py with the saved head record; its CPython tag/commit/hashes are in the workload manifest. No corpus source is executed as code.

Include data/live_manifest_v15.json in future family-exposure audits. These three families are now development/exposed, not untouched test families.

## V17 expanded development grid

Read reports/protocol_v17_expansion.md first. Executed with the same project Python/environment/workload as V15; no installation or downloads. The frozen22-file map precedes846 physical measurements and all optimizer outcomes. The generated median CSV is bound by artifacts/study_v17/recorded_table_binding.json before optimizer reads.

Commands actually executed (project root):

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/collect_live_v17.py
.venv/bin/python scripts/analyze_live_v17.py
.venv/bin/python scripts/run_classical_v17.py
.venv/bin/python scripts/analyze_verify_classical_v17.py
.venv/bin/python scripts/render_expansion_v17.py
.venv/bin/python scripts/verify_expansion_v17.py
```

Precollection tests:120 passed. Collector complete reuse makes no trials; interrupted stages refuse automatic retry. Analysis/optimizer scripts refuse overwriting completed stages. Do not delete these guards/results or reset the cumulative ledger to rerun. On a separately authorized clean reproduction, retained source/data/model/license files and pinned native binary identities are required; installed hardware/OS timing is not portable. Raw payloads and the archive are Git ignored and must be retained separately with the manifest. No fresh-machine reproduction was performed.

The figure-only renderer regenerates results/v17_classical/comparison.png/.svg from saved outcomes, charging its runtime; it makes no model or physical calls. verify_expansion_v17.py is an explicitly post-collection audit, checks saved medians/payloads/freezes/counts and records its runtime. It refreshes current accounting if intentionally rerun. Exact choice replay is saved in artifacts/study_v17/verification.json. The emitted snapshot physical_analysis_ledger_ledger.json is a harmless naming duplication, kept unchanged to match frozen code.

See artifacts/study_v17/evidence.json for hashes of new raw evidence, source references and current review documents. Earlier scientific freezes remain authoritative for their stages; mutable review documents have historical copies. Synthetic fixtures remain under tests/synthetic and are never included in research aggregates.

## V18 retrospective checkpoint audit

The fixed71-file protocol/input map was created after V16/V17 results were known and before computing this decomposition. It is explicitly post-hoc, development only. No acquisition or inference. All30 cases retained.

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/audit_checkpoint_v18.py
.venv/bin/python scripts/audit_checkpoint_v18.py --verify-only
```

All commands actually ran;127 tests passed. The initial analysis writes cases.csv, summary.json, decomposition.png/.svg and refuses overwrite. --verify-only reloads frozen tables/prefixes/arms and compares the exact recomputed summary without plotting. Both modes charge runtime under the unchanged ledger and require five seconds remaining. Do not reset the ledger. V17 analysis/raw evidence remains unchanged; artifacts/history/v18_before_checkpoint_audit/ contains earlier mutable review docs. See artifacts/study_v18/evidence.json for the new audit index.

## V19 prepared mechanism probe (no inference yet)

Preparation and tests actually executed:

```sh
.venv/bin/python scripts/prepare_order_v19.py
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/run_order_v19.py --preflight
.venv/bin/python scripts/run_order_v19.py
```

134 tests passed. Both runner commands returned expected blocked status2 before model loading, because configs/authorization_v19.json remains denied at the exhausted128-call cap. No measured V19 directory exists. Tokenizer-only preparation produced nine frozen prompts/mappings; do not call them model outputs.

After explicit approval of nine extra attempts (cap137, runtime1800/USD0 unchanged), update only the separate authorization record with approval provenance and execute run_order_v19.py followed by analyze_order_v19.py. These paths are implemented but untested end-to-end with real V19 responses. Preserve all nine intended conditions including failures/unattempted cases. No retries or automatic restart; no hidden objective acquisition. Older stage verifiers that assume historical request counts must use their recorded stage snapshots, never reset the live ledger to satisfy them.

See reports/protocol_v19_order.md/.freeze.json, data/order_probe_v19.json and artifacts/study_v19/evidence.json. Prior mutable docs preserved under artifacts/history/v19_before_order_probe/.

## V19 actual execution and controlled result

The direct response “continue” to the specific nine-call approval question authorized cap128→137 only. configs/authorization_v19.json and results/v19_order_probe/started.json record that scope before request129. Runtime1800seconds andUSD0 remained unchanged. The former pending-state documentation/authorization/index is preserved under artifacts/history/v19_before_execution/.

Commands actually succeeded:

```sh
.venv/bin/python scripts/run_order_v19.py
.venv/bin/python scripts/analyze_order_v19.py
.venv/bin/python scripts/render_verify_order_v19.py
PYTHONPATH=src .venv/bin/python -m pytest -q
```

9/9 calls completed;134 post-execution tests passed. All tokens, usage, prompt transformations and request provenance were verified. The standalone PNG/SVG and response_table.csv derive from actual outputs. render_verify_order_v19.py is a post-collection presentation/independent transformation audit, separately indexed; it does not alter the frozen inference protocol. Generation warnings about sample-only settings under greedy decoding were retained in inference.log.

The nine-call stop rule has been reached. Collection and analysis guards preserve completed artifacts. Do not rerun inference or reset ledgers; historical verifiers tied to older caps need recorded stage snapshots. Reproduction on another host/model/session is untested. See artifacts/study_v19/executed_evidence.json for current results/review documents and artifacts/study_v19/executed_accounting.json for actual costs. The earlier preparation index remains a historical snapshot.

## V20 executed rule audit / V21 prepared separating extension

Actual completed commands: scripts/audit_rules_v20.py and --verify-only replay (all24 actual saved responses ×four rules); scripts/prepare_nonmonotone_v21.py (three prompts, tokenizer only).140 tests passed after all changes. The V20 rules/predictions are not model outputs; the synthetic counterexample remains separate from measured aggregates. V21's actual runner was invoked and correctly returned blocked status2 before model loading.

V20 source/formulas are frozen post-hoc in reports/protocol_v20_rules.freeze.json. V21's exact messages and inference/analyzer code are frozen prospectively in protocol_v21_nonmonotone.freeze.json. Authorization remains separately denied at137 calls. After explicit approval of three more calls only, set the authorization record to cap140 and run .venv/bin/python scripts/run_nonmonotone_v21.py followed by scripts/analyze_nonmonotone_v21.py. Keep1800seconds/USD0 unchanged. No current V21 inference result exists; do not substitute expected rule outputs. Analysis/provider behavior on actual interleaved prompts remains untested until then. Historical review docs are preserved under artifacts/history/v20_before_rule_audit/.

## V21 completed actual execution

The direct response “Continue” to the specific three-call request authorized cap137→140 only; the authorization record and started.json precede requests138–140. Runtime1800seconds andUSD0 remained unchanged. Pending-state docs/permission/index are preserved at artifacts/history/v21_before_execution/.

Executed successfully:

```sh
.venv/bin/python scripts/run_nonmonotone_v21.py
.venv/bin/python scripts/analyze_nonmonotone_v21.py
.venv/bin/python scripts/render_verify_nonmonotone_v21.py
PYTHONPATH=src .venv/bin/python -m pytest -q
```

All3/3 real requests completed and140 tests passed. MySQL selected the first ten displayed IDs; lrzip/Brotli returned IDs0–9, selecting alternating positions. The completed summary, exact response CSV and PNG/SVG derive from real responses. Frozen inference/analyzer sources are unchanged; render_verify_nonmonotone_v21.py is an explicitly post-collection mapping audit/presentation script. Do not delete completed guards or reset ledgers; new model reproduction requires a separate bounded allowance. No fresh-host or repeated-condition reproduction was performed.

See artifacts/study_v21/executed_accounting.json and executed_evidence.json. Original model/protocol warnings, pending-state evidence and earlier successful/failing runs remain retained. Existing historical stage verifiers must use their recorded stage ledgers rather than resetting the live ledger to older request counts.
