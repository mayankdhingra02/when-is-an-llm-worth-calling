# STATUS — V72 real paired batch completed; negative escalation result

## Resume here

User approved this exact batch. V72 ran once to completion: 35 real local model
requests, 150 valid physical RocksDB evaluations, no retries or fallbacks, in
167.531 seconds. The owned model server exited 0. Nothing is running. No downloads
or spending occurred. Approval was consumed by this batch; it is no longer a
pending blocker. Do not reuse the exhausted allowance for new inference.

Report: reports/rocksdb_v72.md. The journal-quality goal remains scientifically
incomplete. The goal tool still reports its previous blocked state and offers no
agent-side resume operation; this does not mean this approved batch failed to run.

## Concrete result

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
.venv/bin/python scripts/seal_v72_execution.py --verify-only
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

## Single next research action

Admit independent software families for a prospectively frozen cross-system
replication of this working legal-vector interface with equally strong cheap
controls. Select tasks by provenance/schema/domain criteria, never by observed
LLM benefit. Close this fixed RocksDB batch; do not tune it until positive.
Read reports/next_experiment.md for the ordered plan and readiness limits.

Still untested: useful LLM escalation on independent families under this interface,
development-trained benefit-aware routing versus uncertainty/random/always/never,
untouched grouped test evaluation, practical reliability across hosts/workloads,
and latest clean-machine reproduction. The 400 effective-configuration admission
criterion remains unmet; 512 nominal vectors are not proof. Q2 readiness is not
established. V69's invalid contrast remains excluded; historical closed grids
must not be reopened or relabeled as fresh held-out evidence.
