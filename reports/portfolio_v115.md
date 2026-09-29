# V115: a single deployable classical portfolio

Completed12budget-20classical continuations using the same fixed prefixes as V114, acquiring120new recorded outcomes. The remaining ten turns alternate batch3NN and full-domain sequential3NN; no other branch's outcomes are consulted. This is one executable control, not a free hindsight choice between separately run controls.

Against this control, the36saved real LLM replicas have group-first mean gain **-2.25%**; **0/36** valid replicas improve by>=5%, and **3/36** are worse by>=5%. There are9wins,15ties and12losses; the largest gain is3.34%. 7 replicas improve by at least2%, so the result is not an absence of all benefit. No new model calls occurred. All twelve prefixes and thirty-six replicas are retained.

|Group|Mean LLM gain vs portfolio|Portfolio gain vs batch3NN|Portfolio gain vs sequential3NN|
|---|---:|---:|---:|
|berkeleydb|-0.12%|+0.00%|+2.67%|
|dune_hsmgp|+1.15%|-1.40%|-22.81%|
|hipacc|+2.05%|-1.28%|-4.75%|
|llvm|-0.29%|+0.29%|+0.00%|
|openvpn|-16.30%|-0.32%|-0.44%|
|sac|+0.00%|+0.00%|+0.00%|

Collection/scoring preparation took3.458s; the mean ten-turn portfolio loop took0.025289s, including indexed-table accesses. These are local computation times, not new executions of the original software systems. Actual additional research cost is120charged recorded accesses. A deployed portfolio uses20total objective evaluations and zero model requests; historical prefix collection remains costed. No native/cloud-dollar savings are inferred.

This follow-up was specified after seeingV114model results and is explicitly exploratory. Its rule was frozen before any of its own continuation outcomes. It does not retroactively turn the original joint-control screen into a single-control comparison or replace the stronger original controls. The portfolio can sacrifice the quality of either constituent; that is reported in the last two columns. No favorable blending ratio or starting method was selected after this run.

Independent replay reconstructed every portfolio choice from its own acquired labels, checked exact paired prefixes and budgets, and recomputed all36relative gains from saved actual model outcomes. Six exposed groups remain six groups. Positive or negative contrasts here cannot establish a learned router, population generalization, or journal acceptance.
