# When Is an LLM Worth Calling?

A reproducible research repository on cost- and reliability-aware escalation from classical software-configuration optimization to real local LLMs.

**Latest: V143–V145 complete.** Added one Spark family with five fixed workloads and five seeds: **50 real model requests, 49 completed responses, 175 budgeted arms and 2,000 charged recorded outcomes**. SmolLM3-3B beat both strong classical continuations by more than 1% in **4/25 cases**; Qwen3-8B did so in **1/25**. Both models lost on average. The frozen controllers chose no calls and missed useful opportunities; all Spark cases extrapolate beyond their training range on domain cardinality.

One missing source duration and one interrupted model request are retained. The batch finished under an explicit recovery amendment without increasing its allowance. All primary model/sequential/adaptive comparisons have complete labels; one random-row comparison is inconclusive. This is a substantive mixed result, not a validated generalizable router or journal-readiness guarantee.

Read [STATUS](STATUS.md), [research assessment](reports/research_assessment_v145.md), [measured report](reports/spark_v145.md), [source audit](reports/source_audit_v143.md), [protocol](reports/protocol_v144.md), [amendment](reports/protocol_v145.md) and [figure](results/v145_spark/comparison.png). Prior [two-model replication](reports/models_v141.md) and [native XZ study](reports/xz_v140.md) remain preserved.

**1,091 tests passed.** Independent replay verifies source rows, raw responses, shared prefixes, budgets, decisions and statistics. Four semantic corruptions rejected; report and figures reproduce byte-identically.

```sh
.venv/bin/python scripts/verify_spark_v145.py
MPLCONFIGDIR=/tmp/mpl-v145 .venv/bin/python scripts/report_spark_v145.py
.venv/bin/python scripts/seal_research_v145.py --verify-only
```

No collector or model server is running. Do not rerun create-once collection. Source data and model redistribution rights remain source-specific; no publishing is authorized. This batch used existing models and locally queried author-recorded Spark data, not a cloud cluster.

## Current evidence

| Evidence | Location |
|---|---|
| Original corrected three-system, five-seed smoke | [V3 report](reports/pilot_report_v3.md) |
| Earlier grouped routing evaluation and its limits | [V6 report](reports/pilot_report_v6.md) |
| Broader Qwen robustness comparison | [V91 report](reports/qwen_v91.md) |
| Prior native comparison and controller transfer | [V131 native](reports/native_v131.md), [V132 router](reports/router_v132.md) |
| Post-restart feasibility, including the retained failure | [V101](reports/feasibility_v101.md), [V102](reports/feasibility_v102.md) |
| V103 raw prompts, requests, responses, usage and failures | [Raw records](results/v103_reasoning/) |
| V103 charged acquisitions, metrics and figures | [Analysis](results/v103_analysis/) |
| Tests, independent replay and historical integrity chain | [Receipts](artifacts/study_v103/) |
| Prior detailed README and historical evidence map | [Preserved snapshot](artifacts/study_v103/previous_snapshot/README.md) |

The initial schema error is retained in the [erratum](reports/schema_erratum.md); affected initial runs are not silently pooled with corrected results. Earlier checkpoints and failed attempts remain preserved. Seeds are not independent software systems.

## Replay saved evidence without new inference

The current local environment uses Python 3.10.13 and [pinned dependencies](requirements.lock.txt). With the retained input/model/runtime files:

```sh
.venv/bin/python -m pytest tests -q
.venv/bin/python scripts/verify_proposal_v127_fixed.py
.venv/bin/python scripts/audit_output_capacity_v127.py --verify-only
.venv/bin/python scripts/reproduce_proposal_v127.py
.venv/bin/python -I -S output/v127_replay/replay.py
.venv/bin/python scripts/seal_research_v145.py --verify-only
```

Collectors and acquisition evaluators are create-once; do not rerun them into existing output directories. Use the corrected verifier: the frozen original had a disclosed tie-break error in its independent batch reconstruction. Synthetic tests/fixtures never enter model-performance aggregates. Reproduction verifies saved evidence; fresh inference on another machine and original source correctness remain unverified. Historical restoration is documented in [REPRODUCE.md](REPRODUCE.md); some source/model inputs are ignored by Git.

## Provenance and interpretation

[Primary source audit](reports/source_audit.md), [reasoning-method audit](reports/source_audit_v98.md), [current model manifest](artifacts/study_v91/model_manifest.json), and [third-party attribution](THIRD_PARTY.md) document the sources. Exact SNAP2 code was not located in the bounded source search; paper-based methods are labeled adaptations rather than numerical replications.

Model inputs contain only acquired labels and candidate features. The evaluator separately acquires outcomes and enforces each arm's budget. Shared prefixes, complete failure denominators, system grouping, actual research collection cost and modeled deployment cost remain explicit. No paid/cloud inference, publishing, remote push or author contact is authorized.

The [next experiment](reports/next_experiment.md) prioritizes one coherent prospective multi-family evaluation, retaining strong cheap controls and fixed practical margins. This repository does not guarantee positive findings or acceptance by a journal.

