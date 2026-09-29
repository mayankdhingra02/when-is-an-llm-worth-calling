# Resume checkpoint: V177 manuscript–package consistency, cited earlier experiments, revised repeat plan

No acquisitions, model requests or downloads. Details are in `reports/audit_bundle_v177.md`.

- **Manuscript.** *How the study evolved* and *Data Availability* now separate the project archive from the review package. The controller transfer sentences are corrected: V132 controllers were applied to WavPack/FFTW, V147 controllers to Hadoop, and the Table 10 controllers to Memcached and the native systems. All of these made zero calls. Table 11 is narrowed.
- **Package.** `output/llm_escalation_audit_v177.zip` adds the V131/V132/V134/V136 records and their verifiers. The four receipt-only checks are labelled "not rerun". Its hash and test result are in `artifacts/study_v177/`.
- **Plan.** `reports/proposal_v177_matched_repeat.md` adds the primary-comparison, early-stop and in-flight-cost rules. It is still not frozen or authorized.

Replay:

    .venv/bin/python scripts/check_tables_v176.py
    .venv/bin/python scripts/seal_research_v177.py --verify-only

---

# Resume checkpoint: V176 wording fixes, table checker, reviewer audit bundle, draft repeat plan

No acquisitions, model requests or downloads. Details are in `reports/audit_bundle_v176.md`.

- **Manuscript.** Three wording corrections requested in review:
  - the 3B/8B models "never achieved a baseline-set win";
  - DUNE is described by mean losses;
  - useful-case counts are stated as 11/10/5.

  The new table checker `scripts/check_tables_v176.py` then found four values the paper had rounded twice: gpt-oss draw-1 headroom 0.52 (was 0.53), loop headroom 0.86 (0.87), loop log-ratio −2.48 (−2.49), and native cvc5/Qwen3-8B +0.16 (+0.17). These are corrected. The checker now passes: 80 table rows and 12 in-text numbers.
- **Audit bundle.** `output/llm_escalation_audit_v176.zip` is a private review copy; the DeepPerf and Tuneful tables have unresolved redistribution rights. Its README is `BUNDLE_V176_README.md` and its table map `TABLE_MAP_V176.md`. The ZIP's hash and counts are in `artifacts/study_v176/bundle_receipt.json`. Reproduction was tested from the unpacked ZIP in a fresh environment; see the report for the result.
- **Draft plan.** `reports/proposal_v176_matched_repeat.md` covers the full-cohort matched repeat: 2 one-shot + 2 loop draws, a fixed stopping rule, about $2.27 expected, and a $3.00 hard cap. It is not frozen, not authorized and not run.

Replay:

    .venv/bin/python scripts/check_tables_v176.py
    .venv/bin/python scripts/seal_research_v176.py --verify-only

**No paid run is authorized.**

---

# Resume checkpoint: V175 second manuscript revision (post-hoc analysis, no new collection)

A second external review of `paper/overleaf_v173/main.tex` was addressed. Details are in `reports/revision_v175.md`. `scripts/revision_v175.py` writes `results/v175_revision/analysis.json` (post-hoc, exploratory; zero acquisitions, model requests or downloads).

- **Deployable classical selector.** It trails the reference by −2.58% (ecosystem-balanced) and −1.29% (case-weighted). Its only switch (GP-EI on DUNE) lost about 45% on two cases. The LLM's narrower gap to it mostly reflects the policy's loss.
- **Routers, reweighted without retraining.** The best controller exceeds never calling by at most +0.022 pp (ecosystem), +0.019 (engine) and +0.011 (case). The V154 BORA-inspired and rank-reliability rules are negative under all weightings. Under case weighting, always calling the gpt-oss loop (+0.40%) beats every controller. Native exception: +0.15% from a single call.
- **Matching.** Of the 72 arm–case pairs with an LLM gain >1%, a prespecified cheap alternative did at least as well in 61, came within 1% in 3, and trailed by >1% in 8 (the baseline-set wins).
- **Cost wording.** $1.38 is total recorded spend: $1.374 for the arms plus $0.003 for probes and the stopped attempt. One in-flight request has unknown cost.

The V174 paper is kept at `paper/overleaf_v173/previous/main_before_second_review.tex`.
- Replay: `.venv/bin/python scripts/revision_v175.py --check`.
- Tests: `.venv/bin/pytest -q -p no:cacheprovider tests`.
- Seal: `.venv/bin/python scripts/seal_research_v175.py --verify-only`.

**No approval stands open for paid inference.** A matched gpt-oss repeat needs a new owner decision and a frozen protocol first.

---

# Resume checkpoint: V174 manuscript revision (post-hoc analysis, no new collection)

An external review of the draft paper (`paper/overleaf_v173/main.tex`) was addressed. `scripts/revision_v174.py` produces `results/v174_revision/analysis.json` (post-hoc, exploratory; zero acquisitions, model requests or downloads).

**Findings that changed the manuscript's claims:**
- **Weighting.** "Every model lost on average" holds only for the prespecified ecosystem-balanced (and engine-balanced) average. Case-weighted, the gpt-oss-120b loop gains +0.40% (GP-EI +0.49%).
- **Deployable classical policy** (chosen leave-one-ecosystem-out): gpt-oss arms are at −0.44% to −1.15% ecosystem-balanced, and +0.86%/+1.75% case-weighted for draw 2 and the loop. The local models trail clearly.
- **Routers rerun on Qwen3-14B and the gpt-oss arms,** with the unchanged V151 code (it reproduces V151 exactly for the 3B/8B models): no improvement over never calling beyond +0.02 percentage points.
- **Extended baselines.** One of Qwen3-14B's two baseline-set wins is matched by random prototypes; the gpt-oss wins are unchanged.
- **Native headroom** (V165 exhaustive data): ripgrep kept up to 12.7% headroom that no continuation found; hnswlib had none.
- **Terminology.** "LLM-specific win" is renamed "baseline-set win". The router claim is narrowed to the evaluated controllers. "Pre-registered" is replaced by "prospectively frozen on previously studied systems".

The pre-revision draft is kept at `paper/overleaf_v173/previous/main_before_review_revision.tex`. Replay: `.venv/bin/python scripts/revision_v174.py --check`. Seal: `.venv/bin/python scripts/seal_research_v174.py --verify-only`.

The V173 status below remains current for everything else.

---

# Resume checkpoint: V173 (SNAP2's model, hosted) complete

Start with `reports/research_assessment_v173.md`, then `reports/snap2_model_v173.md` (generated tables), `reports/research_assessment_v172.md` and `reports/audit_v171.md`. The V172 status this replaces is preserved in `artifacts/study_v173/previous_snapshot/STATUS.md`.

## Result

**The frozen V173 decision is `headroom_at_snap2_model_router_question_needs_fresh_cohort`, and it is fragile.**
- `openai/gpt-oss-120b` (SNAP2's model) reached LLM-specific wins in **2 of 7 ecosystems in arm A's first draw**, exactly the pre-registered threshold.
- Arm A's second draw and arm B (the SNAP2-style iterative loop) reach **1 ecosystem** each.
- The two HIPAcc wins that decided draw 1 are marginal (+1.7% and +1.9%) and do not recur in the other runs.
- **Post-hoc** (labeled; `results/v173_analysis/posthoc_sensitivity.json`): with a 2% margin, or requiring a win to recur, every run falls to 1 ecosystem (Spark/Hadoop).

**One replicated LLM-specific win, the first in this study.** `spark::bayes_11` beats every cheap switch in all three gpt-oss runs, by +8.3% one-shot and +31.5% iterative. No local model found it.

**On average gpt-oss still loses to continued sequential 3NN.**

| | Mean gain vs sequential | Hindsight headroom |
|---|---:|---:|
| gpt-oss, three runs | −3.1% to −3.7% | 0.5–0.9% |
| Qwen3-8B | −5.2% | — |
| GP-EI | — | 1.28% |

The iterative SNAP2-style arm is the best gpt-oss interface.

**Implication.** LLM-specific value exists at SNAP2 scale but is rare and concentrated in one ecosystem. A router cannot be tested on this cohort, and a fresh, headroom-gated cohort with positives in several groups would be required.

## What ran (owner-approved paid inference; `artifacts/study_v173/authorization.json`)

- **Service and interfaces.** OpenRouter → `openai/gpt-oss-120b`, reasoning effort `medium`, with strict JSON-schema output equivalent to the V141–V172 grammar.
- **Provider.** DeepInfra `turbo` (bf16), chosen by the probe rule declared in advance.
- **Arm A.** V172's interface, two draws: **140 of 140 valid**, 1,400 recorded acquisitions.
- **Arm B.** 5 rounds × 2 proposals with trajectory feedback, collisions and retries, over 70 cases: 348 model rounds, 2 fallback rounds, 700 acquisitions.
- **Cost.** **$1.38** over 539 recorded attempts (513 responses, 26 HTTP 429). Plus one request in flight when A1 was stopped, with unknown cost.
- **Verification.** Independent replay (`scripts/verify_v173.py`) passed: 0 errors, primary recomputed (2/1/1), 539 requests reconciled, leakage, target and selection mutations rejected.
- **Amendments,** all before any target was read, documented and frozen:
  1. After an operator-stopped A1 (4,000-token truncation plus rate limits): output caps 16k/8k, bounded 429 backoff, provider probe rule. A1 is preserved.
  2. Continuation stages for wall-capped stages, and arm B in eight smaller stages.
- **Tests.** Full suite passes (see `artifacts/study_v173/all_tests.log`).

## Replay commands (no new requests)

    .venv/bin/python scripts/analyze_v173.py --check
    .venv/bin/python scripts/report_v173.py --check
    .venv/bin/python scripts/verify_v173.py
    .venv/bin/python scripts/analyze_v172.py --check
    .venv/bin/pytest -q -p no:cacheprovider tests
    .venv/bin/python scripts/seal_research_v173.py --verify-only

Collectors (`collect_v173.py`, `drive_v173.py`) are create-once and must not be rerun into existing stage directories. They would also spend money.

## Counters (`artifacts/study_v173/closeout.json`)

- **Model starts.** Cumulative 5,487: 514 new V173 generations, counting the in-flight one.
- **Recorded-table charges.** Cumulative 45,113 (2,100 new).
- **Downloads.** Retained 19,381,968,173 of 20 GiB; model payload 18,128,110,983 of 19 GiB (unchanged).
- **Paid spend.** $1.38 reported of a $3 client cap and the owner's $5 credit. The OpenRouter key reported a **$100 limit**, not the planned $5; **lowering it to $5 or deleting the key is recommended.**
- **No approval stands open.** The V173 approval covered V173 only; any new paid run needs a new explicit owner decision.

## Housekeeping

- The API key is in `~/.config/llm-escalation-study/openrouter_key` (owner-only). It is never copied, hashed or sealed. **Delete the file and revoke the key on OpenRouter** when no further hosted runs are planned.
- The Qwen3-14B weights can be moved off-machine (they are pinned by hash, not sealed). SmolLM3 and Qwen3-8B must stay.

## Single most important next action

**Write the paper around the graded result:**
- local 3B–14B models: no LLM-specific headroom;
- SNAP2's model: rare, ecosystem-concentrated wins, strongest with iterative feedback, still losing on average;
- routers: not learnable across systems on present evidence.

Report the frozen V173 decision verbatim, with the labeled post-hoc sensitivities.

**Optional:** two more pre-registered arm B draws (~$1.77) would settle whether ≥2 ecosystems recur. That exceeds the $1.62 left under the $3 cap and needs the owner's decision.

No work continues outside this session.
