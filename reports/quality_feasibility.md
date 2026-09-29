# Runtime gains under an output-size cap: positive feasibility, not an LLM success

**Recorded configurations offer more than10% runtime headroom under a fixed prefix-derived output-size cap in two of ten cases, one in each compression family.** This is a positive feasibility observation for a revised, constrained optimization task. It is not a newly measured algorithm improvement or evidence that an LLM can find those configurations reliably. The previous negative learned-ranking/routing findings remain unchanged.

## What changed in this analysis

All five development seeds for Brotli and lrzip were included. These are the two development tasks whose pinned source documentation explicitly identifies output size. MySQL has no applicable output-size target and was not analyzed under this constraint. No held-out systems or alternative revisions were used.

For each saved prefix, the fastest observed row sets the size cap. A scored configuration must produce an output no larger than that anchor. We then retrospectively score the already collected static-classical, adaptive-classical and LLM branches, and compute nondeployable best-case bounds for the original shortlist and full table. The old optimizers had only acquired runtime; size was read here solely in the offline evaluator. A future constrained optimizer must explicitly acquire and charge joint outcomes before using size.

This is a separately frozen **post-hoc** feasibility analysis. It does not rewrite the earlier .02 success margin, establish a new validated practical threshold, or change any old model responses, labels or policies. Looking for positive results was not used to select cases. Sensitivity at0%,5%,10%,20% is fully retained.

## All ten same-shortlist cases

Primary comparator: the fastest size-feasible row among the20 outcomes already collected by the fixed static-ranking branch. Upper reference: the fastest size-feasible row among the shared prefix and original20-candidate shortlist. Its use of hidden outcomes makes it hindsight, not a deployable method. lrzip runtime units are not specified in the source case README; Brotli runtime is seconds.

| System | Seed | Static branch runtime | Best feasible shortlist runtime | Available relative reduction |
|---|---:|---:|---:|---:|
| lrzip | 11 | 15806.8000 | 15767.2000 | 0.251% |
| lrzip | 23 | 15593.2000 | 15593.2000 | 0.000% |
| lrzip | 37 | 19096.8000 | 15373.6000 | 19.496% |
| lrzip | 53 | 16164.0000 | 16164.0000 | 0.000% |
| lrzip | 71 | 15662.4000 | 15662.4000 | 0.000% |
| brotli | 11 | 1.9000 | 1.9000 | 0.000% |
| brotli | 23 | 2.5080 | 2.0940 | 16.507% |
| brotli | 37 | 1.5700 | 1.5700 | 0.000% |
| brotli | 53 | 1.5280 | 1.5280 | 0.000% |
| brotli | 71 | 1.6300 | 1.6300 | 0.000% |

The same-shortlist mean upper-bound reduction is3.30% for Brotli and3.95% for lrzip (3.63% equally across families). Three cases have any strict point-estimate reduction; two exceed5% and10%; none exceeds20%. Full-table bounds average9.81% for Brotli and5.54% for lrzip, with three of ten cases above10%. These are upper bounds, not achieved average improvements, confidence intervals or guarantees.

## The two larger opportunities

- **Brotli seed23:**2.508→2.094 seconds, **16.5% faster**. Output size also decreases from76,506,051 to75,903,874 bytes. This particular recorded candidate improves both reported quantities compared with the feasible static-branch incumbent. It was not selected by the previously run LLM branch.
- **lrzip seed37:**19096.8→15373.6 recorded runtime units, **19.5% faster**, while meeting the prefix-derived size cap652,020,148. Its output is49 source-size units larger than the static incumbent's652,020,099, so this is **not** strict dominance over that incumbent in both objectives. It meets the predeclared anchor cap. The old LLM's first-half rule happened to include this row; rescoring that occurrence does not establish learned selection.

The other eight cases and small/zero effects remain in the table. No case or seed is counted as an independent software family. Only two families are represented.

## What this supports—and what it does not

The current raw-relative, size-constrained formulation exposes potential value hidden by unconstrained runtime scoring and a global-range threshold. That supports designing a fresh quality-aware experiment. It does **not** show that swapping to a stronger model will work. The historical classical baselines were not designed to optimize runtime subject to this cap, and the LLM was never prompted with it. A fresh cheap constrained baseline is needed before a fair stronger-model comparison. Output size is only a storage constraint, not a rerun of decompression correctness or application quality validation.

The source authors report repeated measurements, but these tables do not provide the paired-run uncertainty needed here for significance or reliability claims. Point-estimate dominance can be affected by measurement noise, workload semantics and configuration effects. Public-data contamination and the two-family limitation also remain. Do not claim generalizable benefit routing or a positive replication of SNAP2.

## Actual execution and costs

**92 tests passed.** Independent verification reread source rows and checked all ten anchors/caps, actual branch membership,60 bound comparisons, relative gains and summary counts. The new analysis used **zero model calls and zero optimizer acquisitions**; all measurements were from existing public tables. Model requests remain128/128 used. External spend and downloads remain unchanged; no worker/background job is running.

The source CSVs and READMEs are bound by the frozen manifest to the original PerformanceEvolution_Website owner repository at commit4ee53dad6b81543c444d44282053def0d82d97b3. Brotli documentation states seconds and compressed bytes; lrzip lists runtime/output size without units. No unit conversion was guessed.

Evidence:

- Specification/hash freeze: `reports/protocol_v11_quality.md` and `.freeze.json`.
- All cases, sizes, chosen row IDs and sensitivity summaries: `results/v11_quality/summary.json` and `cases.csv`.
- Executed analysis: `scripts/analyze_quality_v11.py`, `artifacts/study_v11/analysis.log`.
- Independent source replay: `scripts/verify_quality_v11.py`, `artifacts/study_v11/verification.json` and `.log`.
- Tests: `tests/synthetic/test_quality_v11.py`; full suite log `artifacts/study_v11/tests.log`.

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/verify_quality_v11.py
```

## Follow-up completed and remaining blocker

The actual joint-outcome cheap controls have now run; see [V12 controls](constrained_controls_v12.md). They remove most lrzip headroom and retain mixed per-family results. The prospective next-step discussion below describes what this feasibility audit motivated, not an unexecuted claim that those controls are still pending.

The next technically justified step is a new joint-runtime/size protocol with fresh, charged cheap constrained continuations, followed—only if useful headroom survives those controls—by one predeclared stronger-model comparison with candidate-order checks. Specify size feasibility, meaningful relative improvement and measurement uncertainty before future evaluation; preserve the old results. Existing development families remain exploratory; a router would still need broader untouched groups.

Further real inference cannot run under the exhausted128-request allowance. Generic instructions to continue until positive do not define a new cap, and no paid/cloud inference is authorized. This report records positive **opportunity in the data**, not a positive LLM effect. A positive LLM or router result cannot be promised.
