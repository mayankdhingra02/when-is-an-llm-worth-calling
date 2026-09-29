# STATUS — V96 diagnostic complete; research goal remains open

**Latest result:**40 additional native diagnostic configuration acquisitions completed:37 valid workers,3 failures, all at panel32. All30 smaller-panel workers completed. Primary-source inspection identifies a material limitation in the original SuperLU domain. The V94 and V95 evidence is preserved unchanged; read `reports/superlu_v96.md` and `reports/research_readiness_v96.md`. The positive benefit-prediction hypothesis and Q2 readiness remain unestablished.

## What actually ran

V96 used two previously failing configurations, four panel sizes (16,20,21,32), five isolated repetitions, three planned physical solves each. Conditions and code were frozen before collection with order seed96000. No replacement of failures, model calls, new packages, native-library patches or recorded-table reads. Actual stage runtime9.726967s, within300s; no resource guard tripped.114 physical solves started,111 returned;3 started without returning and6 planned solves did not start. All111 returned vectors independently passed the numerical certificate replay.

Source retrieval added16,060bytes from the owner SciPy v1.13.1 repository. Git blob identities match the previously pinned tree. Sandbox DNS/process-monitoring preflights failed before collection; authorized retries of these infrastructure operations succeeded. Every actual diagnostic acquisition is charged. Full repository validation:757 tests passed in21.09s.

The source limitation changes interpretation of the original SuperLU comparison; successful numerical answers do not resolve it. No completed outcome was removed or replaced. This is a posthoc diagnostic on an exposed system, not new held-out optimization evidence. HiGHS is a separate implementation and is unaffected by the identified source path. Native instruction-level causality, a revised-domain optimization run and second-machine replication remain untested.

## Evidence and commands

- Raw intended conditions, charges, worker journals, vectors, exits and logs: `results/v96_superlu/`.
- Replayed counts and solution checks: `results/v96_analysis/`.
- Frozen protocol: `reports/protocol_v96.md`, `reports/protocol_v96.freeze.json`.
- Source audit: `reports/source_audit_v96.md`; receipts: `artifacts/sources/v96/`.
- Actual execution/test logs: `artifacts/study_v96/`.
- Prior complete resume state: `artifacts/study_v96/previous_snapshot/STATUS.md`.

Safe replay, with zero new model calls or native solves:
```
.venv/bin/python scripts/analyze_superlu_v96.py
.venv/bin/python -m pytest tests -q
.venv/bin/python scripts/seal_superlu_v96.py --verify-only
```
The collection runner refuses existing results. Do not resume V94/V95/V96 collection into completed directories or alter their freezes. The newest manifest resolves historical root documents through explicit snapshots.

## Prior outcomes retained

V94:500 native acquisitions (485 valid,15 failures),100 real model requests. Fixed Qwen3 lost to sequential3NN on both engine means; zero>=5% wins in10 pairs. The SuperLU result now carries the V96 domain qualification. Both development-fitted routers chose never-call. V95:25 model requests/24 responses out of36 intended conditions;12 valid non-thinking answers, no valid thinking answer; one timeout stopped collection.360 recorded-table accesses including explicit fallbacks. No valid model choice beat both strong controls by>=5%. All original results, costs and unknowns remain in their respective reports.

## Limits and next action

Cumulative real-model requests3,843; recorded-table acquisitions27,018, both unchanged. V94 native configuration acquisitions500 plus V96 separately charged40. V96 physical counts114starts/111returns are distinct from configuration labels. Earlier native counts remain unchanged (DuckDB78physical,H2299,Kanzi1265,RocksDB350). Cumulative downloads9,870,221,104bytes /10GiB;867,197,136bytes remain. Model payload9,126,358,023bytes /9GiB remains unchanged. External spendUSD0; electricity/hardware costs unknown. No model server or diagnostic job remains running.

**Next local scientific action:** separately freeze a source-justified restricted-domain optimization comparison with fresh paired acquisitions and real model responses, labeled exploratory because SuperLU is now exposed. Preserve original evidence. Independent replication of HiGHS on a second machine remains desirable; no second host is connected. Final-answer-reserved reasoning and additional independent systems remain outstanding. Do not claim publication readiness from these diagnostics.

User reported a repeated Daybreak/Astra content-display notice during this continuation. Exact platform classification is not visible. Low-level debugging is discontinued for now; completed evidence is saved. Continue ordinary experimental analysis/design without claiming to override the platform restriction. Official product documentation was consulted; no account access or settings were changed.
