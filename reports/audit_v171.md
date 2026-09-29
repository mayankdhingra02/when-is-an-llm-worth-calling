# V171: independent audit of the escalation evidence

Prepared 2026-09-28 by a new reviewer taking over after V170. This is a **post-hoc exploratory re-analysis** of sealed, already-exposed records. I read the outcomes before writing the analysis script, so nothing here is confirmatory. It made no objective acquisitions, model requests, downloads or native executions. Recorded-table and native cohorts are analysed separately and never pooled. Seeds stay inside their software system.

Machine-readable results: `results/v171_audit/audit.json`, produced by `scripts/audit_v171.py`. The script recomputes every contrast from raw per-arm values with explicit objective direction, and asserts agreement with the stored V151/V155 gains. Tests: `tests/synthetic/test_audit_v171.py`.

## 1. What the evidence establishes

**A. Always escalating to these models loses.** Both local models lose to continued sequential 3NN on an equal-group basis. The models are SmolLM3-3B and Qwen3-8B, quantized, called once per case for a batch of proposals projected onto a finite grid.

| Cohort | SmolLM3-3B | Qwen3-8B |
|---|---:|---:|
| Recorded tables, 70 cases, 7 ecosystems | −4.96% (log-ratio −4.56%) | −5.24% (−4.79%) |
| Native, V169/V170 same-session revalidation, 30 cases, 6 implementations | −9.05% (−7.32%) | −7.50% (−6.01%) |

This finding rests on:
- prospectively frozen stages;
- shared saved prefixes;
- charged budgets;
- complete failure denominators;
- two model sizes and 13 software groups.

It is the most robust result in the repository. My independent recomputation reproduces the published aggregates, including V151's −4.95588% and −5.23985%, and V155's GP-EI result of −2.1945% against sequential.

**B. The apparent LLM opportunities are not LLM-specific. This is new in V171.** The benefit target used throughout is LLM gain over *sequential 3NN*. Cheap non-LLM continuations from the same prefix produce at least as many such "opportunities".

In the recorded cohort, every arm acquires ten new rows after the same B10 prefix. Useful means >1% better than sequential; headroom is the equal-ecosystem mean of max(0, gain), a non-deployable diagnostic.

| Arm | Useful cases (of 70) | Hindsight headroom |
|---|---:|---:|
| SmolLM3-3B | 10 | 0.22% |
| Qwen3-8B | 5 | 0.18% |
| Random unseen rows | 11 | 0.32% |
| Adaptive neighbor | 10 | 0.48% |
| Fixed neighbor | 11 | 0.43% |
| GP-EI (ℓ=1, V155) | 22 | 1.28% |
| Random prototypes through the LLM's own projection (Spark/Hadoop only, 40 cases) | 13 of 40 | 3.48% |

- **No LLM-specific wins.** Zero of 140 model-cases beat sequential, random, adaptive *and* GP-EI each by >1%.
- **The LLM-useful cases coincide with cheap-switch wins.** In all 10 SmolLM and 4 of 5 Qwen LLM-useful cases, at least one of these three cheap switches was also >1% better than sequential.
- **The LLM loses to random proposals on its own interface.** In Spark/Hadoop, random prototypes pushed through the LLM's projection beat sequential on average: +1.17% for Spark and +4.42% for Hadoop. SmolLM scored −0.11% and −3.60% there.
- **Interpretation.** The useful LLM cases concentrate where sequential 3NN stalls and almost any diversification helps.

In the native cohort, useful additionally requires a different selected setting from sequential; robust means >10% with quality, stability and 10 ms floor.

| Arm | Useful (of 30) | Robust >10% | Hindsight headroom |
|---|---:|---:|---:|
| SmolLM3-3B / Qwen3-8B | 1 / 1 | 0 / 0 | 0.36% / 0.40% |
| Random full | 1 | 0 | 0.30% |
| Random prototypes | 0 | 0 | 0.18% |
| GP-EI | 3 | 0 | 0.49% |
| Adaptive neighbor | 5 | 0 | 0.85% |
| EZR centroid / Bayes (source-executed) | 3 / 6 | 0 / 0 | 0.79% / 0.90% |

- The LLM offers no more headroom than random search, and less than a cheap classical switch.
- No arm of any kind has a robust win. 17 of 30 LLM selections equal sequential's setting.

**C. The engineering is sound.**
- The V170 seal verifies: 1,558 files, 69 historical checkpoints, manifest `2eb6a885…`.
- 1,325 tests passed before this audit.
- The EZR bridge (`scripts/ezr_bridge_v169.py`) passes only raw features and acquired prefix labels. Unknown objectives are `?`, and each new label is asserted to be EZR's own argmin choice. I found no hidden-label leakage in the audited paths.

## 2. What the evidence does not establish

- **H1/H2 (benefit-aware routing) are untested, not refuted.** In the primary seven-ecosystem grouping, all 10 SmolLM positives lie in Spark/Hadoop:
  - Holding that group out leaves zero training positives.
  - Holding any other group out leaves zero test positives.
  - SmolLM therefore has **0 informative folds of 7**. Qwen has 2 of 7, one with a single training positive. Under the engine grouping the counts are 2 of 8 and 3 of 8.
  - The native cohort has 0 informative folds.
  - The threshold rule maximizes development-group gain with ties toward fewer calls (`scripts/router_v147.py:50-59`). When always-calling loses, it must choose never-call, whatever the predictor's skill.
  - The zero-call outcomes in V132, V147, V148, V151, V153, V159, V163 and V168 are the correct abstention, not evidence about predictive ability.
- **Nothing general about LLM continuation or SNAP2.** SNAP2 used gpt-oss-120b with iterative two-proposal calls; this study used 3B/8B quantized models with one batched call. V136's feedback ablation covered only two exposed families with one 8B model. Model scale is the dominant untested confound.
- **No native effect sizes at the 10% margin.** The native domains leave almost no post-B10 headroom for *any* continuation. They have 64 settings (128 for XGBoost), so B20 evaluates 31% of each (16% for XGBoost), and V165 already found negative headroom for hnswlib. These tasks cannot discriminate between policies.
- **No population, equivalence or journal-readiness claim.** Thirteen exposed groups, dependent seeds and a long development history rule these out.

## 3. Methodological problems, ranked

1. **The router test was non-identifiable (inferential, not a code bug).** Positives are concentrated in one group, so leave-one-group-out evaluation cannot score a working predictor. Reports that call zero-call routers "failures" (`reports/router_v147.md`, `router_v151.md`, `hadoop_v148.md`, `research_assessment_v148.md`) should be read as "untestable with this cohort". No held-out router result can be informative until held-out groups contain positives.
2. **Wrong counterfactual in the benefit target.** The target is gain over sequential 3NN (`scripts/router_v147.py:125-133`, `reports/protocol_v151.md`). A predictor trained on that label learns when sequential stalls, not when an LLM adds value beyond a cheaper switch. The decision-relevant contrast is the LLM against the best *pre-specified* deployable cheap continuation. The V141–V168 "joint win" diagnostic moved toward this, but only against one or two comparators.
3. **The native task design has no headroom.** Domains of 64 settings (128 for XGBoost) with B20 leave nothing for any policy to find; every arm has 0 robust wins. More seeds, hosts or controllers on these tasks cannot change that. Future native tasks need domains where B20 is a small fraction (roughly ≥500 valid settings) and a measured headroom gate before any LLM call.
4. **Transport target shift.** Routers trained on recorded B10+10 best-observed gains were applied to native 17+3 validation medians. This is documented in the V159, V163 and V168 reports, but it compounds item 1.
5. **Forking paths on exposed families.** 170 versions varied prompts, decoders, interfaces and models on overlapping families (for example V38, V49, V51, V93, V127–V129, V164). This mostly threatens a *positive* claim; the negative claim is less vulnerable, since that effort went into making the LLM arm work. A paper must disclose this history.
6. **Asymmetric relative-gain scale.** Equal-group means of (reference − candidate)/reference are dominated by a few large harms: DUNE −21%, XGBoost −26%, OR-Tools −20%. The log-ratio sensitivity in `audit.json` preserves every sign, so no conclusion changes. New protocols should make the log ratio primary.
7. **Report legibility.** Many generated reports have fused tokens such as "70paired cases/model". Sealed files are left unchanged; new reports should be proof-read before external review.

No implementation defects were found in the audited paths:
- EZR bridge;
- V147/V151 fitting, weighting and threshold selection;
- V170 per-arm aggregates, recomputed from raw medians;
- recorded-cohort gains, recomputed from raw arm values with direction.

The earlier V149 key collision was already caught and corrected in V151.

## 4. Strongest defensible contribution

> For small local LLMs (3B and 8B, quantized, one batched call) handed a B10 prefix of a B20 software-configuration search, LLM escalation shows **no LLM-specific headroom**:
> - This holds across 7 recorded ecosystems and 6 native implementations.
> - Each apparent LLM opportunity is matched by a cheap classical switch or by random proposals through the same interface.
> - A benefit-aware router therefore has nothing LLM-specific to select, and its zero-call behavior is correct abstention.
>
> Methodologically:
> - Escalation benefit must be measured against the best pre-specified cheap switch, not the incumbent optimizer's own continuation.
> - A router study must first show positives in several independent groups before leave-one-group-out results mean anything.

This is a bounded negative/boundary result with a reusable evaluation lesson. It is scoped to these models, this interface, this budget and these exposed tasks. It is not a claim that LLM optimization fails, not a refutation of SNAP2, and not novel merely for studying conditional escalation (SNAP2 §VI and BORA already raise it).

## 5. The single next experiment

**Model-scale LLM-specific headroom test on the recorded 70-case cohort.** The full specification is in `reports/proposal_v172.md` and `configs/proposal_v172.json`; both are hash-frozen in `artifacts/study_v171/freeze.json` and **not authorized for collection**.

- **Design.** Replay the saved prompt bytes, grammar, projection and sampling seeds of V141/V145/V148 with one larger owner-published model from the same family (Qwen3-14B, Q4_K_M GGUF from `Qwen/Qwen3-14B-GGUF`). Only the model file changes; the classical arms are already collected.
- **Why this cohort.** Outcomes are deterministic table lookups, so there is no host or timing confound. The contrast isolates model scale.
- **Estimand.** The count of ecosystems with an LLM-specific win: >1% over sequential, random-full, adaptive and GP-EI each. Hindsight headroom versus the same switch set, and log-ratio means, are secondary.
- **Decision rule, fixed now:**
  - Wins in ≥2 of 7 ecosystems: the router question becomes testable. The next step is a fresh, large-domain cohort sized by the arithmetic below.
  - Wins in 0–1 ecosystems: the no-LLM-specific-headroom result extends from 3B to 14B within this interface. Close the router question for local models on this hardware and write up.
- **Resources.**
  - 70 model requests (under `configs/pilot.yaml`'s 100) and 700 recorded acquisitions.
  - About 25–70 minutes of inference, split into two stages of at most 30 minutes, or run under an explicitly approved single cap.
  - RSS cap 12 GiB on the 18 GB machine, with no concurrent workloads.
- **Blockers that need your decision:**
  - The download is about 9 GB (verify the exact bytes on the owner page first).
  - It exceeds the retained-download cap (357,259,054 bytes remain of 10 GiB) and the model-payload cap (9 GiB, 9,126,358,023 bytes used).
  - The disk has only 12 GiB free (98% full); free at least 25 GiB first.
  - I have not raised any cap.

### Second host or more unseen systems?

Neither is the binding constraint for the controller claim.

- **Second host.**
  - It cannot affect the recorded half, which is table lookups.
  - For the native half, the conclusion is that no arm wins robustly; another host could at most move sub-percent differences.
  - It is worth doing only if a paper reports native effect sizes such as OR-Tools −20% as findings, and those cells are mostly under the 10 ms floor anyway.
- **More unseen systems.** These matter more than a host, but only once an LLM arm has non-zero LLM-specific headroom.
  - With zero positive groups so far, the one-sided 95% upper bound on the per-system rate is 34.8% (recorded, 0 of 7) and 39.3% (native, 0 of 6).
  - Expecting five positive-bearing held-out groups needs ≥15 fresh systems even at that optimistic bound, 50 at a 10% rate and 100 at 5%.
  - Twelve more all-negative systems would only lower the recorded bound to 14.6%.
  - The admissible unexposed recorded-table pool is essentially exhausted. By a name-based scan of reports and result paths (not proof about unnamed history), the 22 V5 registry families break down as follows:
    - Observed LLM outcomes: MySQL/MariaDB, lrzip, Brotli, libvpx, HSQLDB and PostgreSQL in V6; BerkeleyDB, DUNE/HSMGP, HIPAcc, LLVM, OpenVPN and SaC in V41 and V127–V148; MongoDB and Storm in V129.
    - Redis was run natively in V60–V61, and 7zip is grouped with the exposed XZ/LZMA family (V140).
    - DConvert, DeepArch and ExaStencils were rejected on task semantics; JavaGC was screened in V53–V58 but its recorded table was never admitted.
    - Only Opus and Z3 lack LLM outcomes, and their classical outcomes were inspected in V30–V31.
  - Native tasks cost roughly two per stage and so far have lacked headroom.

Order of value: model-scale headroom test → (only if positive) a fresh, headroom-gated large-domain cohort → second host last.

If you decline the cap increase, the evidence does not justify further collection with the existing models. The productive next step would then be writing up §4.

## 6. Reproduce this audit

```sh
.venv/bin/python scripts/audit_v171.py --check        # recompute and byte-compare results/v171_audit/audit.json
.venv/bin/pytest -q -p no:cacheprovider tests/synthetic/test_audit_v171.py
.venv/bin/python scripts/seal_research_v171.py --verify-only
```
