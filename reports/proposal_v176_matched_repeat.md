# DRAFT: matched repeat of gpt-oss-120b, one-shot vs iterative loop

**Status:** draft for discussion. Not frozen, not authorized, not executed. No request has been sent, and the spending cap has not been raised. Running it would require the owner to approve it explicitly, set a new cap, and freeze the protocol (below) before any request.

## Why

The manuscript's comparison of the iterative loop with one-shot prompting rests on one loop draw and two one-shot draws. Three observations limit it:

- the loop was more than 1% better than the first one-shot draw in 19 cases and worse in 10;
- the two one-shot draws disagreed by more than 1% in 26 of 70 cases;
- the loop's primary mean (−3.14%) is almost the same as the second one-shot draw's (−3.16%).

With one draw per interface, an interaction effect cannot be separated from sampling variation. This repeat would **improve the evidence** on that question for this cohort. It may not settle it: the outcome "no reliable difference at this sample size" is allowed and would be reported as such.

## Fixed design

- **Cases.** All 70 task–seed cases of the recorded cohort, with their existing saved prefixes, which are identical to V172/V173 (`artifacts/study_v172/jobs.json`). No case is added, removed or selected based on earlier outcomes.
- **Arms.** Two new one-shot draws (O1, O2) and two new loop draws (L1, L2), four arms of 70 cases each. Each arm uses the V173 interface unchanged: the same prompts, JSON schemas, projection, fallback rule and retry policy.
- **Model and settings:**
  - `openai/gpt-oss-120b` via OpenRouter, pinned to the V173 provider (DeepInfra `turbo`, bf16) under the V173 probe rule;
  - reasoning effort medium, temperature 0.7;
  - output caps of 16,000 tokens (one-shot) and 8,000 tokens (loop);
  - the same bounded 429 backoff.
- **Interleaving.** Requests follow one seeded random order that interleaves the four arms within each case block. Provider drift and rate limiting therefore fall on both interfaces alike. Every request records its draw index, and no cached response is reused.
- **Collection is blind to outcomes.** Targets are acquired and scored only in a separate evaluation stage, after all model responses are collected.

## Estimand and decision rule (fixed before collection)

**Primary estimand.** For each case, take the mean relative gain over sequential 3NN of L1 and L2, minus that of O1 and O2. Average these differences with equal weight per ecosystem, the paper's primary weighting. The primary analysis uses only the four new draws. Pooling with the three earlier draws, which have already been seen, is a labelled secondary analysis.

**Reported alongside:**

- engine-balanced and case-weighted averages;
- the leave-one-ecosystem-out range;
- the number of ecosystems in which the loop is ahead;
- disagreement within each interface (O1 vs O2, L1 vs L2);
- baseline-set wins and hindsight headroom per arm.

**Decision** (descriptive; no significance test, consistent with the paper):

- **Loop ahead:** the primary difference exceeds +1 percentage point, the loop is ahead in at least 5 of the 7 ecosystems, and every leave-one-ecosystem-out value is positive.
- **One-shot ahead:** the same three conditions with the signs reversed.
- **No reliable difference at this sample size:** anything else.

## Stopping rule

The sample size is fixed at 4 arms × 70 cases, and nothing stops early because of outcomes. Collection stops before completion only on these operational triggers, each recorded with its time and the full denominators:

1. **Spend.** The next request could push the reported spend past the new hard cap. The client reserves the maximum cost of each request before sending it, as in V173.
2. **Provider.** The serving provider or model identity differs from the pinned one. There is no substitution.
3. **Invalid responses.** More than 10% of any 20 consecutive calls are invalid or truncated.
4. **Wall clock.** A stage exceeds its declared limit. Continuation stages must be declared in advance, as in V173 amendment 2.

A stopped run is reported as incomplete, with every attempted request counted. It is not analysed as the planned estimand.

## Cost and time estimate

The estimate uses V173's recorded provider charges. Prices must be rechecked on the day of freezing.

| Item | Basis (V173 actuals) | Estimate |
|---|---|---:|
| 2 one-shot draws | $0.249 and $0.239 per 70-case draw | $0.49 |
| 2 loop draws | $0.887 per 70-case draw, including retries | $1.77 |
| Provider probe | V173 probes: $0.0017 | $0.01 |
| **Expected total** | | **$2.27** |
| Contingency for token variance and retries (15%) | | $0.34 |
| **Proposed hard cap** | | **$3.00** |

About $1.62 remains under the existing V173 cap, which is not enough, and that authorization covered V173 only. About $3.62 of the owner's $5 credit remains. **A new explicit owner decision and a new cap are required.**

A smaller variant (one new draw per interface, about $1.14) would fit, but it would add only one draw of each interface. It is not recommended.

Expected wall time is roughly 3–4 hours, based on V173 latencies: about 30 s per one-shot call and 10 s per loop call, plus rate-limit pauses.

## Before any request

1. The owner records an authorization with the cap.
2. A config file is written: arms, seeds, interleaving order, caps and provider pin.
3. The protocol file is written with the decision rule above, verbatim.
4. A freeze record hashes the code, prompts (which must match V173 byte for byte), inputs and protocol.
5. The targeted tests pass.

Nothing is sent before step 4.

## What it cannot establish

- **Systems.** It uses the same 70 cases and 7 ecosystems, one of which holds 40 cases, so it says nothing about other systems.
- **Model, provider and budget.** It uses one model, one provider and one budget.
- **Mechanism.** Two draws per interface narrow the uncertainty about sampling variation but do not remove it. A loop advantage would still not identify which part of the loop (feedback, retries or collisions) is responsible.
