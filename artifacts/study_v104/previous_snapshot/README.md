# When Is an LLM Worth Calling?

A bounded research repository on cost- and reliability-aware escalation from a cheap software-configuration optimizer to a local LLM. The core question is whether information available after ten objective evaluations predicts that an LLM is worth using for the remaining ten.

**Current result (V103):** 36 real local Qwen3-8B requests across six exposed systems, two seeds and two modes. Thinking produced 10/12 valid final answers; nonthinking produced 12/12. Neither mode had a valid case improving on both strong classical controls by at least 5%. Mean gains versus sequential 3NN were -7.64% and -6.52%, respectively. This is exploratory development evidence, not an established useful router or journal-ready result.

Start with the [current assessment](reports/research_readiness_v103.md), [full report and figures](reports/reasoning_v103.md), [frozen protocol](reports/protocol_v103.md), and [resume checkpoint](STATUS.md).

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
.venv/bin/python scripts/verify_reasoning_v103.py
.venv/bin/python scripts/audit_usage_v103.py
.venv/bin/python scripts/report_reasoning_v103.py
.venv/bin/python scripts/seal_reasoning_v103.py --verify-only
```

Tests live in a separate namespace and are excluded from research aggregates. Current validation: 780 tests passed across the full suite and three added corruption checks; every saved continuation and all 240 V103 acquisitions replayed. The report and figures reproduce byte-for-byte in the current environment. The latest sealer resolves historical root-document snapshots.

Do not rerun `collect_reasoning_v103.py` or `analyze_reasoning_v103.py` into existing output: those are once-only collection/acquisition steps. Fresh collection needs a new frozen protocol, isolated output namespace and bounded allowance. Current replay assumes local pinned assets; clean-machine fresh-inference reproduction is not established. [REPRODUCE.md](REPRODUCE.md) retains the historical restoration notes; weights, tables and archives may be Git-ignored.

## Provenance and interpretation

[Primary source audit](reports/source_audit.md), [reasoning-method audit](reports/source_audit_v98.md), [current model manifest](artifacts/study_v91/model_manifest.json), and [third-party attribution](THIRD_PARTY.md) document the sources. Exact SNAP2 code was not located in the bounded source search; paper-based methods are labeled adaptations rather than numerical replications.

Model inputs contain only acquired labels and candidate features. The evaluator separately acquires outcomes and enforces each arm's budget. Shared prefixes, complete failure denominators, system grouping, actual research collection cost and modeled deployment cost remain explicit. No paid/cloud inference, publishing, remote push or author contact is authorized.

The [next experiment](reports/next_experiment.md) prioritizes a frozen independent-system replication. This repository does not guarantee positive findings or acceptance by a journal.
