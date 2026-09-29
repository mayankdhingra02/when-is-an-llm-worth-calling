# When Is an LLM Worth Calling?

A bounded research repository on cost- and reliability-aware escalation from classical software-configuration optimization to a real local LLM.

**Latest checkpoint: V130 complete.** One newly admitted native FLAC family, three licensed speech clips, five paired B10/B20 seeds: Qwen3-8B won0, tied2 and lost3 versus sequential3NN, mean gain−0.1869%. It improved over the standard preset by2.6860%, but the cheaper optimizer explained that apparent advantage. All303 configuration trials passed exact sample checks; five actual model requests completed. This is descriptive negative evidence, not demonstrated useful routing or Q2readiness.

Read [STATUS](STATUS.md), [current research assessment](reports/research_assessment_v130.md), [paired results](reports/flac_v130.md), [frozen protocol](reports/protocol_v130.md) and [source audit](reports/source_audit_v130.md). Full suite:1,030passed. Independent replay checks25 paired arms and909 encoder/909 decoder records; report/data/figure reproduce byte-identically. All clips/seeds are one family. No paid/cloud inference or publication.

Safe verification without new inference or objective collection:

```sh
.venv/bin/python scripts/verify_flac_v130.py
.venv/bin/python scripts/analyze_flac_v130.py
.venv/bin/python -I -S output/v130_replay/replay.py
.venv/bin/python scripts/seal_flac_v130.py --verify-only
```

[Private compact replay](output/v130_replay.zip):572,512bytes/378hashed files, standard library only, no network/model/binary/audio. It validates saved records; the full repository verifier also checks physical encoded outputs. It is not a second-host execution. Do not rerun create-once native/model collectors.

Prior results remain: [V129 two-family result](reports/proposals_v129.md), [routing envelope](reports/policy_envelope_v129.md), [V127 full-domain result](reports/proposals_v127.md), [capacity correction](reports/capacity_correction_v127.md). The pre-V130 README is preserved in artifacts/study_v130/previous_snapshot/README.md. Negative means do not erase prior positive exceptions or imply universal impossibility.

## Current evidence

| Evidence | Location |
|---|---|
| Original corrected three-system, five-seed smoke | [V3 report](reports/pilot_report_v3.md) |
| Earlier grouped routing evaluation and its limits | [V6 report](reports/pilot_report_v6.md) |
| Broader Qwen robustness comparison | [V91 report](reports/qwen_v91.md) |
| Latest native family pilot | [V130 FLAC report](reports/flac_v130.md) |
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

