# V99: smaller context did not restore inference

The user-requested 4096-context repeat charged one real Qwen3 request and returned no response before its 120-second deadline. The first condition failed and 35 of 36 conditions were unattempted. No retry or fabricated answer. Total generated/prefill token usage is unknown. Allocated output was 128 tokens.

Lifecycle 130.239 seconds; peak sampled model RSS 5,769,822,208 bytes. The RSS guard did not trip. Cleanup escalated from SIGTERM to SIGKILL after three seconds (exit -9). Prompt processing was still incomplete in the server log. Read-only memory observations suggest pressure but do not establish its cause.

All 36 intended policy arms were retained using explicitly classical fallback and 360 charged recorded-table accesses. Saved-evidence replay passed. Their mean -2.5752% gain against sequential 3NN is entirely fallback behavior, not an LLM-quality result. An empty response journal was initialized after shutdown for consistent replay; its receipt records zero fabricated responses.

The latest completed comparison remains V97: no >=5% LLM win against either strong classical control in five exposed SuperLU seeds. Neither useful benefit prediction nor Q2 readiness is established.

Next: a separately frozen two-condition feasibility check using the binary's documented `--load-mode none`. Keep model, context, sampling, per-request deadline and RSS cap fixed. This may reduce paging, but no improvement is assumed. No new objective acquisition is needed for feasibility. The full runtime help is saved under artifacts/study_v99/.
