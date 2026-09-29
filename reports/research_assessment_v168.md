# Research assessment after V168

We have a stronger, reproducible negative result for the tested local-model escalation mechanism. We do not have evidence that the benefit-aware controller finds useful calls on unseen systems. A journal's quartile is not an experimental quality threshold, and these results do not establish acceptance or readiness by themselves.

## What the new evidence adds

Polars and XGBoost are additional native software implementations with real public inputs and materially different configuration effects. Their admission preceded model outcomes and retained failures. The 800-outcome paired experiment used five seeds per application, five classical continuations, both existing real local models, shared B10 prefixes and three charged fresh validations per B20 arm. All 20 model calls completed with valid responses. The run finished in 544.017 seconds; no cloud or paid inference.

Neither model produced a robust >10% gain against sequential 3NN in any of the ten cases, and neither achieved a joint robust win against sequential, adaptive and GP-EI. Polars mean gains against sequential were +0.071% for SmolLM3 and -0.816% for Qwen3. XGBoost mean gains were -25.538% and -19.402% respectively: selected configurations took longer. Both XGBoost model means were slightly better than GP-EI (+0.263%/+4.973%), showing that the choice of classical comparator matters. It would be misleading to report only that comparison.

All 70 selected configurations passed fresh-validation quality. Only one validation cell exceeded the fixed 5% relative-MAD threshold; none fell below 10 ms. Thus the negative XGBoost comparison is not simply the artifact of charging quality penalties to final model selections. Forty-six acquired search/prefix outcomes failed the accuracy constraint and remain charged, but no final selection did.

Both historical benefit and uncertainty policies chose zero calls. The matched-rate random policy therefore also made zero calls. This matches never-escalate and provides no evidence of useful learned discrimination. Always-escalate lowered equal-family mean gain by 12.734%/10.109% while incurring inference cost. The hindsight upper references achieved only +1.343%/+1.897% under the unfiltered mean and remain non-deployable.

The post-outcome mechanism audit found that model arms retained a prefix setting in 18/20 cases; duplicate proposals occurred in 34/140 evaluated proposal positions and projection in 48/140. These observations describe the tested batch-proposal mechanism. They do not show that a different interface would fix it. V164 already showed a catalog intervention eliminating evaluated duplicates without robust gains on other applications. Do not retune these newly exposed tasks until a favorable result appears.

## Cost interpretation

SmolLM3 used 16.373 seconds for ten requests and Qwen3 used 43.791 seconds, with 4,833/411 and 5,714/581 observable input/output tokens. No missing token-usage requests. Their model stages took 18.315/48.863 seconds with peak server RSS about 3.03/6.78 GB. The inference cost is additional to native search/validation.

A clearly post-hoc break-even diagnostic found only two different-setting positive median comparisons eligible for an estimate, neither passing the robust practical-gain rule. Estimated warm amortization required 1,674 repeated Polars bundles or 1,594 XGBoost bundles; cold scenarios required 3,351/2,927. These are projections of noisy medians and measured branch/request costs, not observed deployment savings. The diagnostic's initial pre-response freeze guard failed and it was explicitly relabeled exploratory; the primary protocol and decisions were untouched.

## Why this is not a general positive-controller result

Only two new implementation groups are in this comparison. Polars reuses the flight workload/data contract previously exercised with DuckDB. Feasibility exposed both task designs; the historical router was transported across different target budgets and quality penalties. Public-data familiarity, one host, small finite grids, quantized models, constrained proposals and filesystem-cache effects remain limitations. Five seeds are repeated runs, not five systems. Fresh validation and deterministic replay improve measurement integrity but do not replace independent systems or hosts.

Historical cohorts used different margins, inputs, budgets and loss functions. They must not be pooled into a single significance test or advertised as one uniform held-out experiment. All earlier negative findings, the excluded V149 case collision and source/admission failures remain preserved.

## Highest-value next evidence

Independently replicate the frozen application comparison on another physical host, keeping the protocol and all outcomes fixed in advance. This tests whether the negative result depends on this machine and its timing regime. Access to another host has not been established; no credentials, cloud resources or remote connection are assumed. More same-host seeds or prompt revisions would be weaker evidence than this replication.

Before claiming a successful learned controller, a separate prospectively selected cohort with enough independent software groups and genuine positive/negative escalation cases is required. Full original-method comparisons also remain incomplete: source-mapped checkpoint adaptations are not complete SNAP2/EZR/BORA/LB-MCTS reproductions. A narrow empirical paper about when these small local models fail is a more defensible direction than claiming a generally successful escalation algorithm. The present result is ready for critical research discussion; journal suitability still requires that independent review and remaining validation.
