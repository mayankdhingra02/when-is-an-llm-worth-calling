# When Is an LLM Worth Calling?

A bounded research repository on cost- and reliability-aware escalation from a cheap software-configuration optimizer to a local LLM. The core question is whether information available after ten objective evaluations predicts that an LLM is worth using for the remaining ten.

**Latest results (V114–V115):** 36 new real Qwen3-8B responses and 480 charged recorded outcomes. Three sampling seeds per fixed prefix produced no >=5% wins over both strong original controls. Against a separately frozen single classical portfolio within B20, there were 9 wins, 15 ties and 12 losses; the largest LLM win was 3.34%, and the group-first mean was -2.25%. Six exposed groups remain six groups; these are exploratory results, not a demonstrated useful router or journal-readiness guarantee.

Start with the [current assessment](reports/research_readiness_v115.md), [sampling-reliability report](reports/sampling_v114.md), [single-portfolio comparison](reports/portfolio_v115.md), and [resume checkpoint](STATUS.md). The [native timing qualification](reports/validation_v113.md) and [unexecuted second-host packet](output/v113_replication/README.md) remain important. No new native workload ran in V114–V115.

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

Current continuation: [V104 admission audit](reports/admission_v104.md) identified NGINX for fresh validation; no new performance/model measurements. Start from [STATUS](STATUS.md). V103's actual negative comparison remains the latest model-quality evidence.

Latest executed continuation: [V105 native NGINX](reports/nginx_v105.md)—six real workloads,49,152byte-exact responses; timing feasibility failed because runs were too short and client CPU use too high. No new LLM calls. See [STATUS](STATUS.md) and [saved-evidence reproduction](artifacts/study_v105/REPRODUCE.md).
