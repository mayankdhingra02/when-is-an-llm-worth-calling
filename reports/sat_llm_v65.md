# V65 — real native SAT proposals fail the frozen reliability contract

Five real local SmolLM3-3B requests ran on all five saved prefixes of the task
admitted by V64. **0/5 outputs satisfied the frozen contract;
5/5 used the paired RF fallback.** No valid LLM proposal arm
was measured and no LLM-attributable quality gain was observed. Equal terminal
scores are operational fallback ties, not evidence of model/classical equivalence.

| Seed | Strict result | Request seconds | Generated tokens | Duplicate occurrences after fence removal | Already acquired distinct IDs |
|---|---|---:|---:|---:|---:|
| 11 | invalid: invalid_json | 5.401 | 217 | 0 | 8 |
| 23 | invalid: invalid_json | 5.321 | 215 | 1 | 6 |
| 37 | invalid: invalid_json | 5.527 | 215 | 3 | 7 |
| 53 | invalid: invalid_json | 5.759 | 227 | 1 | 5 |
| 71 | invalid: invalid_json | 5.345 | 217 | 2 | 7 |

![Actual request latency and reliability](../results/v65_sat_llm_analysis/reliability.png)

## Actual execution and bounded costs

The approved protocol allowed five generations, at most1,024 output tokens each,
900seconds collection,50new recorded acquisitions,0retries/downloads/spending.
Actual: five requests, 1091 generated
tokens and 3005 evaluated input tokens,
28.296seconds total collection including
0.834seconds startup, and **0 new
recorded acquisitions**. The server shut down with exit0. All five requests have
observed token counts; no failed transport or missing intended case. Physical SAT
table construction (288V64 trials plus9admission trials) remains actual research
cost, distinct from inference and a modeled deployment's evaluation cost.

Existing owner-pinned SmolLM3-3B Q4_K_M weights, revision
4965cb60b150737b68a0408c36aeefb65078f894, were used with local llama.cpp b11146.
This is the same3B model already available, not a new model/reasoning-enabled test.
Thinking was off, temperature0, seed11 requested, native unconstrained decoding,
no retries, projection or repair. Exact executable/model hashes, commands,
rendered prompts, token IDs, request starts, native response metadata and raw
outputs are preserved. Fixed seed does not establish cross-device determinism.

## What failed, and what cannot be inferred

All five responses included Markdown code fences despite the explicit JSON-only
instruction. The predeclared parser rejects these. This is partly an interface
contract result; it does not demonstrate that the model cannot optimize SAT.
A separately labeled **post-hoc, outcome-free diagnostic** removes exactly one
outer JSON fence and checks proposal identities, without reading additional
objectives or constructing a repaired optimization arm. Only 0/5 then satisfy
the remaining ten-unique-unobserved contract. See the table for duplicate and
already-acquired proposals. This diagnostic neither overrides the frozen result
nor counts repaired choices as real measured model arms.

All operational arms reuse their corresponding saved RF branch. The primary
always-escalate-versus-never comparison has five ties and pays additional inference
cost; the hindsight best-of-two diagnostic also cannot improve on RF here. No
finite inference break-even is observed. Because terminal improvement is zero,
counting startup or additional overhead cannot turn this implementation into a
net-benefit result. Positive terminal differences against other classical controls
would be RF fallback behavior, not model credit.

The broader opportunity result remains: on planted_512, preselected RF left
47.13% headroom in two of five cases, about43.55ms absolute. Thus lack of opportunity
alone does not explain this failure; reliable novel proposals are an additional
requirement. This is one generated task in one development solver family, after
adaptive feasibility and opportunity admission. It is not an independent held-out
replication, learned-router evaluation, significance result or Q2-readiness proof.
Five seeds cannot substitute for independent software systems.

## Verification and stop decision

Independent verification checks frozen sources/model/runtime and approval hash,
all five request starts and complete raw responses, rendered prompt identity,
context reserve, strict domain/uniqueness/exclusion rules, fallback provenance,
shared ten-prefix/twenty-inclusive budgets, all five pair effects and observed
token counts. The verifier does not use the production parser. All415 Python tests
pass, with ten new synthetic parser/prompt tests isolated from measured outcomes.
The diagnostic above is a report addition made after observing output formatting.

```sh
.venv/bin/python scripts/verify_sat_llm_v65.py
.venv/bin/python scripts/report_sat_llm_v65.py
```

Stop prompt/decoder/grid tuning on these exposed cases as frozen. A future test
would need a separately frozen reliability-preserving interface (for example,
constrained legal unobserved proposals) and fresh eligible software-system groups,
not another prompt chosen until these five cases pass. Such a test remains
unexecuted. No further model allowance, background job, cloud spend or publication
is implied. Raw results: results/v65_sat_llm/; paired fallbacks, cost summaries and
the labeled diagnostic: results/v65_sat_llm_analysis/.
