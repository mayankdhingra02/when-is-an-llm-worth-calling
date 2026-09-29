> **Schema correction:** the original SQLite run dropped a real INDEX option. Earlier full-schema counts/claims are superseded; see [schema_erratum.md](schema_erratum.md). Original measured logs are preserved. Use the corrected v3 report for current conclusions.

# Pilot report: When Is an LLM Worth Calling?

**The classical pilot ran successfully; the real local LLM path failed its reliability gate. The benefit-routing question remains untested.** This repository contains executed code and measured logs, not a generated claim of a positive research result.

## Executed scope

Three pinned MOOT tables: Apache (192 unique configurations), SQLite (4,652 after excluding one repeated feature vector), and x264 (1,152). Five fixed seeds, 20 total evaluations per arm, checkpoint at 10. These are offline recorded-label acquisitions, not new runs of the underlying software. All three have binary options and one minimization objective.

Completed 30/30 classical arms: random and a clearly labeled paper-based EZR centroid adaptation. Completed 10/15 attempted hybrid continuations on the two development systems; every one acquired its remaining ten labels using classical fallback. The five x264 LLM continuations were blocked at the request-attempt cap and retain their place in the intended denominator. They are not counted as completed hybrid results.

| System | Random mean loss | Adapted centroid mean loss | LLM-attempt policy mean loss |
|---|---:|---:|---|
| Apache | 0.01333 | 0.00000 | 0.00000 (all fallback) |
| SQL | 0.14183 | 0.16283 | 0.16283 (all fallback) |
| X264 | 0.03054 | 0.06175 | blocked; 0/5 continuations |

Loss is best observed full-table-normalized d2h; lower is better. Means summarize five seeds, with no inferential significance claim. The centroid adaptation is better on Apache's mean and worse on SQLite/x264's means. This is a useful baseline warning, not evidence against upstream EZR generally. All 10 measured paired gains equal zero **because fallback exactly reproduces the classical continuation**. This does not show successful LLM optimization is equivalent to classical optimization.

![Quality distributions](../results/analysis/quality.png)

## Real inference and the failure denominator

Official Qwen/Qwen2.5-0.5B-Instruct, revision `7ae557604adf67be50417f59c2c2f167def9a775`, ran locally using torch 2.6.0, transformers 4.49.0 and Metal float16. The prompt, strict JSON contract, greedy generation and one-retry policy were frozen before outputs. This is a much smaller and different model than SNAP2's gpt-oss-120b.

- 100 counted request **attempts**: 51 dispatched to the local worker; 49 failed before dispatch because that worker was no longer available. All attempts conservatively consumed the cap.
- 50 actual completed responses, all from Apache; 50 failed the parser; zero accepted model proposals. Typical response: nested lists inside a Python code fence, rather than the required JSON candidates object.
- 1 request timed out at 180 seconds, on SQLite. The worker was terminated and was not restarted. The following 49 fail-fast attempts are a **harness recovery limitation**, not 49 additional measured model generations or parse failures. Future infrastructure should stop or explicitly recover after worker death.
- 50 attempts were retries. 100 remaining-budget acquisitions used classical fallback. No valid projected, duplicate or collision proposals were acquired; those code paths were tested only on synthetic fixtures.
- Observed completed-response tokens: 49,079 input and 4,846 output. Total usage is **unknown**, because timed-out generation usage was not observable; these observed counts are lower bounds, not complete totals.

![Reliability outcomes](../results/analysis/reliability.png)

Raw request starts, responses, exact messages, sampling settings, token counts, model/file hashes, request IDs, timestamps, parser failures and checkpoints are in `results/paired/`. No outputs were fabricated, repaired after the fact, or replaced with Codex-generated “LLM” responses. A first model startup failed due to SciPy 1.15.3 binary compatibility; the failed log is retained, and pinning 1.13.1 fixed imports before the first output.

## Controller status

Never/always escalation, matched-rate random selection, uncertainty-only routing, a standardized ridge benefit predictor, two feature ablations and a non-deployable hindsight reference are implemented. Development-only fitting on Apache+SQLite ran, including leave-one-development-system-out predictions and the predeclared threshold grid. Gains are all zero from fallback, so the fitted benefit predictor is identically zero and selects never-escalate. This is a degenerate fit, not validation of an intelligent routing policy.

Pre-decision x264 features and prospective controller choices are saved under filenames ending in `UNEVALUATED`. **No held-out policy quality, cost-quality curve, missed-benefit risk estimate or oracle headroom result is reported**, because x264's paired counterfactual outcomes do not exist. Completed development cases are not substituted for missing test cases. Even complete results on these three systems would be descriptive smoke evidence only; two development groups and one test group cannot establish generalization.

## Actual collection cost versus deployment estimates

Actual research collection made **700 charged table-label accesses**: 600 across classical arms, plus 100 fallback continuation accesses. Reusing the saved ten-label prefix did not incur another collection access. There were 495 distinct queried configurations summed over dataset/seed instances; overlapping acquisitions between arms are still charged to each arm. Intended logical paired budgets remain 20 per branch; blocked prefixes do not count as completed 20-label branches.

Measured cumulative collection and recorded analysis runtime is about **528.3 seconds**. Request-attempt wall time sums to 511.7 seconds. Model startup wall time was 4.53 seconds, with model loading itself 1.10 seconds; the earlier failed startup also remains in the resource ledger. Installation, source audit, downloads, test execution and the first exploratory rendering pass are setup/audit overhead, not included in that instrumented collection total. Timing is platform-specific.

Additional external experiment/API spending: **USD 0**. Electricity, machine depreciation, and Codex usage cost were not measured. Downloads totaled about 1.29 GB including the conservative metadata allowance; actual weights/supporting model files were 999,602,607 bytes. No cloud-dollar savings are inferred from local tokens.

The deployment-cost evaluator separately selects prefix + controller overhead + one continuation and its request/tokens; loading amortization is excluded and reported separately. It was not used to claim held-out savings with missing test pairs. The expensive collection of both branches is never represented as a B=20 deployment cost.

## Integrity and remaining limitations

18 synthetic tests passed, covering hand-computed metric cases, inclusive budgets, duplicate rejection, paired state isolation, deterministic continuation, hidden-label perturbation invariance, acquired-only bootstrap features, group-split guards, no-paid provider policy, parser/fallback/projection behavior, persistent runtime/request caps, and download caps. Saved-result verification independently replayed classical decisions from acquired observations, recalculated metrics, checked table hashes and prefix equality, and verified real local provenance. Exact executed code/dependency snapshots match the original run manifests. Figures were regenerated and visually checked.

Tests do not establish scientific validity. Exact SNAP2 artifact alignment is unresolved; the selected datasets lack exact original workload/hardware versions. The current model/prompt/interface result cannot be generalized to stronger models or constrained decoding. MPS reproducibility across devices is not guaranteed, and pretraining contamination is unknown. See `source_audit.md`, `decisions.md` and `limitations.md` for details.

## Most important next action

Authorize a **new, explicitly bounded development-only format-feasibility experiment** to obtain reliable valid proposals (for example with constrained decoding or a stronger local model), with worker recovery specified in advance. The existing 100-attempt allowance is exhausted; do not reset it. Only after that gate succeeds should a newly frozen study spend resources on more paired outcomes across independent systems. The current evidence is suitable for discussing a failed feasibility gate and experimental design with Tim Menzies, not for claiming a successful benefit-aware router.
