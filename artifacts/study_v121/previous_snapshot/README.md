# When Is an LLM Worth Calling?

A bounded research repository on cost- and reliability-aware escalation from a cheap software-configuration optimizer to a local LLM. The core question is whether information available after ten objective evaluations predicts that an LLM is worth using for the remaining ten.

**Latest result (V119–V120):** on one new WordCount software family, the original interface failed the output contract in5/5 cases. An explicitly exploratory follow-up using the existing constrained Qwen3-8B adapter produced5/5 valid continuations: mean recorded-latency gain8.07% versus batch3NN and7.60% versus sequential3NN, with2/5 joint5% wins. The unchanged benefit controller escalated0/5 and missed those opportunities. This is a real positive selection result, not demonstrated generalizing routing or Q2 readiness.

Start with the [paired-adapter report](reports/paired_adapters_v120.md), [constrained results](reports/table_check_v120.md), and [resume checkpoint](STATUS.md). Actual new collection:55 real requests and350 recorded acquisitions. Both adapters and every failure are retained. The source's original correctness/measurement provenance is unresolved; this is explicitly a published-label study, not a new native validation. Stronger V52 admission gates remain closed. Earlier [six-family results and their limits](reports/influence_v117.md) remain separate.

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
.venv/bin/python scripts/verify_table_model_v119.py
.venv/bin/python scripts/verify_table_model_v120.py
.venv/bin/python scripts/report_table_v119.py
.venv/bin/python scripts/report_table_v120.py
.venv/bin/python scripts/synthesize_table_v120.py
.venv/bin/python scripts/seal_tables_v120.py --verify-only
```

Current validation:902 tests passed; synthetic fixtures remain separate. Both source/request replays passed; saved-data reports and scientific figures reproduce byte-identically. Collection refuses overwrite. Fresh inference on a clean machine, original workload correctness and second-host native execution remain untested. See STATUS for commands and receipts, and [REPRODUCE.md](REPRODUCE.md) for historical restoration notes. Weights/tables/archives may be Git-ignored.

## Provenance and interpretation

[Primary source audit](reports/source_audit.md), [reasoning-method audit](reports/source_audit_v98.md), [current model manifest](artifacts/study_v91/model_manifest.json), and [third-party attribution](THIRD_PARTY.md) document the sources. Exact SNAP2 code was not located in the bounded source search; paper-based methods are labeled adaptations rather than numerical replications.

Model inputs contain only acquired labels and candidate features. The evaluator separately acquires outcomes and enforces each arm's budget. Shared prefixes, complete failure denominators, system grouping, actual research collection cost and modeled deployment cost remain explicit. No paid/cloud inference, publishing, remote push or author contact is authorized.

The [next experiment](reports/next_experiment.md) prioritizes a frozen independent-system replication. This repository does not guarantee positive findings or acceptance by a journal.

