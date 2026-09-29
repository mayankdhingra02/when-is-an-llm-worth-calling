# V72: valid local-model proposals, no observed escalation benefit

The approved frozen batch completed all 35 real local SmolLM3 generation requests
and all 150 new physical RocksDB evaluations. Every response satisfied the finite
configuration grammar, every proposed setting was unobserved within its arm,
and every physical evaluation passed correctness/configuration checks. There were
no retries, fallbacks, missing cases or extra generation probes.

The LLM-selected configuration had a slower confirmed median than both RF-LCB
and the cheap domain prior on every seed. This is a negative result for escalation
on this specific workload. It is not a model-interface failure: all five LLM
incumbents came from actual LLM proposals, not the prefix or fallback selections.

## Fixed experiment and outcomes

All methods started from the same saved ten-evaluation prefix for each of five
seeds. Each continuation acquired seven new settings, froze its best observed
incumbent, then spent its final three evaluations on fresh confirmations. Thus
every arm consumed an inclusive budget of 20. The model remained resident during
all new arms; execution order was prospectively randomized by round. The worker,
data, trace, prompt, grammar, controls and analysis were frozen before collection.

Confirmed median verified-loop time in milliseconds (lower is better):

| Seed | RF-LCB | Cheap domain prior | Local LLM |
|---|---:|---:|---:|
| 11 | 200.576 | 215.820 | 218.674 |
| 23 | 223.215 | 211.329 | 231.003 |
| 37 | 195.065 | 209.886 | 218.870 |
| 53 | 175.776 | 208.695 | 220.517 |
| 71 | 227.930 | 213.243 | 234.844 |
| Mean of seed medians | **204.512** | **211.795** | **224.782** |

The LLM mean is 9.91% slower than RF's mean. Its per-seed slowdowns versus RF
are 9.02%, 3.49%, 12.20%, 25.45%, 3.03%; versus the prior they are 1.32%, 9.31%, 4.28%,
5.67%, 10.13%. No compared pair selected the same configuration. The predeclared
5% practical-harm flag is triggered on three of five seeds against each control.
These are descriptive flags, not significance tests or validated router thresholds.
Median within-incumbent confirmation CV is 2.405%; there are only three repeats
per incumbent, and some ranges overlap. No true-latency dominance is established.

The cheap prior orders unused vectors by descending cache capacity, ascending
block size, then ascending restart interval. It uses no acquired outcomes to pick
the next vector; like other arms it uses acquired outcomes to select the final
incumbent. Its design was disclosed as exploratory after V71 exposure.

![Paired medians and ranges](../results/v72_rocksdb_analysis/paired_incumbents.png)

## What this says about routing

The frozen RF-versus-LLM hindsight oracle chooses RF on all five cases and has
exactly the same observed mean as never escalating. A separately labeled post-hoc
diagnostic enumerated all 32 binary escalation masks. All 31 masks that call the
LLM on any seed have worse observed mean quality than never escalating. The
fixed-rate random-mask expectations and hindsight best/worst values are retained
in `results/v72_routing_diagnostic/`; they are neither a trained controller nor
an independent held-out evaluation. No uncertainty threshold or benefit model
was fitted to these outcomes. On the observed medians there is no positive LLM
headroom for a router to select, even with hindsight.

This is useful evidence against the current mechanism on this workload, but
does not establish that escalation never helps, that larger models would fail,
or that a general benefit-aware controller has been evaluated adequately.

## Actual collection cost versus deployment estimates

Actual collection took 167.531 seconds, including 0.761 seconds of server startup.
It used 150 NEW physical evaluations (105 search, 45 confirmation) and reused 50
historical shared-prefix evaluations. The fifteen logical 20-evaluation arms
account for 300 charges;300 is not the number of newly executed physical calls.
The new trials performed 15 million timed verified reads, 1.5 million warmup reads,
9,830,400 load writes and 19,660,800 records checked in full scans.

The 35 real requests consumed 303 observed generated tokens and 17,435 observed
input tokens, with no missing usage. Completion transport time was 39.410 seconds.
Total measured selection time was 39.610 seconds for LLM, 0.999 seconds for RF and
0.00327 seconds for the prior. The LLM added about 7.722 seconds of selection time
per seed over RF, excluding startup and physical objective acquisition. These
are observed local decision costs, not a production deployment estimate.

For a hypothetical policy replay, count only its selected branch's measured
selection time, plus its prefix, objective acquisitions, confirmations, controller
and explicitly amortized startup. The diagnostic records only the first term;
it must not be mistaken for total deployment cost. Physical worker wall time
across all collected branches was 125.473 seconds. Peak sampled server RSS was
2,552,774,656 bytes and peak sampled worker RSS 325,746,688 bytes; neither is a
hard memory cap or necessarily a simultaneous total. The owned server exited 0.

No downloads or external spending occurred. Hardware, electricity and human/
agent costs remain unknown. The 35-call allowance is fully consumed; no further
inference was run. Cumulative historical model requests are now 2016. Persistent
download allowance remains 568,438,763 bytes under the existing 5 GiB cap.

## Evidence, verification and limits

- Raw per-request prompts, token IDs, grammar, parameters, responses and decisions:
  `results/v72_rocksdb_paired/v72_seed*_step*/`.
- All physical charges, case states, phase receipts, active engine logs, attached
  cache checks and hashed DB inventories: `results/v72_rocksdb_paired/`.
- Frozen descriptive JSON/CSV and visually checked PNG/SVG:
  `results/v72_rocksdb_analysis/`.
- Approval, resource ledger, verification and test logs:
  `artifacts/study_v72_execution/`.

The read-only verifier replayed 105 search decisions, 35 model responses and 45
confirmation charges; it verified all 150 physical trials and inclusive budgets.
All 524 tests passed in 3.75 seconds after collection. Synthetic fixtures remain
separate from measured results. The first launch failed at the sandbox `ps`
permission preflight, before creating results or making any calls; the authorized
escalated launch ran once. No experiment was silently retried.

This is one development software family and one fixed generated, scaled,
YCSB-C-inspired workload. Five seeds are not five independent systems. The 512
vectors are nominal settings; the 400-effective-configuration criterion remains
unmet. This batch touched 61 distinct new-arm vectors, not 150 distinct settings.
It reuses prefixes measured without model residency, whereas all new continuations
share residency. Timing still includes Python verification overhead and is exposed
to OS cache, thermal effects and sequential-order noise. Full SST data were hashed
then removed by the unchanged worker; logs and metadata are retained, not complete
physical snapshots. Clean-machine reproduction of the latest full collection is
unexecuted. There is no new unseen-system/router-generalization evidence.

## Decision and next experiment

Close this fixed RocksDB batch with its negative finding. Do not search seeds,
prompts, settings or models on these outcomes until a favorable score appears.
The highest-priority next research step is a prospectively selected cross-system
replication using this now working legal-vector interface, with independently
admitted software families and the same cheap-control discipline. Selection must
use provenance/schema/domain criteria, not observed LLM benefit. Freeze the system
split, precision target and resources before acquiring paired outcomes. Only then
can development-only benefit prediction and unseen-system policy comparisons be
meaningful. This result alone does not establish Q2-paper readiness.
