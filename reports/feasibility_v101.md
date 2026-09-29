# V101: local model-loading feasibility

Both-condition feasibility criterion passed: **False**.

| Intended condition | Status | Strict final answer valid |
|---|---|---|
| sac_AllNumeric_11_nonthinking | completed | True |
| sac_AllNumeric_71_thinking | request_failure | False |

Actual requests: 2; returned responses: 1; retries: 0. Allocated output: 640 of 768 tokens. Returned-response output sum: 20; all-request output total: unknown. Actual prefill total: unknown. Missing responses remain unknown, not zero.

Lifecycle 137.293s; startup 2.5517466670000033s; peak sampled model RSS 5,954,420,736bytes; exit 0; resource-stop reason None. Requests were serial with 120-second deadlines. The ten-minute stage cap and 8 GiB RSS guard were not raised.

The server command is unchanged from V100: `--load-mode none` and the same limits, rerun after a user-performed Mac restart. The same pinned Qwen3-8B Q4_K_M model, 4096-token context, prompts, sampling and output limits were retained. A different execution environment and tiny sample prevent causal attribution or a general speed/reliability claim. No system settings or other applications were changed.

Zero new objective outcomes were acquired or scored. These two previously exposed development cases use different seeds: they are not a fair thinking-versus-nonthinking quality comparison, held-out validation or evidence of useful routing. No fallback quality is attributed to the model. V97 remains the latest complete optimization comparison.

Raw evidence: `results/v101_reasoning/`; frozen method/model/code: `reports/protocol_v101.freeze.json`; independent saved-evidence audit: `artifacts/study_v101/feasibility.json`. Run `.venv/bin/python scripts/audit_feasibility_v101.py` and this report script to replay without new inference or labels. Do not rerun the once-only collector into existing output.
