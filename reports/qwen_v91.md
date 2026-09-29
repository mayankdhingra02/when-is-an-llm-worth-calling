# V91 — Larger-model robustness: improvement over SmolLM3, but not classical controls

The approved Qwen3-8B comparison completed locally: **30 paired cases, 300 scientific generation requests, three compatibility requests, and 300 newly acquired recorded outcomes.** There were no malformed choices, fallbacks, retries or timeouts. The server shut down cleanly.

The larger model improved the mean outcome over SmolLM3-3B by **1.22%**, but remained **1.26% below same-pool batch 3NN** and **3.20% below full-domain sequential 3NN**. It therefore failed the frozen primary screening criterion. A favorable comparison with the smaller model does not replace the unfavorable comparisons with the classical controls.

## Actual results

Positive gain favors Qwen3-8B. Means give equal weight to each of the six software families. Bootstrap intervals are descriptive; the 30 seeds/cases are not 30 independent systems.

| Reference | Mean relative gain | Descriptive family bootstrap 95% | Wins / ties / harms |
|---|---:|---:|---:|
| batch_3nn | -1.259% | [-3.424%, -0.036%] | 2 / 18 / 10 |
| full_sequential_3nn | -3.203% | [-6.035%, -0.738%] | 5 / 12 / 13 |
| qwen_0.5 | +1.221% | [+0.011%, +3.414%] | 5 / 24 / 1 |
| qwen_1.5 | -1.363% | [-3.484%, -0.183%] | 1 / 19 / 10 |
| smollm_3b | +1.221% | [+0.011%, +3.414%] | 5 / 24 / 1 |
| presentation_first10 | +1.221% | [+0.011%, +3.414%] | 5 / 24 / 1 |

All 11 comparators and 330 paired contrasts are retained, including the other classical methods and random controls. Qwen3 won in two cases against batch 3NN and five against full-domain sequential 3NN, so this is not a finding that LLMs never help. However, every family mean against full-domain sequential 3NN was negative. Only one family had a weak positive mean against the same-pool control.

The predefined screen required a positive mean and a positive lower descriptive bootstrap bound against **both** primary controls. It failed. These are six previously exposed families, so neither the intervals nor occasional wins establish generalization or a useful router.

## What changed in the model’s choices

Qwen3 selected IDs 0 through 9 in presentation order in **21/30 cases**, compared with **29/30** for the preserved SmolLM3 V47 run. It matched the simple first-ten rule’s final target in 24 cases, improved five and harmed one. That rule was included prospectively in V91; its outcome labels already existed in historical traces, requiring no additional acquisitions.

The larger model therefore changed some decisions. That does not prove it used the observed performance values appropriately. The earlier V48/V49 loss, order and decoder interventions tested SmolLM3; their causal interpretation cannot simply be transferred to Qwen3.

## Fixed design and provenance

All 30 original V41/V47 jobs were retained: six software families, five seeds each, the exact saved ten-observation prefix, the same 20-candidate pool, and identical message content and order. Each model continuation selected ten additional configurations; the evaluator separately charged those outcomes and checked 20 distinct logical evaluations per branch. The collector never opened the objective tables. Historical classical and smaller-model traces were reused as paired comparators, not presented as new measurements.

The model is the owner-released [Qwen3-8B GGUF](https://huggingface.co/Qwen/Qwen3-8B-GGUF), Q4_K_M, revision `7c41481f57cb95916b40956ab2f0b139b296d974`. The 5,027,783,488-byte file matched SHA256 `d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785`. Revision-specific Apache 2.0 license, README and file pointer are retained in `artifacts/sources/v91/`. No repository setup code or shell installer was executed.

The existing llama.cpp b11146 runtime used a 4,096-token context, greedy non-thinking decoding, one slot and one generated ID per request. Grammar excluded previously selected IDs; newlines were inserted between choices. This preserves the earlier interface, not unrestricted reasoning or token-for-token equivalence across tokenizers. All prompts and 21 ID/delimiter token encodings were checked before scientific generation. Three synthetic A/B/C compatibility probes are saved separately and excluded from scientific aggregates, while still counting their real model cost.

The 471-input protocol freeze preceded every generation. All 18 historical predecision policy summaries were retained without refitting. Matched-rate cohort diagnostics and the hindsight oracle remain labeled; these old controllers may be miscalibrated for Qwen3.

## Actual local cost and reliability

| Measurement | Observed value |
|---|---:|
| Inference lifecycle, including startup | 238.415 seconds |
| Startup | 4.097 seconds |
| Scientific request wall-time sum | 233.002 seconds |
| Peak sampled server RSS | 5,952,241,664 bytes — about 5.95 GB / 5.54 GiB |
| Scientific / compatibility generation requests | 300 / 3 |
| All HTTP requests, including metadata and health | 404 |
| Generated tokens, including compatibility | 303 |
| Scientific full-context token sum | 495,610 |
| Runtime-reported tokens actually prefilled | 49,831 |
| New recorded outcomes acquired | 300 |
| External spending | USD 0 |

Full-context token counts include repeated contexts; actual prefill counts reflect cache reuse. They are not interchangeable costs. Electricity and hardware costs are unknown. Historical comparator collection is not free deployment. Retrospective policy costs count selected branches and explicitly exclude startup, objective execution and controller overhead.

No tests, downloads or other managed experiments ran during inference. Ordinary host activity was uncontrolled. The RSS watchdog samples one process group; it is not total system or comprehensive Metal memory accounting. Full GPU offload was requested, but the default log does not enumerate actual device residency. A control-token metadata override warning was retained; tokenization and output checks passed. No restart was performed to obtain more verbose evidence. This run demonstrates local feasibility, not production reliability or causal latency superiority over older runs.

New downloads totaled **5,027,802,744 bytes**, including 19,256 metadata bytes. A zero-byte sandbox DNS failure preceded the allowed transfer; no partial model transfer was retried. Cumulative downloads are 9,867,753,109 bytes, leaving 869,665,131 under the approved 10 GiB cap. Cumulative model downloads are 9,126,358,023 bytes, leaving 537,318,393 under the approved 9 GiB model cap. The download is a setup cost, not a repeated cost per deployed decision.

## Evidence and reproduction

- Protocol and freeze: `reports/protocol_v91.md`, `reports/protocol_v91.freeze.json`.
- Explicit approval and download provenance: `artifacts/study_v91/` and `artifacts/sources/v91/`.
- Raw prompts, tokenization, requests, responses, choices, probes and server logs: `results/v91_qwen/`.
- Acquisitions, arms, all comparisons, policy summaries and figures: `results/v91_analysis/`.
- Independent verification rechecked 300 source outcomes, 300 scientific responses, 330 paired contrasts and 18 policy summaries. A separate audit checked all 303 request charges, three probes, download/model hashes and resource limits. See `independent_verification.json` and `runtime_cost_audit.json` under the stage artifacts.
- **685 tests passed in 21.61 seconds.** The precollection full suite and additional runtime guard tests passed before freezing. Synthetic fixtures remain outside measured aggregates.

Executed scripts, all with `.venv/bin/python`: `fetch_qwen_v91.py`, `freeze_qwen_v91.py`, `collect_qwen_v91.py`, `analyze_qwen_v91.py`, `verify_qwen_v91.py`, `audit_runtime_qwen_v91.py`, and `report_qwen_v91.py` under `scripts/`. The full test command was `-m pytest -q tests`.

Figure regeneration reads saved analysis and makes no model or database calls. Collection and evaluation refuse existing output directories, preventing implicit retries or reacquisitions. Fresh model execution requires an isolated copy, pinned runtime/model and a new request allowance. Current-machine verification is not a clean-machine replication. The server exited; no inference job remains running.

## Limits and next action

This narrows the explanation that only the 3B model was too weak: a larger model helped some outcomes but did not beat either primary classical method under this interface. Architecture, quantization and tokenizer also changed, so this is model-bundle robustness, not a causal parameter-scaling experiment. Non-thinking, one-token selection does not test unrestricted reasoning. Recorded-table results must remain separate from V86’s native-workload findings.

**Next priority:** a prospectively specified Qwen3 loss/order-sensitivity check on the original development groups, reusing the V48/V49 controlled diagnostic design, before trying to learn a router from occasional wins. Compare underlying configuration identities after permutation, and do not select favorable prompts or seeds. All 303 approved V91 requests are consumed; that follow-up needs its own bounded allowance. Independent untouched systems and clean-machine/native replication still remain necessary. Journal readiness is not established by this batch.

![Primary family comparisons](../results/v91_analysis/family_gains.png)
