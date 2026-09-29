# Status — 2026-09-25: V30 prospective classical transfer completed

## Resume here

**Next concrete result delivered:** the unchanged sequential 3NN rule did not transfer uniformly to two previously unacquired families. Against static ranking, relative gain is +12.33382% on Opus and −0.53478% on Z3. The equal-family normalized gain is negative (−0.01241019), while relative gain is positive (+5.89952%). Preserve both metrics. Adaptive shortlist centroid beats sequential 3NN in both family averages under both metrics; sequential averages 3.13590% worse recorded targets against that comparator (1 win, 5 ties, 4 losses).

Read [V30 report](reports/transfer_v30.md), [frozen protocol](reports/protocol_v30_transfer.md), and relevant code. Do not reread the full literature report. This is a descriptive classical transfer check, not demonstrated LLM escalation benefit. Opus and Z3 are now exposed; exclude them from future untouched holdouts.

## What actually ran

- Source audit resolved deferred Opus/Z3 objective direction using the original owner-hosted paper, Table 2. Existing pinned datasets and V5 revision/workload filters were reused. No targets were parsed for feature-only admission.
- Two families × five fixed seeds × five methods = 50 completed arms, each 20 evaluations with the same ten-label prefix within each case.
- 600 new recorded-label acquisitions: 100 fresh prefix labels + 500 branch labels. Logical per-arm total 1,000; hypothetical deployment of one method over ten cases is 200 evaluations.
- Full centroid, static rank, adaptive shortlist centroid, batch 3NN and sequential 3NN. Fixed V29 code reused without tuning; 87 references frozen before all new labels.
- Zero model calls, retries, failed runs or omitted cases. No fresh physical trials.
- 211 tests passed in 1.34 seconds. Acquired-only replay reproduced all 600 decisions and 50 final states. Separate Decimal verification checked source labels and all metric aggregates.
- All 2,086 frozen historical/current references passed. Figure visually inspected; no live or scheduled job remains.

Executed commands:

```sh
.venv/bin/python scripts/fetch_source_v30.py
pdftotext -f 10 -l 13 -layout artifacts/sources/v30/performance_evolution_author.pdf artifacts/study_v30/source_sections.txt
.venv/bin/python scripts/admit_transfer_v30.py
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/run_transfer_v30.py
.venv/bin/python scripts/analyze_transfer_v30.py
.venv/bin/python scripts/analyze_transfer_v30.py --verify-only
.venv/bin/python scripts/verify_transfer_v30.py
.venv/bin/python scripts/audit_history_v30.py
```

Collection and analysis refuse completed outputs. The final three commands are read-only verification. No inference is needed to inspect or replay saved evidence.

## Evidence and resolved failures

- `results/v30_transfer/`: acquisitions.jsonl, ten saved prefixes, 50 arms, checkpoints, progress, all case/pair scores, summary, PNG/SVG figure.
- `artifacts/study_v30/`: source/admission evidence, logs, 211-test receipt, numerical verification, accounting and final checks.
- `data/manifest_v30.json`: pinned data, features, directions, family grouping, source hashes and historical exposure scan.
- `reports/protocol_v30_transfer.freeze.json`: all 87 prospective input references.
- `src/escalation/transfer_v30.py`: fixed method dispatch; existing nearest-neighbor implementation unchanged.
- Before-state documents/ledgers: `artifacts/history/v30_before_admission/`.
- Original source fetch hit sandbox DNS failure, then succeeded through platform-approved network execution. No failed payload bytes were received.
- Original historical audit rejected the newly appended download ledger. `audit_history_v30.py` verifies the exact archived historical identity plus the append-only new paper transfer; scientific inputs and old verifier remain unchanged. See verification_attempts.json.
- V26 standalone ZIP unchanged; reconstructs V25, not V27–V30.

## Limits and costs

Only two independent families; seeds are repeats, not independent systems. This does not establish statistical generalization, a useful learned router or LLM superiority/inferiority. Opus bitrate/channel/sample-rate changes leave equal-output-quality utility unresolved. Recorded aggregate targets lack per-row repetition uncertainty. Full-table normalization is evaluator-only. New LLM behavior, reliability, deployment costs and application-quality-constrained improvement remain untested here. Original V6 grouped router result remains negative/insufficient.

Actual new collection + analysis runtime: 7.278336707 seconds. Historical recorded accesses: 8,108; physical trials: 1,134. Runtime ledger: 2,265.613029755 / 3,600 seconds, 1,334.386970245 remaining, active_since null. Follow-up model allowance: 200/200 exhausted (300 total including initial stage). No new allowance inferred.

Source paper download: 3,971,352 bytes, successful retrieval 2.665940 seconds, separate preparation cost. Accounted downloads 4,518,268,306 bytes; model bytes unchanged at 4,098,574,535. External spend USD 0. No cloud, push, publication or contact.

**Single most important next action:** freeze a prospective paired LLM-versus-strong-classical protocol on additional untouched families with an explicit application-quality constraint. Retain static ranking and adaptive shortlist centroid alongside fixed 3NN. Actual new inference will require a new bounded allowance or compatible provenance-checked cache; the existing cap is exhausted. Do not tune these methods on the newly exposed Opus/Z3 outcomes to obtain a positive result.
