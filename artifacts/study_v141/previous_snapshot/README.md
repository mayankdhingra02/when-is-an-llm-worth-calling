# When Is an LLM Worth Calling?

A bounded research repository on cost- and reliability-aware escalation from classical software-configuration optimization to a real local LLM.

**Latest checkpoint: V139–V140 complete.** Actually ran 353 native XZ configurations, 1,059 compressions/1,059 exact reconstruction checks, and five real local Qwen3-8B calls. Six B20 arms per shared B10 prefix, five seeds, one newly studied software family. The model improved none of the prefixes; continued classical search improved three. Mean model gain versus continued sequential search: **−0.0815%**, below the predeclared 1% practical margin. Frozen routers selected zero calls; this does not establish selective routing skill.

Read [STATUS](STATUS.md), [assessment](reports/research_assessment_v140.md), [measured result](reports/xz_v140.md), [protocol](reports/protocol_v140.md), [source audit](reports/source_audit_v139_v140.md) and [figure](results/v140_native/comparison.png). One new family is not a population validation or Q2-readiness certification. Earlier positive exceptions, native results and failures remain preserved. Node.js mapping is partially recovered but its recorded task remains unadmitted.

Full suite: **1,075 passed**. Independent replay verifies selections, budgets, provenance and decisions; four corrupted copies rejected. Report and figures reproduced byte-identically. Safe verification:

```sh
.venv/bin/python scripts/verify_xz_v140.py
.venv/bin/python -I -S output/v140_replay/replay.py
.venv/bin/python scripts/seal_research_v140.py --verify-only
```

[Private compact replay](output/v140_replay.zip) needs only the Python standard library; it omits native outputs, inputs, sources and model/runtime binaries, so it cannot independently re-decode them or rerun inference. No model or collector is running. Do not rerun create-once collection. Previous mutable documents are preserved under artifacts/study_v139/previous_snapshot/.

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

The [next experiment](reports/next_experiment.md) prioritizes one coherent prospective multi-family evaluation, retaining strong cheap controls and fixed practical margins. This repository does not guarantee positive findings or acceptance by a journal.

