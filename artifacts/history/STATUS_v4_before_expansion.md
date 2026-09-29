# Status — 2026-09-24, v4 design frozen and projection diagnostic complete

## Current result

The user's “do it” follow-up has been carried out as **a larger-study design/registry freeze plus implementation and actual execution of the projection-only control**. The larger 20-system study itself is **not admitted or executed**: the audited catalogue supplies only four untouched schema-compatible named systems, and 203 planned calls exceed the 34 remaining. No caps were increased.

Read [reports/pilot_report_v4.md](reports/pilot_report_v4.md), [reports/registry_audit_v4.md](reports/registry_audit_v4.md), then the frozen [reports/protocol_v4.md](reports/protocol_v4.md). The prior real-LLM pilot remains in [reports/pilot_report_v3.md](reports/pilot_report_v3.md). Full earlier status is preserved at artifacts/history/STATUS_v3_before_registry.md; the earlier schema mistake remains documented in reports/schema_erratum.md.

## What actually ran this session

- Retrieved **47 configuration/system CSV tables** and source documentation from pinned MOOT commit 90803be51b00f881305db45aa0cf6a3b5340804f. SHA-256 and Git blob IDs checked. Inspected feature cells and objective headers only; no new-system objective values parsed or analyzed. Download guard remains enforced. The first sandbox DNS attempt failed; authorized public-owner retrieval succeeded, with both logs retained.
- Pinned PromiseTune owner's catalogue at f614bc482e8cdd7b266ffefbf9989748f8a06e7e. Inspected identity metadata; did not execute its code or accept its row-level workload/version claims as verified facts.
- Built data/registry_v4.json: 14 source-named candidate system groups, three already exposed. **Four untouched schema-compatible groups:** BDB-C (2,560 rows), HSQLDB (864), LLVM (1,024), DeepArch (4,096). The other 32 tables have unresolved system identities and are quarantined. Additional named tables fail binary/size criteria. No 20-group split was issued. Objective direction/provenance admission checks remain pending even for the four candidates.
- Detected identical feature matrices across several SS/rs/wc names and between SS-N and systems/x264. These are overlap warnings, not proof of independent identities; no objective correlations were inspected.
- Froze **46 code/input files** before running the new control. Implemented isolated uniform-coordinate sampling + the exact v3 projection rule. It is explicitly model-free and never substituted for real LLM responses.
- **15/15 projection-control continuations completed** from the saved corrected v3 ten-label prefixes. Each acquired ten further labels, B=20 inclusive: **150 new label accesses, zero new model calls/tokens**. Measured branch runtime about 0.5651 seconds. Checkpoints/raw proposals and all outcomes retained.
- **30 tests passed**; independent projection verification passed. Checks include hidden-objective invariance, RNG isolation, system/alias split rejection, resource refusal, prefix equality, independent projection replay, recorded outcomes, metric and budget validation. Figure visually inspected.

## Diagnostic finding

Mean loss (lower is better), five seeds per already exposed system:

| System | Random | Centroid | Real LLM v3 | Uniform projection control |
|---|---:|---:|---:|---:|
| Apache | 0.01333 | 0.00000 | 0.03000 | 0.01667 |
| SQLite | 0.17420 | 0.18451 | 0.16484 | 0.19672 |
| x264 | 0.03054 | 0.06175 | 0.05881 | 0.02201 |

The LLM materially beats the projection control in 2/15 pairs and loses in 4/15 at the frozen ±0.02 margin. Projection's mean x264 advantage is dominated by seed 37. This is exploratory evidence for keeping the control, not a general superiority claim. Uniform proposals: 110/150 projected, three duplicates and four collisions; LLM v3: 141/150, 61 and 110 respectively. No router was refitted after this diagnostic.

Prior v3 remains unchanged: 30 classical arms, 15 real LLM continuations, 33 requests including three synthetic gates; LLM materially helped versus centroid in 2/15 and hurt in 3/15. Its learned benefit router selected no x264 escalations, with no demonstrated routing advantage. Earlier v1/v2 affected SQLite results remain superseded and preserved.

## Larger-study design and exact blockers

- Target: 20 untouched software-system groups, twelve development/eight test, five fixed seeds, one table per system. Outcome-blind SHA-256 ordering, variants/seeds grouped, old Apache/SQLite/x264 excluded.
- Same binary v3 treatment, B=20/t=10; random, centroid, real LLM and uniform-projection arms. Development-only fitting/thresholds; all fixed policies, matched-rate random diagnostics, non-deployable hindsight, group-level intervals and explicit failure denominators specified.
- **Data gate blocked:** four schema-compatible untouched named systems versus 20 required; original identity/alias and objective provenance remain unresolved elsewhere. Twenty is a planning target, not a power calculation. Do not relabel 20 anonymous tables or repeated seeds as independent systems.
- **Resource gate blocked:** 203 new model calls and 6,000 new labels planned; only 34 calls and about 642.7 seconds remain. Proposed additional-stage cap of 203 calls/60 minutes is explicitly **not authorized or applied**. Preserve historical ledgers; no implicit reset.
- **Implementation scope:** projection control and admission preflight are executable. The full larger-study collector is not yet implemented, and final selected system assignments are empty. A future collector/final manifest must be frozen after admitted data and explicit resource authorization. Current protocol is a frozen study design, not a fabricated completed preregistration of unavailable data.

## Evidence and commands

| Evidence | Location |
|---|---|
| Current report | reports/pilot_report_v4.md |
| Frozen design/config/integrity | reports/protocol_v4.md, protocol_v4.freeze.json; configs/study_v4.json |
| Registry, all schemas/dispositions | data/registry_v4.json; reports/registry_audit_v4.md |
| Source hashes, lineage and audit logs | artifacts/registry_v4/sources.json, lineage.json, build.log, fetch.log, fetch_network.log |
| Executable gate / expected refusal | scripts/preflight_v4.py; artifacts/registry_v4/preflight.json, preflight.log |
| Actual projection records | results/v4_projection_diagnostic/runs.jsonl, manifest.json, completed.json, checkpoints/ |
| Tables and PNG/PDF figure | results/v4_projection_diagnostic/analysis/ |
| Tests, run and verification logs | artifacts/registry_v4/tests_precollection.txt, projection_run.log, verification.log, projection_verification.json |
| Previous paired/classical raw evidence | results/v3/; historical results/classical/, results/paired/, results/v2/ unchanged |
| Full prior status / source audit | artifacts/history/STATUS_v3_before_registry.md; reports/source_audit.md |

Reproduce without new inference or label acquisition:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/build_registry_v4.py
.venv/bin/python scripts/preflight_v4.py  # expected exit 2: recorded admission blockers
.venv/bin/python scripts/verify_projection_v4.py
.venv/bin/python scripts/analyze_projection_v4.py
.venv/bin/python scripts/report_v4.py
```

Analysis adds measured runtime to the existing ledger; refresh report afterward. Registry rebuilding is deterministic and does not parse objective payloads. Source retrieval: scripts/fetch_registry_sources.py, guarded and pinned; tables in data/registry_raw/ are Git ignored. Collection entry point `PYTHONPATH=src .venv/bin/python -m escalation.projection_diagnostic` refuses overwrite. Do not delete outputs/reset ledgers to bypass this guard.

## Remaining limits and environment

- Actual historical collection: **1,658 charged label accesses**, including this stage's 150. Reused historical inference remains charged. Table access is not live Apache/SQLite/x264 benchmarking.
- Requests: **66/100 follow-up attempts**, 34 remaining; **166 historical attempts** including v1. No model call occurred this session. Whole-history token usage remains unknown for prior failed/interrupted requests.
- Runtime: **1,157.2992/1,800 seconds**, about **642.7008 seconds remain** as of report generation. Authoritative artifacts/resource_ledger_v2.json includes all v1–v4 experiment/analysis time; active_since null. Source audit/download/setup/tests/report overhead is separate, not complete researcher time.
- Downloads: **1,338,425,157 accounted bytes**, including 999,602,607 model bytes; within original 5 GiB total / 4 GiB model caps. This session fetched about 51.85 MB of additional public source payload. Read artifacts/download_ledger.json for authoritative accounting.
- External spending **USD 0**; electricity/hardware/Codex usage unknown. Python 3.10.13 and original locked dependencies unchanged. Local M3 Pro/18 GB, pinned Qwen 0.5B unchanged; no new install/model/service.
- No background experiment or worker, no paid API/cloud, no credentials, publication, remote push, contact or email. Local Git files remain uncommitted; no remote.

## Single most important next action

**Extend the outcome-blind benchmark registry with verified original-system lineage and enough compatible independent systems.** If that requires finite numeric/categorical inputs, freeze a new representation/projection treatment and test it before outcomes. Do not spend scarce calls adding seeds to four systems or tuning on x264. Only after data admission should a full collector and explicit larger resource allowance be finalized. Nothing is scheduled to continue outside this session.
