# STATUS — V88 real-data DuckDB feasibility completed

## Resume here

Latest request: keep working toward concrete Q2-paper evidence. Completed V88 on a CC0 real-flight workload instead of waiting for TPC terms. **9/9 actual classical trials passed correctness; all 513 query answers matched an independent Python reference.** Four threads had 47.54% lower median measured time, but repeat spread 20.1075% narrowly failed the frozen 20% stability screen. Do not round this into a pass. No additional repeats or model calls were made. Report: `reports/flights_v88.md`. V87 generator/EULA remains unused and unapproved; it is no longer a blocker to the chosen alternative.

This is measurement feasibility, not a new LLM result or Q2-ready research claim. Principal paper-level candidate remains V86's scoped negative finding about cheap controls removing apparent LLM opportunity. **Next scientific action: prospectively freeze a broader classical DuckDB comparison against the four-thread default, with a precision plan, before requesting any additional inference.** Preserve V88 as exposed development evidence. Do not repeatedly add trials until a desired finding appears.

## Executed V88 evidence

- Data: nycflights13 Python port 0.0.3, CC0; 336,776 real flights and three metadata tables. Original archive and normalized-data hashes saved. No package/setup code executed.
- Independent Python CSV aggregation and SQLite synthetic fixtures validate three custom queries. Installed MIT DuckDB 1.4.4, no extensions.
- Setup: 2.476 seconds, zero objective acquisitions. Frozen code/data/runtime/expected answers: `reports/protocol_v88.freeze.json`.
- Collection: 9 physical trials (3 settings ×3 repeats), 7.314 seconds; 513 checked queries, 432 scored. 0 failed, 0 unattempted, 0 model calls. Maximum sampled trial RSS 77,053,952 bytes. Raw: `results/v88_flights_feasibility/`.
- Objective median seconds: one thread 0.349605; four threads 0.183413; join-order-off 0.332941. Range/median: 11.58%,20.11%,14.12%. Not confidence intervals or optimization improvements.
- Validated summary and figures: `results/v88_flights_analysis/`. Source-answer replay recomputes from original CSV and passes.
- Commands actually run: `scripts/fetch_flights_v88.py`, `scripts/extract_flights_v88.py`, `scripts/run_flights_v88.py prepare`, `freeze`, `run`, `scripts/analyze_flights_v88.py`, `scripts/report_flights_v88.py`, all with `.venv/bin/python`; full tests `.venv/bin/python -m pytest -q tests`.
- Infrastructure: initial zero-byte DNS failure and process-monitor sandbox rejection occurred before scientific execution; exact allowed commands succeeded after execution approval. No scientific failure was retried. Matplotlib used a temporary cache after the default cache was unwritable; figure was produced and inspected.

## Limits and costs

V88 uses all 9 of its native charges; stop this frozen batch here. Added downloads 8,719,722 bytes. Cumulative 4,839,950,365 bytes; **528,758,755 remain under 5 GiB**. Actual external spend USD0; electricity/hardware unknown. Native collection and download costs are separate from warm query timings. No modeled LLM deployment cost from V88.

Historical totals remain 2,191 real model requests, H2 299 physical (298 valid,1 failure;8 historical unattempted), Kanzi1,265, RocksDB350,26,358 recorded-table acquisitions. Add DuckDB9 separately. Prior model allowances are exhausted; no new inference is authorized by V88. No cloud/credentials/remote publish/push/contact. No experiment left running.

## Existing paper candidate and missing evidence

V86 enumerated 65,664 hindsight choices across25cases in3exposed families. Against cheap controls, no choice improves observed RocksDB/Kanzi quality; H2 maximum hindsight mean gain0.262%, adverse repeat scenario0%. No case meets its original practical margin. H2 prior is a standalone3-trial control, not paired continuation. These are scoped negative results, not universal LLM failure or a learned-router evaluation. Report `reports/frontier_v86.md`; portable saved-summary replay `output/frontier_v86_1_reproduction.zip` SHA256881677dc7d696cca352ba52fb3ae7e82780c52f391c0c3f6789eceede954c9b2. It does not replay native/model execution.

Missing: useful benefit variation beyond strong cheap controls, stronger-model robustness, independent untouched system groups, clean-machine native replication, a meaningful grouped controller evaluation. V88 only establishes a real-data correctness and timing harness; it adds no model evidence. Broad research objective is not complete.

## Integrity and tests

Exact prior root files retained in `artifacts/study_v88/previous_snapshot/`. V87 and all older frozen sources/manifests are immutable. Current integrity entrypoint: `.venv/bin/python scripts/seal_flights_v88.py --verify-only`. **653 tests passed in21.23seconds** (14 new cases). Full test count and run timing are recorded in `artifacts/study_v88/tests_all.log` and the report; run `pytest ... tests` explicitly to include root-level tests omitted by configured default testpaths. Do not confuse that subset with historical full-suite counts.
