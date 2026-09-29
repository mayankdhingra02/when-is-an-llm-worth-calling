# Next step after V173

The V172 version of this file is preserved in `artifacts/study_v173/previous_snapshot/reports/next_experiment.md`.

## Where the evidence stands

| Tested so far | LLM-specific wins (ecosystems of 7) |
|---|---|
| Local 3B–14B models (V141–V172) | 0–1 |
| SNAP2's model, gpt-oss-120b, hosted (V173) | 2 in one draw at the threshold; 1 in the other draw and in the SNAP2-style iterative arm |

- **Reproducible positives sit in one ecosystem** (Spark/Hadoop).
- **`spark::bayes_11` is the only win present in all three gpt-oss runs.**
- **Averages still favor cheap classical search.**

## Recommended: write-up

The contribution is a graded boundary result with a reusable methodology:
1. Paired-prefix escalation with charged budgets, hidden-label isolation, full failure denominators and separate research and deployment costs.
2. Escalation benefit measured against the best pre-specified cheap switch, not the incumbent's own continuation.
3. Small local models add no LLM-specific value.
4. SNAP2's model adds rare, concentrated value, strongest under iterative feedback.
5. Routers are non-identifiable when positives are concentrated in one group; zero-call abstention is the correct policy there.

Report the frozen V173 decision exactly, with the post-hoc sensitivities labeled. Disclose the V1–V173 history and every amendment.

## Optional, needs an owner decision

**Pre-registered arm B replication.**
- **Design:** two more draws of the SNAP2-style loop on the same 70 cases.
- **Rule:** fixed before collection, for example "≥2 ecosystems with LLM-specific wins in at least 2 of 3 arm B draws".
- **Cost:** about $1.77 at the measured $0.89 per draw. The remaining V173 client cap is $1.62, so the cap would have to be raised.
- **What it settles:** whether the frozen threshold result is reproducible.
- **What it doesn't:** it cannot create cross-system router evidence on this cohort.

## Not recommended

- Training or reporting a leave-one-group-out router on these exposed cases as if it generalized.
- More seeds, prompts or interfaces tuned on this cohort.
- A second host: it cannot affect recorded-table evidence.

## Long-horizon

A router test requires a fresh cohort with LLM-specific positives in several independent groups:
- many large-domain systems;
- headroom gated before any LLM call;
- the V173 interface frozen.

The admissible unexposed recorded-table pool is nearly exhausted, so this means new native task construction at considerable effort.

Counters after V173: 5,487 cumulative model starts; 45,113 recorded-table charges plus two historical incidental exposures; $1.38 paid spend (V173 only). The V172 and V173 approvals are not standing permission.
