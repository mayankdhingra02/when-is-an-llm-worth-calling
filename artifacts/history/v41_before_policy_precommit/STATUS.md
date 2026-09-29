# STATUS — V41 new six-family classical study executed; model extension pending

Updated 2026-09-25. Resume from this file, `reports/transfer_v41.md`, `reports/protocol_v41_transfer.md` and its immutable freeze, `data/manifest_v41.json`, and the V41 collector/model runner. Do not reread the full deep-research report. Prior mutable state is preserved in `artifacts/history/v41_before_collection/`.

## What actually ran

Six previously unacquired local-study families: BerkeleyDB C, Dune, LLVM, HIPAcc, SaC, OpenVPN. Five seeds each; 30 common ten-label prefixes, 210 classical continuations (seven per prefix), 2,400 newly acquired recorded outcomes. Every completed arm has20 logical evaluations. No new LLM call or physical trial. Source audit resolves objective directions; OpenVPN maximizes throughput. Dune fixes cells=50 in the recorded encoding. Feature-only fixed subsampling bounds larger domains to1,024 candidates. These are table-search adaptations, not live utility claims.

Concrete finding: full-domain sequential3NN vs batch-shortlist3NN has equal-family mean gain1.415%,8wins/16ties/6harms; six-family bootstrap95% interval[0.062%,3.290%], exact sign-flip p=.15625. Descriptive, not strong statistical/generalization evidence. All controls and cases remain reported. No new model/router result; journal readiness not established.

## Evidence and commands

- `results/v41_transfer/`: raw acquisitions.jsonl,30 saved prefixes with predecision features/prompts,210 arms, collection seal, all60 model token preflights,210-row classical_cases.csv, summaryJSON and PNG/SVGfigure.
- `artifacts/study_v41/`: source hashes, recursive exposure audit(1,688 JSON/JSONLfiles; two reviewed metadata-only exceptions), collection/test/analysis logs, replay verification, expected model-gate failure, exact requested extension.
- `reports/source_audit_v41.md`,`reports/transfer_v41.md`,`reports/protocol_v41_transfer.freeze.json`(103 frozen inputs).
-285tests passed:264 existing +21 new. Default pytest only finds tests/synthetic; use explicit full command below to include frozen V41 tests.
-30prefixes,210arms,2,400events independently checked against acquired source targets and deterministic branch/prompt replay. No hidden unacquired target was parsed for verification.

```sh
.venv/bin/python scripts/fetch_sources_v41.py
.venv/bin/python scripts/admit_v41.py
.venv/bin/python -m pytest -q tests/synthetic tests/test_transfer_v41.py
.venv/bin/python scripts/freeze_v41.py
.venv/bin/python scripts/run_transfer_v41.py
.venv/bin/python scripts/analyze_transfer_v41.py
.venv/bin/python scripts/run_models_v41.py
```

Last command intentionally failed before loading a model: exact extension not granted. Do not describe it as inference. Initial source retrieval hit sandbox DNS restrictions; approved escalated retrieval succeeded. Admission initially caught52candidate mentions; all were in two metadata-only zero-acquisition V13 reports. Exceptions are explicit and hash-recorded. No other candidate prior outcome hit. No experiments were silently restarted or discarded.

## Remaining limits and next action

Collection/preflight charged9.782281s; replay/analysis/rendering19.103170s. Cumulative experiment time2560.413959/3600s; remaining1039.586041s. Requests230/230 follow-up(330includinginitial). Recorded outcome accesses12,008 cumulative; physical trials remain1,274. Primary-source download899,606bytes, no model/data downloads. USD0. No active model/process, remote publication, push or author contact.

**Single most important next action: approve and execute the already prepared60-call local extension, cap230→290, with unchanged3600s global cap,700s stage,maximum600new outcomes,zero retries/downloads/spending.** Exact request is `artifacts/study_v41/requested_extension.json`. Both installed model tokenizers accept all30 frozen prompts(897–3302tokens,cap4096). Do not create a granted authorization until user approves this exact bounded request. New grant must bind freeze SHA256 `9ada494788668ba51ec4e871980afb616e15bbc7f9d1e5216d74d409dcfa5c18` and the precise fields enforced in `scripts/run_models_v41.py`.

Classical outcomes are now exposed; no outcome-driven changes to the frozen LLM treatment, primary contrasts or thresholds. Preserve source/collection seals and all existing V38–V40 artifacts. V41 only transfers the old sealed V6 controllers; a new learned-router study needs a separately frozen development/test design. Missing evidence remains application correctness/equal quality/security, independent model family, robust unseen-family routing, measurement noise and novelty against close prior work. Six extra classical families alone do not establish Q2 readiness.
