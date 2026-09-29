# V79: cheap preset control on new compression workloads

This is a prospective classical-only follow-up to the exposed V78 result. It compares a V78-informed owner-preset/block strategy with RF on three complete Silesia files. **No LLM was run on these inputs**, so this study cannot establish that the preset matches an unmeasured LLM continuation or that an escalation controller would improve.

## Actual collection and scope

All 450 physical trials completed, with zero failures or retries, across 15 workload/seed pairs. Each of 30 arms used 20 logical labels: ten shared prefix acquisitions, seven arm-specific searches and three charged confirmations. Actual collection totals 150 prefix + 210 continuation-search + 90 confirmation = 450 physical trials, while logical per-arm accounting totals 600. All 90 confirmation byte counts agree within their own three-repeat sets.

The protocol and code were frozen before collection. Inputs were selected by content category and size before any new Kanzi outcome; the preset itself was deliberately informed by V78. No settings or stopping criteria changed after outcomes. All workloads remain ONE Kanzi development group, not three software systems. Seeds are repeated searches, not independent groups. Runtime is the documented V76 buffer-fix adaptation; no model was resident.

## Confirmed sizes

Lower is better. Each case uses the median of three charged confirmations; means average the five fixed seeds within each workload. Percentage savings is (meanRF−meanPreset)/meanRF.

| Workload | RF mean bytes | Preset mean bytes | Preset savings | Wins/ties/losses |
|---|---:|---:|---:|---|
| dickens | 2,429,511.8 | 2,377,944.0 | +2.12% | 2/3/0 |
| sao | 4,704,659.6 | 4,681,324.0 | +0.50% | 3/1/1 |
| xml | 390,815.4 | 388,529.0 | +0.59% | 2/2/1 |

All cases, including losses:

| Workload | Seed | RF bytes | Preset bytes | Preset savings |
|---|---:|---:|---:|---:|
| dickens | 11 | 2,377,944 | 2,377,944 | +0.00% |
| dickens | 23 | 2,377,944 | 2,377,944 | +0.00% |
| dickens | 37 | 2,582,439 | 2,377,944 | +7.92% |
| dickens | 53 | 2,377,944 | 2,377,944 | +0.00% |
| dickens | 71 | 2,431,288 | 2,377,944 | +2.19% |
| sao | 11 | 4,681,324 | 4,681,324 | +0.00% |
| sao | 23 | 4,634,852 | 4,681,324 | -1.00% |
| sao | 37 | 4,779,056 | 4,681,324 | +2.05% |
| sao | 53 | 4,726,201 | 4,681,324 | +0.95% |
| sao | 71 | 4,701,865 | 4,681,324 | +0.44% |
| xml | 11 | 389,477 | 388,529 | +0.24% |
| xml | 23 | 388,529 | 388,529 | +0.00% |
| xml | 37 | 413,785 | 388,529 | +6.10% |
| xml | 53 | 388,529 | 388,529 | +0.00% |
| xml | 71 | 373,757 | 388,529 | -3.95% |

![Paired classical outcomes](../results/v79_kanzi_analysis/classical.png)

## Interpretation boundaries

A cheap preset sweep can test an alternative explanation for prior model-selected settings. Its performance here is measured prospectively on the selected new inputs, but its design is development-informed and the software family remains exposed. No outcome has been substituted for an LLM response. There is no held-out router fit, significance claim, cross-system inference, or pooled comparison of unlike objectives. A loss is retained exactly like a win. No new corpus or seed will be selected merely to improve this table.

## Costs and provenance

Actual collection took 581.31 seconds, including 900 native application processes; summed process time was 569.57 seconds. Peak sampled JVM process-group RSS was 271,532,032 bytes. Total continuation decision time was RF 3.109329 seconds and preset 0.030859 seconds across 15 cases. Zero model calls, zero model downloads and zero external spending. Hardware/electricity costs are unknown.


Confirmed incumbent process times (mean of five seed medians, seconds; descriptive and host-dependent):

| Workload | RF compression | Preset compression | RF decompression | Preset decompression |
|---|---:|---:|---:|---:|
| dickens | 1.2289 | 0.9244 | 0.8866 | 0.4944 |
| sao | 1.2943 | 0.8944 | 1.2076 | 0.6946 |
| xml | 0.5570 | 0.4346 | 0.3601 | 0.2005 |

A small selector overhead does not imply a faster selected compressor. Size and native application time remain separate; no arbitrary scalar utility or amortization advantage is asserted.

Owner-hosted corpus retrieval added 8,181,238 bytes; raw sizes and published MD5 values were checked and SHA256 pins retained. Remaining total-download allowance is 553,914,019 bytes. No blanket redistribution license was established; raw corpus bytes remain in ignored `data/raw/`, outside shareable artifacts. See [workload audit](workload_audit_v79.md) for original-source attribution and caveats. The fixed [protocol](protocol_v79.md) records the owner-preset strategy, duplicate handling and failure/resource rules.

`deployment_estimates.json` separately counts the recorded prefix plus only one chosen continuation. It is retrospective branch accounting and excludes prefix-selection computation, other orchestration/I/O and future controller overhead. Actual collection included both continuations. These estimates are not V78 model-resident costs and not a dollar estimate.

## Checks and reproducibility

The frozen analyzer replays every acquired-only decision, shared prefix, arm order, 20-label budget, charge and selected incumbent; it checks saved headers/settings, checksums and byte-equality receipts. At collection, every valid compressed stream was decompressed and compared exactly. Successful bulky payloads were then removed under the frozen retention rule. Offline replay checks retained evidence, not deleted bytes anew. No failed observations were dropped. 590 tests passed before collection; synthetic tests are separate from measured outcomes. After V80 adapter preparation, the full suite passed 594 tests in 4.04 seconds; V80 inference remains unexecuted.

Raw logs: `results/v79_kanzi_classical/`. Verified JSON, CSV and figures: `results/v79_kanzi_analysis/`. Costs, sources, snapshots and evidence manifest: `artifacts/study_v79/`.

Executed collector: `.venv/bin/python scripts/run_kanzi_v79.py`. Analysis/report: `.venv/bin/python scripts/analyze_kanzi_v79.py` and `.venv/bin/python scripts/report_kanzi_v79.py`. Run analysis regeneration only in a separate copy after sealing. Current read-only history verification: `.venv/bin/python scripts/seal_evidence_v79.py --verify-only`. A fresh collection needs a new output namespace and prospectively bounded scope. No current model process or background experiment remains.

Limitations: three historical public files, one patched software family, one machine, deterministic size objective, sampled resource monitoring, no independent-family holdout or clean-machine V79 rerun. Additional workload diversity is not a substitute for independent software systems. Journal readiness and broad beneficial escalation remain unestablished.
