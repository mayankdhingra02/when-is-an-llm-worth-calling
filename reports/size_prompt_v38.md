# V38: size-aware prompts improve one comparison, but not the strongest observed cheap control

Thirty real local Qwen2.5-1.5B requests completed on two exposed software families. The prespecified assigned-ID comparison improved mean feasible runtime by **1.7534% over exact joint3NN shortlist**, with **2 wins, 7 ties and 1 harm**. It improved by **2.0444% over matched historical runtime-only LLM responses**, with 3 wins, 7 ties and no harms.

The result does **not** establish that escalation is worth its cost. Across all three presentations, the runtime3NN control is at least as good in all 30 paired cases: **0 LLM wins, 24 ties, 6 harms**. The new model calls therefore add no observed quality benefit over that control under this metric. This is an exploratory result on two previously exposed systems, not a successful held-out benefit router or confirmation of the original hypotheses.

## Executed design

The [protocol](protocol_v38_size_prompt.md) and its 428 input hashes were frozen before execution. The exact 30-call extension was recorded in [authorization](../configs/authorization_v38.json), including the user's verbatim direct instruction to proceed and its interpretation after the preceding resource proposal. Global follow-up allowance rose from 200 to 230; the 3,600-second experiment ceiling, USD 0 spending and no-download restriction were unchanged.

Brotli 0.3.0 and lrzip 530 each have seeds 11, 23, 37, 53 and 71. Each case reused its saved ten-evaluation prefix, fixed prefix-derived output-size cap, and twenty-candidate shortlist. Three frozen ID/display presentations produced thirty branches. Each branch acquired ten distinct new runtime/size vectors, retained the fastest acquired feasible incumbent, and respected twenty inclusive evaluations. Infeasible acquisitions were charged. Original candidate features, mappings, order and acquired normalized runtime observations were preserved; only acquired sizes, the cap and explicit size-constrained instructions were added. Unacquired outcomes were absent from prompts.

The owner-verified model was `Qwen/Qwen2.5-1.5B-Instruct`, revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`, CPU float32, greedy generation, twenty-token candidate grammar. All 30 intended calls and arms completed with zero retries, timeouts, malformed selections, duplicate selections, projections or fallbacks. Grammar constraints restrict output syntax; this is not evidence of unconstrained generation reliability. Greedy decoding has no sampling seed guarantee and can still have numerical nondeterminism.

## All prespecified comparisons

Gain is `(comparator feasible runtime - LLM feasible runtime) / comparator feasible runtime`; positive favors the LLM. Average the five seeds within each family, then weight the two families equally. All fifteen presentation/comparator combinations are retained; no winning presentation was selected after inspection.

| Presentation | Comparator | Mean gain (%) | Wins / ties / harms |
|---|---|---:|---:|
| assigned_ids | runtime_only_llm | +2.0444 | 3 / 7 / 0 |
| assigned_ids | exact_joint_shortlist | +1.7534 | 2 / 7 / 1 |
| assigned_ids | exact_joint_full | +0.4209 | 1 / 4 / 5 |
| assigned_ids | runtime_3nn | -0.2211 | 0 / 9 / 1 |
| assigned_ids | static_rank | +3.4044 | 3 / 6 / 1 |
| reverse_display | runtime_only_llm | +0.0000 | 0 / 10 / 0 |
| reverse_display | exact_joint_shortlist | +0.2406 | 2 / 5 / 3 |
| reverse_display | exact_joint_full | -1.1159 | 1 / 4 / 5 |
| reverse_display | runtime_3nn | -1.7339 | 0 / 7 / 3 |
| reverse_display | static_rank | +2.0932 | 3 / 5 / 2 |
| reassigned_ids | runtime_only_llm | +0.3621 | 2 / 8 / 0 |
| reassigned_ids | exact_joint_shortlist | +0.1027 | 1 / 8 / 1 |
| reassigned_ids | exact_joint_full | -1.2299 | 0 / 5 / 5 |
| reassigned_ids | runtime_3nn | -2.1981 | 0 / 8 / 2 |
| reassigned_ids | static_rank | +1.7536 | 2 / 7 / 1 |

The primary assigned-ID gain comprises Brotli **+2.8593%** and lrzip **+0.6476%** family means. Its non-tied cases are Brotli seed 23 **+16.5072%**, lrzip seed 11 **+3.2378%**, and Brotli seed 11 **−2.2105%**. Seven cases tie. A single Brotli case contributes much of the positive average; seeds are not independent systems.

The assigned-ID comparison against full-domain joint3NN has a positive mean (+0.4209%) but **one win and five harms**, further showing why the mean alone is inadequate. Reversed and reassigned presentations lose on average to that comparator. All three presentations lose on average to runtime3NN.

![All prespecified comparisons](../results/v38_size_prompt/comparison.png)

## Prompt and constraint diagnostics

The size-aware prompts changed 13/30 selected sets: 6 assigned-ID, 3 reversed-display and 4 reassigned-ID sets. Against the matched old LLM selections, feasible terminal runtime improves in 5/30 cases, ties in 25, and worsens in none. These old responses were collected in an earlier session; this is not a contemporaneously randomized causal estimate of adding size information.

Constraint violations among acquired continuation vectors **increase from 75/300 to 84/300**: assigned IDs 25→29, reverse display 25→25, reassigned IDs 25→30. Thus improved final feasible runtime does not establish improved constraint prediction. The unconstrained fastest acquired row violates the cap in 8/30 new branches versus 9/30 old branches. Final selections themselves all obey the cap because the evaluator retains a feasible incumbent. These diagnostics are descriptive, not fitted routing features.

## Actual cost versus deployment estimates

Actual incremental collection: **30 model requests, 300 new recorded joint-vector acquisitions**, 55,302 observed input tokens and 600 observed output tokens. No new physical benchmark trial was run. Thirty logical branches use 600 inclusive evaluations, with the existing prefixes reused rather than recollected. Prior classical branches, historical LLM requests and prefixes retain their original collection costs.

Measured request time totals **229.090471 seconds**; provider startup **8.277166 seconds**, including 4.943876 seconds loading weights. The complete collection charged **241.110346 seconds**, analysis/rendering **3.196673**, total **244.307020**. These accounting intervals overlap with request/startup subcomponents and must not be added twice. Tests and read-only verification are maintenance costs outside this experimental ledger.

Cumulative ledger: **2530.796723/3,600 seconds**, **1069.203277 seconds remaining**; **230/230 follow-up requests**, 330 including the initial stage; **9,608 recorded-vector acquisitions**, **1,274 physical trials** across prior stages. Downloads unchanged, USD 0 external spend. No remote publication, push, cloud use or contact occurred.

Estimated deployment of one fixed presentation across these ten prefixes would use ten model calls and 200 inclusive evaluations, not thirty calls and 600 evaluations. A classical policy would use the same twenty-evaluation budget per case without a model request. This is budget arithmetic, not measured deployment cost or monetary savings. Loading amortization, actual evaluation latency, controller overhead and application value remain unvalidated. Against runtime3NN, no observed positive feasible-runtime gain exists to repay positive inference overhead in these cases.

## Verification and evidence

- **258 tests passed in 1.99 seconds**; fixtures remain under the synthetic namespace.
- The frozen analyzer checked all 30 raw responses against local tokenization, generated token IDs, grammar traces, prompt hashes, model/revision, cache keys, request sequence 201–230, source strings, shared prefixes and budgets. Its read-only replay passed.
- A separate standard-library [Fraction checker](../scripts/verify_size_prompt_v38.py), importing no study code, independently reconstructed source-bound scores for all 30 arms, 150 paired gains and 15 summaries. This checks scoring independently; tokenizer provenance remains the frozen analyzer's responsibility.
- The historical audit passed all **3,586 frozen references**, including 350 unchanged V22 evidence files and the earlier development-sealed V6 group split/policies. The V38 figure was rendered and visually inspected.
- The collection and analyzer exited successfully and the ledger is inactive. The provider executed its child-process cleanup. A separate operating-system process listing was unavailable in the sandbox; no independent process-table assertion is made.

Raw evidence: [requests.jsonl](../results/v38_size_prompt/requests.jsonl), [acquisitions.jsonl](../results/v38_size_prompt/acquisitions.jsonl), per-branch `arms/`, [summary.json](../results/v38_size_prompt/summary.json), [comparisons.csv](../results/v38_size_prompt/comparisons.csv). Commands and receipts are in `artifacts/study_v38/`. The V35.1 ZIP remains a V34 snapshot and does not contain V38.

Read-only reproduction with the retained pinned data/tokenizer:

```sh
.venv/bin/python scripts/analyze_size_prompt_v38.py --verify-only
.venv/bin/python -I -S scripts/verify_size_prompt_v38.py
.venv/bin/python -m pytest -q
.venv/bin/python scripts/audit_history_v30.py
```

The collection and analysis commands are in STATUS.md. They deliberately refuse to overwrite completed work; do not rerun inference. No claim of isolated clean-machine V38 reproduction is made.

## Limits and next experiment priorities

Only two exposed family groups were evaluated; no confidence interval, statistical significance, generalization or learned-router success is claimed. The cap is a research default, not an application-approved requirement. Recorded outcomes lack fresh row-level uncertainty/correctness validation. Prompt history, earlier study choices and many exploratory versions limit confirmatory interpretation. Historical old-model calls confound session with treatment; presentation sensitivity remains. This is a small-model, constrained-candidate adaptation, not a numerical replication of SNAP2 or proof that larger models cannot help.

**Single most important next action: review this completed result with Tim before funding or expanding the experiment**, using the strongest cheap-control comparison as the decision point. No message has been sent. A defensible narrow result is that supplying the missing constraint improves a fixed comparison, while a stronger cheap control eliminates the observed escalation benefit.

If a larger study is warranted, prioritize (1) an application-defined utility and genuinely untouched software families with measurable opportunity beyond runtime3NN and joint controls, (2) one prospectively frozen, contemporaneously interleaved prompt comparison with order controls and physical uncertainty/correctness evidence, and only then (3) group-held-out benefit routing. New collection requires its own bounded authorization; the 230-call allowance is exhausted. More seeds or prompt tweaks on these exposed families cannot establish held-out routing. Positive results, novelty and acceptance remain unproven.
