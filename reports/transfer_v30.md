# V30: the earlier nearest-neighbor advantage does not transfer uniformly

The unchanged sequential 3NN optimizer was tested prospectively on two software families with no prior acquisitions found in this repository. All 50 arms completed. Its primary comparison against static ranking is mixed: better on Opus, worse on Z3. The adaptive centroid shortlist comparator has better family averages on both families under both metrics. This is a concrete warning against treating V29's exposed-development result as a general advantage. It does not establish whether an LLM or learned escalation controller would help on these families.

## Admission and frozen design

The original source paper resolves two previously deferred objective descriptions: Opus encoding time and Z3 solving time. See Table 2, page 10, and sections 3.2–3.3 of Kaltenecker, Mühlbauer, Grebhahn, Siegmund and Apel, [Performance Evolution of Configurable Software Systems: An Empirical Study](https://www.se.cs.uni-saarland.de/publications/docs/KMG%2B23.pdf), [published DOI](https://doi.org/10.1007/s10664-023-10338-3). The [owner repository](https://github.com/ChristianKaltenecker/PerformanceEvolution_Website/tree/4ee53dad6b81543c444d44282053def0d82d97b3) identifies the measurements and feature models. The local dataset files were already pinned to that commit; no new dataset download occurred. Owner repository licensing is GPL-2.0; local measurement files remain Git ignored, with no additional redistribution rights asserted.

Use the existing V5 revision/workload filters: Opus 1.0.0, 6,480 rows; Z3 4.3.2, LRA workload, 256 rows. The feature-only admission checked schemas, feature models and 43 historical result journals before acquiring targets. Both families were absent from those acquisition/model records. This is project-local exposure evidence, not proof against public-data or model-pretraining exposure. OpenVPN remains excluded: its case README says throughput while the paper uses a generic response-time description. FastDownward remains quarantined. These single-target tasks do not meet the separate V13 runtime/size/correctness contract.

The [protocol](protocol_v30_transfer.md) and [87 input references](protocol_v30_transfer.freeze.json) were frozen at 2026-09-25 04:45:44.666820 UTC, before the first acquisition at 04:45:45.136590 UTC. Five seeds (11, 23, 37, 53, 71) per family generated ten new prefixes. Every branch reused its case's saved ten-label prefix and acquired ten more labels. The five methods were full-space centroid, static shortlist rank, adaptive shortlist centroid, batch 3NN and sequential 3NN. The 20-row shortlist and nominal-distance k=3 implementation were unchanged; no parameter search or outcome-based family selection was performed. All variants and seeds remain grouped with their software family.

## Actual result

Mean normalized terminal loss, lower is better. Full-table extrema were available only to the post-collection evaluator.

| Family | Full centroid | Static rank | Shortlist centroid | Batch 3NN | Sequential 3NN |
|---|---:|---:|---:|---:|---:|
| Opus | 0.00655820 | 0.00938107 | 0.00354392 | 0.00936063 | 0.00508451 |
| Z3 | 0.04105012 | 0.01002387 | 0.01002387 | 0.01097852 | 0.03914081 |
| Equal-family mean | 0.02380416 | 0.00970247 | 0.00678389 | 0.01016957 | 0.02211266 |

Each gain below is comparator minus sequential 3NN; positive favors sequential 3NN. Relative gain divides the target difference by the comparator's target, calculated per case before equal-family averaging. Percentages are recorded target changes, not measured deployment speedups.

| Comparator | Equal-family normalized gain | Equal-family relative gain | Wins / ties / losses, 10 cases |
|---|---:|---:|---:|
| Full centroid | +0.00169150 | +1.08908% | 5 / 3 / 2 |
| **Static rank (primary)** | **−0.01241019** | **+5.89952%** | **4 / 3 / 3** |
| Shortlist centroid | −0.01532877 | −3.13590% | 1 / 5 / 4 |
| Batch 3NN | −0.01194309 | +5.88999% | 3 / 5 / 2 |

Against static ranking, Opus's average relative gain is +12.33382%, Z3's is −0.53478%. Their normalized gains are +0.00429656 and −0.02911695 respectively. The overall normalized and relative metrics disagree, so neither supports an unqualified success claim. Against shortlist centroid, sequential 3NN loses on both metrics in each family. Sequential feedback also harms two cases relative to batch 3NN, unlike the earlier V29 sample. All harms and ties remain in the denominator.

![Mean normalized loss by family](../results/v30_transfer/comparison.png)

Panel scales differ and are labeled. The figure was visually inspected. All individual scores and gains are retained in [cases.csv](../results/v30_transfer/cases.csv), [paired_gains.csv](../results/v30_transfer/paired_gains.csv) and [summary.json](../results/v30_transfer/summary.json).

## Execution, costs and verification

Actual collection: 100 fresh prefix labels plus 500 branch labels = **600 charged acquisitions**, including overlapping rows acquired independently by different branches. All 50 arms completed at 20 unique evaluations each, with the same ten-label prefix within each case. There were no run failures, omitted cases, retries or new model calls. These are accesses to recorded measurements, not new physical software executions. Historical recorded acquisitions now total 8,108; physical trials remain 1,134.

Logical evaluations across all arms total 1,000 because shared prefixes are counted in each arm's budget. Hypothetical deployment of one method over these ten cases would use 200 objective evaluations and zero model requests; it would not incur all paired research-collection costs. Runtime for collection was 4.758256 seconds and analysis/figure generation 2.520081 seconds, totaling **7.278337 seconds**. The global ledger is 2,265.613030 / 3,600 seconds, with 1,334.386970 seconds remaining and no active session. Read-only validation, test and preparation time are separate from that experimental runtime convention.

The author-hosted PDF added 3,971,352 downloaded bytes; the successful transfer took 2.665940 seconds. Its initial sandbox DNS attempt failed before receiving payload; the platform-approved retry succeeded. The download ledger now contains 4,518,268,306 total accounted bytes and 4,098,574,535 model bytes. No model weights were downloaded. External spend remains USD 0. Follow-up model allowance remains exhausted at 200/200 requests (300 including the initial stage).

Validation evidence under [artifacts/study_v30](../artifacts/study_v30/):

- **211 tests passed in 1.34 seconds**, including synthetic budget/state-isolation tests separated from research results.
- Independent acquired-only replay reproduced all ten prefixes, 50 arms, 600 decisions/source acquisitions, shortlist membership and 3NN neighbor/prediction traces.
- A separate standard-library Decimal verifier checked 1,000 source labels including shared prefixes, 80 paired metrics, 16 family gains, eight aggregate gains, 12 win/tie/loss counts, ten family losses and five aggregate losses. It also checked freeze-before-acquisition and prefix-before-branch timestamps.
- All 2,086 historical/current frozen input references passed, together with the original smoke, grouped split, router seal and policy-denominator checks.
- The original historical audit initially rejected the changed download ledger. The new narrowly scoped wrapper checks the exact archived original ledger identity plus the current append-only single-paper byte delta. No scientific input or old audit was changed. The failure and resolution are retained in `verification_attempts.json`.

Executed commands (collection/analysis refuse existing completed outputs):

```sh
.venv/bin/python scripts/fetch_source_v30.py
pdftotext -f 10 -l 13 -layout artifacts/sources/v30/performance_evolution_author.pdf artifacts/study_v30/source_sections.txt
.venv/bin/python scripts/admit_transfer_v30.py
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/run_transfer_v30.py
.venv/bin/python scripts/analyze_transfer_v30.py
.venv/bin/python scripts/analyze_transfer_v30.py --verify-only
.venv/bin/python scripts/verify_transfer_v30.py
.venv/bin/python scripts/audit_history_v30.py
```

Raw evidence includes `results/v30_transfer/acquisitions.jsonl`, `prefixes/`, `arms/`, `checkpoints/` and `progress.json`. Python and dependency pins remain unchanged. The V26 standalone ZIP remains an unchanged V25 reconstruction snapshot; it does not contain V30.

## Limits and prioritized next experiment

Two independent families support a descriptive transfer check, not a powered generalization test. Repeated seeds are not independent systems. The method was motivated by earlier exposed outcomes, although these new families were selected and frozen before acquisition. Both families are now exposed and must not be reused as untouched holdouts. Absolute target units and repetition-level uncertainty are not established. Opus configurations change bitrate, channels and sampling rate, so faster recorded encoding need not preserve audio quality. There is no new LLM comparison, reliability measurement or controller validation here; none can be inferred from classical scores.

1. **Freeze a prospective LLM-versus-strong-classical protocol on additional untouched families with an explicit application-quality constraint.** Retain static ranking and adaptive shortlist centroid alongside fixed 3NN, and specify utility/aggregation before outcomes. This is the single most important next action.
2. Admit enough independent families to separate development and evaluation credibly, preserving all variants/seeds within groups. If that is infeasible, label the work descriptive and avoid fitting a claimed general-purpose router.
3. Execute paired real local-model continuations only under a new explicit bounded inference allowance or a compatible provenance-checked public cache. The current allowance is exhausted. Preserve current negative/mixed results and do not tune toward a positive result on these families.
