# V8: selection from recorded candidate rows

Exploratory development-only follow-up to v7. This is one fixed formulation, not a search for a positive result. A good-enough pilot result means complete paired data, credible controls, traceable real inference and bounded conclusions, regardless of effect direction. After this comparison, synthesize findings for review; do not keep tuning until a positive result appears. No router training or held-out access in v8. All five seeds [11,23,37,53,71] remain grouped in the same three development systems (MySQL, lrzip, Brotli).

## Frozen intervention and controls

Reuse the exact v6 ten-acquisition prefixes. From the available feature table, rank every unacquired row by nominal distance to the acquired best modal centroid minus distance to the acquired rest modal centroid. Stable ties retain the saved prefix's shuffled candidate order. Retain the first 20 rows. Fix this shortlist for the entire continuation; no hidden targets enter it. Shuffle presentation with a separate RNG seed +70000 and assign the twenty IDs 0–9,A–J. All three new arms use exactly that mapping.

The real local model receives the feature definitions, acquired-only normalized losses for ten observed feature strings, and twenty candidate feature strings with IDs. Select ten distinct IDs in one batch. A constrained decoder permits remaining IDs at each choice, newline separators and final EOS. The model's greedy logits select each ID. Every selection maps directly to a recorded unobserved configuration; no nearest-row projection. Retain raw responses, generated token IDs, masks, prompts, rendering hashes, usage, time and pinned model provenance. Changed prompt, output representation, shortlist, and distinctness constraint jointly define this formulation: this is not a single-factor causal contrast to v7.

Two newly measured controls select ten distinct rows from the same shortlist: uniform sampling without replacement (seed +40000), and static classical rank (first ten ranked rows). Neither control is an LLM output. Also compare with immutable original v6 adaptive classical, original LLM and v7 prefix-excluding LLM continuations. The adaptive classical comparator is the primary escalation reference; the shortlist controls isolate the model's added selection value under the new formulation.

Use the already pinned Qwen/Qwen2.5-0.5B-Instruct revision 7ae557604adf67be50417f59c2c2f167def9a775, local CPU/float32, four threads, greedy decoding, zero retries, 60-second request timeout, 1024-token configured output maximum. Real-tokenizer preflight will determine exact grammar length (ten ID choices, nine newlines, EOS) and prompt lengths before collection. This is a tiny-model adaptation, not a SNAP2 replication. No download, API, credential use or external spending.

## Budgets, failures and analysis

Per branch: checkpoint10 + ten new target accesses =20 logical evaluations. New collection: 15 uniform controls +15 static controls +15 LLM continuations, 450 target accesses total, fifteen intended model attempts. Historical prefixes and comparison arms are reused; their collection costs remain charged historically. Preserve all45 intended branches, including blocked/failed cases. Malformed/error responses receive a marked adaptive classical fallback if runtime remains; failure is never reported as successful model selection. No automatic repeat of an interrupted transaction. The provider stops at a limit and terminates its worker.

Freeze scientific code, tests, data schema/hashes, prefix/old-arm hashes, shortlist and prompt digests before acquiring new control outcomes. No adaptation after outcomes. Score only in retrospective evaluator with full-table one-target normalized minimum loss and existing direction. Compare paired loss gains, fixed .02 material help/harm, all per-seed results, and system means. Three development groups support descriptive evidence only; no p-values, generalization claim or treating seeds as independent systems. If any intended model case is incomplete, show completion counts and control results; do not issue a selected-completers model comparison.

Predeclare a nondeployable diagnostic: best attainable loss in the frozen20-row shortlist combined with prefix. Hidden targets for this hindsight reference are read only by the retrospective evaluator; they do not train or change the model, shortlist, control, or protocol. This is not a budgeted policy or actual oracle acquisition. It measures available shortlist headroom. Model ID validity and zero duplicates are guaranteed by constraints, so they are validity checks, not evidence of usefulness.

Separate actual new collection cost (both controls and LLM, model loading, failed calls, runtime) from hypothetical deployment cost (only one chosen continuation per case:300 logical labels, up to15 calls). No precise monetary savings inferred from local tokens. Shorter output format changes token costs; do not attribute that difference solely to improved reliability.

## Resource boundary and stopping

At preparation the shared ledger has113/113 used attempts and1630.1201/1800 experiment seconds. Controls are authorized with zero model calls. Configs/authorization_v8.json defaults to granted:false and current cap113. Full inference preflight requires15 available attempts and cannot pass at the existing cap. The proposed explicit allowance is **113 →128** (fifteen additional attempts), with the same cumulative1800-second runtime and USD0 spending cap. User approval, if given, must be recorded exactly before any request, separately from this scientific freeze. Generic continuation is not interpreted as a silent cap increase. Do not reset historical ledger counts. If runtime is insufficient, checkpoint and report the full denominator.

After this formulation, produce a reviewable synthesis of v6 routing and v7/v8 mechanism evidence, including negative results. A stronger model, nonbinary empirical tasks and a broader untouched-system routing test remain separate future studies requiring a new design/resources.

Commands (project-local environment):

```sh
.venv/bin/python scripts/prepare_v8.py
PYTHONPATH=src .venv/bin/python -m escalation.study_v8 controls
PYTHONPATH=src .venv/bin/python -m escalation.study_v8 preflight
# only with explicit bounded approval:
PYTHONPATH=src .venv/bin/python -m escalation.study_v8 llm
PYTHONPATH=src .venv/bin/python -m escalation.analyze_v8
.venv/bin/python scripts/verify_v8.py
.venv/bin/python scripts/report_v8.py
```
