# Research assessment after V164

**New finding: removing a concrete proposal problem did not recover practical optimization benefit in this development cohort.** Explicit candidate catalogs reduced duplicate/projection events sharply, while increasing inference cost. Neither interface produced a robust joint win over the three strong classical controls. This strengthens the explanation of the bounded negative result; it does not establish a successful benefit-aware controller or Q2 readiness.

## What was tested

V163 exposed two application groups and showed many repeated/projected proposals. V164 prospectively froze an interface intervention on those same groups before collecting any new response or continuation outcome. It reused only the ten saved B10 prefixes, not the old continuation outcomes. Both models made fresh calls in both conditions. All five classical controls and four model/interface arms performed fresh continuation search and validation.

The catalog condition changes several things together: it displays all eligible configurations, requests candidate IDs, and constrains the grammar to eligible IDs. The numeric condition retains the original prompt. Both conditions receive identical acquired labels, use the same objective and B20 allocation, and resolve duplicates by the same feature-space projection. This is a compound interface intervention, not identification of the isolated effect of encoding, prompting, or grammar.

Actual new collection: 40 real local-model starts, 900 configuration outcomes, 2,700 native invocations, 90 logical arms and 270 fresh validations. The historical 100 prefix outcomes/300 invocations are identified as reused, not newly collected or free historical research. All 40 responses parsed; all 900 outcomes met correctness/quality. One of 90 validation cells exceeded the fixed MAD threshold and remains in the descriptive means.

## Concrete result

Among the first seven proposals actually evaluated per case:

| Condition | Proposals | Needed projection | Duplicate proposals |
|---|---:|---:|---:|
| Numeric | 140 | 77 | 68 |
| Catalog | 140 | 0 | 0 |

The grammar enforces eligible IDs but does not enforce uniqueness. Across all ten returned proposals per case, the catalog still had two duplicates/projections among 200 proposals, both outside the first seven evaluated; numeric had 117 duplicates and 128 projections among 200. All denominators are retained. This is an observed interface reliability improvement on these prompts, not a proof of universal duplicate prevention.

There were **zero robust catalog wins or losses** against numeric under the predeclared 10% rule, and zero robust joint wins for either interface against sequential3NN, adaptive neighbor and GP-EI. Seventeen of 20 numeric/catalog pairs selected the same configuration. Mean catalog gains versus numeric were -1.187% / -0.521% for Smol on text search / ANN, and +1.096% / +0.577% for Qwen. Those small signed values, especially same-setting comparisons, do not support equivalence or a reliable sub-percent effect.

The catalog used 2.32 times as many input tokens for Smol and 2.43 times for Qwen; observed request time increased to 1.43 and 1.53 times numeric, respectively. These are measured descriptive costs within this batch, not general latency guarantees, dollar savings, or energy measurements. Output tokens decreased, but total request time increased. Cold startup remains separately logged.

## What this changes in the research argument

The earlier failure cannot simply be dismissed by saying that none of the proposals were usable: both interfaces produced valid outputs, and the catalog supplied unique unobserved configurations among the evaluated proposals. Under this particular intervention, repairing that observed defect was insufficient to make escalation beat the controls by the practical margin. It does not prove that duplication never matters, isolate a causal mediator, or rule out another representation/model/workload.

The limited-headroom explanation remains important. Both ANN interfaces retained the prefix incumbent in all five seeds for both models. The task has a small fixed 64-setting domain, public toy-scale vectors, and a B10 checkpoint; it is not evidence about industrial ANN tuning. Further tuning on the same cases cannot make them held-out evidence. The catalog must not be selected retrospectively and reported as an independently validated general method.

## Credibility and unresolved gaps

All 1,282 tests passed. Independent replay checked 900 new outcomes, 100 reused prefix outcomes, shared states, all 70 GP decisions, 270 validations, every response/prompt, and the mechanism/cost aggregates. Four objective/quality/identity/prompt-field corruptions were rejected. Eight report/data/figure artifacts reproduce byte-identically. Both model servers exited normally, no retry or external spending occurred, and collection finished in 465.352 seconds of its 1,800-second limit. The earlier 65-checkpoint chain remains preserved and V163 becomes the 66th historical checkpoint.

This is still internal verification on one host and two already exposed groups. No independent-host run, broad application sample, production-scale deployment, full original-method replication, or generalized useful router has been established. The historical controller target differs from this native17+3 design. More cases from these same seeds/domains would not supply the missing independent evidence.

**Single most important next action: independent replication of the frozen comparison on another host.** A request for second-machine availability was sent in the chat; no answer/access has yet been established in this checkpoint. Do not treat silence as permission or provision cloud. Meanwhile, any future local expansion should prospectively select larger realistic workloads and separate development of checkpoint/representation from untouched evaluation. The present result is a useful mechanism check for a bounded negative empirical paper discussion, not a guarantee of a journal category or acceptance.

Read [experiment report](apps_v164.md), [mechanism figure](../results/v164_native/mechanism.png), [protocol](protocol_v164.md), [STATUS](../STATUS.md), and [next experiment](next_experiment.md). No paper was submitted or person contacted.
