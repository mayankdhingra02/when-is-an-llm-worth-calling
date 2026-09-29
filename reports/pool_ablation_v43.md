# V43: changing the candidate pool exposes opportunity but does not solve selection

**A random candidate pool creates substantially more hindsight headroom than
the original shortlist, but its cheap selector performs worse on average.**
This is a concrete mechanism result from new recorded-table acquisitions. It
does not yet show that an LLM can exploit the opportunity, or that a router can
predict when to call one.

## What actually ran

All six V41 software families, all five fixed seeds and their saved ten-label
prefixes were retained. Two alternative twenty-candidate pools were fixed before
new acquisition: uniformly sampled unobserved configurations; and the original
batch3NN's ten choices plus ten greedily diverse configurations. Each pool had
two isolated ten-evaluation continuations: batch3NN and its complementary
coverage arm. Both inherit the same prefix, so each uses twenty logical
evaluations. The coverage arm is an audit intervention, not a claimed strong
optimizer.

Executed **120 continuations and 1,200 charged recorded outcome accesses**.
All completed; none were dropped or replaced. These include repeated accesses
to previously observed source rows, charged conservatively. There were zero
new model calls, live physical trials, downloads or external dollars spent.
V43 collection/preparation/analysis/verification/rendering took **7.256034s**,
inside its120-second bound and the unchanged global3,600-second bound. Tests
are logged separately from experiment runtime.

This is **exploratory work on already exposed systems**. The frozen protocol
precedes these new acquisitions, but does not make these independent test groups.
V41 real LLM results remain unchanged; no old response was reused for a changed
candidate prompt.

## Main comparison

Mean relative gain against full-domain sequential3NN, equal family weights:

| Candidate pool | Actual batch3NN | Perfect within-pool selection, always used | Perfect selection plus perfect routing |
|---|---:|---:|---:|
| Original shortlist | -1.9416% | -1.8207% | +0.2915% |
| Uniform20 | -2.7912% | -0.6179% | +2.7127% |
| Retained10 + diverse10 | -1.9524% | -1.7064% | +0.3038% |

The last two columns are **outcome-informed, nondeployable diagnostics**. They
use all charged pool outcomes: the final column selects the pool only when its
best possible result beats classical continuation. They are neither model scores
nor results from a deployable router. Both new pools still have negative mean
gain even with perfect selection if used on every case.

Uniform20 has five cases with positive ceiling gain, thirteen ties and twelve
harms versus full-domain3NN. Four cases exceed1% potential gain and three exceed5%.
Two Dune seeds offer32.75% and30.79% potential gains, while batch3NN loses0.148%
and0.337%, respectively. BerkeleyDB contributes two other positive opportunities
that batch3NN already captures. Almost all aggregate hindsight opportunity is
therefore concentrated in Dune and BerkeleyDB, not demonstrated broadly across
six systems. A method that simply routes by family after seeing these results
would leak outcomes and is not implemented.

The diversity pool's ceiling cannot be worse than original batch3NN by construction:
it retains that control's complete selected set. This guarantee is not a new
empirical discovery. Its ceiling mean gain versus original batch3NN is only
+0.2248%; actual batch selection changes that to-0.0104%. Feature-space novelty
alone does not reliably supply useful target improvements in these cases.

All120case/comparator rows, all12summary contrasts, six-family means and fixed
0/1/5% margin counts are in `results/v43_pool_ablation/summary.json` and the CSV.
No comparator or pool was omitted for unfavorable outcomes. Exact uniform
selection expectations are also retained. They average the gain of each random
outcome against the fixed comparator; they are not new executed search runs.

## Verification and reproduction

Independent standard-library verification matched all1,200 events to1,047
distinct source rows, checked120 paired budgets and120comparison rows, and
directly enumerated11,085,360 hypothetical subsets to check all60finite random
distributions. Enumeration is computation over acquired outcomes, not millions
of new measurements. Source objectives were parsed only for acquired rows.
The synthetic and transfer suites passed320tests before V44 preparation; the
final combined suite passed321tests including the V44 authorization test. Figure visually checked.

```sh
.venv/bin/python scripts/run_pool_ablation_v43.py prepare
.venv/bin/python scripts/run_pool_ablation_v43.py collect
.venv/bin/python scripts/run_pool_ablation_v43.py analyze
.venv/bin/python -I -S scripts/verify_pool_ablation_v43.py
.venv/bin/python scripts/render_pool_ablation_v43.py
.venv/bin/python -m pytest -q tests/synthetic tests/test_transfer_v41.py
```

Preparation/collection/analysis are one-shot and reject overwrite. Their
measured outputs already exist; use the verifier and renderer to inspect them,
or a clean isolated copy for new collection. Evidence lives in
`artifacts/study_v43/`; original V41/V42 freezes and the V41 review ZIP remain
unchanged. The ZIP does not yet contain V42/V43.

## Interpretation and next experiment

The result supports testing candidate construction as a cause of limited
escalation opportunity, while showing that wider pools trade away reliable
selection. It does not prove that an LLM can recover the lost quality.
[LLAMBO's original paper](https://arxiv.org/html/2402.03921v2) already studies
generation separately from surrogate selection, and
[SNAP2](https://arxiv.org/html/2607.02583v1) projects proposed configurations
to measured rows rather than imposing our fixed twenty-row shortlist. Our
ceiling therefore does not bound either method generally. See the bounded
primary-source audit in `reports/literature_update_v43.md`.

**Next action:** the prepared V44 assay runs the real1.5B model on both alternative
pools, all30prefixes each, to test whether it captures the newly available gains
beyond the cheap selectors. All60prompts are frozen and locally tokenized;
maximum input3,301tokens. Inference is unexecuted and authorization is disabled.
It requires a new60-call extension,290→350, with450seconds collection inside the
unchanged global3,600seconds, at most600recorded accesses, zero retries/downloads/
spending. This is still exploratory; a positive outcome would motivate an
independent development/test design, not establish useful routing or Q2 readiness.

Equal application utility/correctness, measurement noise, new independent
software groups, an independent model family and a defensible novel contribution
remain unresolved. No publication or external communication was performed.
