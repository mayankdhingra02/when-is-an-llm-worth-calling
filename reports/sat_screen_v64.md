# V64 — measured SAT configuration opportunity screen

**The frozen opportunity gate passes for planted_512. This justifies preparing a bounded real-model comparison; it does not establish that an LLM improves anything.**

All 288 intended physical trials ran: 279 valid solutions and
9 resource noncompletions. Every valid solution
was independently checked against every clause of its original CNF. No retries or
dropped failures. Collection took 579.614 seconds under the
explicitly approved 7,200-second envelope. No model calls, downloads or spending.

| Task | Valid trials | Resource failures | Best median ms | Median valid CV % | Threshold % | Gate cases | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| planted_256 | 144/144 | 0 | 4.094 | 2.130 | 5.000 | 1/5 | stop |
| planted_512 | 135/144 | 9 | 48.845 | 0.446 | 5.000 | 2/5 | pass |

![Remaining recorded headroom](../results/v64_sat_screen/headroom.png)

The primary comparator was RF-LCB before full-grid outcomes. Random and 3NN are
controls, not candidates for post-hoc selection of a favorable primary method.
Each of five fixed seeds has the same saved ten-evaluation prefix across three
arms, each ending at twenty inclusive evaluations. Thirty arms consumed 400
charged recorded-table acquisitions in 2.782 seconds.
Full-table scoring occurred only after decisions. Headroom is the improvement
available relative to that arm's best score, not an achieved LLM improvement.
The hindsight portfolio remains diagnostic only.

Forty-eight configurations vary decay, restart and phase-saving options. Each row
is the median of three fresh physical runs. An 18-second CPU / 20-second wall /
sampled 512 MiB RSS limit applies per trial; resource noncompletion receives a
40,000-ms PAR2-style objective score. This penalty is not reported as measured
runtime. The gate requires RF-LCB headroom at least max(5%, twice the median CV
percentage among fully valid settings) for at least two of five seeds. Undefined
noise thresholds cannot pass. The threshold is a screening heuristic, not a test
of statistical significance or equivalence.

## Scope and limitations

Both admitted generated tasks (256 and 512 variables) were retained. The three
1,024-variable CPU-limit noncompletions from V62 remain in the admission report.
The 512-variable task followed one disclosed adaptive size calibration. There
will be no further size calibration in this series. These are planted random
3-CNF tasks with known witnesses saved for validation only, not production or
SAT-competition samples. Seeds, tasks and parameter settings do not create
independent software systems. MiniSat is conservatively grouped with historical
Z3. The current evidence supplies one development solver family, no fresh held-out
router validation and no basis for a journal acceptance claim.

The owner MiniSat commit and compatibility patch are pinned in the V62 source
manifest and V64 freeze. Search code was not changed. CPU noncompletions are part
of the denominator; three repetitions and one host leave uncertainty about noise,
machine dependence and stable minima. Outcomes are now exposed development data.
No threshold or configuration-grid change may be described as confirmatory.

## Costs and verification

Actual research collection cost: 288 physical solver invocations plus the nine
earlier admission invocations, and 400 recorded aggregate acquisitions for this
screen. A modeled deployment of one 20-outcome arm using the same median-of-three
recipe would require 60 physical trials, including failures and initialization.
That is an estimate from the recipe, not measured deployment time or evidence
that full-grid data would be free. All resource-failure wall times remain logged.
External experiment spend is zero; hardware, electricity and researcher costs
are unknown. Model request/token/runtime costs are absent because this stage
contains no inference.

Independent verification reconstructed all 288 physical receipts and schedule,
all returned models, table medians, noise thresholds, 400 charged acquisitions,
360 optimizer choices, shared prefixes, inclusive budgets and gate decisions.
Verification took 3.870 seconds. Synthetic tests are
separate from these measurements. Raw evidence: results/v64_sat_physical/;
tables, acquisition journals, arms, CSV and figures: results/v64_sat_screen/.

```sh
.venv/bin/python scripts/verify_sat_v64.py
.venv/bin/python scripts/report_sat_v64.py
```

Collection and primary analysis are one-shot and refuse existing output trees.
The exact approval receipt is artifacts/study_v64/approval_receipt.json; the
pre-outcome protocol and input hashes are reports/protocol_v64_sat_screen.md and
its freeze JSON. No additional inference allowance follows from the runtime
approval. The next step must respect the decision above.
