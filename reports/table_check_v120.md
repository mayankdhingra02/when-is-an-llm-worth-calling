# V120: exploratory constrained-adapter WordCount check

This experiment evaluates selection of the original authors' published latency labels, not independently validated execution time or output correctness. It is a separate table-only scope; stronger V52 admission stays closed. Five fixed optimization seeds are repetitions of one Storm family, not five independent systems.

This follow-up was chosen after all five V119 answers failed the format contract. It reuses the V91 grammar-constrained greedy adapter and the same prefixes, controls and frozen router masks. The table is now exposed: this is exploratory, not a new held-out test or an isolated causal estimate of grammar, because decoding/template handling also differ. No threshold was refit. Existing source/metric limitations remain.

| Classical control | Mean relative LLM gain | Wins / ties / losses | Valid gains ≥5% |
|---|---:|---:|---:|
| batch_3nn | 8.070% | 3 / 1 / 1 | 3/5 |
| full_sequential_3nn | 7.597% | 2 / 1 / 2 | 2/5 |
| random_full | 12.587% | 4 / 1 / 0 | 3/5 |
| single_portfolio | 8.081% | 3 / 1 / 1 | 3/5 |

Valid joint ≥5% wins over both co-primary controls: **2/5**. The predeclared descriptive success criterion (positive mean against both and at least one joint win) is **met**. This is not a significance test or a journal-readiness criterion.

| Optimization seed | Published-label incumbent selected by LLM arm | Batch 3NN gain | Sequential 3NN gain |
|---|---:|---:|---:|
| 11 | 51.458 | 24.952% | 19.631% |
| 23 | 47.387 | 0.000% | 0.000% |
| 37 | 49.017 | 6.415% | 24.855% |
| 53 | 52.784 | 16.772% | -2.857% |
| 71 | 51.331 | -7.788% | -3.642% |

## Frozen controller transfer

The old V6 controller uses only prefix features and its original development-only preprocessing/thresholds. It was not retrained for this model or relative-gain metric; its transfer is a diagnostic, not calibrated benefit prediction. All policy rows, including development-rate random, matched-rate random and the non-deployable hindsight oracle, are saved in `comparison.json`.

| Policy | Escalations /5 | Mean gain vs batch | Mean gain vs sequential |
|---|---:|---:|---:|
| never | 0 | 0.000% | 0.000% |
| always | 5 | 8.070% | 7.597% |
| benefit | 0 | 0.000% | 0.000% |
| uncertainty | 0 | 0.000% | 0.000% |
| random_matched_benefit_diagnostic | 0 | 0.000% | 0.000% |
| random_development_benefit | 0 | 0.000% | 0.000% |
| random_matched_uncertainty_diagnostic | 0 | 0.000% | 0.000% |
| random_development_uncertainty | 0 | 0.000% | 0.000% |

## Actual collection and reproducibility

50 real local requests, 5 valid continuations and 0 fallbacks. Actual recorded acquisitions: 50 (50 new LLM/fallback; 250 shared-prefix/classical and 50 V119 fallback acquisitions are historical, not recollected); every logical branch remains B20. Replaying saved evidence adds no acquisition. Model lifecycle: 20.194s, peak sampled server RSS: 6,196,396,032 bytes; actual generated tokens: 50; reported prefill tokens: 3987. Missing response usage: 0. Startup/loading is retained separately in the raw ledger. Zero new downloads, paid calls or external spending.

A deployed policy would use the prefix and one selected branch. Per-policy model-request/token/runtime components are retrospective estimates, excluding loading and unmeasured native application costs. They are not cloud-dollar or end-to-end latency savings. Research collection used all branches and is reported separately.

Source and protocol: `data/manifest_v119.json`, `reports/protocol_v120.md`; raw prompts/responses: `results/v120_qwen/`; prefix/control journals: `results/v119_classical/`; model-arm journal and figures: `results/v120_analysis/`. The source table comes directly from the pinned owner ZIP; no derivative target-direction assumption is needed. Throughput was not parsed.

## Limits

Only one exposed table/family and one greedy constrained continuation per prefix. The archive does not supply original per-run correctness/failure records or an executed-code manifest; metric-substitution and measurement-duration questions remain. These labels are not fresh native measurements. Public benchmark pretraining contamination is unknown. No pooled confirmatory inference with previously exposed groups, no useful learned-router generalization assertion, and no guarantee of Q2 acceptance. All seeds, failures and controls remain visible regardless of direction.
