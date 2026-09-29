# V25: a matched-shortlist classical experiment

**The new cheap adaptive-shortlist optimizer improves the original classical baseline's average loss, but does not beat the LLM average.** The existing static-shortlist rule comes much closer to the LLM average. This exposes the importance of the search space and cheap controls without claiming that a learned router works.

We actually ran **15 new classical continuations and charged150 recorded-label accesses**, using all existing MySQL/lrzip/Brotli development prefixes and five fixed seeds per family. There were no new LLM calls, failed arms or omitted cases. Every arm retained the exact ten-observation prefix, acquired ten further labels sequentially, and finished at20 evaluations.

## What changed

The original classical continuation could search the full remaining table. The LLM instead received a20-row shortlist computed from configuration features and the ten acquired labels. V25 restricts the unchanged adaptive centroid procedure to those same20 candidates, preserving the original seeded tie order. Labels remain behind the charged oracle; IDs and display order do not affect classical recommendations. The shortlist is fixed throughout the branch, while its acquired best/rest state updates after each evaluation.

The prior static shortlist control selects its ten highest-ranked rows without sequential feedback. It is distinct from the first-displayed-ten control: display was shuffled after ranking. Its previously measured outcomes are reused with historical costs retained. LLM comparisons reuse V22's real1.5B outputs; the three distinct presentations are averaged per prefix, and exact repeats are excluded from efficacy means.

## Actual results

Lower normalized loss is better. Each family row averages its five seeds; LLM also averages its three presentations. The final row weights families equally.

| Family | Original full-space classical | Static shortlist rank | New adaptive shortlist | LLM mean |
|---|---:|---:|---:|---:|
| Brotli | 0.00068959 | **0.00041457** | 0.00063662 | 0.00046855 |
| lrzip | 0.00139187 | 0.00139187 | **0.00078113** | 0.00124491 |
| MySQL | 0.04465970 | **0.03220595** | 0.03800966 | 0.03224341 |
| Equal-family mean | 0.01558039 | 0.01133746 | 0.01314247 | **0.01131896** |

The new adaptive-shortlist arm gains **+0.00243792** over the original classical comparator, but loses0.00182351 to the LLM average and0.00180501 to static shortlist rank. These are normalized-loss differences, not runtime-saving percentages.

Across15 paired prefixes, the new arm versus original classical has3 wins,11 ties and1 loss. One gain and one harm exceed the existing0.02 diagnostic margin. Against static rank it has2 wins,11 ties and2 losses; again one material gain and one material harm. Against the LLM's per-prefix presentation mean it has8 wins,4 ties and3 losses, but one large loss outweighs its smaller wins in the aggregate. It strictly beats all three LLM presentations in0/15 cases and is no worse than all three in12/15.

For example, MySQL/23 improves from0.07373924 with original classical to0.01927233 with the new arm. MySQL/11 goes the other way:0.04195699 becomes0.06317371, while static rank reaches0. This is not a uniform improvement and these cases are not an exclusion rule. All case outcomes remain in [cases.csv](../results/v25_shortlist/cases.csv).

The LLM's mean advantage over static shortlist rank is only **+0.00001851**. Across prefixes, the LLM mean wins3, ties4 and loses8 against static rank; one LLM gain exceeds0.02 and no loss does. Numerical closeness of the aggregate does **not** establish equivalence, non-inferiority or a practical cost threshold. Choosing the best cheap method separately for each family after seeing these outcomes would also be hindsight, not a validated policy.

![Measured comparison](../results/v25_shortlist/comparison_readable.png)

Each panel has its own vertical scale. The initial plot's long labels overlapped; the readable version was produced by a separately labeled presentation-only script. Both files are retained; frozen collection/evaluation code and numerical outcomes were unchanged.

## Validation and collection cost

The [protocol](protocol_v25_shortlist.md), code, tests, data/prefix/pool hashes and reused outcomes were frozen before new acquisitions, after exposure to earlier development results. **177 tests passed in1.19seconds.** Synthetic checks cover branch isolation, presentation-order independence, forbidden shortlist entries, exact acquisition counts and invariance to targets outside the shortlist.

The separate evaluator independently reconstructed all150 recommendations using a Python modal-centroid/distance implementation, checked every journal entry against original source row/target values, replayed all15 final states and20/10 budgets, and recomputed45 LLM metrics. Read-only replay passed. The final figure was visually inspected. [Raw logs and receipts](../artifacts/study_v25/); [acquisition journal](../results/v25_shortlist/acquisitions.jsonl); [all intended statuses](../results/v25_shortlist/progress.json).

Actual new collection:150 recorded-objective accesses, including accesses to targets seen in older branches; no claim these are free because the source tables already exist. No new physical measurement occurred. Collection charged0.957621seconds, analysis/replay/initial figure0.612506seconds, readable presentation0.454216seconds: **2.024344 experimental seconds** total. Measured branch loops sum0.238948seconds, excluding setup/verification and not a deployed-service latency measurement.

Recorded-objective history is now **7058 accesses**, with1134 separate physical trials unchanged. Calls remain **200/200 follow-up** (300 including initial stage); cumulative experimental runtime2252.612712/3600seconds,1347.387288seconds remaining; active_since isnull. Downloads and external spending added:zero. Hypothetical deployment of this classical arm across15 cases uses300 logical evaluations andzero model requests, distinct from collecting all research branches.

## What this establishes—and what it does not

The fixed shortlist is a useful classical intervention on this exposed sample, and a simple static ranking produces an aggregate very close to the tested LLM. More sequential updating is not consistently better. A comparison only against the original full-space baseline can therefore leave the source of apparent LLM benefit unclear.

This is an exploratory development-only ablation with three independent families, not a fresh held-out confirmation. Sequential classical feedback differs from the LLM's one-batch continuation. No claim isolates model intelligence, establishes a universal shortlist benefit, proves novel routing, or justifies inference cost in a real application. The single0.02 margin is historical and not an application-validated utility. Future models, other tasks, arbitrary presentations and live deployment remain untested.

**Single next action:** review the complete matched-control evidence with Tim and agree on an application-grounded benefit/cost threshold and untouched task families before another model/router campaign. The next collection should prospectively compare static and adaptive shortlist controls, not choose the favorable cheap method after inspecting outcomes.

Executed commands:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python -u scripts/run_shortlist_v25.py
.venv/bin/python scripts/analyze_shortlist_v25.py
.venv/bin/python scripts/analyze_shortlist_v25.py --verify-only
.venv/bin/python scripts/render_shortlist_v25.py
```

Collection and analysis refuse started/completed outputs; read-only replay does not acquire new labels or change ledgers. Do not delete guards or reset accounting.
