# When Is an LLM Worth Calling?

A bounded research repository on cost- and reliability-aware escalation from a cheap software-configuration optimizer to a local LLM. The core question is whether information available after ten objective evaluations predicts that an LLM is worth using for the remaining ten.

**Latest work (V116–V118):** completed an original-source/feature/exposure audit and reanalyzed the saved36real Qwen3-8B continuations. No new model calls or objective acquisitions. None of these continuations beats the single B20 classical portfolio by5%; even the non-deployable observed branch-selection oracle gains only0.568%on average. The mean loss is sensitive to OpenVPN; dropping it changes−2.252%to+0.557%, so broad claims of average LLM harm are unwarranted. All families remain in the primary result.

Start with the [current assessment](reports/research_readiness_v117.md), [family-influence analysis](reports/influence_v117.md), [reserved-family audit](reports/admission_v116.md), and [resume checkpoint](STATUS.md). Latest actual collection remains [V114](reports/sampling_v114.md)/[V115](reports/portfolio_v115.md):36real responses and480recorded accesses, nine small wins, maximum3.34%. The [original Storm archive](reports/archive_v118.md) now has verified license/schema provenance but still lacks linked validation evidence. No independent new group was admitted. This is a scoped empirical study, not a demonstrated generalizing router or journal-readiness guarantee.

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
.venv/bin/python scripts/audit_reserved_v116.py --verify-only
.venv/bin/python scripts/analyze_influence_v117.py
.venv/bin/python scripts/audit_archive_v118.py --verify-only
.venv/bin/python scripts/seal_reserved_influence_v118.py --verify-only
```

Current validation:893 tests passed; new synthetic fixtures remain separate from measured results. The influence figures and saved-data report reproduce in the pinned environment. Source/model collection is create-once and must not overwrite existing logs. Fresh inference, clean-machine reproduction and second-host native execution remain untested beyond the documented checks. See [REPRODUCE.md](REPRODUCE.md) for historical restoration notes and STATUS for current receipts. Weights/tables/archives may be Git-ignored.

## Provenance and interpretation

[Primary source audit](reports/source_audit.md), [reasoning-method audit](reports/source_audit_v98.md), [current model manifest](artifacts/study_v91/model_manifest.json), and [third-party attribution](THIRD_PARTY.md) document the sources. Exact SNAP2 code was not located in the bounded source search; paper-based methods are labeled adaptations rather than numerical replications.

Model inputs contain only acquired labels and candidate features. The evaluator separately acquires outcomes and enforces each arm's budget. Shared prefixes, complete failure denominators, system grouping, actual research collection cost and modeled deployment cost remain explicit. No paid/cloud inference, publishing, remote push or author contact is authorized.

The [next experiment](reports/next_experiment.md) prioritizes a frozen independent-system replication. This repository does not guarantee positive findings or acceptance by a journal.

