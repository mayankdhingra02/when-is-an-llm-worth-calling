# STATUS — V35.1 portable reconstruction complete

Updated2026-09-25. Resume here and from [V35.1 report](reports/reproduction_v35.md), [protocol](reports/protocol_v35_1_reproduction.md), and relevant code. The scientific result remains V34; this stage establishes portable saved-result reconstruction and exposes a numerical reproducibility issue. Prior root documents/ledgers are preserved under `artifacts/history/v35_before_execution/`.

**Next concrete result achieved:** V34 reconstructs in an extraction outside the checkout under isolated Python3.10.13 and3.12.14, with identical scientific outputs. All9corruption tests rejected,including8with refreshed file-index hashes. Deterministic rebuild is byte-identical. **241 project tests pass**.

## Artifact and actual execution

- Delivered ZIP: `output/llm_escalation_v34_reproduction_v35_1.zip`,3,690,811bytes,418content files plus manifest.
- SHA256:`75333386b2ab80ac5a49ec554050fc1f4ba92e708a2c1908c1cdfcccecb663f9`.
- Extract then run:`python3 -I -S scripts/verify_reproduction_v35_1.py`. No packages,network,weights or credentials.
- Independently replayed:2source tables,10prefixes,10shortlists,300adaptive decisions,60output-token/provenance records,30relevant model selections,70arms,800journal charges,120paired comparisons,240Decimal scores,family aggregates/constraint diagnostics.
- Successful harness30.153254s maintenance time; clean replays3.001s on3.10 /2.117s on3.12. No new experiment charge.
- Receipts/logs:`artifacts/reproduction_v35_1/`; report:`reports/reproduction_v35.md`; protocols/freezes:`reports/protocol_v35_reproduction.*` and `reports/protocol_v35_1_reproduction.*`.
- Build:`.venv/bin/python scripts/build_reproduction_v35_1.py --output <new-local-zip>`; builder refuses overwrite.
- Executed validation:`.venv/bin/python scripts/test_reproduction_v35_1.py --archive output/llm_escalation_v34_reproduction_v35_1.zip --second-python /Users/mayankdhingra/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
- Full suite:`.venv/bin/python -m pytest -q`; historical audit:`.venv/bin/python scripts/audit_history_v30.py`(2,758frozen references passed).

## Failure and versioned correction

Initial V35 passed on3.10 but failed on3.12. Diagnostics found5of200saved joint-control decision states differed because Python3.12 builtin float summation handles differently ordered triples differently from the historical reduction. V35.1 explicitly reproduces the original left-to-right binary64 arithmetic. Original experiment code/trajectories/scores were untouched; this is not evidence that the NumPy optimizer itself changes on3.12. The unchanged failed archive is`output/llm_escalation_v34_reproduction.zip`; use the corrected filename above. Failed receipts and diagnosis:`artifacts/reproduction_v35/`. A pre-archive README filename mismatch was resolved with an identical compatibility file and logged separately.

## Scientific result and untested scope

V34 assigned-ID LLM versus size-aware shortlist3NN:−0.3015% feasible-runtime gain,1win/6ties/3harms. Static rank comparison+1.3495%; full joint3NN−1.6470%; runtime3NN−2.6023%. Across three presentations versus runtime3NN:0wins/19ties/11harms. Raw evidence and full report:`results/v34_constrained/`,`reports/constrained_v34.md`.

Two exposed families; runtime-only prompts evaluated retrospectively with a research size cap. No size-aware inference,unseen-system routing benefit,application validation or actual deployment savings established. V35.1 adds no scientific samples. Same-host cross-interpreter reconstruction is not a second-machine reproduction,fresh inference or verification of model weights. The archive reproduces V34 and its needed dependencies,not all intermediate studies. Older V26/V25 archive unchanged.

## Remaining allowance and next action

Experiment/download ledgers byte-identical to pre-V35. Runtime2281.347753/3600s; remaining1318.652247s. Follow-up calls200/200(300includinginitial); recorded accesses9,108; physical trials1,274. Downloads4,518,268,306bytes total/4,098,574,535model bytes. No new inference,labels,physical trials,downloads,external spend,cloud,push,publishing or contact. No ongoing/background job.

**Single next action:** run the corrected archive on a second machine for independent validation before more collection. Scientific follow-up remains`reports/next_experiment_v34.md`: define application quality/practical gain,retain strong controls,reserve untouched groups,and obtain an explicit bounded local-call extension or truly compatible cache. Generic continuation does not expand the exhausted inference allowance.
