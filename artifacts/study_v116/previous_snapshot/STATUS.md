# STATUS — V114 sampling replication and V115 single-control comparison complete

Resume here. All new experiments finished; no model, native benchmark, or background job remains running. Read `reports/research_readiness_v115.md`, `reports/sampling_v114.md`, and `reports/portfolio_v115.md`. Do not repeatedly reread the original discovery report or recollect old outcomes.

## Latest concrete research result

V114 collected **36 new real local Qwen3-8B responses**: three model sampling seeds (1009, 2027, 3041) for each of 12 unchanged ten-evaluation prefixes, across six exposed software-system groups and optimization seeds 11/37. Every answer was valid; no fallback, retry, transport failure, or unattempted condition. The server exited normally after **293.705 s**, with peak sampled RSS **6,808,207,360 bytes**, below the existing 8 GiB cap.

All 36 continuations were independently scored with ten charged recorded-table acquisitions each, maintaining B20. **Zero of 36 improved by >=5% over BOTH original strong controls.** Group-first mean gains: **-2.67% versus batch 3NN; -6.45% versus sequential 3NN**. Four of twelve prefixes changed selected configuration sets across sampling seeds; only two changed the final incumbent objective. Joint >=5% benefit classification did not change. Sampling replicas are nested observations, not additional independent systems. These are actual model outputs and recorded-table outcomes, not fresh native runtimes.

V115 then addressed the objection that the joint screen compares two separate controls. It executed **one** classical continuation alternating prefix-ranked batch 3NN and updated full-domain sequential 3NN, five turns each, under the same ten remaining evaluations. All 12 prefixes completed, acquiring **120 new recorded outcomes**. No other branch's labels were used. Against this single portfolio, the same 36 LLM replicas produced **9 wins, 15 ties, 12 losses**; largest win **3.34%**, none >=5%, group-first mean **-2.25%**. Seven replicas gained >=2%, so do not claim absence of all benefit. This follow-up was frozen before its own acquisitions but after V114 outcomes, and is explicitly exploratory. Keep the original stronger controls too; the blend can sacrifice their quality.

These additions strengthen a scoped negative-result paper candidate. They do not establish positive benefit-aware routing, useful prediction on unseen systems, universal LLM harm, or Q2 readiness. Do not keep adjusting prompts, seeds or thresholds on this exposed cohort to obtain a positive result.

## Evidence and executed commands

- V114 frozen protocol/config/jobs: `reports/protocol_v114.md`, `.freeze.json`, `configs/study_v114.json`, `artifacts/study_v114/jobs.json`.
- Real model inputs, templates, raw responses, requested/applied seeds, timing/tokens, starts, choices and resource ledger: `results/v114_reasoning/`.
- All 360 charged objective acquisitions and B20 states, nested sampling summaries, CSV and figures: `results/v114_analysis/`.
- V115 frozen protocol and 120 actual portfolio acquisitions: `reports/protocol_v115.md`, `.freeze.json`, `results/v115_portfolio/`; independent comparison/figures: `results/v115_analysis/`.
- Execution/replay/test/derived-output receipts: `artifacts/study_v114/` and `artifacts/study_v115/`.

Actual collection commands, already completed, were `scripts/collect_sampling_v114.py`, `scripts/evaluate_sampling_v114.py`, and `scripts/run_portfolio_v115.py`, all using `.venv/bin/python`. Do not rerun them into existing directories. Every output is create-once. A new collection requires a new frozen namespace and separately counted allowance; V114's 36-call allowance is consumed.

Safe saved-evidence replay (no new labels or inference):
```
.venv/bin/python scripts/verify_sampling_v114.py
.venv/bin/python scripts/report_sampling_v114.py
.venv/bin/python scripts/analyze_portfolio_v115.py
.venv/bin/python scripts/plot_portfolio_v115.py
.venv/bin/python -m pytest tests -q
.venv/bin/python scripts/seal_sampling_portfolio_v115.py --verify-only
```

Full suite: **877 passed, 14 third-party deprecation warnings, 29.99 s**. New tests verify fixed-prefix sampling coverage, strict request/output/acquisition caps, tamper rejection, equal group weighting, portfolio alternation, budget and prefix isolation. Synthetic fixtures are separate and never treated as measured LLM output. Figures were visually inspected; replay and byte-identical derived-output checks are saved.

Pre-execution template substitution initially produced a nonexistent runtime import. The initial collector/freeze bytes are preserved under `artifacts/study_v114/preflight_correction/`; the corrected freeze documents restoration of the existing pinned V103 runtime before any call. Independent verification initially aliased and mutated its expected prefix lists; disk comparisons showed all saved prefix/control pairs matched. The verifier now clones state. Its initial failure is retained. No scientific response, objective value, collection code after freeze, or primary criterion was changed by that verifier correction.

## Preserved native limitation

V113 completed 90 new native confirmations and independently checked all 270 solver outputs. Five of eight contrasts selecting identical settings nevertheless differed by >=5%; largest 23.68%. Median relative range across repeated incumbent labels was 35.92%. This weakens precise native-runtime effect claims; it does not invalidate the separate recorded-table trace results. V94/V97 original evidence and failures remain preserved, with their existing limitations.

NGINX V111 stopped under its frozen rule: ten valid prefix acquisitions, one charged 60 s timeout (row 758), 29 unattempted slots. All owned clients/server exited. No NGINX LLM experiment ran. V112 is a synthetic-tested, prepared semantic adapter only, not a measured model result. Do not silently restart dependent collection on this failed harness.

## Single next action

**Independent validation remains the priority.** The concrete prepared resource is `output/v113_replication/README.md`: 30 frozen configurations, 90 charged validation acquisitions, 270 planned solves on a second, otherwise quiet Mac/Linux CPU host. Python 3.10, NumPy 2.2.6, SciPy 1.13.1, HiGHS 1.7.2; no GPU/model/API needed. Limits: 30 s and 2 GiB per worker, 1,800 s overall. Local preflight succeeded; second-host/Linux execution remains untested. Only the current Mac is available. A prior resource question about another host is unanswered; no access, paid provisioning, or transfer is assumed.

For a recorded-data-only study, a separately admitted independent software-system cohort would instead address generalization. The existing reserved/admission candidates still require source, utility/schema and exposure checks before outcomes. V114 metadata-only consideration of Zopfli/OptiPNG did not download, admit or run another benchmark. Do not silently treat old variants as independent groups.

The scoped negative contribution is ready for technical discussion, not a guaranteed journal tier. Review `reports/research_readiness_v115.md` before more exposed-cohort tuning. No emails, submissions, publication or remote pushes were made. The private replication packet is not a license-cleared public release; HB dataset redistribution terms remain unresolved.

## Cumulative costs and remaining limits

- Real model requests: **3,974** (prior 3,938 + 36). Recorded-table acquisitions: **28,458** (prior 27,978 + 360 + 120).
- V114 actual generated tokens: **720** from a 4,608-token allocation; actual reported prefill and summed full-context tokens both **59,286**. No missing usage in this new batch. Historical missing usage remains unknown.
- V115 collection/preparation: **3.458 s**; mean ten-turn portfolio loop **0.025289 s**, including indexed accesses. These are local computation costs, not fresh target-software runtimes or a model/cloud savings claim.
- Native ledgers unchanged this continuation: numerical 880 acquisitions; NGINX 81 charged attempts / 35,853,130 byte-valid responses including partial timeout responses; older DuckDB 78 physical, H2 299, Kanzi 1,265, RocksDB 350. Do not mix these units.
- Downloads unchanged: **9,875,903,117 / 10 GiB**, leaving **861,515,123 bytes**. Model payload **9,126,358,023 / 9 GiB**. Zero new downloads or external spending. No system setting or package installation changed.
- Actual new collection is 36 model calls and 480 recorded acquisitions. Historical saved prefixes/control acquisitions remain costed in old ledgers. A single deployed continuation uses one answer/one branch; choosing the best of three after scoring them would cost three calls and thirty continuation acquisitions, not the original ten.
- Existing model: owner Qwen3-8B-Q4_K_M revision `7c41481f57cb95916b40956ab2f0b139b296d974`; SHA256 `d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785`; local llama.cpp b11146. All 36 replicas used the unchanged V103 nonthinking interface and strict parser.

## Integrity checkpoint

The combined V115 seal includes V114–V115 measured evidence, code, reports and tests, following the immutable V113 manifest SHA256 `063c7a01e5274a0ec91fccd5056c0c89b1a5846b9272e1632de94d672aa44b09`. Previous root documents are preserved under `artifacts/study_v114/previous_snapshot/`. Historical manifests and raw outputs are not overwritten. See `artifacts/study_v115/seal_verification.json` for the new manifest hash and verified file/history counts.
