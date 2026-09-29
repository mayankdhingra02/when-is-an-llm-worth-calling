# DRAFT (revision 3): matched repeat of gpt-oss-120b, one-shot vs iterative loop

**Status:** draft for discussion. Not frozen, not authorized, not executed. No request has been sent, and the spending cap has not been raised. Running it would require the owner to approve it explicitly, set a new cap, and freeze the protocol (below) before any request.

This revision supersedes `proposal_v177_matched_repeat.md` and `proposal_v176_matched_repeat.md`, which are kept unchanged. Revision 2 made two rules explicit: which comparison is primary, and what happens if the cap or another stop is reached before every pair is complete. Revision 3 corrects when objective values are acquired. Revision 2 said all targets would be acquired after every response was collected, which is impossible for the iterative loop: each round needs the values measured in earlier rounds.

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
- **Which outcomes each arm sees.** Each loop arm acquires its own charged objective labels round by round and uses them as feedback in its next round, exactly as the V173 loop collector did. It never sees another arm's outcomes. One-shot arms need no feedback, so their proposals are collected first and their targets acquired afterwards, as in V173. No comparative scoring and no result-dependent decision happens until collection has finished or an operational stop has occurred.

## Estimand and decision rule (fixed before collection)

**Primary estimand.** For each case, take the mean relative gain over sequential 3NN of L1 and L2, minus that of O1 and O2. Average these differences with equal weight per ecosystem, the paper's primary weighting.

**Which draws count.** The primary comparison uses only the four new, balanced draws: two per interface on every case. The three earlier draws (two one-shot, one loop) are never mixed into it. A secondary analysis pools all seven draws. It is reported separately and labelled as including draws whose outcomes had already been seen when this plan was written.

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

**Completeness, retries and in-flight costs:**

- **Unit of completion.** A case is complete only when all four new arms (O1, O2, L1, L2) have finished for it, including any fallbacks. Because requests are interleaved within case blocks, at most one case block is partly done at any time.
- **If collection stops early.** The report gives the number of complete cases out of 70 and lists every partly finished case with the arms it has. The primary estimand is not computed, and no conclusion about loop versus one-shot is drawn. Complete cases may be described, labelled as an incomplete descriptive summary. Partly finished cases are never dropped from the denominators.
- **Retries and 429s.** Loop retries after invalid responses count as calls, and their reported cost counts toward the cap. Rate-limit rejections (HTTP 429) are logged with their count and backoff, but not counted as calls.
- **In-flight requests and the cap.** Before each request, the client reserves that request's maximum possible cost (output cap × output price, plus the prompt), as in V173. It sends only if spend plus all reservations stays within the cap, so an in-flight request cannot take spending past the cap. Reservations are reconciled against the provider-reported cost when each response arrives. If a request is still in flight when collection stops, its cost is recorded as unknown, not zero, until reconciled. The report states the maximum it could have added.
- **Budget check before starting.** If the expected total at the day's prices exceeds 80% of the cap, the run is not started, and the plan returns to the owner.

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
