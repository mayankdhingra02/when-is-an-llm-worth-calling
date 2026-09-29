# STATUS — V39 portable V38 reconstruction completed

Updated2026-09-25. Resume here, [reproduction report](reports/reproduction_v39.md), [V38 scientific report](reports/size_prompt_v38.md), and relevant code. Previous STATUS/README/ledgers are archived under `artifacts/history/v39_before_reproduction/`.

**New concrete result:** corrected V38 archive reconstructs outside the checkout using standard-library-only Python3.10.13 and3.12.14 with identical scientific outputs. All10corruption controls fail as intended; restored replay and byte-identical rebuild pass. 258project tests pass in1.30s. No new scientific data or model calls.

Archive: `output/llm_escalation_v38_reproduction_v39_1.zip`; 4,041,210bytes,553content files plus manifest; SHA256`79d622f175347a098629bdaeb8b05faac1b885fea1b99be23e3a4eccec686b0a`. Extract,enter its root,run `python3 -I -S scripts/verify_reproduction_v39.py`. This verifies30response decodings,300charged vectors,150paired comparisons,15summaries and200exact classical decisions plus historical V35.1 replay. No network/model weights/packages required. Input tokens remain bound to recorded provenance,not independently retokenized.

## Actual commands and receipts

```
.venv/bin/python scripts/build_reproduction_v39_1.py --output output/llm_escalation_v38_reproduction_v39_1.zip
.venv/bin/python scripts/test_reproduction_v39_2.py --archive output/llm_escalation_v38_reproduction_v39_1.zip --second-python /Users/mayankdhingra/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
.venv/bin/python -m pytest -q
.venv/bin/python scripts/audit_history_v30.py
```

Final validation: `artifacts/reproduction_v39_2/validation.json`,per-interpreter JSON,corruption checks,restored replay,deterministic rebuild. Build and258-test receipts: `artifacts/reproduction_v39_1/`. Current final integrity receipt: `artifacts/reproduction_v39_2/final_checks.json`.

Failures retained: initial V39 archive lacked an older request-start log; V39.1 fixed package completeness. The first checksum test then failed its harness expectation because the earlier frozen-source guard correctly rejected it. V39.2 corrects that expected message only. Both earlier failures and frozen versions remain available; scientific files and the portable verifier were unchanged. The working deliverable is the V39.1 ZIP; V39.2 names its successful validation harness.

## Scientific result and limits remain unchanged

V38:30real local calls/300newrecorded vectors. Primary assigned-ID gain1.7534% over exact joint3NNshortlist (2wins,7ties,1harm); across all30cases versusruntime3NN:0wins,24ties,6harms. A narrow positive prompt comparison does not establish worthwhile escalation. All150comparisons retained. Two exposed families,not held-out routing evidence.

No new inference,acquisitions,physical trials,downloads,spend,cloud,push,publication or contact. Resource/download ledgers are byte-identical:230/230follow-up calls,330includinginitial;2530.796723/3600experiment seconds,1069.203277remaining;9608recorded vectors;1274physical trials. Read-only verification/packaging maintenance times are recorded separately. No task continues in the background.

Untested: separate physical-machine V38 reconstruction,fresh inference/logits,input retokenization in the portable checker,physical uncertainty/correctness,application utility,and generalizable benefit-aware routing. V35.1/V37are historical V34snapshots; latest archive is V39.1.

**Single next action:** an independent reviewer runs the portable V38 archive on another machine and reviews the complete finding with Tim. Do not infer extra model-call permission from continuation;230calls remain exhausted. Any future collection needs a new bounded protocol grounded in untouched families and opportunity beyond strong cheap controls.
