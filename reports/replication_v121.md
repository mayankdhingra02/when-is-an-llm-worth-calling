# V121: does the fixed adapter add value beyond free candidate ordering?

The earlier WordCount result needs an important qualification: all five V120 continuations selected candidate IDs0–9 in presentation order. Replaying those exact already-acquired configurations gives the same outcome with a zero-model first-ten rule. The8.07%/7.60% gains over the original controls were real, but did not establish incremental value from calling an LLM. No new objective values were needed for this identity proof. The original failures, successes and model costs remain preserved.

V121 prospectively evaluates the fixed constrained adapter on the owner MongoDB table. Software/workload and runtime direction are documented; journal/security semantics are held fixed, leaving270 configurations. Five seeds are repetitions of one family, not five systems. A new matched controller was fitted on all35 saved cases from seven other families before any MongoDB target was acquired. No threshold was changed after the test.

## Normal-adapter result

| Control | Mean relative gain | Wins/ties/losses | Valid ≥5% wins |
|---|---:|---:|---:|
| batch_3nn | 0.729% | 2/3/0 | 0/5 |
| full_sequential_3nn | 0.540% | 2/3/0 | 0/5 |
| random_full | 0.458% | 2/3/0 | 0/5 |
| single_portfolio | 0.670% | 2/3/0 | 0/5 |
| presentation_first10 | 0.000% | 0/5/0 | 0/5 |

Joint ≥5% wins against batch3NN, sequential3NN and first-ten: **0/5**. The predeclared descriptive criterion is **not met**. No confidence interval or significance claim from one test family.

## Paired loss-removal intervention

The loss-blind condition replaces observed normalized losses with0.5; configurations, IDs, order, shortlist, instructions and decoding are held fixed. The shortlist itself was acquired-label-dependent, so this does not remove every possible source of performance information.

| Seed | Normal IDs | Loss-blind IDs | Same ordered IDs | Normal first-ten |
|---|---|---|---|---|
| 11 | 0123456789 | 0123456789 | True | True |
| 23 | 0123456789 | 0123456789 | True | True |
| 37 | 0123456789 | FCEBDAHIJG | False | True |
| 53 | 0123456789 | 0123456789 | True | True |
| 71 | 0123456789 | 0123456789 | True | True |

Identical choices under this intervention demonstrate insensitivity to the supplied loss values for these particular prompts. They do not prove that the model cannot use observations elsewhere or isolate all internal mechanisms. Differing selections would be retained equally.

## Frozen routing result

| Target / control | Policy | Escalations | Mean gain | Missed ≥5% wins |
|---|---|---:|---:|---:|
| primary / batch_3nn | never | 0/5 | 0.000% | 0 |
| primary / batch_3nn | always | 5/5 | 0.729% | 0 |
| primary / batch_3nn | benefit | 0/5 | 0.000% | 0 |
| primary / batch_3nn | uncertainty | 0/5 | 0.000% | 0 |
| primary / batch_3nn | random_development_benefit | 0/5 | 0.000% | 0 |
| primary / batch_3nn | random_development_uncertainty | 0/5 | 0.000% | 0 |
| primary / full_sequential_3nn | never | 0/5 | 0.000% | 0 |
| primary / full_sequential_3nn | always | 5/5 | 0.540% | 0 |
| primary / full_sequential_3nn | benefit | 0/5 | 0.000% | 0 |
| primary / full_sequential_3nn | uncertainty | 0/5 | 0.000% | 0 |
| primary / full_sequential_3nn | random_development_benefit | 0/5 | 0.000% | 0 |
| primary / full_sequential_3nn | random_development_uncertainty | 0/5 | 0.000% | 0 |
| first10 / presentation_first10 | never | 0/5 | 0.000% | 0 |
| first10 / presentation_first10 | always | 5/5 | 0.000% | 0 |
| first10 / presentation_first10 | benefit | 5/5 | 0.000% | 0 |
| first10 / presentation_first10 | uncertainty | 5/5 | 0.000% | 0 |
| first10 / presentation_first10 | random_development_benefit | 0/5 | 0.000% | 0 |
| first10 / presentation_first10 | random_development_uncertainty | 5/5 | 0.000% | 0 |

Two model-matched regressions predict (a) the minimum gain against the two original controls and (b) gain against the free first-ten rule. Standardization/coefficients/thresholds were fitted only on development groups; all seven families were retained. Thresholds optimize group-mean selected gain with fewer-call tie breaks, not a fabricated dollar penalty. Leave-family-out predictions select development thresholds; there is still only one prospective test family. All matched-rate diagnostics and hindsight rows are in summary.json.

## Same-adapter historical context (not a pooled held-out result)

| Family | Role | Batch gain | Sequential gain | First-ten gain |
|---|---|---:|---:|---:|
| berkeleydb | exposed_development | -0.597% | -0.015% | 0.023% |
| dune_hsmgp | exposed_development | -0.349% | -8.945% | 6.603% |
| hipacc | exposed_development | 0.132% | -1.233% | -0.031% |
| llvm | exposed_development | 0.000% | -1.990% | 0.630% |
| mongodb | prospective_test | 0.729% | 0.540% | 0.000% |
| openvpn | exposed_development | -6.605% | -6.634% | 0.103% |
| sac | exposed_development | -0.133% | -0.404% | 0.000% |
| storm | exploratory_development | 8.070% | 7.597% | 0.000% |

## Cost, reliability and reproducibility

Actual new collection: 100 real requests, 400 recorded acquisitions (50prefix+250classical+100normal/blind), 100 generated tokens, 11581 reported prefill tokens, 49.655s model lifecycle, peak sampled RSS7,108,558,848bytes. Normal/blind fallbacks: 0/0. New source bodies: 4,827,315bytes. No retries, paid/cloud calls or system installs; zero external spend. The raw ledger preserves startup, HTTP count and caps.

A deployed policy uses one selected branch after its prefix; ten requests per model escalation versus zero for first-ten. The blind intervention and all counterfactual branches are research cost, not deployment requirements. Historical training collection is reused, not free. Native software runtime and dollars are unmeasured; no production cost-saving claim follows.

Source documents, Git-object checks and feature-only manifest: artifacts/sources/v121/ and data/manifest_v121.json. Frozen protocol: reports/protocol_v121.md. Matched development fits: results/v121_router/. Classical prefixes/controls/masks: results/v121_classical/. Raw real inference: results/v121_qwen/. Acquisitions: results/v121_analysis/. Replays/tests: artifacts/study_v121/. Regenerate this report/figure with scripts/report_replication_v121.py.

## Limits and next research priority

This is original recorded-label optimization, not a new MongoDB benchmark run. The workload has a custom configuration not fully archived here; repeated-run dispersion is documented but per-attempt correctness and failure linkage remain unverified. The fixed partition restricts external validity. Pretraining contamination is unknown. ExaStencils was downloaded for audit but excluded without reading performance values because workload/version and performance-stage identity remain unresolved. No new stronger V52 admission is claimed.

The immediate research priority is an adapter that demonstrates incremental value over cheap ordering controls on development families, then a separately frozen evaluation on additional independent families. Avoid further positive-outcome hunting with the unchanged decoder. A useful learned router cannot be established by predicting gains obtainable without inference. Preserve null results and remaining small genuine model advantages in the historical data. Q2 readiness is not established by these traces alone.
