# V100: local model-loading feasibility

Both-condition feasibility criterion passed: **False**.

| Intended condition | Status | Strict final answer valid |
|---|---|---|
| sac_AllNumeric_11_nonthinking | request_failure | False |
| sac_AllNumeric_71_thinking | unattempted | False |

Actual requests: 1; returned responses: 0; retries: 0. Allocated output: 128 of 768 tokens. Returned-response output sum: 0; all-request output total: unknown. Actual prefill total: unknown. Missing responses remain unknown, not zero.

Lifecycle 139.723s; startup 16.507453292026184s; peak sampled model RSS 5,802,639,360bytes; exit -9; resource-stop reason None. Requests were serial with 120-second deadlines. The ten-minute stage cap and 8 GiB RSS guard were not raised.

The only server-command change from V99 was `--load-mode none`, supported by the saved installed-runtime help. The same pinned Qwen3-8B Q4_K_M model, 4096-token context, prompts, sampling and output limits were retained. A different execution environment and tiny sample prevent causal attribution or a general speed/reliability claim. No system settings or other applications were changed.

Zero new objective outcomes were acquired or scored. These two previously exposed development cases use different seeds: they are not a fair thinking-versus-nonthinking quality comparison, held-out validation or evidence of useful routing. No fallback quality is attributed to the model. V97 remains the latest complete optimization comparison.

Raw evidence: `results/v100_reasoning/`; frozen method/model/code: `reports/protocol_v100.freeze.json`; independent saved-evidence audit: `artifacts/study_v100/feasibility.json`. Run `.venv/bin/python scripts/audit_feasibility_v100.py` and this report script to replay without new inference or labels. Do not rerun the once-only collector into existing output.
