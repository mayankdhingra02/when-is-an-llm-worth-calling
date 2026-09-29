# V32: a small classical gain changes sign under fresh physical measurements

**The Zstandard family-average advantage of the fixed cheap optimizer's selected settings over random selections changed from +0.499% to −0.103% in fresh measurements.** LZ4 stayed near +0.59%; zlib selected the same configuration in both methods. The equal-family point estimate fell from +0.364% to +0.161%. This is a new physical reliability result, not another replay of the original timing table. It shows why these small gains should not be treated as stable routing labels without measurement uncertainty.

All **140/140 compression trials completed**, using seven fixed configurations over twenty shuffled rounds. Every output decoded exactly and matched the historical compressed size and hash. No LLM, new optimizer run or new software family was involved. No claim of significance, equivalence or broad optimizer superiority follows.

## Fixed selections, fresh measurements

V17 measured an expanded compression grid three times and ran cheap joint3NN and random continuations from identical prefixes under recorded output-size caps. Its apparent optimizer gains were small relative to descriptive timing variation. V32 retains all fifteen historical cases: Zstandard, LZ4 and zlib, five seeds each. It measures the settings those methods already selected, together with each case's fixed historical full-table feasible minimum. The historical reference is not reselected using fresh timings.

The forty-five case/role assignments reduce to **seven distinct configuration IDs**. Each setting was measured once per round; the resulting observation is reused for every case/role pointing to that setting. Ten cases have identical cheap/random settings, and the other five cases reduce to only **three distinct configuration pairs**. Shared observations and repeated seeds are not independent systems or independent replications of optimizer behavior.

The [protocol](protocol_v32_reliability.md), [selection manifest](../data/reliability_v32.json), deterministic schedule and [71 input references](protocol_v32_reliability.freeze.json) were frozen before collection. Twenty complete shuffled rounds used seed 2026092532. There were no warmups, retries, discarded observations, parameter changes or new winner selection. The stage used a single worker, a two-second process-group timeout per attempt and a sixty-second collection cap. Every attempt was journaled and charged before launch.

The workload remains the 901,120-byte CPython source archive from V15/V17. The installed CPython, codec executables and linked-library hashes matched the saved environment. Zstandard 1.5.7, LZ4 1.10.0 and zlib 1.2.12 remain the recorded implementations. V17's timing boundary was reused: CLI launch/pipes/codec work for Zstandard and LZ4, Python API work for zlib. No cross-family raw-speed ranking is intended. The old reference-derived size caps remain research defaults, not an application-approved utility requirement.

## Results

Positive gain means the cheap setting is faster than the random setting. Compute each configuration's fresh median from twenty repetitions, then `(random median − cheap median) / random median`; average within family and equally across families.

| Family | Original mean gain | Fresh mean gain | Fresh wins / ties / losses | Same-setting cases |
|---|---:|---:|---:|---:|
| Zstandard | +0.4990% | **−0.1032%** | 1 / 3 / 1 | 3/5 |
| LZ4 | +0.5922% | +0.5866% | 3 / 2 / 0 | 2/5 |
| zlib | 0% | 0% | 0 / 5 / 0 | 5/5 |
| Equal-family mean | +0.3637% | +0.1612% | — | 10/15 |

The identical-setting ties are structural: those roles use the same observations, not separate timing samples that happened to be equal. The three LZ4 wins reuse one configuration pair; they are not three independent confirmations.

For the three distinct nonidentical pairs, paired-round distributions are broad and include both signs:

| Pair / case mapping | Gain from medians | Median paired-round gain | Paired-round 10th–90th percentiles | Faster / slower rounds |
|---|---:|---:|---:|---:|
| Zstandard / seed 37 | +0.8791% | +1.6223% | −3.6898% to +10.0145% | 13 / 7 |
| Zstandard / seed 71 | −1.3949% | −1.8072% | −6.0452% to +1.7734% | 6 / 14 |
| LZ4 / seeds 11, 23, 71 | +0.9777% | +0.1390% | −7.8132% to +5.2476% | 11 / 9 |

These percentile ranges describe observations, not confidence intervals. Ratio of medians and median of paired ratios are different statistics; neither is silently substituted for the predeclared primary statistic. All per-case timings/statistics remain in [cases.csv](../results/v32_reliability/cases.csv).

The fixed historical hindsight reference also changed relative ranking. Its mean gain over the cheap setting was originally +0.5373% for Zstandard, but is **−0.4289%** in the fresh session. LZ4 changed from +0.1974% to +0.1955%; zlib stayed zero. Negative reference gain is retained. It is not “negative full-grid headroom”: this campaign did not remeasure the full grid or find its fresh optimum. Selection of an old minimum and timing variation are plausible explanations, but this single session does not identify a cause.

![Original and fresh comparisons](../results/v32_reliability/comparison.png)

The figure was visually checked. Across the seven settings, fresh timing CV ranged from 2.37% to 41.64%. The largest observed compression time was 30.57 ms versus that setting's 9.70 ms median. All observations remain in the data. The seven settings produced six distinct compressed outputs; output identity alone does not establish runtime equivalence.

## Validation and actual costs

**220 tests passed in 1.35 seconds** before freeze/collection. New synthetic checks cover complete shuffled rounds, identity comparisons, fixed gains, invalid timings and the distinction between paired ratios and ratios of medians. They are excluded from measured results.

Independent verification reconstructed all historical selections from their acquired labels and the recorded source table. It checked all twenty-round schedules, sizes/caps and retained payload hashes, then **decoded all 140 saved compressed outputs again** and compared their bytes with the original workload. Separate Decimal calculations checked thirty case/reference comparisons, 120 reported statistics and ninety paired-round counts. Read-only analysis replay passed. All **2,313 frozen historical/current references** passed integrity checks. Old scientific inputs/results and the V26 reconstruction ZIP remain unchanged.

| Cost | Actual added amount |
|---|---:|
| Physical compression/decompression measurement attempts | 140 |
| New recorded optimizer acquisitions | 0 |
| New model requests | 0 |
| Collection runtime | 6.730717 seconds |
| Analysis and figure runtime | 0.544802 seconds |
| Independent decoding/verification runtime charged | 0.733595 seconds |
| Total added experiment runtime | **8.009114 seconds** |

The extra decoding is correctness verification of retained bytes, not another compression objective measurement. It is separately charged as computation. These 140 fresh measurement attempts are additional research cost; they must not be hidden inside the earlier twenty-evaluation optimizer budget or presented as free deployment probes. Hypothetical deployment of one historical optimizer still has its declared twenty configuration-vector acquisitions; using this extra validation procedure would add its own measurement cost. No deployment saving is estimated here.

Historical physical trials now total **1,274**. Recorded optimizer accesses remain **8,308**. The runtime ledger is **2,276.095609 / 3,600 seconds**, leaving **1,323.904391 seconds**, with no active job. Follow-up model allowance remains exhausted at 200/200 requests, 300 including the initial stage. No model/cache output was fabricated. No downloads, new packages, cloud spending, remote push, publication or external contact occurred; external spend remains USD 0.

Executed commands:

```sh
.venv/bin/python scripts/prepare_reliability_v32.py
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/collect_reliability_v32.py
.venv/bin/python scripts/analyze_reliability_v32.py
.venv/bin/python scripts/verify_reliability_v32.py
.venv/bin/python scripts/analyze_reliability_v32.py --verify-only
.venv/bin/python scripts/audit_history_v30.py
```

Collection refuses restart/overwrite. The independent verifier's first execution charges computation; `--verify-only` can recheck saved evidence without new compression trials. Raw starts, trial results and complete denominator are under [results/v32_reliability](../results/v32_reliability/). Source bindings, tests, schedule, cost receipts, independent decode records and final checks are under [artifacts/study_v32](../artifacts/study_v32/). Actual compressed bytes are retained under `artifacts/sources/live_v32/outputs/` and remain Git ignored.

## Limits and next action

This one later timing session does not isolate measurement noise, workload interference, thermal state or temporal drift. It uses a small fixed archive, a developer machine, CLI/API timing differences and already exposed systems. It checks previously selected settings, not all configurations or fresh optimizer choices. Twenty repetitions and three distinct nonidentity comparisons do not establish generalization. The result neither validates a learned benefit predictor nor measures LLM reliability. The separate V31 shortlist ceiling remains a recorded-table diagnostic, not a statement about fresh physical runtimes.

**Next action:** freeze a quality-constrained development task, practical minimum gain and measurement-repetition budget before collecting new LLM routing labels. The current evidence supports keeping uncertainty in those labels rather than calling any positive timing difference useful. Use development data to design that measurement rule, reserve untouched software families for evaluation, and retain the strong classical controls. Additional real inference still requires a new bounded allowance or compatible provenance-checked cache. Do not keep remeasuring these cases until a preferred sign appears.
