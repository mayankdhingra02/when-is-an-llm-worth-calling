# V173 protocol: SNAP2's model on the recorded cohort

**Purpose.** V172 showed no testable router question for local 3B–14B models. The biggest remaining objection is that SNAP2 (Srinivasan & Menzies, arXiv:2607.02583v1, §IV-E) used `openai/gpt-oss-120b` via OpenRouter with an iterative two-proposal loop. V173 tests that model on the same exposed 70-case recorded cohort in two arms:
- **Arm A** holds V172's interface fixed and changes only the model.
- **Arm B** adopts SNAP2's iterative design.

The owner's approval for this paid inference, with a $3 cap enforced in our own code, is recorded in `artifacts/study_v173/authorization.json`. All tasks and classical comparators are exposed, so these are new model draws on exposed tasks, not a fresh held-out cohort.

## Common settings (fixed before any scientific request)

- **Model and service.** `openai/gpt-oss-120b` via `https://openrouter.ai/api/v1/chat/completions`.
- **Provider pinning.** Pinned to one provider with `allow_fallbacks: false` and `require_parameters: true`.
  - The provider is the first of `coreweave/fp4`, `nebius/fp4`, `deepinfra/bf16`, `dekallm/bf16` to pass preflight, and stays fixed for every scientific request.
  - fp4 matches the weights' released precision. Weights cannot be hash-pinned on a hosted service; the provider, model ID, response ID and usage are recorded for every request.
- **Reasoning.** Effort is fixed at `medium`. SNAP2 does not report its setting, so this is our choice, made in advance.
- **Output.** `max_tokens` is 4,000, SNAP2's cap for tasks with fewer than 77 features; our widest has 59. Reasoning tokens count against it.
- **Sampling.** Temperature 0.7. top-p is 0.95 in arm A (V172's value) and 1.0 in arm B (SNAP2's value). Seeds are fixed per request; a seed does not guarantee determinism on a hosted service.
- **Constrained output.**
  - Responses must follow a strict JSON schema `{"proposals": [...]}` with exactly N strings. Each string gets a per-position pattern over the same symbol alphabet and domains as V141–V172, so the grammar is expressed as a schema.
  - The parser accepts that object, or a bare array of exactly N strings. Anything else, a truncation (`finish_reason` other than `stop`) or an HTTP error is invalid.
- **Costs and caps.**
  - Before each request, the client checks: recorded spend plus the worst case for this request (estimated input tokens plus `max_tokens`, at the listed price, times 1.25) must stay within $3.00. Otherwise it refuses.
  - Recorded spend is OpenRouter's reported cost where available, and otherwise tokens times listed price times 1.25.
  - Per-stage request caps: P 4, A1 70, A2 70, and 180 for each of B1–B4.
  - The key's own $5 limit sits behind the client cap.
- **Scope of access.** The client reads only `~/.config/llm-escalation-study/openrouter_key` and never logs the key. Requests go only to `openrouter.ai`, and redirects are refused.

## Arm A: model-only contrast with V172

- **Inputs.** The same 70 message lists, byte-identical to V172. Two draws: A1 uses each job's `sampling_seed`, and A2 uses its `redraw_seed`.
- **No retries.** An invalid response takes the origin stage's historical fallback, exactly as in V172: V141 cases use batch 3NN; Spark and Hadoop cases use stepwise sequential 3NN.
- **Evaluation E.** Seal all 140 selections using V172's `evaluate_v172.select`, then charge at most 1,400 recorded acquisitions through the V172 oracles and a V173 ledger.

## Arm B: SNAP2-style iterative loop

- **Rounds.** Each case gets 5 rounds of 2 proposals, 10 acquisitions after the shared B10 prefix (a B20 budget).
- **Messages per round:**
  1. A system role message: an optimizer proposing exactly two configurations per round, JSON only.
  2. The case's original V172 task messages as context, with the count explicitly overridden to two.
  3. A round block containing:
     - hard per-position symbol constraints;
     - the objective direction;
     - the trajectory of every measured setting (prefix plus acquired so far), sorted worst to best and formatted as in the origin prompt;
     - a collision list of earlier proposals that mapped to already-measured settings;
     - a retry notice when the previous attempt was invalid;
     - a reminder of the rules and remaining budget;
     - the output format.
- **Only acquired labels ever appear in prompts.**
- **Projection.** Each proposal maps to the nearest unmeasured row using the origin stage's feature distance. A proposal whose nearest row overall is already measured is a collision: it is nudged to the nearest unmeasured row and listed in later rounds.
- **Retries and fallback.** Each round allows one retry after an invalid response. If the retry also fails, the round takes two acquisitions from the origin's fallback rule and is counted as a fallback round.
- **Order of operations.** Each round's selection is recorded before its targets are acquired. At most 700 acquisitions.
- **Stages.** Four stages, B1–B4. Each takes half of a V172 split in V172 job order (B1: split 1, first half; B2: split 1, second half; B3 and B4 likewise for split 2). Each is capped at 1,800 s and at 10 requests per case (180). A stage stopping early keeps its unfinished cases in the denominator; stage EB rebuilds each unfinished case from its saved prefix with the origin fallback for all 10 labels, without model requests. Acquisitions already charged in an interrupted attempt stay charged and are reported.

## Stage order, gates and failure rules

- **Order.** P → A1 → A2 → E (arm A) → B1 → B2 → B3 → B4 → EB, one stage at a time.
- **P (preflight).**
  - Records the key's reported limit and usage, without printing the key.
  - Checks the chosen provider's listed parameters.
  - Sends synthetic, non-research requests (at most 4, trying providers in the order above) until one returns a schema-valid 2-string answer. That provider becomes the pinned provider.
- **No other retries and no stage repeats.**
- **Any provider mismatch** in a response, a spend-cap refusal or a wall cap ends the stage with its denominator intact.
- **Freeze first.** Code, config, protocol, jobs and tests are hash-frozen in `artifacts/study_v173/freeze.json` before P.

## Analysis (frozen in `scripts/analyze_v173.py`)

- **Primary.** For arm A (draw A1) and arm B separately: the number of V151 ecosystems with an LLM-specific win, meaning beating sequential 3NN, random-full, adaptive neighbor and GP-EI (ℓ=1) each by >1%.
- **Decision.**
  - If A1 or B reaches ≥2 of 7 ecosystems: LLM-specific headroom exists at SNAP2's model scale on this cohort. A router study would then need a fresh, headroom-gated cohort.
  - Otherwise: the no-LLM-specific-headroom boundary extends to SNAP2's model on this cohort.
- **Secondary:**
  - A2 as a sampling-variability check;
  - equal-ecosystem relative and log-ratio gain against sequential, and hindsight headroom;
  - counts against each single switch;
  - paired comparisons with the V172 arms;
  - validity, fallbacks, retries, collisions, reasoning and output tokens, and dollars.
- **Scope of claims.** Cohorts are never pooled, seeds are not independent systems, and there are no significance tests. Every arm, failure and cost is reported.
