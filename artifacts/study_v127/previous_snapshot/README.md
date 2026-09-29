# When Is an LLM Worth Calling?

A bounded research repository on cost- and reliability-aware escalation from a cheap software-configuration optimizer to a local LLM. The core question is whether information available after ten objective evaluations predicts that an LLM is worth using for the remaining ten.

**Latest result (V124–V126):**198 real local Qwen3-8B requests plus an exhaustive recorded-domain audit are complete. Demonstrating the required answer format improved validity from4/9to9/9in a small development probe. That is not an optimization result. The domain audit finds theoretical≥5%gain over both classical controls in only4/30prefixes, concentrated in two of six exposed families.

**Design correction:** V42had already proved the old shortlist could never meet the recent joint5%quality screen. V123/V124overlooked that known restriction. Raw outcomes remain preserved, but that failed screen cannot refute unrestricted LLM optimization. Read the [correction](reports/attainability_v125.md), [current research assessment](reports/research_assessment_v126.md), [domain audit](reports/domain_audit_v126.md), [surrogate result](reports/surrogate_v124.md), [format diagnostic](reports/format_probe_v125.md) and [STATUS](STATUS.md).

980tests pass. Independent replay verified198new model requests,60optimization acquisitions,4,932coverage acquisitions and102historical control states. Two reports/figures reproduce byte-identically. This is exposed development evidence; useful unseen-system routing and Q2readiness are not established.

Private executed replays: [corrected V124 ZIP](output/v124_replay_corrected.zip), [V125 format ZIP](output/v125_replay.zip), [V126 domain ZIP](output/v126_replay.zip). Standard-library replay uses no inference or new outcome acquisitions. Source redistribution qualifications remain; no uploads occurred. V124's original ZIP predates the attainability correction; use the corrected bundle. These bundles do not replace fresh inference replication on another machine.

## Current evidence

| Evidence | Location |
|---|---|
| Original corrected three-system, five-seed smoke | [V3 report](reports/pilot_report_v3.md) |
| Earlier grouped routing evaluation and its limits | [V6 report](reports/pilot_report_v6.md) |
| Broader Qwen robustness comparison | [V91 report](reports/qwen_v91.md) |
| Latest completed native workload comparison | [V97 report](reports/numerical_v97.md) |
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
.venv/bin/python scripts/verify_replication_v121.py
.venv/bin/python scripts/audit_router_v121.py
.venv/bin/python scripts/verify_cached_v122.py
.venv/bin/python scripts/report_replication_v121.py
.venv/bin/python scripts/report_cached_v122.py
.venv/bin/python -I output/v121_replay/replay.py
.venv/bin/python scripts/seal_replication_v122.py --verify-only
```

Both model-collection stages and cached-selection outputs are create-once. Raw responses, original failures, source hashes, grouped training fits, charged budgets and all intended cases are retained. Source/request/projection checks and compact isolated-Python replay passed. Final tests are recorded in STATUS and `artifacts/study_v122/tests_final.log`. Synthetic fixtures never enter measured aggregates. Fresh inference on another machine and original workload correctness remain untested. See [REPRODUCE.md](REPRODUCE.md) for historical restoration notes; some large source/model inputs are ignored by Git.

## Provenance and interpretation

[Primary source audit](reports/source_audit.md), [reasoning-method audit](reports/source_audit_v98.md), [current model manifest](artifacts/study_v91/model_manifest.json), and [third-party attribution](THIRD_PARTY.md) document the sources. Exact SNAP2 code was not located in the bounded source search; paper-based methods are labeled adaptations rather than numerical replications.

Model inputs contain only acquired labels and candidate features. The evaluator separately acquires outcomes and enforces each arm's budget. Shared prefixes, complete failure denominators, system grouping, actual research collection cost and modeled deployment cost remain explicit. No paid/cloud inference, publishing, remote push or author contact is authorized.

The [next experiment](reports/next_experiment.md) prioritizes demonstrating incremental value over free controls on development data before another independent-system evaluation. This repository does not guarantee positive findings or acceptance by a journal.

