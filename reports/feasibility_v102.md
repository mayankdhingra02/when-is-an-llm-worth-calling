# V102: local model-loading feasibility

Both-condition feasibility criterion passed: **True**.

| Intended condition | Status | Strict final answer valid |
|---|---|---|
| sac_AllNumeric_11_nonthinking | completed | True |
| sac_AllNumeric_71_thinking | completed | True |

Actual requests: 3; returned responses: 3; retries: 0. Allocated output: 384 of 384 tokens. Returned-response output sum: 168; all-request output total: 168. Actual prefill total: 10035. Missing responses remain unknown, not zero.

Lifecycle 211.675s; startup 2.0403897909999955s; peak sampled model RSS 5,958,451,200bytes; exit 0; resource-stop reason None. Requests were serial with 120-second deadlines. The ten-minute stage cap and 8 GiB RSS guard were not raised.

The server command is unchanged from V100: `--load-mode none` with a shorter 128-token thought allowance followed by the unchanged 128-token final-answer allowance. The same pinned Qwen3-8B Q4_K_M model, 4096-token context, prompts and sampling were retained; only the thought/output-allocation limits were reduced. A different execution environment and tiny sample prevent causal attribution or a general speed/reliability claim. No system settings or other applications were changed.

Zero new objective outcomes were acquired or scored. These two previously exposed development cases use different seeds: they are not a fair thinking-versus-nonthinking quality comparison, held-out validation or evidence of useful routing. No fallback quality is attributed to the model. V97 remains the latest complete optimization comparison.

Raw evidence: `results/v102_reasoning/`; frozen method/model/code: `reports/protocol_v102.freeze.json`; independent saved-evidence audit: `artifacts/study_v102/feasibility.json`. Run `.venv/bin/python scripts/audit_feasibility_v102.py` and this report script to replay without new inference or labels. Do not rerun the once-only collector into existing output.
