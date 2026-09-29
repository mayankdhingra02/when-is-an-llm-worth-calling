# V175: response to the second manuscript review (post-hoc, exploratory)

Source: `scripts/revision_v175.py` → `results/v175_revision/analysis.json`. It reuses sealed V141–V174 records and V151/V154 decisions unchanged. It makes no acquisitions, model requests or downloads. Everything here was computed after all outcomes were known.

## Accepted and implemented

1. **The deployable classical selector itself loses to the reference.** It trails the reference by −2.58% (ecosystem-balanced) and −1.29% (case-weighted); it is better than the reference in 0 cases and worse in 2. It switched away from sequential 3NN only once, to GP-EI when DUNE was held out, and GP-EI lost ~45% on two DUNE cases. The LLM's smaller gap to this policy mostly reflects the policy's own loss. The paper now shows this as the first row of Table 7. The "sits between the two" claim is removed, and the policy is described as "chosen using only the other, training groups".

2. **Router claim scoped, then reweighted.** Held-out decisions are fixed per case, so they were reweighted without retraining.

   | Weighting | Best controller over never calling (all six arms) |
   |---|---:|
   | Ecosystem | +0.022 pp |
   | Engine | +0.019 pp |
   | Case | +0.011 pp |

   - The V154 BORA-inspired and rank-reliability rules are negative under all three weightings.
   - Under case weighting, always calling the gpt-oss loop (+0.40%) beats every controller by ≥0.39 pp.
   - On native systems, one transferred rule gained +0.15% from a single call.
   - The claim now reads: "on the recorded cohort, no controller beat the better of always and never calling by as much as 0.03 percentage points under ecosystem, engine or case weighting". The native exception is stated.

3. **"Matched" made precise.** New Table `tab:match` classifies the 72 arm–case pairs where an LLM beat the reference by more than 1%:
   - 61: a prespecified alternative (random, adaptive neighbour, GP-EI) did at least as well;
   - 3: an alternative came within 1%;
   - 8: the LLM was ahead by more than 1%, i.e. the baseline-set wins.

   The counts of the last group equal the V174 win counts. This is asserted in the analysis script.

4. **Wording.**
   - The cohort is now "14 workloads × 5 prefix seeds = 70 task–seed cases".
   - Native: "did not demonstrate robust improvements over the reference".
   - Conclusion: "one task–prefix pair achieved a baseline-set win in all three evaluated gpt-oss-120b arms".
   - The cost-section claim is scoped to "the primary ecosystem-balanced average".
   - The operations table has defined columns: planned calls, retries, 429 rejections, invalid, fallbacks.

## Partly contested

- **Cost.** The $1.38 already includes the stopped first attempt ($0.0015) and the provider probes ($0.0017). The three analysed arms cost $1.374. Only the one in-flight request of the stopped attempt has unknown cost. The paper now states this breakdown.

## Checks

- `.venv/bin/python scripts/revision_v175.py --check` reproduces the analysis byte-for-byte.
- The analysis script asserts that the reweighted ecosystem values equal V174's router table and V154's summaries.
- `tests/synthetic/test_revision_v175.py` asserts that the manuscript's new numbers equal the analysis output.
