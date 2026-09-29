# V19: controlled display-order dependence in actual local-model selections

**All nine real responses selected exactly the first ten displayed candidates, in display order.** Reversing candidate display order changed all ten selected configurations in each of the three cases. Reassigning IDs while preserving feature order left all ten selected configurations unchanged. The result supports display-position sensitivity for this model/prompt on these three development cases; low numeric IDs alone do not explain the observed selections.

This is a concrete controlled finding about the measured selection behavior. It is not evidence of useful LLM optimization, learned-router benefit, internal reasoning, or broad generalization. No new optimization outcome was acquired or scored in this probe. A first-ten display rule exactly reproduces all nine selections without model inference; that is an observed equivalence on these inputs, not a guarantee for untested inputs.

## Fixed interventions and complete results

One fixed case per V8 development family, seed11, chosen as the first predefined seed before this probe's responses. Three fresh conditions per case, same already acquired prefix labels and20 candidate configurations. Original prompts were byte-identical to the archived V8 prompts. Reverse display retained feature-to-ID bindings; reverse IDs retained feature/display order and changed only the ID assignments. Treatment execution order was counterbalanced across families. All instructions, pinned model, greedy decoding and distinct-ID grammar remained fixed.

| Family | Display reversal: overlap with fresh original | ID reassignment: overlap with fresh original | First displayed ten, all conditions |
|---|---:|---:|---:|
| MySQL | 0/10 | 10/10 | 3/3 |
| lrzip | 0/10 | 10/10 | 3/3 |
| Brotli | 0/10 | 10/10 | 3/3 |

Original-condition raw outputs were IDs0 through9. Both intervention conditions output J,I,H,G,F,E,D,C,B,A; those were the first ten entries displayed after the corresponding intervention. Because ID-to-configuration mappings differ between interventions, identical output IDs do not imply identical selected configurations. The fresh original outputs matched the earlier V8 originals in all3 cases.

![Every measured selection](../results/v19_order_probe/selection_order.png)

All **9/9 requests completed** with no failures, timeouts, retries, fallbacks or unattempted cases. The full nine-condition denominator is preserved in [progress.json](../results/v19_order_probe/progress.json). These are nine controlled conditions over three cases, not nine independent software-system samples. There was no repeated stochastic sampling or significance test.

## Provenance and verification

Actual local Qwen/Qwen2.5-0.5B-Instruct, revision7ae557604adf67be50417f59c2c2f167def9a775;CPU,torch.float32,PyTorch2.6.0,four threads,greedy decoding. The worker checked the pinned model-file digests before loading. No new model or package was downloaded/installed. The old V8 distinct-ID grammar remains unchanged: ten decision positions with20 down to11 allowable IDs. Syntax did not force either displayed sequence.

The25-file [scientific freeze](protocol_v19_order.freeze.json) was created before any V19 inference. Its protocol title still says pending authorization because that historical pre-execution artifact is immutable; the separately recorded [approval](../configs/authorization_v19.json) and [run-start snapshot](../results/v19_order_probe/started.json) establish authorization before inference. The user replied “continue” directly to the explicit nine-call cap request. Only the requested128→137 increase was applied; the1800-second runtime andUSD0 spending limits did not change.

The frozen analyzer verified every actual token sequence/grammar trace, raw output, prompt hash, tokenizer count, condition and model revision. A separate post-collection check independently inspected JSON transformations and ID-to-source-row mappings, consecutive request IDs129–137 and approval timing. **134 tests passed after execution** (also134 before), including permission/intervention/deadline guards. Figure visually inspected.

Transformers emitted warnings that sample-only settings such as top_k are inactive with do_sample=False. Those warnings are retained in the inference log; generation remained greedy and completed. They are not failed model calls. Earlier denied preflights remain archived; they did not reserve model requests. No prior raw outcomes or executed source files were changed.

## Raw evidence and reproducibility

- [Real prompts, raw responses, token IDs and usage](../results/v19_order_probe/requests.jsonl); [request reservations](../results/v19_order_probe/request_starts.jsonl); [runtime identity](../results/v19_order_probe/model_runtime.json).
- [All nine rows](../results/v19_order_probe/response_table.csv), [machine summary](../results/v19_order_probe/summary.json), [saved per-condition selections](../results/v19_order_probe/outcomes/).
- [Prepared messages/mappings](../data/order_probe_v19.json), [protocol](protocol_v19_order.md), [independent execution checks](../artifacts/study_v19/execution_verification.json), [post-execution tests](../artifacts/study_v19/post_execution_tests.log).
- Execution logs: artifacts/study_v19/inference.log, analysis.log, render_verification.log. Prior pending review state: artifacts/history/v19_before_execution/.

Executed project-local commands:

```sh
.venv/bin/python scripts/run_order_v19.py
.venv/bin/python scripts/analyze_order_v19.py
.venv/bin/python scripts/render_verify_order_v19.py
PYTHONPATH=src .venv/bin/python -m pytest -q
```

Do not delete run guards or reset the ledger to repeat them. Collection and analysis refuse overwriting completed outputs. A fresh model rerun requires a separately authorized bounded study. All values in the table/figure derive from actual responses; synthetic fixtures remain separate. The response analyzer and new provider have now been exercised end-to-end.

## Actual costs and scope limits

Observed usage:14364 input tokens,180 output tokens,missing usage0 requests. Output count includes forced syntax/EOS as well as model decisions. Request wall time **18.3699seconds**. Model startup **4.2211seconds**, including0.8716seconds reported model loading; do not add load time to startup again. Overall inference-session time **23.6912seconds** also includes hash validation and orchestration. Execution plus analysis/render this turn:26.6799seconds; V19 including prior tokenizer preparation:29.3851seconds.

**0 new objective acquisitions,0 physical trials,0 download bytes,USD0 external spend.** Historical dataset construction and earlier paired collection remain charged. No deployment-dollar or quality-saving estimate is made. Cumulative follow-up attempts **137/137 exhausted**,237 including the initial stage; runtime **1773.5859/1800seconds**, **26.4141seconds left**, ledger inactive. Prior1134 physical trials and5408 recorded objective accesses unchanged. No running worker, cloud use, credentials, remote publishing or contact.

The stop rule of nine attempts has been reached. Stronger models, other prompts/grammars, more permutations, repeated seeds, untouched groups and selection-quality consequences are untested. The broad benefit-routing question remains unresolved. V6's chosen zero escalation rate does not demonstrate useful discrimination at nonzero rates; V17/V18's small feasible headroom is a separate benchmark limitation. This mechanism result should be discussed with those limits, not presented as a successful router.

**Single next action:** review this controlled finding with Tim to decide whether a small methodological report centered on position controls is worthwhile before expanding inference. Novelty, publication and professor acceptance are unestablished. Nothing has been sent or submitted.
