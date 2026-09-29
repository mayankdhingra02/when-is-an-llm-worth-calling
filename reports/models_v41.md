# V41 real-model transfer: completed negative/mixed result

**Both real local models completed all30paired cases on six newly admitted software families. The1.5B model nearly ties the feedback-matched batch3NN control, but neither model improves the mean over full-domain sequential3NN. The transferred benefit router provides no useful gain.** These findings do not establish Q2 readiness, a successful generalizable router, or acceptance prospects.

## Frozen design and actual scope

Six independent family groups (BerkeleyDB C,Dune,LLVM,HIPAcc,SaC,OpenVPN), five fixed seeds each, one saved10-evaluation centroid prefix per case, ten continuation acquisitions per arm. Both local Qwen2.5-Instruct sizes0.5B/1.5B used identical precommitted candidate-ID prompts and twenty-candidate shortlists, greedy CPUfloat32 inference and20output tokens. There were seven classical controls, not a single selected weak baseline. Batch3NN is the primary comparison because it shares the shortlist and absence of new within-batch feedback; full-domain sequential3NN is a required end-to-end strong control.

Source/admission and complete hypothesis/analysis definitions are in `reports/source_audit_v41.md`, `reports/protocol_v41_transfer.md`, and `reports/analysis_addendum_v41.md`. The original103-input freeze and later policy/analysis seal remain intact. Frozen policy masks preceded all new model responses. Classical outcomes were inspected after the original protocol freeze and before analysis implementation; this timing is disclosed, not retrospectively hidden.

Each large table uses a fixed feature-only subset of1,024 configurations; Dune has384 at its fixed recorded problem-size level and OpenVPN512 at revision2.1.0. Thus these results concern the admitted recorded search spaces, not all original configurations or current live systems. Minimize recorded time; maximize OpenVPN throughput. No hidden full-table target normalization or target-dependent admission. All families and seeds remain included.

## All measured comparisons

Positive numbers mean improved acquired best target relative to the stated comparator, averaged with equal family weight. Intervals resample six families, not30independent seeds. Exact sign-flip p-values enumerate64family sign assignments; all14contrasts remain visible. These are exploratory summaries without multiplicity-adjusted significance claims.

| Model | Comparator | Mean relative gain | Family bootstrap95% | Wins / ties / harms | Exact family p |
|---|---|---:|---:|---:|---:|
| 0.5B | full_classical | -2.4004% | [-5.5545%, -0.3669%] | 3 / 13 / 14 | 0.06250 |
| 0.5B | static_rank | -2.5637% | [-5.8043%, -0.1363%] | 3 / 17 / 10 | 0.06250 |
| 0.5B | batch_3nn | -3.0260% | [-6.4279%, -0.2073%] | 2 / 14 / 14 | 0.09375 |
| 0.5B | sequential_3nn | -3.0873% | [-6.4279%, -0.3299%] | 1 / 15 / 14 | 0.03125 |
| 0.5B | full_sequential_3nn | -4.9260% | [-10.6579%, -0.7877%] | 2 / 13 / 15 | 0.03125 |
| 0.5B | random_shortlist | -1.3644% | [-3.5243%, -0.1953%] | 1 / 20 / 9 | 0.03125 |
| 0.5B | random_full | -1.0802% | [-3.1593%, +0.2870%] | 3 / 19 / 8 | 0.40625 |
| 1.5B | full_classical | +1.2047% | [-0.8595%, +4.3675%] | 5 / 19 / 6 | 0.59375 |
| 1.5B | static_rank | +0.7202% | [+0.1462%, +1.6115%] | 8 / 21 / 1 | 0.06250 |
| 1.5B | batch_3nn | +0.1024% | [+0.0000%, +0.3073%] | 2 / 27 / 1 | 1.00000 |
| 1.5B | sequential_3nn | +0.0419% | [+0.0000%, +0.1258%] | 2 / 27 / 1 | 1.00000 |
| 1.5B | full_sequential_3nn | -1.8356% | [-4.6633%, -0.0152%] | 6 / 15 / 9 | 0.15625 |
| 1.5B | random_shortlist | +1.2212% | [+0.0454%, +3.4315%] | 6 / 23 / 1 | 0.25000 |
| 1.5B | random_full | +1.5485% | [+0.1603%, +3.6620%] | 14 / 11 / 5 | 0.12500 |

The1.5B primary mean(+0.1024%) comes entirely from HIPAcc's positive family mean; the other five family means are zero. It has2wins,27ties and1harm, with exact family p=1. Against full-domain3NN it is−1.8356%(6wins,15ties,9harms). A claim based only on its+1.2047% mean against centroid would conceal the stronger comparison. The smaller model is worse than both primary and strong controls on average.

Figures: `results/v41_model_analysis/model_contrasts.png` and `family_gains.png` (alsoSVG). All420paired comparator rows: `paired_cases.csv`. Full summaries and policies: `summary.json`.

## Frozen policy transfer

The old benefit router selects only OpenVPN seed11; uncertainty selects no calls.29/30prefixes have at least one feature outside a development range. This is transfer of an old controller trained with a different LLM interface/target, not a newly validated calibrated predictor. No threshold was refit after seeing these outcomes.

| Model | Reference | Policy | Calls /30 | Quality gain | Net gain with0.01 relative penalty/call |
|---|---|---|---:|---:|---:|
| 0.5B | batch_3nn | never | 0 | +0.0000% | +0.0000% |
| 0.5B | batch_3nn | always | 30 | -3.0260% | -4.0260% |
| 0.5B | batch_3nn | benefit | 1 | -1.1008% | -1.1341% |
| 0.5B | batch_3nn | uncertainty | 0 | +0.0000% | +0.0000% |
| 0.5B | batch_3nn | random_matched_benefit_diagnostic | 1 | -0.0080% | -0.0414% |
| 0.5B | batch_3nn | hindsight_oracle_diagnostic | 2 | +0.0567% | +0.0135% |
| 0.5B | full_sequential_3nn | never | 0 | +0.0000% | +0.0000% |
| 0.5B | full_sequential_3nn | always | 30 | -4.9260% | -5.9260% |
| 0.5B | full_sequential_3nn | benefit | 1 | -1.1064% | -1.1397% |
| 0.5B | full_sequential_3nn | uncertainty | 0 | +0.0000% | +0.0000% |
| 0.5B | full_sequential_3nn | random_matched_benefit_diagnostic | 1 | +0.1668% | +0.1335% |
| 0.5B | full_sequential_3nn | hindsight_oracle_diagnostic | 2 | +0.1767% | +0.1335% |
| 1.5B | batch_3nn | never | 0 | +0.0000% | +0.0000% |
| 1.5B | batch_3nn | always | 30 | +0.1024% | -0.8976% |
| 1.5B | batch_3nn | benefit | 1 | +0.0000% | -0.0333% |
| 1.5B | batch_3nn | uncertainty | 0 | +0.0000% | +0.0000% |
| 1.5B | batch_3nn | random_matched_benefit_diagnostic | 1 | +0.0000% | -0.0333% |
| 1.5B | batch_3nn | hindsight_oracle_diagnostic | 2 | +0.1075% | +0.0583% |
| 1.5B | full_sequential_3nn | never | 0 | +0.0000% | +0.0000% |
| 1.5B | full_sequential_3nn | always | 30 | -1.8356% | -2.8356% |
| 1.5B | full_sequential_3nn | benefit | 1 | -0.0083% | -0.0417% |
| 1.5B | full_sequential_3nn | uncertainty | 0 | +0.0000% | +0.0000% |
| 1.5B | full_sequential_3nn | random_matched_benefit_diagnostic | 1 | +0.1744% | +0.1411% |
| 1.5B | full_sequential_3nn | hindsight_oracle_diagnostic | 6 | +0.2816% | +0.1984% |

Oracle call counts in this table are for penalty0; the oracle may change its calls at positive penalty. Full per-penalty counts are in the machine summary. A hindsight oracle is explicitly nondeployable. The random matched policy requires the cohort's realized predecision rate and is a diagnostic; the zero development-rate random policies are also retained in the machine summary. All108policy/model/reference/penalty combinations are independently checked, not selected after results.

For the1.5B model, even hindsight's observed opportunity averages only0.1075% versus batch3NN(2calls) and0.2816% versus full-domain3NN(6calls), before any model cost. The transferred benefit router's single call gives no gain versus batch3NN and slightly harms the strong-control result. Its0.5B call produces material harm. A zero-call uncertainty policy merely equals never-escalate; it does not demonstrate useful discrimination.

## Reliability and actual cost

Actual model stage: 60 requests, 600 new recorded outcome accesses, 277.213992s including the failed startup and recovery. Combined V41collection uses3,000recorded accesses(2,400classical+600model branches), despite each deployment arm having only20logical evaluations. Full request usage:98,342input tokens and1,200output tokens; request wall time254.780243s. Both sizes consumed49,171input/600output tokens; request times were65.264995s(0.5B) and189.515248s(1.5B). These are measured local times, not dollar prices or live-system evaluation costs. External spend USD0; no downloads or paid/cloud inference.

There were zero failed/malformed model requests and zero request retries, but **one real infrastructure startup failure**. The0.5B model completed all30cases. The first1.5B process then failed with OpenMP Error179(Cannot open SHM), before any1.5B request. The terminal original process and its failure are preserved in `artifacts/study_v41/recovery_attempt1/`. A one-shot execution-recovery wrapper ran only the30unattempted1.5B cases after sandbox escalation. It kept the same model revision, precision, threads, prompts, seeds, decoding and candidate sets; preserved all63completed0.5B files by hash; and subtracted the first attempt's74.260286s from the700-second stage cap. This was a startup retry, not a model-request retry. No failed case or cost was discarded.

Transformers emitted existing sliding-window/SDPA and inactive-sampling-parameter warnings, retained in raw logs. Inference used the recorded pinned implementation, not a claim of equivalence to every official inference backend. Complete syntax success partly reflects the constrained output grammar and does not establish semantic optimization reliability.

Actual research cost includes collecting both counterfactual branches and every control. Retrospective deployment estimates in the policy summary count one selected continuation per prefix,20logical evaluations/case, and only selected calls/tokens. Their runtime includes observed components and explicitly excludes startup, policy scoring, model-branch lookup time and unmeasured overhead. Hypothetical penalties0,.01,.05 are fractions of comparator performance, not measured dollars. Dataset lookup time is not the original system's physical evaluation cost.

## Verification and reproduction

-300tests passed, including budget/direction/isolation and policy/unknown-usage/failure tests.
-All600new acquired targets match pinned source rows; independent standard-library checking agrees on Python3.10/3.12,542distinct acquired rows.
-All60rendered prompt hashes, input/output token counts, decoded raw outputs, grammar traces and cache keys replay exactly with the local tokenizers. Model logits were not recomputed.
-Independent Fraction arithmetic agrees on420contrasts,14model/comparator summaries and108policy means on Python3.10/3.12. No model call or new target acquisition was used in replay.
-All original protocol/policy seals and completed0.5B files remain unchanged. Both figures were rendered and visually checked.

```sh
.venv/bin/python -m pytest -q tests/synthetic tests/test_transfer_v41.py
.venv/bin/python -I -S scripts/verify_source_events_v41.py --kind model
.venv/bin/python scripts/analyze_models_v41.py
.venv/bin/python scripts/verify_model_tokens_v41.py
.venv/bin/python -I -S scripts/verify_model_results_v41.py
.venv/bin/python scripts/render_models_v41.py
```

Collectors deliberately refuse to overwrite prior attempts. Raw requests, starts, model identity and branch/checkpoint states are in `results/v41_models/`. Reproducing new inference requires the pinned local weights, data and explicit remaining resource allowance; this replay is not a promise of identical numerical inference on another physical machine.

## What this changes, and what remains

This is a completed independent-family extension with actual LLM evidence, stronger than the previous two-family result. It supports a bounded negative/mixed conclusion: here, model size and comparator choice change the apparent benefit, while transferred escalation does not produce useful gains. It does not establish that LLM escalation is generally ineffective.

Q2 readiness is still unproven. Novelty overlaps known strong-baseline and routing cautions; six new families, two sizes from one model family, old public benchmarks, nominal/subsampled domains, unvalidated application quality/security and no useful router remain substantive limitations. Repeated tests cannot repair those limitations. Independent model-family/physical replication, deployment utility, measurement-noise effects and new-controller generalization remain untested. DeepPerf data-specific redistribution permission is unresolved; full source tables stay local/ignored.

**Prioritized next action:** obtain a scientific assessment of whether the constrained-checkpoint and controller-transfer failure is a sufficiently distinct empirical contribution relative to the close prior work already audited. Prepare this result for discussion with Tim Menzies; do not contact him automatically. If further experiments are justified, the next protocol should establish a usable signal on independent development families with application-quality constraints and an independent model family before attempting another held-out router. Do not spend another batch merely retuning these now-exposed cases until the mean turns positive.
