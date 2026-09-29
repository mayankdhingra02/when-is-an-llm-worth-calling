# Local review guide: what the latest research actually supports

V45 packages completed V41–V44 evidence; it is not another experiment, fresh
held-out evaluation or claim of journal readiness. The original V41 archive
remains byte-for-byte unchanged. This is a local review artifact; nothing has
been sent or published. Dataset-specific redistribution permission remains
unresolved, including DeepPerf. Review licensing before external redistribution.

## Read these first

1. `reports/models_v44.md`: all60approved changed-pool model cases and the
   negative mechanism finding. Both LLM treatments lose on average to the
   strong full-domain sequential3NN control. Uniform-pool selection never
   beats its own cheap batch selector on any of30cases.
2. `reports/pool_ablation_v43.md`: the classical/coverage experiment that
   motivated V44. Wider pools expose hindsight opportunity but do not show
   that any deployable selector/router can exploit it.
3. `reports/selection_reference_v42.md` and `reports/models_v41.md`: the
   original shortlist ceiling and six-family model/control comparison.
4. `reports/analysis_correction_v44.md`: the detected mutable-prefix analysis
   bug, preserved failed attempt and isolated-state correction. Raw model
   outputs and on-disk prefixes were unaffected. No failed summary was used.
5. `reports/literature_update_v43.md`: primary-source limits on novelty and
   why this candidate-ID adaptation is not a numerical SNAP2 replication.

The paired CSVs and summary JSON files retain every comparator, case, family,
failure denominator, hypothetical ceiling and cost field. PNG/SVG figures are
in the corresponding result folders. Raw requests and acquisition journals
are retained; no synthetic model responses were used to obtain research scores.

## Replay with no ML dependencies

After extracting the local ZIP:

```sh
python3 -I -S scripts/verify_review_bundle_v45.py
```

The verifier uses only the standard library. It checks the hash of every bundled
file, runs the independent V41 arithmetic verifier, checks4,800recorded
acquisition events for source identity and consistency, replays120V43 and240V44
case/comparator calculations,60V44exact uniform-subset references and eight V44
aggregate contrasts. The V41 verifier additionally checks420comparisons,
fourteen summaries and108policy means. V42's analytic/exhaustive validation
receipts are retained; this command does not rerun its full enumeration.

This proves consistency of the supplied acquired records and calculations.
It cannot independently authenticate omitted original datasets, prove a hash
manifest came from an independent party, rerun model logits, establish absence
of pretraining contamination or replicate on another physical machine. Local
source-row checks and tokenizer/grammar replay receipts document what was
verified in the full repository. Neither hash checking nor software tests
establishes that the scientific hypothesis is true.

The package excludes full source tables, model weights, third-party papers,
credentials and the execution environment. Pinned data/model identities and
source/license manifests remain. Fresh inference requires the full project,
original inputs, pinned environment, suitable hardware and a new explicit
bounded run. Included collectors are one-shot and must not overwrite evidence.

## What the reader should decide

The supported conclusion is narrow: under these saved prefixes, nominal
feature encodings, small Qwen models, candidate pools and recorded-table
budgets, stronger cheap controls remove apparent advantages and widened
opportunity is not reliably captured by the model. Do not generalize this to
all LLM optimizers or claim a successful learned escalation policy.

The key research decision is whether this controlled negative finding is
sufficiently distinct from the close prior work to justify a paper, or whether
another study needs a different semantic intervention, independent model
family, equal application utility and independent development/test groups.
That judgment is not settled by journal quartile or by a positive average
against a weaker comparator. The frozen stopping rule ends further tuning
of this specific small-model/candidate-ID adaptation on these exposed systems.
