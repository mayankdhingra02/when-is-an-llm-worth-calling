# New paired controls: little remaining room in the 32-setting spaces

After collecting the live measurement tables, we completed **15 paired cases / 30 classical arms** on Zstandard, LZ4 and zlib, with five fixed seeds per family. Each arm had **20 recorded-vector evaluations**, including the same saved **10-evaluation prefix**. The adaptive cheap method and random continuation were effectively tied. This is an exploratory development result, not a positive LLM/router result or a held-out test.

| Family | Mean cheap gain over random | Wins / losses / ties | Mean full-table hindsight headroom after cheap continuation |
|---|---:|---:|---:|
| Zstandard | −0.00384% | 1 / 1 / 3 | 0.2753% |
| LZ4 | +0.00321% | 1 / 0 / 4 | 0% |
| zlib | 0% | 0 / 0 / 5 | 0% |

These tiny differences are much smaller than the measurement variation observed in V15 and do not support a reliable method advantage. The table reports descriptive point estimates; no significance or equivalence test is claimed. Zero hindsight headroom means the cheap branch reached the best recorded feasible median for that case, not a proven optimum over every possible compressor setting or workload.

## Fixed setup and evidence

The objective vector is median compression milliseconds over three V15 physical observations plus compressed size. The storage cap is the measured size of a predeclared reference configuration, held fixed. Reference settings are research defaults, not application-approved requirements or claims of each library's exact default behavior.

A prefix acquires the reference, three seeded random configurations and six adaptive three-nearest-neighbor selections. The remaining ten evaluations compare continued adaptive selection with uniform-order random selection. Both branches independently clone the same acquired prefix. Candidate features contain only configuration parameters. The unchanged nominal-Hamming predictor uses acquired runtime/size labels; it never filters candidates by hidden true size. Every branch retains its feasible incumbent.

All three families and all seeds were retained, with no post-result parameter search. Every family is development/exposed, and the workload is the same one small source archive. Twenty evaluations visit a large fraction of a 32-setting space. Output-equivalent configurations further reduce effective variety. These limitations explain why this dataset should not be treated as a challenging, independent test of LLM routing.

Full-table feasible headroom was computed only after all optimizer decisions were saved, as a nondeployable diagnostic. It did not enter the predictor, feature preprocessing, prefix, cap or candidate ranking. No case had more than 10% remaining headroom. The result supplies no reason to spend model calls on this particular setup.

## What actually ran

```sh
.venv/bin/python scripts/run_classical_v16.py
.venv/bin/python scripts/analyze_verify_classical_v16.py
PYTHONPATH=src .venv/bin/python -m pytest -q
```

The collector completed all intended cases. Independent Python replay reconstructed the seeded initialization, each acquired-only prediction choice, both branches, source objective vectors, feasible incumbents, shared prefix, inclusive budgets and all **450 recorded-vector lookups**. There were no new physical trials or LLM calls. **116 tests pass**, including charged bad-target attempts, hidden-target isolation, duplicate rejection and prefix-budget/state isolation.

Actual research cost is **450 new recorded-vector lookups**, in addition to the V15 dataset's **288 charged physical trials** and the earlier **4,508 table accesses**. Across the repository these are now **4,958 table accesses + 288 physical trials**; do not imply the physical dataset was free or that all cost types are interchangeable. A single deployed classical arm would use 20 recorded-vector evaluations here. This stage does not estimate LLM deployment savings.

- Frozen specification: `reports/protocol_v16_classical.md` and `.freeze.json`.
- Saved prefixes and branches: `results/v16_classical/prefixes/`, `joint_3nn/`, `random/`.
- Durable accounting: `results/v16_classical/acquisitions.jsonl`.
- Complete denominator: `progress.json`; all cases and diagnostic bounds: `outcomes.csv`, `summary.json`.
- Execution/replay/tests: `artifacts/study_v16/collection.log`, `analysis_verification.log`, `verification.json`, `precollection_tests.log`.

## Decision

The live collector works on this workload, but this small configuration space leaves almost no useful selection opportunity beyond cheap search. **Before any additional inference, use a prospectively specified larger or more varied development task to establish headroom under a justified utility.** Changes motivated by these outcomes must remain exploratory, and untouched evaluation families are still required for generalization. Do not widen a grid repeatedly until a favorable LLM comparison appears, or relabel hindsight as an achieved router.

The existing 128/128 model allowance remains exhausted. No positive LLM result, stronger-model result, new prompt-order result, broad generalization or live production benefit has been tested.
