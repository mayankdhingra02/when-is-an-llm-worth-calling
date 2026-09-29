> Latest completed: **V164** tested the proposal-interface explanation with **40 fresh local-model calls and900 new configuration outcomes**. Catalogs eliminated duplicates/projections among140 evaluated proposals, but produced no robust10% gain and increased inference cost. **1,282tests passed**; eight analysis artifacts reproduce byte-identically. Read [STATUS](STATUS.md), [report](reports/apps_v164.md), [assessment](reports/research_assessment_v164.md), and [mechanism figure](results/v164_native/mechanism.png). This is development evidence on exposed applications, not Q2 certification. Earlier checkpoints below remain preserved.

> Latest completed work: **V160–V163** added two real-input application families, 80 feasibility outcomes and **800 paired configuration outcomes / 2,400 native invocations / 20 real local-model calls**. Neither model achieved a robust joint 10% win; 1,258 tests passed. Read [STATUS](STATUS.md), [application report](reports/apps_v163.md) and [assessment](reports/research_assessment_v163.md). Ten analysis artifacts reproduce byte-identically. All model processes stopped; journal readiness remains unestablished. Older sections below are preserved history.

> Latest completed work: **V156–V159** added two pinned native solvers, 80 feasibility probes and **800 real native evaluations with 20 local-model calls**. Neither model achieved a robust joint 10% win; 1,227 tests passed. Read [STATUS](STATUS.md), the [new report](reports/solvers_v159.md) and [research assessment](reports/research_assessment_v159.md). This strengthens bounded negative evidence, not Q2 readiness. All processes stopped. Older sections describe earlier checkpoints.

# Latest checkpoint: V154–V155

[STATUS.md](STATUS.md) is the resume entry. New [checkpoint-controller comparisons](reports/controllers_v154.md) execute BORA-inspired and rank-reliability adaptations over140genuine historical model-cases. New [GP-EI continuations](reports/gp_v155.md) execute1,393charged recorded acquisitions:139/140arms complete, one missing-source sensitivity failure retained. Both local models lose against the primary GP baseline in all seven ecosystem means. Calibrated routing still selects no calls. **1,190tests passed**; reports/figures reproduce byte-identically.

The [assessment](reports/research_assessment_v155.md) describes the stronger negative evidence and its limits. No new LLM inference or native run occurred this stage. Full published algorithms were not replicated; these are explicitly mapped checkpoint adaptations. No journal-readiness guarantee. [Next research priority](reports/next_experiment.md): prospective evaluation on additional independent families, without retuning on these outcomes.

# Prior checkpoint: V149–V153

Resume from [STATUS.md](STATUS.md). The new [native Memcached study](reports/native_study_v153.md) ran **400 objective evaluations and ten real local-model calls**, following [40 feasibility probes](reports/native_feasibility_v152.md). Neither model beat both strong classical controls by >1% in any seed. The [corrected richer-router analysis](reports/router_v151.md) adds group-aware nonlinear/feature comparisons; V149 was rejected for a case-ID collision and remains excluded. **1,165 tests passed**; independent replays and byte-identical report/figure regeneration passed.

The [research assessment](reports/research_assessment_v153.md) explains the results, timing noise and remaining evidence gaps. No journal-readiness or successful general-router claim. The [focused novelty audit](reports/novelty_audit_v153.md) identifies closer baselines for the [next experiment](reports/next_experiment.md). No model/native server or collector remains running. Do not rerun create-once collection.

# Prior checkpoint: V146–V148

Resume from [STATUS.md](STATUS.md). New [Hadoop transfer result](reports/hadoop_v148.md):30real local model requests,1200recorded charges,one new family. [Nested router analysis](reports/router_v147.md):seven exposed families,55cases/model. The [assessment](reports/research_assessment_v148.md) separates useful model exceptions from failed selective routing; no journal-readiness claim. Both studies have raw logs, independent replay and deterministic figures.

# When Is an LLM Worth Calling?

A reproducible research repository on cost- and reliability-aware escalation from classical software-configuration optimization to real local LLMs.

**Historical: V143–V145 complete.** Added one Spark family with five fixed workloads and five seeds: **50 real model requests, 49 completed responses, 175 budgeted arms and 2,000 charged recorded outcomes**. SmolLM3-3B beat both strong classical continuations by more than 1% in **4/25 cases**; Qwen3-8B did so in **1/25**. Both models lost on average. The frozen controllers chose no calls and missed useful opportunities; all Spark cases extrapolate beyond their training range on domain cardinality.

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

