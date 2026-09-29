# V119: external WordCount recorded-table check

This experiment evaluates selection of the original authors' published latency labels, not independently validated execution time or output correctness. It is a separate table-only scope; stronger V52 admission stays closed. Five fixed optimization seeds are repetitions of one Storm family, not five independent systems.

The source, table, controls, inference settings, controller masks and analysis criterion were fixed before continuation outcomes. No model or threshold was selected using this table's results. Existing source/metric limitations remain.

| Classical control | Mean relative LLM gain | Wins / ties / losses | Valid gains ≥5% |
|---|---:|---:|---:|
| batch_3nn | 0.000% | 0 / 5 / 0 | 0/5 |
| full_sequential_3nn | -1.425% | 2 / 1 / 2 | 0/5 |
| random_full | 4.071% | 2 / 1 / 2 | 0/5 |
| single_portfolio | -0.250% | 2 / 2 / 1 | 0/5 |

Valid joint ≥5% wins over both co-primary controls: **0/5**. The predeclared descriptive success criterion (positive mean against both and at least one joint win) is **not met**. This is not a significance test or a journal-readiness criterion.

| Optimization seed | Published-label incumbent selected by LLM arm | Batch 3NN gain | Sequential 3NN gain |
|---|---:|---:|---:|
| 11 | 68.567 | 0.000% | -7.091% |
| 23 | 47.387 | 0.000% | 0.000% |
| 37 | 52.377 | 0.000% | 19.704% |
| 53 | 63.421 | 0.000% | -23.584% |
| 71 | 47.622 | 0.000% | 3.846% |

## Frozen controller transfer

The old V6 controller uses only prefix features and its original development-only preprocessing/thresholds. It was not retrained for this model or relative-gain metric; its transfer is a diagnostic, not calibrated benefit prediction. All policy rows, including development-rate random, matched-rate random and the non-deployable hindsight oracle, are saved in `comparison.json`.

| Policy | Escalations /5 | Mean gain vs batch | Mean gain vs sequential |
|---|---:|---:|---:|
| never | 0 | 0.000% | 0.000% |
| always | 5 | 0.000% | -1.425% |
| benefit | 0 | 0.000% | 0.000% |
| uncertainty | 0 | 0.000% | 0.000% |
| random_matched_benefit_diagnostic | 0 | 0.000% | 0.000% |
| random_development_benefit | 0 | 0.000% | 0.000% |
| random_matched_uncertainty_diagnostic | 0 | 0.000% | 0.000% |
| random_development_uncertainty | 0 | 0.000% | 0.000% |

## Actual collection and reproducibility

5 real local requests, 0 valid continuations and 5 fallbacks. Actual recorded acquisitions: 300 (50 shared-prefix +200 classical +50 LLM/fallback); every logical branch remains B20. Replaying saved evidence adds no acquisition. Model lifecycle: 32.480s, peak sampled server RSS: 5,921,718,272 bytes; actual generated tokens: 300; reported prefill tokens: 3897. Missing response usage: 0. Startup/loading is retained separately in the raw ledger. Zero new downloads, paid calls or external spending.

A deployed policy would use the prefix and one selected branch. Per-policy model-request/token/runtime components are retrospective estimates, excluding loading and unmeasured native application costs. They are not cloud-dollar or end-to-end latency savings. Research collection used all branches and is reported separately.

Source and protocol: `data/manifest_v119.json`, `reports/protocol_v119.md`; raw prompts/responses: `results/v119_reasoning/`; prefix/control journals: `results/v119_classical/`; model-arm journal and figures: `results/v119_analysis/`. The source table comes directly from the pinned owner ZIP; no derivative target-direction assumption is needed. Throughput was not parsed.

## Limits

Only one external table/family and one sampled answer per prefix. The archive does not supply original per-run correctness/failure records or an executed-code manifest; metric-substitution and measurement-duration questions remain. These labels are not fresh native measurements. Public benchmark pretraining contamination is unknown. No pooled confirmatory inference with previously exposed groups, no useful learned-router generalization assertion, and no guarantee of Q2 acceptance. All seeds, failures and controls remain visible regardless of direction.
