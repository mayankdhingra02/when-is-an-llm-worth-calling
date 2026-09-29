# STATUS — V113 completed; native timing reliability is the next blocker

Resume here. No model, NGINX, or solver experiment remains running. No remote upload, spending, or background job is queued. Read `reports/research_readiness_v113.md` and `reports/validation_v113.md`, not the original long discovery report again.

## Latest concrete result

V113 freshly confirmed all 30 configurations selected by the V94 LLM, batch 3NN, and sequential 3NN branches: two numerical engines × five seeds × three arms. **90/90 new native acquisitions completed; all 270 physical solver outputs passed independent certificate recomputation.** Zero failures/unattempted slots; 47.387 s collection; no new inference or downloads. These are new real software timings, not synthetic fixtures or cached objective scores.

No case beat both controls at the frozen 5% margin. However, **5 of 8 contrasts selecting identical configurations showed apparent timing differences of at least 5%**, with a maximum 23.68%. Median relative range across the three fresh labels per incumbent was 35.92%; 26/30 incumbents exceeded 10%. This posthoc negative-control diagnostic weakens confidence in precise native-runtime effect magnitudes. It is not evidence of causal LLM harm or a population false-positive rate. Preserve all cases and the original V94 findings; do not cherry-pick the clearer negative averages.

The original search budget stays 20. These are three separately charged validation acquisitions per incumbent, each containing three physical solves. Search plus validation would cost 23 acquisitions/69 physical solves per deployed arm. Actual V94 plus V113 collection is 590 native acquisitions and the original 100 real model requests. Reusing their frozen selected configurations does not make original inference free.

Evidence: `results/v113_validation/` contains requests, raw vectors, physical starts/returns, timing, failures/cleanup fields and ledgers. `results/v113_analysis/` contains independently verified comparisons, identical-configuration diagnostics, CSV and figures. `reports/protocol_v113.md` and `.freeze.json` predate the new timings. No new router was fitted.

## NGINX work completed in this continuation

| Stage | Actual attempts | Byte-valid responses | Outcome |
|---|---:|---:|---|
| V106 C client | 6 | 6,291,456 | Client CPU screen failed |
| V107 memcmp client | 6 | 6,291,456 | Reference feasibility screens passed |
| V108 shorter workload | 6 | 786,432 | Reference screens passed; 768/768 native syntax checks passed |
| V109 classical smoke | 40 | 5,242,880 | Correct paired B20 arms; expanded domain exposed short runs/client saturation and unstable confirmations |
| V110 four-process client | 6 | 6,291,456 | Six reference/stress screens passed; reference range 8.15% |
| V111 expanded-domain smoke | 11 of 40 intended | 10,900,298 | 10 valid prefix attempts, one charged 60 s timeout, 29 unattempted |

V111 row 758 timed out in all four clients after 414,538 correct responses; this is an unfinished workload, not a 60 s successful completion. Owned clients/server all exited. The frozen stopping rule forbids more dependent local NGINX LLM collection on this workload. No configuration was dropped or retried. The 768 legal settings are not 768 independent systems or proven distinct runtime distributions; NGINX is now exposed development.

V112 names a prepared seven-choice semantic model adapter and synthetic parser/pre-decision tests. **No V112 model call, native continuation, paired protocol freeze or measured result exists.** It remains unexecuted because the native measurement prerequisite failed.

## What remains from the model studies

V103 is still the latest model-quality comparison: 36 actual Qwen3-8B requests, six exposed systems, two seeds, two modes, 24 intended conditions and 240 recorded acquisitions. Thinking had 10/12 valid finals; nonthinking 12/12. Neither mode had a valid >=5% win over BOTH strong controls. Group-first mean gains versus sequential 3NN were -7.64% and -6.52%; the two thinking fallbacks remain visible. This is scoped exploratory evidence, not a useful learned router or a universal negative claim.

V94's native negative observations remain preserved but must now be read with V113's timing qualification. The recorded-table results are separate and were not remeasured by this timing check. Enough untouched independent system groups, useful benefit-aware escalation, reliable native effect magnitudes, and journal readiness remain unestablished.

## Single next action and resource needed

**Run the fixed-incumbent confirmation packet on a second, otherwise quiet Mac or Linux computer.** Local packet: `output/v113_replication/` (16 files, 692,571 bytes before any packaging). It contains 30 fixed configurations, the 90-slot schedule, two small inputs, certificates and bounded runner. Python 3.10, NumPy 2.2.6, SciPy 1.13.1 and HiGHS 1.7.2; CPU only, no GPU/model download/API. Limits: 30 s/2 GiB per worker, 1,800 s whole stage, 90 acquisitions/270 planned solves. Preflight passed locally with zero objectives. It refuses same-host-name execution as a practical guard, not proof of hardware independence. Linux and independent-host execution remain untested.

An asynchronous question asks whether the user has a second Mac/Linux computer; no answer is assumed and no transfer is authorized merely by asking. Existing access is to this Mac. The packet was not uploaded; standalone HB dataset redistribution terms remain unresolved, so this private packet is not a license-cleared public release. See its README and original V94 provenance. Do not silently provision cloud resources or spend money.

If no other host is available, finish review of the recorded-data negative study with explicit native limitations; do not repeatedly tune exposed prompts or workloads to obtain a positive result. A Q2 label is not an experimental success criterion and acceptance cannot be guaranteed.

## Tests, reproducibility, integrity

Full suite: **862 passed, 14 third-party deprecation warnings, 23.80 s** (`artifacts/study_v113/tests_all.log`). New synthetic checks reject corrupted native counts, branch labels, schedules, budgets, request configurations, solver labels and certificates; fixtures remain separate. Figures were visually inspected, including a correction showing the V111 timeout as unfinished and its confirmations as unattempted. Replay/derived-output checks are in the same artifact directory.

Read-only evidence replay:
```
.venv/bin/python scripts/report_nginx_native_v106.py --stage 106
.venv/bin/python scripts/report_nginx_native_v106.py --stage 107
.venv/bin/python scripts/report_nginx_native_v106.py --stage 108
.venv/bin/python scripts/verify_classical_nginx_v109.py
.venv/bin/python scripts/report_nginx_v110.py
.venv/bin/python scripts/verify_classical_nginx_v111.py
.venv/bin/python scripts/analyze_validation_v113.py
.venv/bin/python scripts/report_validation_v113.py
.venv/bin/python output/v113_replication/run.py --check-only
.venv/bin/python scripts/seal_validation_v113.py --verify-only
```
Do not rerun collection into existing output folders. New execution requires a new protocol/output namespace and separately counted allowance. Original native commands, matching local compiler and process-only SDK selection are in `artifacts/study_v110/REPRODUCE.md`. No system settings or installations changed.

The combined V113 seal includes V106–V113 artifacts and follows V105's immutable seal SHA256 `2bda57422f27ae174e3b86648b0cf7b7a7aa9286e39cec5ddb0e81bcbcbd7077`. V105 root documents are preserved under `artifacts/study_v106/previous_snapshot/`; older history is resolved by snapshot mappings, never rewritten. Check the V113 seal verification receipt for the resulting manifest hash and file counts.

## Cumulative measured cost and remaining limits

- Real model requests: 3,938, unchanged. Recorded-table acquisitions: 27,978, unchanged.
- Numerical native acquisitions: 880 (prior 790 + 90 new validations).
- NGINX: 81 charged attempts including original V105 six; 35,853,130 byte-valid HTTP responses, including partial timeout responses. Local transfers are not internet downloads.
- Older native ledgers unchanged: DuckDB 78 physical, H2 299, Kanzi 1,265, RocksDB 350. Their units remain separate.
- Download total: 9,875,903,117 / 10 GiB; 861,515,123 bytes remain. Model payload: 9,126,358,023 / 9 GiB. No new downloads in V106–V113.
- External spending: zero. Historical missing token/duration fields remain unknown; electricity/hardware cost unknown. Actual validation/paired-collection costs are separate from hypothetical single-policy deployment costs.
- Existing model: owner Qwen3-8B-Q4_K_M, revision `7c41481f57cb95916b40956ab2f0b139b296d974`, model SHA256 `d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785`, local llama.cpp b11146. No new model is needed for the immediate next action.
