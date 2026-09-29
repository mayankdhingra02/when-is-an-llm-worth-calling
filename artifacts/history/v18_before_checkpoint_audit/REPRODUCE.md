# Reproducing and auditing this pilot

Start with `reports/decision_brief.md`. The current workspace includes the pinned environment, downloaded inputs, frozen scientific code, and all raw measured outputs. Python3.10.13 and exact package versions in `requirements.lock.txt` were used. Model identity/revision and every local model file hash are in `artifacts/model_manifest.json`; dataset URLs/commits/schema hashes are in the versioned data manifests.

## Verify the supplied evidence without inference

From the project directory:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/verify_pilot_completion.py
```

Both commands actually ran successfully. The historical unified audit covers the original scope through V9; it does not independently replay V10–V12. The first executes synthetic correctness tests only; it does not manufacture measured results. The second verifies downloaded source/model hashes, deterministic acquired-label states, actual generated tokens, budgets, paired prefixes, group split, features, sealed controller and seven policy results. Fresh verification logs go to `artifacts/completion_audit/`; historical evidence is preserved. It makes no model requests and leaves the live resource ledger unchanged. The current frozen numerical analysis additionally includes exhaustive distribution checks saved in `results/v9_analysis/summary.json`.

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
