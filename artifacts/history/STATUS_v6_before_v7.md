# Status — 2026-09-24, v6 paired expanded smoke completed

## What actually ran

**30 new real local-LLM paired continuations completed on six new software families, five fixed seeds each. 46 tests pass.** This continuation completed semantic admission, a real finite-domain model adapter, a guarded collector, classical/projection controls, development-only controller fitting, held-out execution, analysis, verified figures and a generated pilot report. It did not stop at the v5 registry milestone.

Start with **reports/pilot_report_v6.md**, reports/admission_v6.md, reports/protocol_v6.md and data/manifest_v6.json. Read relevant code next; do not reread the initial deep-research report. Prior raw results and frozen v4/v5 snapshots are unchanged. Previous status is saved in artifacts/history/STATUS_v5_before_v6.md.

### Admission and frozen allocation

Seven families had explicit objective meanings in pinned primary case READMEs. Six were chosen by the pre-outcome SHA256(v6-bounded:family) rule:

- Development: MySQL 5.6.10, lrzip 530, Brotli 0.3.0.
- Held-out: VP8 v0.9.1, HSQLDB 2.1.0, PostgreSQL 10.0.
- OpenVPN was admitted as throughput maximization but not selected by this allocation.

All seeds [11,23,37,53,71] and variants stay in their family. MySQL/MariaDB and VP8/VP9 are grouped; Apache/SQLite/x264 stay excluded. All six measured feature tables are binary. The finite-domain interface has mixed-domain synthetic coverage, not empirical numeric-domain results. Other v5 candidate families remain unadmitted. Workload/revision contradictions and the Fast Downward quarantine remain documented.

### Executed experiment

- Per case: saved 10-label classical prefix; paired 10-label classical, uniform-projection and real LLM continuations; independent 20-label random baseline. Inclusive logical budget 20 per arm.
- 60 classical/random arms, 30 uniform-projection continuations and 30 real LLM continuations completed. Actual new acquired-label accesses: **1,800**. No live subject-system benchmarking was rerun.
- **32 local-model requests**: 2 separate synthetic format gates (4 ternary and 30 binary features) + 30 measured pairs. Both gates passed; all pairs completed; no retries, parse failures, fallbacks or dropped cases.
- Official pinned Qwen/Qwen2.5-0.5B-Instruct weights, revision 7ae557604adf67be50417f59c2c2f167def9a775. This run used CPU/float32; v3 used MPS. One batch of ten finite-symbol proposals per prefix, rather than v3's two batches of five. This is an explicit treatment adaptation.
- Lazy target acquisition and a durable acquisition journal; all nonselected objectives excluded. Frozen per-case hashes, exact prefixes and independent branch states. A started incomplete transaction fails closed pending journal audit; arbitrary automatic crash recovery is not claimed.
- Benefit/uncertainty controllers fitted only on three development groups and hash-sealed before the first held-out acquisition. All required policies evaluated, with hindsight and realized-rate random clearly diagnostic.

## Actual result

On 15 held-out cases across three families, the LLM materially helped versus classical in **2/15** and harmed in **3/15**, using the frozen .02 loss margin. Group-mean loss (lower better): never-escalate **0.061505**, always-escalate **0.074581**, hindsight oracle **0.055799**.

Both benefit-aware and uncertainty-only policies selected **0/15** calls. The matched random baseline also selected zero. This does **not** demonstrate useful benefit prediction or a routing advantage. Three test families remain insufficient for generalization.

A clearly labeled post-hoc diagnosis found **279/300 proposals exactly copied configurations from the original ten-observation prefix**. There were 281 unique-within-batch strings in total; this was mainly copying observed examples, rather than repeating one row ten times. Overall 289 proposals required feature-space projection, 279 collided with acquired rows, and none used fallback. Counts overlap. This diagnosis did not change prompts, policies, thresholds or collected results.

## Evidence and commands

| Evidence | Location |
|---|---|
| Generated current report | reports/pilot_report_v6.md |
| Semantic source admission / explicit targets | reports/admission_v6.md; data/manifest_v6.json |
| Pre-outcome protocol and source hashes | reports/protocol_v6.md; protocol_v6.freeze.json |
| All actual charged objective accesses | results/v6/acquisitions.jsonl |
| Prefixes and complete states | results/v6/prefixes/, classical/, paired/, checkpoints/ |
| Real model prompts, output, tokens and timing | results/v6/request_starts.jsonl; requests.jsonl; model_runtime.json |
| Separate synthetic real-inference gates | results/v6/feasibility/ |
| Development-only fitted policies | results/v6/router_seal.json; router_seal.sha256.json |
| Machine-readable outcomes / policy costs | results/v6/outcomes.json; summary.json; policies.csv; policy_cases.csv |
| Verified figures | results/v6/quality_cost_review.png, .svg; paired_gains.png, .svg |
| Post-hoc prefix-copy diagnosis | results/v6/proposal_diversity.json |
| Executed logs / independent verification | artifacts/study_v6/ |
| Collected-source snapshot | results/v6/source_snapshot/ |

Executed:

```sh
.venv/bin/python scripts/admit_v6.py
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/freeze_v6.py
PYTHONPATH=src .venv/bin/python -u -m escalation.study_v6
.venv/bin/python scripts/verify_v6.py
PYTHONPATH=src .venv/bin/python -m escalation.analyze_v6
.venv/bin/python scripts/diagnose_v6.py
.venv/bin/python scripts/report_v6.py
```

Collection refuses to overwrite the completed run. Verification is retrospective and makes no model calls or new optimizer acquisitions. Analysis uses the runtime ledger. Do not reset/delete ledgers or raw evidence to rerun. A new collection needs a new version/namespace and adequate authorized allowance.

Independent verification passed for all 30 pairs: exact source labels, complete source hashes, deterministic prefix/classical/projection/LLM replay, token IDs matching the real tokenizer/raw output and grammar, request/evaluation budgets, router-seal timing, and intact v4/v5 freezes. **46 tests passed in 1.28 s**. Figures were visually inspected; overlapping policy labels in the initial plot were grouped in a presentation-only follow-up, without altering data.

An initial added replay-verifier check failed because replay mutated its own in-memory prefix list. Fixed the verifier to clone replay states; no frozen collector or raw result changed. Preserved explanation: artifacts/study_v6/replay_verifier_failure.txt. Initial Matplotlib font-cache warnings were harmless; plotting completed and the follow-up uses project-local caches.

## Costs and remaining limits

- New actual model usage: **26,796 input tokens, 8,260 output tokens**, **275.683 s request wall time**; startup 4.278 s separately.
- New v6 collection/analysis/diagnostic ledger time: **313.808 s**. Source audit, coding, tests and verification overhead are separate.
- Cumulative experiment ledger: **1,471.1077/1,800 s**, **328.8923 s remaining**. Inactive (`active_since: null`).
- Shared follow-up attempt ledger: **98/100**, **2 remaining**. Including original v1: **198 historical attempts**. Unknown historical failed-request usage remains unknown.
- Historical charged label total: **3,458** (prior 1,658 + v6 1,800).
- Downloads unchanged at **1,412,812,979 bytes**, model bytes **999,602,607**. No new packages/model weights this continuation.
- **USD 0 external spending**. No cloud, paid endpoint, credentials, push, publish or contact. No background model/experiment process remains.
- Estimated deployment costs select one branch only and are separate from actual collection; timing excludes load, fit and unmeasured router-prediction overhead. No dollar-savings extrapolation.

## Remaining untested and single next action

**Next: a development-only paired experiment preventing the observed prefix-copying behavior, before scaling the router.** Keep current prefixes and projection controls, define the change before collection, and preserve all current evidence. This ablation is proposed, not implemented or run. A full three-family × five-seed arm would need 15 calls; only 2 remain, so the complete next arm requires explicit additional request allowance. No increase is assumed.

Still untested: improved proposal mechanism, stronger model, empirical nonbinary domains, and adequately broad untouched-system routing. All six v6 families are now exposed; do not adaptively reuse its three test families as an untouched test set. The larger 20-group plan is unexecuted and lacks validated final data/resources. See reports/next_experiment.md. Nothing is scheduled outside this session.
