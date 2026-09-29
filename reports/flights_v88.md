# V88: real-flight DuckDB feasibility result

Nine of nine prospectively specified classical trials completed. All 513 checked query executions exactly matched an independent Python reference built from 336,776 real flight records. Four threads had a 47.54% lower median query time than one thread. However, its range/median was 20.1075%, narrowly above the frozen 20% screen. We retain that failure; no threshold adjustment or extra repetitions were made.

| Setting | Three observed objective times (seconds) | Median (seconds) | Range/median | Frozen screen |
|---|---|---:|---:|---|
| One thread | 0.349605, 0.328653, 0.369126 | 0.349605 | 11.58% | Pass |
| Four threads | 0.205447, 0.183413, 0.168567 | 0.183413 | 20.11% | Fail |
| One thread, join-order optimizer disabled | 0.332941, 0.319478, 0.366499 | 0.332941 | 14.12% | Pass |

Each objective is the sum of execute-and-fetch time for 16 repetitions of three queries after three warmup suites. Exact answer checking and JSON writes are outside this objective; whole-process collection costs include them. The four-thread measurement was lower than either one-thread configuration in every repetition block, but these three repeats on one host are not an inferential test or a general speedup guarantee. The selected settings are only three configurations, not a budgeted optimizer comparison. The stability screen is a coarse engineering rule, not a confidence interval.

## Source audit and implementation

The [original nycflights13 project](https://nycflights13.tidyverse.org/) documents real 2013 NYC flights and related airline, aircraft and airport data under CC0. This experiment uses Michael Chow's [Python port, release 0.0.3](https://pypi.org/project/nycflights13/0.0.3/), whose registry metadata also declares CC0. Port/archive SHA256: `d9ef2f5cf1bebca7e30b4daf69dcd7a8fd71f25b7196f5dc489879ad7e3e8a37`. We do not claim byte equivalence to the current R release. Only allowlisted CSV/metadata members were extracted; downloaded package/setup code was never installed or executed. Registry receipts, original CSVs and transformation hashes are retained.

The queries are custom analytical workloads, not author benchmark queries: monthly carrier counts/positive arrival delay, high-altitude destination routes, and delayed summer flights by older-aircraft manufacturer. Missing arrival delay is explicitly counted as missing, not called a cancellation. Four tables contain 336,776 flights, 16 airlines, 1,458 airports and 3,322 aircraft. Only needed columns are normalized, with exact integer parsing and preserved nulls. Python dictionary aggregation computes expected results without executing the objective SQL. Hand-computable fixtures cross-check both that reference and the SQL in SQLite. After collection, the Python reference was recomputed from original CSVs and exactly reproduced every expected answer.

DuckDB 1.4.4 is the already pinned MIT runtime from V87. The TPC generator, extension and its unapproved EULA were not used. This is a versioned alternative to V87, not permission to execute that stage. No new model adapter, dependency or service was installed. This custom workload is now exposed development data, not an untouched evaluation family.

## Design and integrity

`reports/protocol_v88.md` specifies limits, queries, configuration contrasts, repetition order, metrics and the stability rule. `reports/protocol_v88.freeze.json` hashes protocol, runner/analyzer, tests, independent reference, expected answers, data and runtime before the first measured query. Setup acquired zero objective labels. The Latin order was 1-thread/4-thread/join-off, 4-thread/join-off/1-thread, then join-off/1-thread/4-thread. Configuration settings are read back; autoload, autoinstall and external access are disabled during trials. A charge is recorded before each process. Failures and unattempted trials remain in the denominator (both zero here).

All nine acquisitions include warmups and repeat checks: 513 total query executions, 432 scored. Repeats are internal to nine physical configuration trials, not 513 independent optimization acquisitions. There were no hidden timing probes, LLM calls, retries or post-result reruns. The watchdog samples process memory and scratch; it is not a hard operating-system memory reservation. Frozen limits: 60 seconds/trial, 900 seconds/stage, 512 MiB DuckDB memory, 2 GiB sampled RSS, 1 GiB scratch.

## Actual collection cost versus deployment estimates

Actual setup wall time: 2.476 seconds; native collection: 7.314 seconds; peak sampled trial RSS: 77,053,952 bytes. This excludes source retrieval, test execution and analysis from the native collection subtotal. Download receipts separately record 8,719,722 new bytes (including registry metadata), bringing cumulative recorded downloads to 4,839,950,365 bytes; 528,758,755 bytes remain below 5 GiB. A zero-byte sandbox DNS failure and pre-setup process-monitor permission rejection are retained as infrastructure events; neither ran an objective. Spend is USD0; electricity and hardware costs are unknown. Local file sizes are not network costs.

Median query times above describe warm local execution under this workload, not an end-to-end deployment estimate. No LLM deployment cost or savings estimate can be made from this stage. Historical real-model requests remain 2,191; their prior allowances are consumed. Existing H2/Kanzi/RocksDB counts are unchanged; add nine DuckDB physical trials separately.

## What this contributes, and what remains missing

This supplies a working, reproducible real-data SQL workload with exact independent correctness checks and visible configuration sensitivity. It is a concrete infrastructure and measurement result. It does **not** establish LLM opportunity, a useful router, fair 10+10 continuations, reliability at production scale, or Q2 publication readiness. A cheap thread-count rule may explain all observed gains. The small in-memory data and repeated warm queries may favor parallelism differently from larger or concurrent deployments. The four-thread times trend down across blocks; host drift/cache state is a plausible but untested explanation, not a measured cause. Do not compare these timings across machines as if hardware were fixed.

The prior V86 negative result remains the principal paper-level empirical candidate: strong cheap controls eliminate the observed material small-model opportunity across the selected RocksDB/Kanzi/H2 cases. V88 is not an additional LLM family supporting that result.

**Next scientific action:** freeze a broader, semantically justified DuckDB classical comparison against the four-thread default before allocating model calls. Include all correctness-checked queries, independent configuration repeats and realistic resource settings; explicitly handle measurement precision. Choose dimensions from documented semantics before inspecting new results, retain all settings even if cheap controls win, and define the budget and practical margin prospectively. Any subsequent LLM claim still needs newly authorized inference, paired frozen prefixes, independent software groups and a meaningful untouched evaluation. Extra seeds of this exposed workload cannot replace those groups.

## Reproduction and evidence

- Raw charges, processes, settings, plans, exact answers and timings: `results/v88_flights_feasibility/`.
- Rechecked summaries, query breakdown and figures: `results/v88_flights_analysis/`.
- Source/download, extraction, preparation and dataset manifests: `artifacts/sources/v88/`, `artifacts/study_v88/`.
- Saved-source replay/figure regeneration: `.venv/bin/python scripts/report_flights_v88.py`. It performs no database/model calls. Summary recomputation: `scripts/analyze_flights_v88.py` requires an absent destination directory; preserve current results and use a clean copy rather than overwrite historical outputs.
- Native reproduction requires a fresh isolated checkout/copy and the pinned runtime/data. `scripts/run_flights_v88.py prepare`, `freeze`, `run` are deliberately one-shot and refuse to overwrite existing scientific records. Local absolute commands in receipts describe this machine. This is not yet a clean-machine native replication or portable end-to-end bundle.
- **653 tests passed in21.23seconds**, including14new synthetic cases. Full test evidence: `artifacts/study_v88/tests_all.log`; synthetic fixtures remain in `tests/` and outside research aggregates.

![Three-setting feasibility](../results/v88_flights_analysis/feasibility.png)
