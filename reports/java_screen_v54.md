# V54 — real Java workload: correctness passed, escalation-opportunity gate failed

We collected **144 fresh JVM trials across 48 GC configurations** and executed
**15 classical continuation arms across five fixed seeds**. All workload outputs
passed validation. The saved ten-evaluation prefixes were already within
**0.51–1.10% of the best recorded median**. The frozen opportunity screen failed
in **all five seeds**. No LLM call was justified or made in this stage.

This adds an application benchmark and another bounded negative result. It does
not establish general LLM uselessness, cross-system router performance, novelty,
or Q2 publication readiness.

## What actually ran

- Temurin 17.0.20.1+1 ARM JRE, installed only inside this project. Released
  DaCapo 9.12-MR1-bach / Xalan 2.7.1; original artifact hashes and licenses pinned.
- Fixed default Xalan input: 100 repetitions of 17 XML transformations, one
  application worker, 512 MiB initial/max heap, ParallelGC with adaptive sizing
  disabled. Three GC parameters vary across a frozen 48-setting factorial grid.
- Three roundwise-randomized fresh-JVM repetitions per setting. Each invocation
  has one warmup and one timed iteration: **144 warmups + 144 measured iterations**.
  No retries, dropped trials, failures or unattempted cases. Collection: **466.03 s**.
- Owner validation stays enabled. Every final transformed output has exactly
  **23,901,000 bytes** and the same SHA256 as V53's retained reference. This
  supplements the owner's completion-message validation, which alone does not
  hash the transformed output. Reference equivalence is not a proof of XSLT
  standards conformance. Warmup payloads are not independently hashed.
- Median-of-three runtime table; no outlier removal. Five seeds, shared saved
  10-evaluation prefix, and three independent ten-evaluation continuations:
  random, greedy 3NN, and a 64-tree random-forest lower-confidence-bound policy.
  All arms total 20 acquired aggregate outcomes and retain their best incumbent.

All classical selection code and analysis rules were frozen before physical
collection. Optimizers receive only configuration features and their own acquired
observations. Full-table scoring occurs after decisions are written. All three
branches reuse identical prefixes, with separate continuation state and RNGs.

## Recorded outcomes and uncertainty

| Seed | Prefix best ms | Random best ms | 3NN best ms | RF-LCB best ms | Best-of-three remaining headroom |
|---|---:|---:|---:|---:|---:|
| 11 | 1186 | 1173 | 1186 | 1179 | 0% |
| 23 | 1179 | 1173 | 1179 | 1173 | 0% |
| 37 | 1179 | 1179 | 1173 | 1179 | 0% |
| 53 | 1186 | 1173 | 1173 | 1183 | 0% |
| 71 | 1186 | 1183 | 1185 | 1175 | 0.1702% |

The full-table minimum median is **1173 ms**. The best-of-three reference selects
an arm in hindsight; it is **not a deployable policy**. Individual arm differences
are also small and do not establish a reliable ranking of the classical methods.

Median per-configuration coefficient of variation is **4.7378%**. The frozen
gate required remaining headroom at least `max(5%, 2 × median CV)` in at least
two seeds: here **9.4757%**, met in **0/5**. Timing variability is considerably
larger than the observed room for improvement from the saved prefixes. A
noise-sensitive table minimum is an optimistic hindsight reference; neither it
nor the median table is an exact physical optimum. The CV gate is a descriptive
screening heuristic, not a confidence interval or statistical guarantee.

![Actual repeated timings](../results/v54_java_screen/physical_times.png)

![Classical screen](../results/v54_java_screen/classical_screen.png)

## Cost accounting and reproducibility

**Actual collection:** 144 new JVM invocations, 288 benchmark iterations counting
warmups, 466.03 s stage time. The earlier V53 feasibility study adds three JVM
invocations and six iterations separately. V54's offline screen acquired **200
recorded median vectors**: `5 × (10 shared prefix + 3 × 10 continuation)` and took
1.429 s. No model requests, tokens, paid inference or cloud resources. Electricity
and user/agent time are unpriced. Download/setup costs are in V53's ledger.

**Modeled deployment:** one selected arm would acquire 20 aggregate outcomes.
Under this three-repetition measurement recipe, that means 60 JVM invocations
and 120 workload iterations including warmups. It would not incur all three
counterfactual branches or the complete 48-setting grid. Actual invocation wall
times include loading, extraction, warmup and validation; reported objective
milliseconds measure the whole timed Xalan iteration, including its output writes.
We do not claim a precise deployment dollar/time saving from these local records.

Evidence:

- `results/v54_java_physical/`: predeclared schedule, starts, all 144 raw process
  logs, validation reports, runtime and output hash/size receipts.
- `results/v54_java_screen/`: sealed 48-row table, repetitions, five prefixes,
  15 arms, 200-event charge ledger, summary, regenerable PNG/SVG figures and CSV.
- `reports/protocol_v54_java_screen.md` and its SHA256 freeze: budget, grid,
  measurement, baseline and gate definitions committed before execution.
- `artifacts/study_v54/`: collection, analysis, independent verification and test
  receipts; final evidence manifest. Large binaries/canonical output stay local.

Independent verification reconstructed **all 180 adaptive classical choices**,
checked all 200 source charges and shared prefixes, checked physical schedules,
runtime/log/validation receipts and recomputed the gate. **365 tests passed.**
The figures were visually checked. No frozen collector or primary analysis was
changed after outcomes. This is a local reproducible study, not yet a new portable
clean-environment reproduction bundle.

```sh
# These two collectors are one-shot and refuse overwrite:
.venv/bin/python scripts/collect_java_v54.py
.venv/bin/python scripts/screen_java_v54.py
# Re-run these against saved evidence:
.venv/bin/python scripts/verify_java_v54.py
.venv/bin/python scripts/report_java_v54.py
.venv/bin/python -m pytest -q tests
```

## Limitations and next decision

One JVM family, one historical application workload, one worker, one collector,
three tunable parameters, 48 settings, three repetitions and five correlated seeds
are narrow scope. No steady-state convergence, thermal/frequency isolation,
production representativeness or cross-system generalization is established.
No newly paired LLM arm or new router evaluation was run. Models may have other
useful roles that this finite configuration study does not test.

**Stop this grid as an LLM-benefit discovery experiment.** Keep it as a validated
negative-control benchmark. Do not broaden settings or repeat prompts merely to
obtain a positive score. V49's separate prompt/decoder stopping decision remains.

**Single next action:** resolve a fixed FastDownward planning task's configuration
mapping, plan validity/cost and failed-run accounting, then prospectively freeze
its classical screen. This is a different development-family lead already in
the source audit, not a reserved evaluation family. Its eligibility and headroom
are unproven. Preserve MongoDB, Redis and Storm reservations and require genuinely
independent, utility-valid families before claiming a learned router result.
