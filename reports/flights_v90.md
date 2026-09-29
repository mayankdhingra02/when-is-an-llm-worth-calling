# V89–V90: broader classical control screen

The complete V90 follow-up ran **60/60 valid physical trials**, covering12settings in five fixed randomized blocks. All12,060persisted query answers matched the independent reference. **No setting met the frozen requirement of at least10% improvement in every block plus the repeat-stability screen.** The best median within-block gain was1.64% for eight threads/defaultpasses, with losses in some blocks. This is descriptive failure to meet the screen, not statistical equivalence, evidence of universal lack of headroom, or an LLM result.

| Setting | Median seconds | Median block gain vs4-thread control | Range/median | Material in all5blocks |
|---|---:|---:|---:|---|
| t1_j0_f0 | 1.312960 | -109.36% | 41.37% | False |
| t1_j0_f1 | 1.485396 | -122.76% | 5.07% | False |
| t1_j1_f0 | 1.303210 | -94.40% | 16.52% | False |
| t2_j0_f0 | 0.918013 | -38.73% | 7.97% | False |
| t2_j0_f1 | 1.074773 | -62.26% | 29.53% | False |
| t2_j1_f0 | 0.901546 | -35.20% | 8.01% | False |
| t4_j0_f0 | 0.666805 | +0.00% | 25.24% | False |
| t4_j0_f1 | 0.732853 | -9.91% | 10.41% | False |
| t4_j1_f0 | 0.657516 | +0.64% | 28.74% | False |
| t8_j0_f0 | 0.642455 | +1.64% | 9.01% | False |
| t8_j0_f1 | 0.752172 | -14.95% | 8.14% | False |
| t8_j1_f0 | 0.685621 | -1.39% | 11.03% | False |

`t` denotes threads; `j1` disables join-order optimization, `f1` disables filter pushdown. All other optimizer passes retain defaults. The four-thread control itself has25.24% range/median, failing the20% stability screen. This limits timing conclusions; no equivalence or statistical significance is claimed. Static plan fingerprints reduce to3observed shapes across the12settings. Thread-count changes can affect execution without changing printed plans.

## Retained failure and exploratory domain change

V89 froze16settings: thread counts1,2,4,8 × independently disabling/enabling two optimizer passes, with five blocks. It stopped as specified on trial9: joint disabling at one thread hit the60second wall limit. Actual V89 denominator:9charged,8valid,1failed,71unattempted of80intended. The failed summer-query static plan contains CROSS_PRODUCT nodes. This is consistent with disabled transformation passes but does not prove the timeout mechanism. The worker buffered answers until successful completion, so partial completed-query counts inside the killed trial are unknown; no successful total is invented. Its full process time and failure charge are retained.

A collection mistake also occurred: the full test suite ran concurrently with part of V89. Log-file birth/last-write timestamps identify trial08(the timeout) as possibly overlapping. The8successful trials were outside that recorded interval, but this is an approximate bracket, not a precise process trace. No measurements were dropped or used as a complete grid. V89 therefore supplies a failure record, not a clean timing comparison. The V89 frozen complete-grid analyzer correctly cannot analyze it as complete; a separate post-failure audit rechecked all1,608persisted answers.

V90 is a prospectively frozen **exploratory correction after seeing that failure**: retain both single-pass contrasts, exclude simultaneous disabling, and run12settings ×5blocks. No tests/source fetches/figure generation ran alongside V90. Ordinary uncontrolled host background activity remains. It used60of the71unspent slots, preserving the original combined maximum80charges. Actual combined V89+V90charges69, below80;11remaining slots are not used to chase a finding. V89 unattempted71 remains unchanged rather than being rewritten as completed follow-up trials. Combined native collection138.337seconds, below900. No native trial was silently retried.

## Protocol, cost and reproducibility

Source, query semantics and CC0 data provenance inherit `reports/flights_v88.md`. Domain semantics were verified against [DuckDB configuration documentation](https://duckdb.org/docs/current/configuration/overview) and [exact1.4.4 optimizer source](https://raw.githubusercontent.com/duckdb/duckdb/v1.4.4/src/optimizer/optimizer.cpp). Current docs describe1.5; installed1.4.4 optimizer names were separately queried and retained before collection. We did not run downloaded source code or install an extension.

Both frozen protocols and hashes remain: `reports/protocol_v89.md`, `reports/protocol_v89.freeze.json`, `reports/protocol_v90.md`, `reports/protocol_v90.freeze.json`. Data/runtime pins are inherited fromV88 and checked before execution. Actual setting readbacks, exact answers, per-query times, static plans, charge-before-launch receipts and watchdog process logs are under `results/v89_flights_grid/` and `results/v90_flights_grid/`. Independent complete-grid checks and all-setting summaries are under `results/v90_flights_analysis/`; failure audit under `results/v89_flights_failure_audit/`.

V90 measured3warmup+64scored suites pertrial:201checked,192scored queries. Objective is execute+fetch sum, with exact validation and finalserialization excluded. UnlikeV88, JSON writes happen after the trial rather than between queries; timings are not pooled across versions. V90 actual collection68.035seconds, peak sampledRSS106,151,936bytes. V89 actual collection70.302seconds, including its killedtrial. The watchdog is a sampled safeguard, not hard memory enforcement. Model calls0, externalspendUSD0, retained new download payloads0; source web inspection is not a model/data-file download. Electricity/hardware costs remain unknown. Warm query timing is not an end-to-end deployment estimate.

Executed: `.venv/bin/python scripts/run_flights_v89.py freeze`, `run`(retained failure); `scripts/audit_flights_v89_failure.py`; `scripts/run_flights_v90.py freeze`, `run`; `scripts/analyze_flights_v90.py`; `scripts/report_flights_v90.py`. Shell process-monitor access required actual environment escalation before scientific execution. Re-run native stages only in a fresh isolated copy: runners deliberately reject existing result directories. The report script regenerates figures from summaries and makes no model/database requests. Current-machine verification is not clean-machine replication.

## Scientific decision

**Do not add LLM calls to this12-setting workload.** A20-evaluationbudget can enumerate the entire domain even before allocating a controller; the measured cheap default leaves little consistent observed opportunity and has unstable repeats. More seeds do not fix the domain size or create independent systems. The result narrows workload choice; it is not new evidence that an LLM never helps.

The paper-level candidate remains V86's scoped negative finding about strong cheap controls across existing native families. The next priority is a bounded larger-model robustness test on existing saved paired benchmarks, not more DuckDB microbenchmark tuning. An owner-pinned Qwen3-8B candidate and explicit resource proposal are in `reports/resources_v91.md`. Its5.03GBfile exceeds the remaining528,758,755downloadbytes and existing cumulative model cap. No model download or generation is authorized/executed by this report. Independent untouched evaluation, stronger native workload coverage and clean-machine replication still remain; journal readiness is not established.

![All-setting grid](../results/v90_flights_analysis/grid.png)

Full final suite: **672 passed in 20.71s**. NewV89/V90grid and V91permission fixtures remain synthetic; no model approval is created by a passing fixture.
