# V173 amendment 2: continuation stages and smaller arm B stages

Written 2026-09-28, while stage A1R was running and **before any V173 recorded target was read and before any arm B request**. Hashes are in `artifacts/study_v173/freeze_amendment2.json`.

## Why

On the provider selected in P2 (`deepinfra/turbo`), gpt-oss-120b at reasoning effort `medium` writes about 4,500–7,800 completion tokens per arm A request, 3,000–6,000 of them reasoning. Each request takes about 25–46 s, so a 70-request arm A stage exceeds the 1,800 s per-stage wall cap after about 50 cases. Arm B stages of 17–18 cases would likewise stop about two-thirds through.

Under amendment 1, cases never started because the clock ran out would become fallbacks. That measures wall time, not the model. The per-stage cap follows the project's 30-minute-per-experiment convention in `configs/pilot.yaml`, and it is **kept, not raised**.

## Changes

1. **Continuation stages for arm A.** When A1R or A2 ends with never-started cases, continuation stages `A1R.c1`, `A1R.c2`, `A1R.c3` (and the same for A2) run **only those cases**, with identical settings and seeds, one at a time, each under the 1,800 s cap.
   - This is equivalent to having split the draw into smaller stages in advance. Which cases continue is decided by the clock, not by any outcome, and arm A reads no targets until E.
   - A case that was attempted and came back invalid, including a 429 that outlasted the backoff, is **not** retried.
2. **Arm B in eight stages, B1–B8.** Each takes a quarter of a V172 split in V172 job order, at most 9 cases, with a cap of 10 requests per case.
   - Cases never started because of the wall cap continue in `Bk.c1`–`Bk.c3`.
   - A case interrupted mid-loop (after some acquisitions) is **not** restarted with the model. As originally declared, EB rebuilds it fallback-only from its prefix, and its partial acquisitions stay charged.
3. **Order.** E waits until both arm A chains end. EB waits until all eight arm B chains end.
4. **Cost check.** Arm A costs about $0.004 per request on this provider. If the arm A spend projects arm B beyond the $3 client cap, **arm B will not start** until the owner decides. The cap is not raised automatically.
5. **Probe note.** In P2, `mancer/fp8` answered as "Mancer 2", and the client's name check treated that as a provider mismatch. Under the probe rule it counted as a failed probe; its response and cost are recorded. The chosen provider's served name (`DeepInfra`) matches its tag.

Nothing else changes: prompts, schema, seeds, token caps, reasoning setting, estimand and decision rule.
