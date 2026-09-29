# Reproducing and auditing this pilot

Start with `reports/concrete_result.md`. The current workspace includes the pinned environment, downloaded inputs, frozen scientific code, and all raw measured outputs. Python3.10.13 and exact package versions in `requirements.lock.txt` were used. Model identity/revision and every local model file hash are in `artifacts/model_manifest.json`; dataset URLs/commits/schema hashes are in the versioned data manifests.

## Verify the supplied evidence without inference

From the project directory:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/verify_pilot_completion.py
```

Both commands actually ran successfully. The first executes synthetic correctness tests only; it does not manufacture measured results. The second verifies downloaded source/model hashes, deterministic acquired-label states, actual generated tokens, budgets, paired prefixes, group split, features, sealed controller and seven policy results. Fresh verification logs go to `artifacts/completion_audit/`; historical evidence is preserved. It makes no model requests and leaves the live resource ledger unchanged. The current frozen numerical analysis additionally includes exhaustive distribution checks saved in `results/v9_analysis/summary.json`.

## Regenerate the latest figure

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
