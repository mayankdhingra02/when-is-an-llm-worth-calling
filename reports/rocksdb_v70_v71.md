# V70–V71: corrected RocksDB measurements and confirmed classical incumbents

**Completed:** three corrected feasibility trials and 200 live classical objective
evaluations, all valid. The classical experiment contains five seeds and three
continuations per seed. Every arm stays within 20 objective evaluations, including
three fresh confirmation measurements. RF-LCB has the lowest average confirmed
time, but does not win on every seed. This supplies a working baseline for a
paired LLM experiment; it does not demonstrate LLM benefit or held-out routing.

## Correctness and configuration repair

V70 uses the same pinned RocksDict 0.3.27 / RocksDB 9.8.4 runtime, expected values,
request trace and settings as V69. Both creation and reopening explicitly supply
default-column-family options. Active engine LOG/OPTIONS must match the requested
cache capacity, block size and restart interval, and the supplied cache must have
positive usage after warmup. All three corrected trials passed. Verified-loop times
were 0.313938292, 0.791605417 and 0.307441834 seconds for reference, contrast and
reference. These are descriptive feasibility observations, not reliable effect or
noise estimates from two reference repeats.

Every trial checks all 100,000 timed responses against exact expected 1,000-byte
records, with full 65,536-record scans before and after. Atomic phase receipts
preserve timings before optional result metadata is serialized. Three new failure-
injection tests cover serialization failure, atomic replacement failure and raw-byte
metadata. Old V69 results and its invalid contrast remain separate and unchanged.

The workload remains a scaled YCSB-C-inspired adaptation: read-only, fixed scrambled-
Zipfian trace, Python RNG/binding, ten deterministic fields, OS-warm cache recipe,
and a three-dimensional geometric options domain. It is not Java YCSB replication
or a production workload sample. The domain has 512 nominal vectors, not proof of
512 performance-distinct configurations. V71 physically measured 129 unique vectors.
The stronger 400-distinct-effective-configuration admission criterion remains unmet.

## Frozen budget and selection design

Seeds: 11, 23, 37, 53 and 71. Each shared prefix contains four random unique settings
and six acquired-only nearest-neighbor choices. Random, 3NN and RF-LCB then each
make seven further search choices. Each arm freezes its best observed configuration
after 17 search evaluations and spends its final three evaluations remeasuring it.
Confirmation values cannot change the selected configuration or any decision.

Thus every logical arm uses **10 prefix + 7 search + 3 confirmation = 20** objective
evaluations. This reliability allocation differs explicitly from earlier screens
with 20 unique-row acquisitions. Shared prefixes are physically collected once:
five × [10 + 3 × (7 + 3)] = **200** actual evaluations, versus 300 logical per-arm
charges. All repeated confirmation outcomes are charged. There is no measurement
reuse between post-prefix branches, and their execution order is shuffled at each
step with an isolated predeclared RNG.

RF-LCB uses the frozen 64-tree random forest, mean minus standard deviation. 3NN
uses stable nearest-three distances. Feature scaling uses declared option ranges,
not outcomes. No full performance table exists. V69/V70 timings were not optimizer
inputs. The primary endpoint is each selected configuration's median of three new
confirmation times. Reported ranges are repetitions, not confidence intervals.

## Actual result

| Seed | Random (ms) | 3NN (ms) | RF-LCB (ms) |
|---:|---:|---:|---:|
| 11 | 235.186 | 230.593 | 224.686 |
| 23 | 255.085 | 253.668 | 255.041 |
| 37 | 245.594 | 222.286 | 199.801 |
| 53 | 231.869 | 229.239 | 204.757 |
| 71 | 223.911 | 248.531 | 254.740 |
| Mean of seed medians | **238.329** | **236.863** | **227.805** |

RF's confirmed median is 18.65% and 11.69% lower than random on seeds 37 and 53,
but 13.77% higher on seed 71. It is 4.46% lower on seed 11. **All three methods
selected the same configuration on seed 23**, so their small differences there are
measurement variation, not an algorithmic improvement. Random and 3NN also share
the selected setting on seeds 11 and 53. Do not interpret each sign difference as
a policy win. The machine-readable raw sign counts are accompanied by this explicit
same-configuration interpretation in `interpretation.json`.

Median within-incumbent confirmation CV is 1.064%, from only three repetitions per
incumbent. Some search minima look optimistic on confirmation; others improve.
This motivates charged repeated measurement, but does not quantify all runtime
uncertainty, optimizer variance or host drift. There is one software family, no
global optimum, no significance test and no evidence that an LLM can exploit the
remaining variation. More seeds are not more independent systems.

## Artifacts and verification

- `results/v70_rocksdb_feasibility/`: three complete native DB snapshots, phase
  receipts, active engine logs and supervisor records.
- `results/v71_rocksdb_classical/`: 200 charge records, saved prefixes, all arm
  decisions and confirmation values, phase receipts, native LOG/OPTIONS/MANIFEST
  files, physical-file inventories and failures/denominator fields.
- `results/v71_rocksdb_analysis/`: JSON summaries, same-setting interpretation,
  CSV and PNG/SVG figure. The figure was rendered and visually checked.
- `reports/protocol_v70.md` and `protocol_v71.md` with timestamped SHA256 freezes;
  unchanged inputs/runtime from `data/generated_v69/` and `configs/runtime_v69.lock.json`.
- `artifacts/study_v70/` and `artifacts/study_v71/`: tests, collection logs, independent
  replay, resource ledger and evidence seal.

V71's transient DB data files were hashed and removed after archiving receipts and
engine metadata, keeping scratch to one owned trial at a time. These archives are
not full DB snapshots. Fixed raw inputs, request traces, response digests and full-
scan digests remain. Read-only verification recomputes every expected response/scan
digest, verifies all 203 trials' active settings, replays all 155 search decisions,
and checks all 45 confirmation charges, prefixes and inclusive budgets. It makes
no new DB queries. **505 tests passed**, including native synthetic integration
fixtures when the optional pinned runtime is present.

```
.venv/bin/python scripts/verify_rocksdb_v71.py
.venv/bin/python scripts/seal_evidence_v71.py --verify-only
.venv/bin/python -m pytest -q tests
```

The first two commands are read-only; pytest executes tiny synthetic database
fixtures. The one-shot collection scripts refuse existing result directories.
Rerender figures in a copy to preserve sealed image bytes.

## Actual cost versus deployment

V70 collection took 3.145 seconds; V71 took 180.110 seconds including orchestration,
model fitting for the classical optimizer, DB setup, archiving and cleanup. Combined
worker process time was 181.471 seconds. Peak sampled worker RSS was 342,458,368
bytes. Across 203 trials: 13,303,808 load writes, 20,300,000 checked timed reads,
2,030,000 warmup reads and 26,607,616 full-scan records. Setup and validation are
actual research costs; the objective measures only the verified read loop, including
Python, timer instrumentation, payload checks and response hashing.

No new downloads, LLM requests, paid services or remote publication. Historical
recorded-table acquisitions remain 26,358; the 200 **new live physical objective
charges** are recorded separately rather than mislabeled table accesses. Cumulative
model requests remain 1,981. Download allowance remaining: 568,438,763 bytes.
Electricity, hardware and human/agent time are unpriced. A deployed classical arm
under this recipe needs 20 physical evaluations; total deployment latency including
controller/model service and production measurement costs is not established.

## Next research decision

Prepare a small **exploratory paired local-model test from all five saved prefixes**,
using legal complete-vector generation, the same charged 7-search/3-confirmation
continuation, and freshly measured classical controls under the same model-resident
machine conditions. Include a cheap domain-prior control as well as RF: an LLM gain
over RF alone could merely express the obvious prior that larger caches help reads.
Freeze prompts, controls, fallback behavior, request count and limits before calls.
Do not choose only the seeds on which RF looked weak, fit a router on this one
family, or claim this is a new held-out test. No new inference allowance is granted
by V70/V71; implementation and a concrete bounded request scope come first.

Still missing for the original research objective: useful real LLM continuations
with this interface, multiple independently admitted families, a development-trained
benefit controller and untouched system-level evaluation with meaningful precision.
Q2-readiness is not established by these classical results.
