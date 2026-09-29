# Live measurement feasibility: 288 verified physical trials

A new local collector completed **288/288 physical compression trials**: 32 configurations each for Zstandard, LZ4 and zlib, with three observations per setting. Every actual compressed output decoded exactly to the original input. No trial failed, timed out or disappeared. This is a successful measurement-feasibility result; it does not establish useful LLM selection or generalization.

The input was a 901,120-byte deterministic archive of three unmodified [CPython v3.10.13 source files](https://github.com/python/cpython/tree/49965601d6afedafe47cc85556d99b7a24981051), with their original license and hashes retained. It is real source-code data, but only one small workload. All three compressor families are designated development/exposed for future studies; they are not new untouched test groups after this work.

## What was measured

| Implementation | Settings × trials | Successful exact roundtrips | Median within-setting timing CV | Settings above 10% CV | Distinct saved outputs |
|---|---:|---:|---:|---:|---:|
| Zstandard CLI 1.5.7 | 32 × 3 | 96 | 1.64% | 1 | 32 |
| LZ4 CLI 1.10.0 | 32 × 3 | 96 | 1.48% | 0 | 20 |
| Python zlib 1.2.12 | 32 × 3 | 96 | 1.13% | 0 | 24 |

Timing CV is sample standard deviation divided by the mean of three compression timings. The 10% flag was fixed before collection and is only descriptive. Three observations cannot establish dependable uncertainty estimates. All settings remain in the results, including the Zstandard setting with 10.70% CV.

Some nominal settings produce identical output on this input. In particular, block sizes exceeding much of the small archive need not create distinct LZ4 outputs. Identical output is not proof of identical internal work or timing; these settings were not removed after observation.

Configuration axes were fixed before measurement: Zstandard level/window/checksum, LZ4 level/block size/block dependence, and zlib level/memory/strategy. Local version/help output, exact binary/extension/library hashes and workload construction are recorded in `artifacts/study_v15/`. The window parameter is documented in the [Zstandard 1.5.7 owner manual](https://github.com/facebook/zstd/blob/v1.5.7/programs/zstd.1.md); the zlib options follow its [Python API](https://docs.python.org/3.10/library/zlib.html). No new compressor was installed.

For Zstandard/LZ4, timing includes CLI startup and pipe handling. For zlib, it measures the Python API operation. Therefore raw timing across families is not a controlled implementation comparison. Each physical observation ran in a fresh worker, and the three rounds were shuffled with a fixed seed. No free warmups or retries were used. The parent enforced a whole-process-group timeout and retained the actual compressed artifact from every trial.

## Actual costs and verification

Each physical repetition is one charged runtime/size/correctness vector: **288 new physical-vector attempts**, separately identified from prior recorded-table lookups. Collection took **13.5987 seconds** in the persistent experiment ledger; worker elapsed times sum to 13.2943 seconds. Analysis/rendering also consumed the existing allowance. Model requests and external spending remained zero for this stage.

The executed worker checked byte-for-byte decoded equality. Offline verification reconstructed the schedule and checked every charge, source identity, saved compressed payload hash/size and recorded equality result. It did not rerun the compressors or pretend that a hash check is a second physical replication. Completed collector invocation was tested: it reused the completed dataset with no extra trials.

The pre-collection test suite caught a trial-ID scheduling error, which was fixed before the protocol freeze or first physical measurement. It is recorded in `artifacts/study_v15/pre_freeze_test_note.json`. The first figure render used a temporary font cache after a sandbox cache warning; it completed successfully and its time was charged. The presentation-only rerender uses the project cache. Neither event altered measured outcomes.

**113 tests passed at this stage**; the subsequent paired-control stage brings the suite to **116**. No upstream source code from the workload was executed, and no system settings were changed.

## Reproduce and inspect

- Raw actual observations: `results/v15_measurements/trials.jsonl`.
- Durable charges and fixed denominator: `acquisitions.jsonl`, `schedule.json`, `progress.json`, `complete.json` in the same directory.
- Per-setting summaries: `configuration_summary.csv`, `summary.json`.
- Actual compressed bytes: `artifacts/sources/live_v15/outputs/` (Git ignored); every path/digest is in the raw observation.
- Frozen protocol/code/inputs: `reports/protocol_v15_live.md` and `.freeze.json`.
- Worker/environment/workload provenance and logs: `artifacts/study_v15/`.
- Features and development-family exposure: `data/live_manifest_v15.json`.

```sh
.venv/bin/python scripts/render_live_v15.py
PYTHONPATH=src .venv/bin/python -m pytest -q
```

Rendering reads saved numerical evidence and charges computation time; it does not acquire labels or make model calls. The collector preserves completed outputs and refuses automatic recovery of incomplete transactions. A fresh physical replication requires a separate output namespace and resource accounting; do not delete evidence to bypass that guard.

![Within-setting timing variability](../results/v15_measurements/timing_variability.png)

The next check was completed in the same continuation: [paired classical controls on these recorded medians](classical_controls_v16.md). Their limited remaining headroom matters more to LLM escalation than the successful measurement infrastructure alone.
