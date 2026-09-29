# STATUS — V74 Kanzi correctness/resource feasibility passed

## Resume here

Three actual Kanzi trials (reference/contrast/reference) passed checksum,
independent header/settings checks, and full decompression byte equality.
Six JVM processes; zero failures/retries/new model calls. Nothing is running.
Report: reports/kanzi_v74.md. Raw: results/v74_kanzi_feasibility/.
Descriptive CSV/JSON and inspected figures: results/v74_kanzi_analysis/.

Compression seconds: 0.252776 / 0.597935 / 0.230801. Compressed bytes:
6502417 / 7052949 / 6502417. One artificial 16 MiB input; these are feasibility
observations, not optimization gains. Header and verbose logs confirm applied
settings; reference outputs have identical hashes. Peak sampled RSS 215.2 MiB.
Owner-pinned Kanzi1.9 source and local Java/compiler pins are saved. A separate
same-host rebuild produced an identical JAR. No clean-machine rerun yet.

All 537 tests passed in 3.70 s with `.venv/bin/python -m pytest -q tests`.
Default testpaths runs only the 510 synthetic tests; use explicit `tests`.
Offline replay verifies all three trials without application/model calls.

Single next action: freeze a source-supported Kanzi domain and workload utility
before a bounded classical optimization batch. Read reports/next_experiment.md.
Only two settings are validated so far; >=400 effective settings, production
workloads, statistical timing precision, classical search, LLM continuation and
cross-system generalization remain untested for Kanzi. This is development-only.
Do not tune a new workload to turn the contrast into a favorable outcome.

V74 downloads 3429761 bytes; cumulative 4806613863, remaining 562095257.
New physical feasibility trials 3 / native processes 6, separate from prior350
V71+V72 RocksDB trials. Historical table acquisitions26358, model requests2016
unchanged. External spend USD0; other monetary costs unknown. Cost evidence:
artifacts/study_v74/resource_ledger.json. V72 inference allowance fully consumed;
no new model batch is defined or approved by V74's feasibility protocol.

Read-only replay: `.venv/bin/python scripts/analyze_kanzi_v74.py`.
Current chain verifier: `.venv/bin/python scripts/seal_evidence_v74.py --verify-only`.
Prospective freeze: reports/protocol_v74.freeze.json. Prior entry documents saved
under artifacts/study_v74/previous_snapshot/; all older evidence retained.
No paper-readiness or positive-routing claim is established.

## Historical V73/V72 record (figures and commands below refer to those stages)


## Resume here

The previous turn completed the real V72 batch. This turn made independent
progress through a primary-source and feature-only cross-system audit. No model,
physical benchmark or hidden objective call was made in V73. Nothing is running.
No new inference allowance is pending; the approved V72 scope is fully consumed.

New report: reports/admission_v73.md. Kanzi's 4,180 original feature vectors
reconcile with 4,112 released vectors; 68 are omitted and original IDs are reused.
Its XML thread choices 1/32/64 disagree with sample levels 1/4/8. Failure reasons
and output correctness remain unresolved. Archived timings are NOT admitted.
No claim that missing evidence does not exist elsewhere in the partial archive.

Four configuration-only samples and two source script bodies were inspected.
No objective member was opened or downloaded code executed. A partial directory
reader avoided downloading the 401 MB archive or its 46 MB directory. Extracted
member CRC/SHA256 hashes are checked; full archive MD5 remains unverified.
Source downloads 2,913,745 bytes; cumulative 4,803,184,102; remaining 565,525,018.
All 529 tests passed in 3.84 seconds. Synthetic fixtures are not research data.

Single next action: pin Kanzi from its program owner's source/release, audit
family exposure, and build a bounded fresh compression/decompression feasibility
harness with exact byte equality, checksum enabled, canonical transforms and
recorded failures. Fix the workload prospectively. This is development admission,
not held-out evaluation. Read reports/next_experiment.md before implementation.

Evidence: artifacts/sources/v73/, results/v73_admission/summary.json,
artifacts/study_v73/. Current read-only verification command:
`.venv/bin/python scripts/seal_evidence_v73.py --verify-only`.
Prior entry documents are saved in artifacts/study_v73/previous_snapshot/.
The V72 negative result below is unchanged. Journal readiness is not established.

## Previous actual experiment (V72)


All 35 constrained model responses were legal and distinct within their arms.
Every LLM-selected incumbent came from a genuine model proposal. Nevertheless,
the LLM was slower than RF AND the cheap domain prior on all five seeds' confirmed
medians. Mean of seed medians: RF 204.512 ms; prior 211.795 ms; LLM 224.782 ms.
LLM mean is 9.91% slower than RF. It used 39.610 s of decision time versus RF's
0.999 s across five seeds, about 7.722 extra seconds per seed. Tokens: 303 output,
17,435 input, no unknown usage. No observed gain even for the hindsight RF/LLM
oracle. This is a one-family descriptive negative result, not a universal claim.

Five fixed seeds: 11,23,37,53,71. Shared historical prefix 10, new search 7,
charged confirmations 3: total 20 per arm. Actual NEW physical collection 150;
historical shared prefixes 50; logical arm charges 300. No new prefix queries.
The frozen same-model-residency controls ran freshly with randomized round order.
Three confirmation repeats per incumbent cannot establish precise true latency.

Post-hoc diagnostic, clearly separate from a trained policy: all 32 RF/LLM masks
were enumerated; the 31 with any escalation had worse observed mean quality.
This gives no positive observed routing headroom here. No router was fitted.

## Evidence and checks

- Raw: results/v72_rocksdb_paired/ (35 request/response folders, 150 evaluation
  folders, all charges, case states, engine logs, phase receipts and metadata).
- Frozen analysis: results/v72_rocksdb_analysis/ (JSON, CSV, inspected PNG/SVG).
- Retrospective mask diagnostic: results/v72_routing_diagnostic/ (JSON/CSV).
- Approval, costs and verification: artifacts/study_v72_execution/.
- Protocol/runtime/model/data pins: reports/protocol_v72.freeze.json and
  reports/analysis_v72.freeze.json; production code unchanged since freezing.
- All 524 tests passed in 3.75 s. Synthetic fixtures excluded from measured data.
- Read-only replay verified 150 trials, 105 search choices, 35 model outputs,
  45 confirmation charges, shared prefixes and all per-arm budgets.

```
.venv/bin/python scripts/verify_rocksdb_v72.py
.venv/bin/python scripts/seal_evidence_v73.py --verify-only
```

Do not rerun the one-shot collection or analysis over existing results. Reproduce
in a separate project copy and obtain a new inference allowance when needed.
Physical SST data were hashed then removed as declared; retained archives are
not complete DB snapshots. No clean-machine rerun of latest collection exists.
All historical entry documents were preserved before editing under
artifacts/study_v72_execution/previous_snapshot/. The current execution seal
checks prior manifests against exact matching snapshots. Old standalone seal
commands may expect old entry documents; use the current chain verifier above.

## Costs and remaining limits

35 newly consumed model requests; cumulative historical requests 2016. New live
objective charges 150; V71+V72 live charges 350. Historical recorded-table
acquisitions remain 26358 (different counter). New downloads 0; persistent total
4800270357 bytes; remaining 568438763 bytes under 5 GiB. External spend USD 0.
Hardware/electricity/human/agent costs unknown. Detailed research collection costs
are in artifacts/study_v72_execution/resource_ledger.json, separate from any
hypothetical selected-branch deployment estimate.

