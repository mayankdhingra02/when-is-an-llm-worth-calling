# V103: reasoning with a final-answer reserve

**Development-only methodological comparison.** The previous V95, V97 and interrupted V98 studies remain unchanged. V99–V102 failures and feasibility checks also remain separate. This adds no independent held-out software systems and does not establish a learned router.

| Procedure | Valid finals / intended | Mean policy gain vs sequential | Valid model >=5% wins vs BOTH strong controls |
|---|---:|---:|---:|
| thinking | 10/12 | -7.64% | 0 |
| nonthinking | 12/12 | -6.52% | 0 |

Thinking uses up to128 tokens followed by a separate128-token final-answer request. The actual first response is reused verbatim; the end-of-thinking delimiter is explicit prompt control, not recorded as model output. Nonthinking has one128-token request. Both use native decoding and owner-informed mode-specific sampling. Strict ten-unique-ID parsing is unchanged. Mode and sampling differ together, so this is not a pure causal ablation of reasoning alone.

## All system groups

| System | Reasoning policy vs sequential | Nonthinking policy vs sequential | Reasoning policy vs batch | Nonthinking policy vs batch |
|---|---:|---:|---:|---:|
| berkeleydb | +2.62% | +2.56% | -0.06% | -0.12% |
| dune_hsmgp | -45.74% | -21.76% | -24.86% | -0.21% |
| hipacc | -2.31% | -3.01% | +1.08% | +0.41% |
| llvm | -0.29% | -0.29% | +0.00% | +0.00% |
| openvpn | -0.13% | -16.60% | +0.00% | -16.51% |
| sac | +0.00% | +0.00% | +0.00% | +0.00% |

Each group has two seeds per mode. System means, not seed counts, are the independent-domain unit; all six systems were already exposed during development. Full intended-policy means include the fixed classical fallback for failures/unattempted cases. Such gains are not attributed to the LLM. Valid-only coverage and means are retained separately in `coverage_quality.json`; do not silently drop failures or confuse partial coverage with the intended24-condition comparison.

## Reliability and actual cost

Charged model requests:36; returned responses:36; lifecycle:936.011s; peakRSS:8,356,478,976bytes. Allocated output ceiling consumed:4,608tokens. No retries. Returned generated tokens:2,122; reported actual prefill:60,806; summed full context:60,806. Both inference phases and repeated prefill are counted. Missing response usage, if any, remains unknown.

Newly charged recorded-table accesses:240, covering all24 intended arms with ten continuation labels each. Each uses its saved10-label prefix for logicalB20. Old prefix/classical-reference collection is historical cost and is not free. No native numerical workload was executed in this stage. New downloads0, external spendUSD0; electricity/hardware unknown.

For modeled deployment, a thinking escalation uses up to2 model requests and256 allocated output tokens; nonthinking uses1 request and128 tokens. Both select at most10 new configurations after the same10-label checkpoint. This is an accounting scenario, not measured deployed savings.

## Limits and interpretation

This is an adaptation of prior budget-forcing ideas with a small quantized model and a short reasoning allowance. Final-answer delivery and selection quality are separate outcomes. No result here establishes unrestricted reasoning quality, model-wide behavior, novel routing ability or publication readiness. Public-benchmark contamination and exposed development data remain limitations. Do not choose a new threshold, prompt or budget using held-out outcomes.

Raw prompts, thought/final responses, controls, usage and failures: `results/v103_reasoning/`. Saved acquired labels and outcomes: `results/v103_analysis/`. Protocol/code/model/data freeze: `reports/protocol_v103.freeze.json`. The budget-forcing source audit explicitly distinguishes prior work from this adaptation.

Reproduce saved-data audit with `scripts/verify_reasoning_v103.py` and report with `scripts/report_reasoning_v103.py`. Do not rerun `analyze_reasoning_v103.py` into existing results: it is the once-only charged acquisition step.
