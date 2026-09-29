# V40: exact routing opportunity audit and exploratory paper candidate

**All 30,720 allocations across 30 scenarios were computed and independently verified.** Against runtime3NN, no deterministic or randomized router selecting these recorded branches can obtain positive feasible-runtime gain. Even a hindsight selector allowed to pick the best of the three tested presentations only ties that control in every case. This is a finite observed-data conclusion, not a claim about new systems, model samples or larger models.

The new analysis adds no model calls, physical trials or objective acquisitions. It uses the real V38 branch outcomes whose source/token/budget provenance was independently checked and packaged in V39.1. The analysis plan was frozen before computing these summaries, after V38 outcomes were exposed: it is explicitly exploratory.

## Exhaustive result

Maximum mean feasible-runtime improvement in percent, optimizing call count with hindsight:

| Comparator | Assigned | Reversed | Reassigned | Presentation mean | Worst tested | Best tested (oracle) |
|---|---:|---:|---:|---:|---:|---:|
| runtime_only_llm | 2.0444 | 0.0000 | 0.3621 | 0.8022 | 0.0000 | 2.4065 |
| exact_joint_shortlist | 1.9745 | 1.9745 | 0.3238 | 1.4243 | 0.3238 | 1.9745 |
| exact_joint_full | 1.6507 | 1.6507 | 0.0000 | 1.1005 | 0.0000 | 1.6507 |
| runtime_3nn | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| static_rank | 3.6254 | 2.7924 | 1.9747 | 2.7975 | 1.1417 | 3.6254 |

All eleven exact call budgets for every scenario—including unfavorable outcomes—are in [curves.csv](../results/v40_frontier/curves.csv). The [summary](../results/v40_frontier/summary.json) also retains subset counts, exact rational gains, uniform-random expectations and probabilities of positive aggregate gain. These finite allocation probabilities are not p-values or sampling intervals.

The assigned-ID maximum against joint shortlist is1.9745% using two hindsight-selected calls. The worst-tested-presentation maximum is0.3238% using one call. Against full-domain joint3NN the corresponding maxima are1.6507% and0%. Static rank leaves larger opportunity; runtime3NN leaves none. No presentation is selected as a deployed policy.

![Exact quality bounds](../results/v40_frontier/frontiers.png)

Primary-result influence: omitting Brotli seed23 changes the original assigned-ID/joint-shortlist mean from1.7534% to0.0475%, retaining equal family weights. The case is not removed from reported results. All ten leave-one-case-out values are saved; this is a sensitivity diagnostic, not a confidence interval or new train/test split.

## What follows, and what does not

For recorded gain g_i and escalation probability q_i≥0, G=sum(q_i*g_i)/n. If all g_i≤0, G≤0. Our independently verified data meet that condition versus runtime3NN for all tested presentations. Adding a positive per-call penalty cannot improve this finite quality result. This elementary inequality is not a new theorem or a cost guarantee for production.

The positive V38 comparison remains real and reported. It does not establish useful routing, because the baseline matters and a cheap alternative matches or wins on every case. A small-model/batch/shortlist strategy can fail without implying that all LLM optimizers fail. A fresh larger or differently structured model experiment cannot be inferred from these outcomes.

## Validation and accounting

264 tests passed in1.34seconds, including exact arithmetic, empty/oversized input, tiny positive gains, known mixed gains, ties and permutation-invariant bounds. Sorted-gain formulas were checked against independent bitmask enumeration during analysis. A separate standard-library checker uses integer scaling and combinations; both installed Python3.10.13 and3.12.14 return identical330-row/30,720-allocation verification receipts. Read-only analysis replay passed and the figure was visually inspected.

Charged analysis/render time:0.731785seconds. Cumulative experiment time:2531.528508/3600seconds;remaining:1068.471492. Calls remain230/230,330includinginitial;recorded-vector accesses9608,physical trials1274,external spendUSD0. Read-only verification/tests/drafting are maintenance outside experiment-time accounting. Download ledger unchanged; web primary pages were inspected without downloading new model/data files.

## Paper deliverables and sufficiency

A complete [short-paper manuscript](../paper/manuscript.md), [bibliography](../paper/references.bib), [claim-evidence map](../paper/claim_evidence.md), [readiness decision](../paper/readiness.md) and [primary-source update](literature_update_v40.md) now accompany the measured results. Central numerical claims are mechanically checked by `scripts/verify_paper_v40.py`.

The literature update identifies a close HPO strong-control study and established option-order sensitivity. Those observations must not be claimed as new. The potential contribution is the constrained-checkpoint case study and its presentation-wise routing opportunity audit. It is enough for a narrow exploratory paper draft and research discussion; originality and submission suitability remain unresolved. It is not enough for the original broad successful-router claim.

**Single next action:** technical review of that narrow contribution against the close prior work before additional collection. No contact, submission, publication or remote push occurred. If a broader study is justified, it needs untouched admitted software groups, application-defined utility/correctness and a prospectively bounded model study. More analysis of these two exposed families cannot supply those missing data. The exhausted model allowance was not increased.
