# When Is an LLM Worth Calling?

A bounded research repository on cost- and reliability-aware escalation from classical software-configuration optimization to a real local LLM.

**Latest checkpoint: V131–V132 complete.** Two new native families,648configuration trials,10real Qwen3-8B requests. WavPack's mean model gain versus sequential3NN is+0.0058%(25.2bytes); FFTW's freshly validated mean is−1.5160%. The one apparent FFTWwin uses identical settings and is timing variability.

A separate controller was trained on40historical cases/eight groups, with ten decisions frozen before either new family's LLM continuation outcomes. Benefit and uncertainty policies chose0calls and matched never-escalate. This is an actual small outcome-blind transfer test, not demonstrated learned selective advantage or Q2readiness. All seeds/windows stay in their software group.

Read [STATUS](STATUS.md), [assessment](reports/research_assessment_v132.md), [native results](reports/native_v131.md), [router results](reports/router_v132.md), [source audit](reports/source_audit_v131.md), and frozen protocols[V131](reports/protocol_v131.md)/[V132](reports/protocol_v132.md). Full suite:1,042passed. Independent replay reconstructs native selections/correctness receipts, real model responses, historical features, group-exclusion fits/thresholds and decision-before-outcome timing. Five generated artifacts reproduce byte-identically.

Safe verification without new model/native collection:

```sh
.venv/bin/python scripts/verify_native_v131.py
.venv/bin/python scripts/verify_router_v132.py
.venv/bin/python scripts/analyze_native_v131.py
.venv/bin/python scripts/analyze_router_v132.py
.venv/bin/python -I -S output/v132_replay/replay.py
.venv/bin/python scripts/seal_native_router_v132.py --verify-only
```

[Private compact replay](output/v132_replay.zip):870hashed files, standard-library-only replay, no audio/binaries/weights/network. Compact mode checks saved receipts; full workspace verification also checks native output files. Not a second-host experiment. No paid/cloud spending, external contact or publication. Do not rerun create-once collectors.

Previous evidence: [V130 FLAC](reports/flac_v130.md), [V129 Storm/MongoDB](reports/proposals_v129.md), [V127 full-domain proposals](reports/proposals_v127.md) and its[capacity correction](reports/capacity_correction_v127.md). The prior README is preserved in artifacts/study_v131/previous_snapshot/README.md. Original positive exceptions, failures and adaptive history remain.

## Current evidence

| Evidence | Location |
|---|---|
| Original corrected three-system, five-seed smoke | [V3 report](reports/pilot_report_v3.md) |
| Earlier grouped routing evaluation and its limits | [V6 report](reports/pilot_report_v6.md) |
| Broader Qwen robustness comparison | [V91 report](reports/qwen_v91.md) |
| Latest native comparison and controller transfer | [V131 native](reports/native_v131.md), [V132 router](reports/router_v132.md) |
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

