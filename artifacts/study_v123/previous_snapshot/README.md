# When Is an LLM Worth Calling?

A bounded research repository on cost- and reliability-aware escalation from a cheap software-configuration optimizer to a local LLM. The core question is whether information available after ten objective evaluations predicts that an LLM is worth using for the remaining ten.

**Latest result (V121–V122):** the earlier WordCount gains were exactly reproducible by selecting the first ten displayed candidates without calling an LLM. A prospectively frozen MongoDB replication found the same identity in5/5 normal continuations. A controller trained on seven other families escalated5/5 against that free baseline and gained0%. Loss removal changed one of five selections; the model is not universally insensitive to observations.

This continuation executed100real requests and450recorded acquisitions, including an exploratory real-cache projection that also failed the stronger controls. Read the [independent-family result](reports/replication_v121.md), [cached projection](reports/cached_projection_v122.md), [research assessment](reports/research_assessment_v122.md), and [STATUS](STATUS.md). Earlier outcomes are preserved with this qualification. This is a reproducible negative-result candidate, not a successful generalizing router or a journal-tier guarantee.

A compact private [standard-library replay](output/v121_replay/README.md) has been executed in isolated Python; [ZIP](output/v121_replay.zip). It checks saved evidence without weights/installations, not a fresh model run.

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

