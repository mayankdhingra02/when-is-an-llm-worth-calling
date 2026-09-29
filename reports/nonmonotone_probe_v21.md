# V21: interleaved IDs produce mixed selection behavior

**The three real responses do not follow one universal first-ten rule.** MySQL returned the first ten displayed IDs, while lrzip and Brotli returned IDs0–9, selecting alternating display positions. All3/3 requests completed. This narrows the earlier V19 result: selection followed display order in its nine conditions, but that pattern did not generalize to all three interleaved-ID prompts.

| Case | Actual output sequence | Selected display positions | Fixed rule matched | Configuration overlap with V19 original |
|---|---|---|---|---:|
| MySQL |0 J 1 I 2 H 3 G 4 F|1–10|Display prefix|10/10|
| lrzip |0 1 2 3 4 5 6 7 8 9|1,3,5,…,19|Endpoint sequence and lowest IDs|5/10|
| Brotli |0 1 2 3 4 5 6 7 8 9|1,3,5,…,19|Endpoint sequence and lowest IDs|5/10|

These are actual model outputs, not the synthetic rule predictions used to design the test. Each rule fails to explain at least one of the three new outputs; endpoint-sequence and lowest-ID explanations remain indistinguishable for the two responses they match. Matching a rule does not establish the model's internal algorithm. No significance, generalization or optimization-benefit claim follows.

![Actual interleaved-ID selections](../results/v21_nonmonotone/interleaved_selection.png)

## Frozen test and interpretation

The [27-file freeze](protocol_v21_nonmonotone.freeze.json) preceded inference. Features, displayed feature order, already acquired prefix labels, instructions, model and grammar were held fixed relative to the three original V19 prompts. Only the candidate IDs were reassigned to0,J,1,I,…,9,A. The first-display rule and canonical endpoint-sequence rule then predict different sequences/sets, as specified before responses. Exactly one call per case, MySQL/lrzip/Brotli seed11, no added seeds or prompt adaptation after outcomes.

The original V19 nine-call result remains true for its tested ascending/descending ID lists. V20 correctly identified that those lists could not distinguish display-prefix selection from ID-sequence continuation. V21 supplies counterexamples to a universal display-prefix explanation. It does not prove a universal alternative or discover a successful optimizer. No fresh original-condition repetition was budgeted in V21, so configuration comparisons to V19 originals are across sessions. Those V19 originals matched the older V8 originals, but this does not guarantee session invariance.

For lrzip/Brotli, changing ID assignment while retaining feature order changed half the selected configuration set relative to V19. This is observed behavior across the tested sessions, not evidence that the new settings are better/worse. **No objective values were newly acquired or scored.** Hidden candidate targets never entered the prompts. All cases were previously exposed development cases, not untouched systems.

## Actual execution and verification

User “Continue” directly answered the specific three-call permission request; only cap137→140 was approved. The [authorization](../configs/authorization_v21.json) and [start snapshot](../results/v21_nonmonotone/started.json) precede requests138–140. Cumulative runtime1800seconds andUSD0 external spending stayed unchanged. The historical frozen protocol still says permission pending because approval is intentionally separate.

Actual model: Qwen/Qwen2.5-0.5B-Instruct,revision7ae557604adf67be50417f59c2c2f167def9a775,CPUfloat32,PyTorch2.6.0,four threads,greedy. Same V19 provider and V8 distinct-ID grammar, with20→11 allowable IDs over ten decision positions. All model-file hashes were checked before loading. No download or installation.

All3/3 attempts succeeded;0 retries,failures,timeouts,fallbacks or unattempted cases. Actual output tokens were decoded and checked against the grammar trace; rendered prompt hashes, tokenizer counts, model identity and per-case mapping were verified. A separate post-collection audit independently checked feature preservation, ID-to-configuration mappings, approval timing and request IDs. **140 tests passed after execution**; plot visually inspected. Sample-only generation-setting warnings under greedy decoding are retained in inference.log and did not prevent completion.

## Evidence and commands

- [Actual prompts/raw outputs/tokens/usage](../results/v21_nonmonotone/requests.jsonl), [request starts](../results/v21_nonmonotone/request_starts.jsonl), [full three-case denominator](../results/v21_nonmonotone/progress.json).
- [Exact response table](../results/v21_nonmonotone/response_table.csv), [machine-readable rules and outcomes](../results/v21_nonmonotone/summary.json), [per-condition outcomes](../results/v21_nonmonotone/outcomes/).
- [Protocol](protocol_v21_nonmonotone.md), [prepared messages](../data/nonmonotone_probe_v21.json), [independent execution checks](../artifacts/study_v21/execution_verification.json), [post-run tests](../artifacts/study_v21/post_execution_tests.log).
- Logs: artifacts/study_v21/inference.log,analysis.log,render_verification.log. Prior pending review/approval/index preserved at artifacts/history/v21_before_execution/.

Executed with project Python:

```sh
.venv/bin/python scripts/run_nonmonotone_v21.py
.venv/bin/python scripts/analyze_nonmonotone_v21.py
.venv/bin/python scripts/render_verify_nonmonotone_v21.py
PYTHONPATH=src .venv/bin/python -m pytest -q
```

All succeeded. The new provider path and analyzer are now exercised end-to-end. The renderer/mapping audit is explicitly post-collection, separately indexed from frozen inference. Completed-run/analysis guards prevent overwrites; do not delete them or reset ledgers. Reproduction with fresh model calls or another host remains untested and requires a separate bounded allowance.

## Costs and disposition

Observed4788 input tokens,60 output tokens,missing usage0. Output usage includes forced syntax/EOS. Requests:6.4575seconds;startup:4.0899seconds, including0.6839seconds model loading (do not double-count). Whole inference session:11.6498seconds, including model hash checks/orchestration. This turn with analysis/render:14.3014seconds; V21 including preparation:17.0909seconds.

0 new objective acquisitions,0 physical trials,0 download bytes,USD0 external spend. Historical data collection is not free or reset. No deployment cost/quality savings are estimated. Follow-up calls **140/140 exhausted**,240 including the initial stage. Cumulative runtime **1790.6854/1800seconds**, **9.3146seconds remaining**,ledger inactive. Recorded objective accesses5408 and physical trials1134 unchanged; separate cost types. No running worker, scheduled followup, paid/cloud usage, credentials, contact or publication.

The fixed three-attempt stop rule is complete. Stronger models, broader arbitrary permutations, repeated conditions, untouched families, true internal mechanisms, selection quality and useful escalation remain untested. The bounded pilot has concrete behavioral findings and falsified an overly broad explanation; it still has not demonstrated a useful benefit router.

**Single next action:** review the complete V19–V21 evidence with Tim and decide whether this limited, format-sensitive selection result warrants a larger prospectively specified study. No novelty, acceptance or publication claim is established; nothing has been sent.
