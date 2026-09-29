# When Is an LLM Worth Calling?

A bounded research repository on cost- and reliability-aware escalation from classical software-configuration optimization to a real local LLM.

**Latest checkpoint: V137–V138 complete.** Collected 600 recorded evaluations across 60 cheap-control continuations on six exposed systems, five fixed seeds. Adaptive incumbent-neighbor search beats the historical valid one-shot Qwen3-8B outcome in 15 cases, ties 14 and loses 1; it does not uniformly beat continued sequential3NN. Zero new model calls. New independent-cohort audit admits no group yet; Node.js workload mapping remains unresolved.

Read [STATUS](STATUS.md), [assessment](reports/research_assessment_v138.md), [measured controls](reports/incumbent_v138.md), [protocol](reports/protocol_v138.md), [source audit](reports/source_audit_v137.md) and [figure](results/v138_incumbent/comparison.png). Six exposed systems are exploratory evidence, not fresh router validation or a Q2-readiness certification. Earlier genuine model responses, positive exceptions, native results and failures remain preserved.

Full suite: 1,071 passed. Independent replay verifies every selection/acquisition and comparison; four deliberately corrupted copies rejected. Safe verification:

```sh
.venv/bin/python scripts/verify_incumbent_v138.py
.venv/bin/python -I -S output/v138_replay/replay.py
.venv/bin/python scripts/seal_research_v138.py --verify-only
```

[Private compact replay](output/v138_replay.zip) needs only the Python standard library. No model or collector is running. Do not rerun create-once collection. Previous mutable documents are preserved under artifacts/study_v137/previous_snapshot/.

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
.venv/bin/python scripts/seal_proposal_v127.py --verify-only
```

Collectors and acquisition evaluators are create-once; do not rerun them into existing output directories. Use the corrected verifier: the frozen original had a disclosed tie-break error in its independent batch reconstruction. Synthetic tests/fixtures never enter model-performance aggregates. Reproduction verifies saved evidence; fresh inference on another machine and original source correctness remain unverified. Historical restoration is documented in [REPRODUCE.md](REPRODUCE.md); some source/model inputs are ignored by Git.

## Provenance and interpretation

[Primary source audit](reports/source_audit.md), [reasoning-method audit](reports/source_audit_v98.md), [current model manifest](artifacts/study_v91/model_manifest.json), and [third-party attribution](THIRD_PARTY.md) document the sources. Exact SNAP2 code was not located in the bounded source search; paper-based methods are labeled adaptations rather than numerical replications.

Model inputs contain only acquired labels and candidate features. The evaluator separately acquires outcomes and enforces each arm's budget. Shared prefixes, complete failure denominators, system grouping, actual research collection cost and modeled deployment cost remain explicit. No paid/cloud inference, publishing, remote push or author contact is authorized.

The [next experiment](reports/next_experiment.md) prioritizes demonstrating incremental value over free controls on development data before another independent-system evaluation. This repository does not guarantee positive findings or acceptance by a journal.

