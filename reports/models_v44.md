# V44: the real model does not exploit the wider candidate pools reliably

**Completed all60approved local-model calls. Changing candidate pools did not
produce a useful escalation result.** On the uniform pool, the1.5B model never
beat the same pool's cheap batch3NN selector:24ties and6harms. On the diversity
pool it achieved a very small average advantage over its own batch selector,
but remained worse than full-domain sequential3NN.

This executes the follow-up motivated by V43's larger hindsight opportunity.
It is a negative mechanism result on six exposed software families, not a
fresh held-out routing study, a SNAP2 replication or evidence of Q2 readiness.

## Actual experiment and primary findings

Six families × five fixed seeds × two pools =60real Qwen2.5-1.5B-Instruct
requests. All share their original ten-label V41 prefix, then acquire ten
continuation outcomes. Model revision, CPUfloat32/4threads, constrained candidate
IDs, greedy decoding, prompts and analysis definitions were fixed in advance.
Both pools and every case remain in the results. No request retries, request
errors, missing responses or fallbacks occurred. Grammar validity is not proof
of useful or semantically reliable optimization.

Equal-family mean relative gain; W/T/H counts refer to30paired cases per pool:

| Candidate pool | Reference | Mean gain | W/T/H |
|---|---|---:|---:|
| Uniform20 | Same-pool batch3NN (primary) | -1.21144% | 0/24/6 |
| Uniform20 | Original batch3NN | -2.16248% | 5/12/13 |
| Uniform20 | Full-domain sequential3NN | -4.01660% | 1/14/15 |
| Uniform20 | Pool ceiling, nondeployable | -4.38092% | 0/22/8 |
| Retained10 + diverse10 | Same-pool batch3NN (primary) | +0.00248% | 3/21/6 |
| Retained10 + diverse10 | Original batch3NN | -0.00787% | 3/21/6 |
| Retained10 + diverse10 | Full-domain sequential3NN | -1.94405% | 4/15/11 |
| Retained10 + diverse10 | Pool ceiling, nondeployable | -0.23445% | 0/21/9 |

Within these measured uniform-pool cases, choosing between the model and
same-pool batch3NN cannot improve quality over always using batch3NN: there is
no positive case for a router to select, while LLM requests add cost. This is a
finite-sample observation, not a theorem that no LLM or router can ever help.

For full-domain sequential3NN, the uniform pool's2.7127% perfect-selection-plus-
perfect-routing opportunity from V43 is only16.09% captured by the model's own
positive gains. Even that capture ratio is outcome-informed and nondeployable:
it clips harmful cases after outcomes, while always calling averages-4.0166%.
The diversity pool captures87.31% of a much smaller0.3038% hindsight opportunity;
its always-call mean remains-1.9441%. No predictive router achieved these ratios.

The model attains its pool ceiling22/30times for uniform and21/30for diversity.
Against exact uniform ten-of-twenty selection, expected model gain is-1.9149%
on the uniform pool and+0.8018% on the diversity pool. The latter favorable
comparison does not survive the stronger full-domain control. All case rows,
six-family means, null/signed capture values and exact random expectations are
retained in the summary; no favorable comparator was selected for reporting.

## Cost and provenance

Actual collection:60requests,600charged recorded outcome accesses,
98,358input tokens,1,200output tokens and397.139428seconds request wall time.
Total model stage413.729752seconds, within the approved450seconds. Uniform and
diversity pools each used49,179input/600output tokens; their request times were
204.299879s and192.839548s respectively. No new physical trials, downloads,
paid/cloud inference, publication, remote push or external communication.

The preceding V41 and V43 collection costs were3,000 and1,200recorded accesses;
the combined sequence therefore costs4,800, not20. Each hypothetical deployed
arm still uses20logical evaluations and one model request if escalated. Per-case
deployment traces are explicitly modeled from saved prefixes/requests, with
loading amortization stated and unmeasured scheduler/objective-access overhead
excluded. They are not measured live deployment latency or cloud-dollar savings.

The follow-up request ledger is now350/350 (450including the initial stage).
Cumulative recorded accesses14,408; physical trials remain1,274. Total runtime
after collection, failed/corrected analysis, verification and rendering:
3,293.338663/3,600seconds, leaving306.661337seconds. No process remains running.

## Analysis defect, correction and verification

The original frozen analyzer stopped on its paired-state guard. Constructing a
State directly from a prefix dictionary aliased mutable lists, so first-pool
replay mutated the in-memory prefix later used by the second pool. The stored
prefix and model outputs were unchanged. The failed attempt produced no quality
summary; its partial cost output/log and2.695453seconds are preserved.

The original analyzer remains unchanged. The corrected copy deep-clones the
prefix before replay; it has its own correction record and seal. This fixes the
calculation without changing scientific endpoints or experimental choices.
See `reports/analysis_correction_v44.md`. Do not run the superseded analyzer.

Verification completed:

- **338tests pass**, including a two-pool regression test in both target
  directions. Synthetic fixtures remain outside measured results.
- All60prompts, raw token outputs, constrained grammar traces, cache identities,
  shared-prefix states and600acquisition events replay in the corrected analyzer.
- The independent standard-library verifier matches600events to565distinct
  acquired source rows and recomputes240paired comparisons,60exact random
  comparisons and8aggregate contrasts. It imports no optimizer implementation.
- Deliberate corruption of a temporary copied result was rejected; original
  outputs remain unchanged. Original protocol/analysis seals remain intact.
- PNG/SVGfigure visually checked. Model logits were not recomputed on a second
  machine, and this does not establish independent hardware reproducibility.

Evidence:
`results/v44_models/` contains raw starts/responses, provenance, checkpoints,
branches and acquisitions. `results/v44_model_analysis/` contains the full
summary,240-rowCSV, cost record and figure. Logs, verification receipts and
tests are in `artifacts/study_v44/`. Earlier review ZIPs remain unchanged and do
not yet include this experiment.

Executed commands:
```sh
.venv/bin/python scripts/run_pool_models_v44.py
.venv/bin/python scripts/analyze_pool_models_v44.py  # failed; preserved
.venv/bin/python scripts/analyze_pool_models_v44_fixed.py
.venv/bin/python -I -S scripts/verify_pool_models_v44.py
.venv/bin/python scripts/render_pool_models_v44.py
.venv/bin/python -m pytest -q tests/synthetic tests/test_transfer_v41.py
```
Collection and analysis refuse overwrite. Use the verifier/renderer on existing
outputs; fresh inference needs a separate preserved run and resource allowance.

## Decision and remaining research gap

The frozen decision rule says to stop this particular adaptation if expanded
candidate opportunity is not captured robustly beyond cheap selection. V44
meets that stopping condition. Do not keep tuning pools, prompts or thresholds
on these exposed cases until a favorable mean appears.

The defensible current contribution is an exploratory audit showing how cheap
controls and candidate-pool construction change apparent LLM value. It still
lacks validated benefit-aware routing, independent-model-family evidence,
equal application-utility/correctness controls and established novelty. Those
gaps prevent an honest claim that this research is ready for a Q2 journal.

**Single most important next action:** review this negative mechanism result
and the close prior work with Tim Menzies before funding or authorizing another
collection design. No message has been sent. If a new study is justified,
prioritize a genuinely different, semantically informed model intervention,
equal application utility and independent development/test software groups;
more calls to this fixed small-model adaptation are not the priority.
