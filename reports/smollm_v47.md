# V47 — Cross-model robustness result: SmolLM3 did not improve optimization

Completed 2026-09-25. This is an exploratory cross-model/runtime comparison on
six previously exposed software families and five fixed seeds. SmolLM3-3B Q4_K_M
used the exact saved ten-observation prefixes and original twenty-candidate
pools; each continuation acquired ten additional outcomes, retaining the incumbent.
No model/prompt/pool/threshold selection used its new outcomes.

## Actual result

| Reference | Mean relative gain | Descriptive family bootstrap 95% | Wins / ties / harms |
|---|---:|---:|---:|
| batch_3nn | -3.026% | [-6.428%, -0.207%] | 2 / 14 / 14 |
| full_sequential_3nn | -4.926% | [-10.658%, -0.788%] | 2 / 13 / 15 |
| qwen_0.5 | +0.000% | [+0.000%, +0.000%] | 0 / 30 / 0 |
| qwen_1.5 | -3.130% | [-6.428%, -0.410%] | 2 / 13 / 15 |

Positive gain favors SmolLM3. Family means, not seeds, are the inferential units.
Both primary means are negative, so the predeclared positive screening criterion
was not met. The intervals are descriptive six-family bootstraps on exposed
systems, not confirmatory evidence or a population guarantee. All seven classical
controls and both historical Qwen models are reported in `results/v47_analysis/summary.json`.
Compared with the stronger full-domain sequential3NN, all six family mean gains
are negative. Same-pool batch3NN comparison has one weakly positive family.

## Diagnostic finding

SmolLM3 selected IDs 0 through 9 in presentation order on 29/30 cases. In one
case it selected 0,1,2,4,5,6,8,9,A,B. This came from actual model outputs under
a constraint excluding already-selected IDs, not a scripted choice generator.
Twenty IDs were available initially; their display order was randomized in V41.

A post-hoc no-LLM ordering control simply selects IDs 0 through 9. Those exact
rows were already evaluated by historical Qwen0.5 in all thirty cases, so the
control required no new target access. Its final target equals SmolLM3's in
**30/30 cases**, and its selected row sequence equals SmolLM3's in 29/30.
This establishes observed equality of final scores for this cohort only, not
statistical equivalence or a universal assertion about the model.

This is evidence consistent with an ordering shortcut in this constrained,
symbol-encoded interface. It does not establish a causal explanation: no new
randomized presentation intervention was run. The zero-cost rule is a clearly
labeled post-hoc diagnostic, not a preregistered winning baseline. Larger model
size by itself did not rescue this local adaptation. Historical Qwen1.5 did
better than SmolLM3 on average under a different tokenizer/runtime/precision.

## Frozen policy transfer

All old V41 masks were applied unchanged, without training on SmolLM3 outcomes.
Relative to full-domain sequential3NN, never-escalate has zero incremental gain;
always-escalate is -4.926%; the old benefit-aware policy selects one of thirty
cases and has -1.106% cohort mean gain. Uncertainty selects no cases. The matched
one-call random diagnostic is +0.167%; the nondeployable hindsight oracle selects
two cases for +0.177%. These tiny selection counts and out-of-distribution policy
transfer do not validate a learned router. All 18 policy/comparator summaries
are saved; favorable diagnostics are not promoted to achieved policies.

## What actually ran and cost

- Thirty real SmolLM3 continuations, no fallback, missing case or retry.
- Three hundred actual local HTTP generation requests, ten per continuation.
  Each request chooses one remaining ID using greedy constrained real logits;
  delimiters are forced between requests. This preserves the semantic distinct-ID
  constraint but is not token-for-token equivalence with the Qwen decoder.
- 300 generated choice tokens; 321,560 full-context input-token counts summed
  across requests; 32,426 prompt tokens actually evaluated according to runtime
  timing counters with prefix caching. These are different cost quantities.
- 66.917 seconds for the live collection stage including startup/shutdown;
  65.963 seconds summed request wall time. Startup about 0.621 seconds.
- 300 additional charged recorded-objective accesses; 14,708 cumulative accesses.
  All arms have twenty distinct logical evaluations (ten prefix + ten continuation).
  No new physical software execution trials; the existing count remains 1,274.
- $0 external spending, zero new downloads. Local hardware/electricity cost unknown.
- Historical research follow-up requests remain separately recorded at 350;
  with V47 research they total 650. Adding V46's two hardware requests gives
  652 follow-up requests, or 752 including the original hundred-request stage.

Research collection includes every counterfactual branch. Deployment estimates
in policy summaries include only selected cases' ten model requests and their
observed wall time, with startup, controller, objective-access and historical
classical overhead explicitly excluded. They are not end-to-end deployment
latencies or causal speed comparisons with historical CPU Qwen runs.

The temporary server listened on loopback only, used the pinned local model,
and exited cleanly with code 0. No inference process remains running. Metal
availability was checked in V46 and full offload requested; this runtime's
normal log did not expose actual per-layer placement.

## Integrity, reproduction and limitations

The protocol and 420 listed inputs were frozen before collection. Preflight
rendering/tokenization for all thirty prompts was sealed before first generation;
first-choice requests had zero cached tokens from previous cases. The collector
never opened target tables. Outcome acquisition occurred only afterward in a
separate evaluator. Exact prompts, prompt tokens, grammars, returned token IDs,
raw responses, request timestamps, source-line events, costs and failures are
preserved under `results/v47_smollm` and `results/v47_analysis`.

Pre-run compilation caught one extra closing brace in the frozen analyzer.
The command orchestrator nevertheless started the independent collector before
that compilation failure was handled. No analysis had executed or outcome been
inspected. The frozen original is preserved; `analyze_smollm_v47_fixed.py` removes
only that brace. The timestamped correction records both hashes and the exact
replacement. This workflow error is disclosed; future launch scripts must gate
collection on successful compilation/tests.

Independent stdlib verification checked 300 request sequences, 300 acquisitions
against actual source cells, 270 paired contrasts and 18 policy summaries.
All 344 tests under `tests/` pass. Configured default discovery alone runs 321;
use the explicit `tests` path to include the remaining tests. No synthetic
fixture enters these aggregates. V46 hardware prompts stay separate.

Reproduce without new inference/acquisition:

```sh
.venv/bin/python scripts/verify_smollm_v47.py
.venv/bin/python scripts/report_smollm_v47.py
.venv/bin/python -m pytest -q tests
```

Original execution: `scripts/collect_smollm_v47.py`, followed by
`scripts/analyze_smollm_v47_fixed.py`. Both refuse overwriting an existing run.
Do not delete outputs to bypass accounting. Figure sources regenerate PNG/SVG.

Limits remain: exposed small cohort, uncertain application-utility equivalence,
public-data pretraining contamination, symbol-encoded interface, constrained
non-reasoning decoding, quantization/runtime/model-size confounding, and old
Qwen-trained controllers. Upstream weights revision is not specified by the
GGUF publisher, though the exact downloaded GGUF is hash pinned. This is neither
SNAP2 replication nor evidence of useful generalizable benefit-aware routing.
No Q1/Q2-readiness claim follows. Nothing was published, pushed, or sent.

## Next experiment, in priority order

1. Treat ordering insensitivity as the next falsifiable mechanism. Before more
   optimization runs, freeze a representation/order sensitivity assay using
   development-only prefixes: actual named settings versus current symbol strings,
   independently permuted candidate presentation, and an observed-label ablation.
   Evaluate whether selections respond to observations beyond choosing early IDs.
   This is a changed intervention, not another run of this stopped adapter.
2. Keep that diagnostic outside independent evaluation. Audit the existing family
   registry and exposure history to identify genuinely unused software groups;
   collect fresh groups if none remain. Freeze all related versions/seeds together.
   Do not relabel an already exposed system as held out merely by changing seeds.
3. Advance to paired controller training/evaluation only if development runs show
   incremental benefit over both batch and sequential classical controls. Freeze
   the intervention and resource budget before any untouched evaluation outcomes.
   If no intervention demonstrates benefit, develop the bounded negative-result
   contribution and its novelty instead of tuning until a positive result appears.

A subsequent admission-only audit found 11 registry group names absent from
locally admitted manifests: 7zip, dconvert, deeparch, exastencils, fastdownward,
fpga_sort256, javagc, mongodb, noc_cm_log, redis, storm (33 registry entries,
including variants/aliases). This is a lead for future source validation, not
proof of untouched labels or eleven eligible independent tasks. Several have
unresolved objective semantics or feature-domain exclusions. No new raw targets
were read. Receipt: `artifacts/study_v47/future_group_admission_audit.json`.
