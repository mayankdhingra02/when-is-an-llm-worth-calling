# V51 — faster measurement interface, no recovered escalation opportunity

Completed 2026-09-25. Continued beyond the V50 utility audit into a new, frozen,
actually executed physical experiment. **960/960 fresh compression trials passed
exact decompression and required frame checks.** No failures, retries, dropped
outliers, model calls or spending. Five paired repetitions for every one of 48
settings in each of Zstandard and LZ4, through both their CLI and native library.

The native API is faster on this small workload, but it does not provide a harder
optimization task. Cheap search reached the best recorded size-feasible native
API setting in all ten cases (two families × five seeds). Thus the new native
measurement table leaves zero recorded mean-quality gain for an LLM continuation
against those classical branches. This is a finite-table bound, not a claim about
all possible configurations, true noiseless optima or other workloads/models.

## Physical comparison

| Family | Settings × paired repetitions | Median across settings of paired CLI/API time ratio | Byte-identical API/CLI pairs | Median within-setting API CV | CLI CV |
|---|---:|---:|---:|---:|---:|
| Zstandard | 48 × 5 | 1.8356× | 40 / 240 | 2.285% | 2.127% |
| LZ4 | 48 × 5 | 1.9053× | 240 / 240 | 1.528% | 1.374% |

Each setting ratio is the median of its five paired timing ratios; the family
value is the median of 48 setting values. These are actual compression durations,
not total worker lifetimes. The ratios are not averages across heterogeneous raw
runtimes, nor measured production gains. Synthetic FFI checks are separate.

All LZ4 matched outputs were byte-identical. Zstandard outputs differed in 200
of 240 pairs and in compressed size for those same pairs. Hence this is an
interface comparison, not a causal estimate of startup overhead alone. API
one-shot compression and stdin streaming differ in available size information and
potential internal choices. Library loading was outside the API timer; context
and buffer allocation, compression and output copying were inside. CLI startup,
pipes and compression were timed together. Neither mode reused a compression
context across physical observations. Parent Python startup is outside both timers.

Zstandard APIs used compression level, window log, checksum ON, zero workers and
content-size field OFF; LZ4 preferences set level/block size/independence/checksum.
Every stream was decoded with its pinned CLI and compared byte-for-byte with the
same 901,120-byte CPython archive. These flags preserve the V50 research contract;
no claim of identical RAM, power, or corruption-detection strength across codecs.
The library bindings use installed owner headers, whose hashes are frozen.

## Equal-budget classical comparison

Twenty cases, forty arms, 600 newly charged recorded-vector acquisitions after
measurement: API/CLI × two families × five seeds. Each paired comparison shares
an acquired ten-vector prefix and gives each continuation ten more evaluations.
The unchanged nominal joint-3NN selector and random control see only acquired
runtime/size labels. Independent replay reconstructs selections and final scoring.

| Family | Interface | Mean classical gain over random | W / T / H | Mean hindsight headroom | Maximum headroom |
|---|---|---:|---:|---:|---:|
| zstd | api | 0.000% | 0 / 5 / 0 | 0.000% | 0.000% |
| zstd | cli | 0.000% | 0 / 5 / 0 | 0.000% | 0.000% |
| lz4 | api | 0.000% | 0 / 5 / 0 | 0.000% | 0.000% |
| lz4 | cli | -0.007% | 1 / 3 / 1 | 0.765% | 1.913% |

Full-table headroom is evaluator-only and nondeployable. Neither the bounds nor
mode comparisons were used by the optimizer. All individual seeds and exact
source values are retained. Five trials per setting remain too few for strong
claims about tiny differences; repeated seeds are not independent software systems.
The small CLI-LZ4 differences are not asserted statistically significant.

The reference size cap was acquired separately for each interface using the same
reference settings. LZ4 caps match at 288,926 bytes. Zstandard caps differ:
184,881 bytes for API versus 185,333 bytes for CLI. Those are research defaults,
not application-approved requirements. Different caps further limit a causal
cross-mode comparison. The within-mode zero-headroom finding remains valid.

A separately labeled post-hoc checkpoint diagnostic found that all ten native
prefixes had already reached the best recorded feasible setting after ten
acquisitions. CLI had seven of ten. This uses saved prefix labels plus the offline
evaluator's minimum and is not a deployable decision rule. It explains why this
small workload cannot validate a beneficial escalation controller at that checkpoint.
It does not replace the frozen primary endpoint after twenty evaluations.

## What ran and what it cost

Physical collection: 960 charged runtime/size/correctness vectors, 53.546 seconds,
within the 180-second limit. Classical collection plus independent replay:
600 recorded-vector accesses, 0.228 seconds, within the 30-second limit.
No free warmups/retries, downloads, LLM calls, cloud use or external spending.
Two earlier synthetic wrapper roundtrips are explicitly separate correctness
fixtures; their results are excluded from measured aggregates and speed claims.

Together with V50, this continuation executed 846 saved-file decode checks,
960 fresh compression trials, and 1,050 charged recorded-vector acquisitions.
Cumulative recorded accesses are 15,758; physical compression trials 2,234;
model requests including the original stage stay 1,976. All historical ledgers
remain unchanged. Actual research collection includes counterfactual methods
and repeated trials; a twenty-evaluation policy deployment is a separate model
of cost. No claimed paid-inference savings. Hardware/electricity cost unknown.

The parent owned bounded process groups and reaped workers. No experiment remains
running. All 358 tests passed before and after collection. Independent verification
checked 960 events and payload hashes, 480 API/CLI pairs, 600 optimizer charges,
20 cases/40 arms and source arithmetic. Frozen replay separately verified choices.
No collector, algorithm or primary analysis correction was made after observation.

## Reproducibility

- Protocol/config and 27-input freeze: `reports/protocol_v51_interface.md`,
  `reports/protocol_v51_interface.freeze.json`, `configs/study_v51.json`.
- All scheduled and charged physical trials: `results/v51_interfaces/`.
- Actual compressed payloads: `artifacts/sources/live_v51/outputs/`, local/ignored.
- All physical summaries, sealed median tables, setting ratios, PNG/SVG figures:
  `results/v51_analysis/`.
- Prefixes, paired arms, 600 acquisitions and outcomes: `results/v51_classical/`.
- Execution/verification/test receipts: `artifacts/study_v51/`.
- Renderer regenerates both figures and the labeled post-hoc checkpoint diagnostic.

Read-only replay:
```sh
.venv/bin/python scripts/verify_interface_v51.py
.venv/bin/python scripts/report_interface_v51.py
.venv/bin/python -m pytest -q tests
```
Collection, physical analyzer and classical replay refuse to overwrite completed
runs. The verifier checks saved evidence; it does not rerun physical compression.
Figures were visually inspected. Nothing was published, pushed or sent.

## Research decision

This continuation completed two studies rather than another prompt variation.
It closes two concrete gaps: explicit utility/frame checks and fresh paired
execution-interface measurements. Neither yields evidence for useful LLM routing.
The frozen grid and small workload should be retired as a benefit-discovery
benchmark; retain them as verified regression/negative-control cases.

The next research stage needs a genuinely different, source-justified application
workload with verified correctness and a search space that cheap search does not
already exhaust in effect. Choose it by application/measurement criteria before
seeing gains, and preserve family grouping. Do not repeatedly enlarge or tune
this compression workload until a favorable result appears. Independent-system
router validation, a distinct contribution against prior work, representative
workloads and journal readiness remain unresolved. These results are suitable
for a candid research discussion; they are not a Q2-readiness claim.
