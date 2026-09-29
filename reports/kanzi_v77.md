# V77: completed classical comparison on the repaired Kanzi adaptation

All200physical evaluations completed with valid applied settings, checksum and
byte-exact decompression. All15arms used the same saved10-evaluation prefix per
seed,7fresh search choices and3charged confirmations:20evaluations per arm.
The50prefix measurements were collected anew; no V75 outcomes were reused.
The result is a complete classical comparison on one artificial workload, not
an LLM result or evidence of cross-system routing.

Confirmed compressed bytes (three identical confirmation values for every arm):

| Seed | Random | 3NN | RF-LCB |
| --- | ---: | ---: | ---: |
| 11 | 5,529,352 | 5,529,352 | 4,751,282 |
| 23 | 5,248,371 | 5,739,996 | 5,739,996 |
| 37 | 5,150,518 | 4,686,563 | 4,976,391 |
| 53 | 5,302,168 | 5,302,168 | 4,686,563 |
| 71 | 5,248,371 | 5,248,371 | 5,248,371 |
| Mean of seed medians | 5,295,756 | 5,301,290 | 5,080,520.6 |

RF's mean is4.0643%smaller than random's mean, winning3seeds, tying1 and losing1.
3NN wins1/ties3/loses1 versus random. This is a descriptive comparison, not a
significance or uniform dominance claim. Which policy wins varies by seed.
Relative to the shared-prefix best, RF's size reductions are14.07%,0%,3.38%,
11.61%,0%; 3NN improves9.01%on seed37 only, while random improves8.56%on seed23.
Every other continuation keeps its prefix's observed size. This shows remaining
search opportunity on some prefixes, not that an LLM will find it.

![Measured classical comparison](../results/v77_kanzi_analysis/classical.png)

## Validity, provenance and limits

V76's isolated owner-source buffer repair is labelled explicitly. The original
Kanzi1.9 JAR and V75 failed run remain intact. V77 changes only the executable
relative to V75's frozen algorithm/domain/input choices. No failed candidate,
seed, entropy codec or input section was removed. All comparisons use the same
patched version and fixed16MiB workload; this is not the archived ICSE experiment.

The448candidate grid is canonical/source-distinct, not certified448distinct
behaviors. Across the collected200trials,126unique configurations were observed,
with126distinct byte counts and compressed hashes. That is evidence about this
sample only; no unseen configuration was scored to establish an optimum or
select a favorable task. One software family regardless of five seeds.

Primary objective is compressed bytes. Runtime is collection cost, not silently
mixed with output size or pooled with RocksDB milliseconds. Every phase starts
fresh JVM; startup/JIT/logging and watchdog overhead are included. All45confirmed
byte counts repeated exactly. This does not prove timing stability, production
corpus validity or general correctness of the patch.

A separate original-control/patched-output test in V76 reproduced the failure
and recovered patched output using the original decoder. It supports that narrow
repair, not a universal bug fix or publication novelty claim. No author contact,
remote publication, external spending or download occurred in V76/V77.

## Costs and verification

200new physical trials =50shared prefix+105search+45confirmation;300logical arm
charges. V77 ran400native processes in532.168957seconds, with526.517101seconds
summed process wall time and peak sampled RSS330,399,744bytes (~315.1MiB).
Watchdog sampling can miss instantaneous peaks. Distinct research costs include
V75's9trials (1failed) and V76's3diagnostic trials (1expected application failure).
Do not hide those abandoned/diagnostic costs in a20-evaluation deployment claim.
No deployment monetary estimate is inferred. Hardware/electricity/human/agent
costs remain unknown. New model calls0; cumulative historical calls2016unchanged.

548tests passed before collection. After preparing the next adapter,552tests
passed; all are tests, not measured model outputs. Independent replay verifies
all200charges/results, saved-prefix identities, acquired-only selections, per-arm
uniqueness, selected incumbents,45confirmation charges and randomized arm order.
Validated bulky outputs were removed after hashes/header/logs were durably saved,
per the prospective protocol. Their byte equality is supported by contemporaneous
receipts; offline replay cannot directly recompare deleted files. V76 retains its
full diagnostic products. Clean-machine reproduction of V77 remains untested.

Evidence:
- `results/v77_kanzi_classical/`: raw charges, prefix/case states, commands,
  process logs, phase receipts, setting headers, output hashes and retention notes.
- `results/v77_kanzi_analysis/`: replay-checked JSON/CSV and inspected PNG/SVG.
- `reports/protocol_v77.md` and `.freeze.json`: prospective protocol/code pins.
- `artifacts/study_v76/`, `artifacts/study_v77/`: diagnosis, builds, tests, costs,
  source patch, historical snapshots and combined evidence seal.

Read-only checks:
```
.venv/bin/python scripts/verify_kanzi_v76.py
.venv/bin/python scripts/verify_kanzi_v77.py
.venv/bin/python scripts/seal_evidence_v77.py --verify-only
```
Regenerate figures via `scripts/analyze_kanzi_v77.py` in a separate copy because
render metadata may change sealed file hashes. Do not rerun the one-shot collector
or overwrite V75/V77 results to seek a better outcome.

## Next actual research test

V78 is prepared and prospectively frozen:35real local SmolLM3 calls,150fresh paired
trials, the5saved prefixes, RF/3NN/LLM arms under matched model residency,30minute
cap, no downloads or spending. It has NOT executed; a new request allowance is
needed because the prior35-call scope was consumed. All test fixtures remain
separate. This next test asks whether the LLM adds size benefit beyond the cheap
controls, and at what observed decision/collection cost. It alone will still be
one-family exploratory evidence, not enough to claim Q2 readiness or a learned
router's generalization. See reports/research_claims_v77.md for broader limits.
