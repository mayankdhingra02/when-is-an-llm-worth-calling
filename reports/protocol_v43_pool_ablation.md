# V43: candidate-pool intervention, exploratory classical experiment

Freeze before any new outcome acquisition. V41/V42 outcomes motivated this
experiment: these same six families are exposed development cases, not a new
held-out test. No LLM inference, router training, paid service or download.

Question: does a predecision expansion of the candidate region increase useful
headroom, and can cheap selection already capture it? Use every V41 dataset,
seed and saved ten-label prefix, unchanged feature domain, target and direction.
Do not select cases or parameters after outcomes.

Compare the original twenty-candidate pool to two alternatives:
1. Uniform20: sample twenty unobserved rows using Python Random(seed+43000),
   in the saved prefix's candidate order.
2. Retained10-diverse10: retain the exact original batch-3NN selection of ten.
   Add ten rows by greedy maximum minimum nominal Hamming distance from the
   prefix plus all already selected pool rows; ties follow saved candidate order.
   Retaining the original ten guarantees the diagnostic ceiling cannot worsen
   relative to original batch 3NN. That identity is not an empirical discovery.

Save both pools and their selection partitions for all thirty prefixes before
collecting any new outcome. Freeze hashes of protocol, implementation, source
manifests/data, old prefixes/comparators, new pools and analysis code. Only acquired
prefix labels may affect rank; diversity uses features only.

Each new pool has two isolated continuations: batch3NN selects ten using only
the prefix; a complementary coverage arm selects the remaining ten. Both retain
the prefix and use exactly twenty logical evaluations. The complement is a
coverage intervention, not a competitive optimizer claim. No arm sees the other
arm's labels. Acquisitions are charged even if an outcome appeared in old work
or another arm. Maximum 30 prefixes x 2 pools x 2 arms x 10 = 1,200 new recorded
accesses. No new prefix access. Journal each requested target before using it.
Keep intended denominators and stop on failure; never replace cases.

Collection limit 90 seconds; total V43 experiment computation at most120seconds,
inside unchanged global3,600 seconds. Preparation/analysis/verification share
the remaining30seconds; checkpoint at a limit. The exhausted model cap remains
290; this stage has zero allowed calls. No existing cap is raised. Saved-table
target access is not a live physical trial. Preserve prior raw files and freezes.

Analysis: evaluate actual batch3NN and nondeployable best-in-pool ceiling against
both original batch3NN and full-domain sequential3NN. Report each case, each
family and equal-family means, all wins/ties/harms. Report hindsight positive
headroom separately from always-use ceiling. Also show fractions of cases with
ceiling gain above0,1%,5% (fixed grid, no selected threshold). Compute exact
uniform-ten-of-twenty expected gain for each new pool using all previously
charged pool outcomes. These conditional distributions are not new optimization
runs, deployable knowledge or population p-values. No new significance tests.

Interpretation: more oracle headroom is insufficient to justify an LLM/router;
cheap capture, unseen-group transfer, equal application utility and model costs
must still be established. No model response from the old pool is reused as a
counterfactual response to a changed prompt. This is not a SNAP2 or LLAMBO
replication. No universal or journal-readiness claim follows from this ablation.
