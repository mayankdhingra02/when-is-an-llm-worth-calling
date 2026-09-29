# Research brief

## Status

This is a proposed protocol for a pilot, not an implemented method, completed experiment, preregistration, or established novel contribution. The exported research report motivates the question; verify its claims before relying on them.

Working title: **When Is an LLM Worth Calling? Cost- and Reliability-Aware Software Optimization**.

## 1. Narrow question

At a fixed checkpoint in a software-configuration optimization run, can a cheap controller estimate the **incremental benefit of LLM continuation relative to classical continuation**, using only evidence available at that checkpoint?

Do not reframe this as general coding-agent routing, program repair, code generation, or a new foundation model. The first study is offline configuration selection on public recorded data. Any conclusions apply to that setting, the evaluated model, and the selected tasks—not automatically to live production systems.

The motivation is the SNAP2 paper, Srinivasan and Menzies, arXiv:2607.02583. It explicitly discusses conditional escalation as future work. Therefore, “call the LLM only if needed” is not a defensible standalone novelty claim. The candidate contribution is an incremental-benefit predictor, tested against uncertainty-only routing under fair budgets and unseen-system evaluation. A current literature audit could still find this has already been done.

## 2. Proposed hypotheses

H1: At matched escalation rates, a small predictor of incremental LLM benefit selects more useful escalations than random selection and an uncertainty-only rule.

H2: Task/trajectory features plus cheap reliability signals predict benefit better than uncertainty alone on held-out software systems.

H3: A validation-selected escalation policy trades fewer LLM requests/tokens for a tolerable, explicitly measured change in optimization quality and missed-benefit risk.

These are questions to falsify, not success requirements. Set any practical quality margin before examining held-out outcomes. Do not claim formal risk guarantees or non-inferiority from a tiny pilot.

## 3. First execution stages

### A. Source and environment audit

Read the main paper's methods, metrics, limitations, and artifact links. Verify EZR/MOOT versions and licensing. Check for exact SNAP2 code, prompts, and released traces; do not guess paths. Record a source-to-implementation mapping, including unresolved ambiguities.

Inspect CPU, RAM, storage, and any already available local inference service. A local development environment and a cloud Codex environment may have different hardware. Do not assume the user's laptop GPU/RAM is present in a remote runner.

Create `reports/source_audit.md` and `reports/protocol.md`. Pin important paper/repository/data/model versions. Record what has been fetched, inspected, and actually executed as different statuses.

### B. Classical smoke test

Use three eligible datasets from distinct underlying software systems and five fixed seeds, selected by declared size/schema criteria before seeing performance. Prefer modest software-configuration/performance datasets. Do not select three variants of the same system and call them independent tasks.

Default total budget B = 20, decision checkpoint t = 10, remaining continuation budget = 10. Check that every selected dataset supports this. Implement random search and the intended EZR classical baseline. Validate the metric on hand-computable fixtures and confirm acquired-label counts.

### C. Paired LLM smoke test

Use one real local model with a documented identity/revision, or a compatible public cache with complete provenance. Do not download a model exceeding the configured limits or use a paid endpoint. A smaller/different model is an adaptation, not the original paper's numerical replication.

From each identical saved t=10 prefix, run both the classical and LLM continuations with 10 more allowed objective evaluations per branch. Clone state so branches cannot see each other's labels. Fix prompt/parameters before outcome comparisons. This small pilot establishes pipeline feasibility only.

### D. Router evaluation

Implement cheap controllers now; draw empirical conclusions only when enough independent development/test system groups exist. Repeated seeds increase repeated-run observations, not the count of independent systems.

For a larger study, use a declared system-group split or nested group cross-validation. Keep families/versions together, and use inner development folds for feature preprocessing, hyperparameters, and thresholds. Assess feasibility within resource limits; if it cannot run, deliver exact planned manifests/commands and clearly mark unexecuted work.

## 4. Budget and hidden-label semantics

A configuration evaluation means acquiring a previously unavailable objective vector for a configuration in the selected table. The objective oracle holds hidden values; optimizer code sees only the candidate feature table and acquired labels. Outcomes of multiple objectives for one row follow one documented charge rule.

The entire known candidate feature table may be used for unsupervised geometry in this explicitly transductive offline setting. Unobserved objective values may not be used for distances, nearest-row selection, pruning, ranking, features, normalization, or prompts. Match the paper's candidate projection using feature-space information only, or document a deliberate adaptation.

Define duplicate handling, invalid proposals, parse failures, tie breaking, nearest-row projection, and fallback policy before running. A repeated row cannot create a free new label; repeated model requests still have real cost. Charge any newly acquired labels used in reliability estimates. Bootstrap resampling of already acquired labels is allowed with computation cost recorded.

Metric orientation and scaling must be explicit. Reproduce the intended objective aggregation only after checking it. If a paper-style evaluator uses full-table objective extrema, keep those values exclusively in offline scoring; they must never enter the optimizer or router. Use only predeclared/acquired-label scaling inside the online policy. Audit whether a faithfully reproduced upstream routine assumes hidden-label statistics and document or fix this as a separate adaptation rather than silently changing semantics. Handle constant objectives and divide-by-zero cases.

## 5. Paired outcomes and controller targets

Let Q be the fixed quality metric, oriented so larger is better. Define:

`gain = Q(LLM continuation from prefix) - Q(classical continuation from same prefix)`.

For a lower-is-better loss L, use `gain = L_classical - L_LLM` instead. Do not mix directions. Full-table evaluation may generate retrospective training targets, but outcomes are never controller input features.

Candidate features are number/type of configuration variables; objective count; candidate count; trajectory progress; plateau length; best/rest separation; bootstrap recommendation disagreement computed from acquired labels; and remaining budget. No IDs that simply memorize software identity, no target ranks, and no outcomes from either continuation. Do not call an LLM merely to produce the routing features.

Begin with a shallow decision tree or regularized linear/logistic model. Use ablations for trajectory/task features versus uncertainty. At a fixed B=20 pilot, budget is constant; do not claim budget generalization without running multiple budgets.

Estimate cost using information known at decision time. Actual future response lengths, retries, latency, and costs can be targets/evaluation records, not deployable routing inputs. Avoid arbitrary unit-mixing utility weights; prefer a validation-selected threshold and a quality/cost curve, with explicitly specified units when utility is used.

## 6. Required policies

- **Never escalate:** continue classically to B.
- **Always escalate:** use the same prefix then LLM continuation to B. This is the fixed-hybrid baseline, not “LLM from the start.”
- **Random escalation:** use the development-selected rate, independent of quality outcomes. Also report a matched-realized-rate random diagnostic on held-out runs using no outcomes to select cases; label this retrospective rate matching, not an online policy.
- **Uncertainty-only escalation:** threshold on a predeclared acquired-label uncertainty signal; tune only on development groups.
- **Benefit-aware escalation:** small model/threshold trained on paired gains from development groups only.
- **Hindsight oracle:** choose the better branch after seeing both outcomes; label non-deployable, optionally account for costs. It estimates available routing headroom, not an achieved result.

An LLM-only-from-start arm is optional for later contextual comparison; it is not essential to isolate the handoff decision. Plain random configuration search remains a useful sanity check.

## 7. Costs: do not hide research overhead

Collecting both continuations costs more than deploying one selected branch. Maintain separate ledgers:

1. **Actual research collection:** both branches, training data, retries, validation, repeated inference, and actual invoices/usage if later authorized. For a saved shared prefix, record actual distinct objective accesses plus logical per-branch budgets; do not simply declare the whole paired experiment costs B.
2. **Estimated policy deployment:** prefix + controller overhead + only the selected branch for each held-out instance. Include warm-up/loading costs separately and document amortization assumptions.

Reusing cached paired traces across multiple policies may avoid new collection requests; it does not make historical inference free. Cache keys must include model/provider/revision, prompts, sampling configuration, prefix/data hashes, relevant seed, and parser/projection version. Arbitrary canned responses or incomplete traces are not a valid counterfactual cache.

Do not report precise cloud-dollar savings from local token counts without a clearly labeled, dated pricing scenario. Unknown tokens/latency are unknown. Disclose that model pretraining contamination of public benchmarks may remain unknowable.

## 8. Reliability and analysis

Report quality distributions, paired gains, escalation fraction, requests and retries, observed tokens, wall time, parse/projection/duplicate rates, fallback incidence, and missing/failed runs. Count a fallback under its actual policy, rather than hiding it as a successful LLM decision.

Distinguish two risks: missing a useful escalation (LLM would have beaten classical by a predeclared margin), and escalating harmfully (LLM continuation is materially worse than classical continuation under equal budget). Always retain the best evaluated incumbent within each arm; that does not imply every escalation beats the classical counterfactual.

Aggregate first at system level where appropriate. Do not treat hundreds of seeds from a few systems as hundreds of independent domains. Use group-aware intervals only with enough groups; otherwise report descriptive pilot outcomes. No claim of “same quality” merely because a small study has a nonsignificant test. Show a predeclared threshold grid, not only its best-looking point.

If LLM continuations rarely help even in hindsight, report low available routing headroom. A learned router cannot demonstrate meaningful selection gains where there is little useful variation to select.

## 9. Resource defaults and blockers

`configs/pilot.yaml` is an initial specification, not an existing executable config. Codex must implement its validation and guards. No API payment/cloud spending is authorized. No system-wide installs or credential discovery. Small verified model downloads within the file's limit are allowed only without account creation, new service acceptance, or special privileges.

If unavailable code, incompatible traces, missing real model access, hardware, or resource caps block part of the study: finish independent classical work, implement interfaces/tests, record the exact blocker, and stop that component. Never label mocked outputs as LLM results. Do not turn the study into a different topic just to claim completion.

## 10. Deliverables and acceptance criteria

Expected implementation artifacts:

- A minimal Python package/runner with environment lock, configuration validation, tests, and exact run commands.
- `reports/source_audit.md`, `reports/protocol.md`, a dataset manifest with system-group mapping/hashes, and source/license attribution.
- Real raw JSONL/CSV records plus run manifests, command logs, failures, and versioned model prompts/response provenance.
- Regenerable plots/tables from actual records, never hand-written result numbers.
- `reports/pilot_report.md` explaining executed scope, what worked, negative findings, limitations, and whether meaningful LLM routing was actually measured.
- `reports/next_experiment.md` with justified scale/model/budget needs and a conditional, unsent outreach summary based only on verified findings.
- `STATUS.md` with resume instructions and remaining limits.

Use CSV/JSONL for machine data; no spreadsheet presentation or website is required. Keep public third-party papers/data/model weights out of a shareable Git history unless their licenses explicitly allow redistribution.

Acceptance is evidence-based: tests must actually run; budget/isolation/split guards must pass; logs must support each claim; all measured LLM results must have real provenance; insufficient sample size or blocked components must be disclosed. Positive gains, novelty, publication, and volunteer acceptance are not acceptance criteria.
