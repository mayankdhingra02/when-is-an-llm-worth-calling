# Research assessment after V159

The new experiment strengthens a reproducible **negative result about this particular escalation procedure**. It does not establish a successful benefit-aware router, a universal claim about LLM optimization, or Q2 readiness. The defensible claim remains narrower than the publication goal.

## What changed

Earlier work covered 70 cases per model across eight engine families, grouped into seven ecosystems, plus separately reported native studies. V154–V155 added source-mapped conditional-call rules and GP-EI. Those additions did not reveal a useful transferable escalation policy. Their full original algorithms were not replicated. Their outcomes must not be pooled with the new 17-search-plus-three-validation design.

V156 audited two new implementations and installed hash-locked official wheels in an isolated environment. V157's first workload failed admission: cvc5 timed out in all 20 probes, while one CP-SAT cell was below the timing floor. V158 changed only board sizes under a separately frozen protocol; all 40 new probes passed. Both stages remain visible. This workload selection exposes the families for subsequent design, even though no LLM gain had been seen.

V159 executed **800 actual native evaluations and 20 real local-model requests**, using five seeds per engine, identical saved prefixes, five classical controls, two pinned models and fresh validation. All solver outputs were independently validated; all model outputs parsed; all 70 validation cells met the 5% relative-MAD rule. No retry, timeout penalty or fallback was needed in the paired stage. Both model servers exited normally. Paired collection took about 401 seconds locally.

| Engine | Model | Mean gain vs sequential 3NN | Mean gain vs GP-EI | Robust joint wins / 5 |
|---|---|---:|---:|---:|
| cvc5 | SmolLM3-3B | +0.402% | -0.263% | 0 |
| cvc5 | Qwen3-8B | +0.623% | -0.030% | 0 |
| CP-SAT | SmolLM3-3B | -22.024% | -21.200% | 0 |
| CP-SAT | Qwen3-8B | -21.203% | -20.377% | 0 |

Positive gain means shorter median validation runtime. A joint win required a different configuration, >10% gain over sequential, adaptive and GP-EI, correct validation, and stable timing. Both models had zero such wins. The historical benefit and uncertainty policies called neither model. The mapped BORA and rank policies called but lost mean quality. A retrospective oracle shows only tiny gains and is not deployable.

## What can and cannot explain this

A post-outcome diagnostic, not a new policy, separates two situations. On cvc5 the sequential arm kept a prefix configuration in all five seeds; measured search improvements by other arms were small. On CP-SAT, sequential, adaptive and GP improved their acquired search incumbent in three of five seeds, while both model arms kept the prefix incumbent in all five. Thus the latter result is not explained solely by every continuation having no observed opportunity. These comparisons among acquired observations do not establish a known global optimum.

The output representation remains a limitation. Among the first seven CP-SAT proposals per seed, 16/35 SmolLM and 19/35 Qwen proposals required projection; duplicate counts were 7/35 and 15/35. Twelve of the 20 model/sequential pairs selected the same configuration. This motivates a future representation ablation but does not prove that changing prompts would fix performance. Tuning on these families cannot produce an untouched test.

## Credibility and limits

There are 1,227 passing tests. Independent numerical replay checks every new objective, branch and budget, all 70 GP decisions, selections, model provenance and aggregate outcomes, and rejects three semantic corruptions. Policy features/decisions are recomputed from prefix-only data using previously tested helpers. Reports and figures reproduce byte-identically. This is internal consistency, not independent replication.

The implementations share generated N-queens, with different fixed sizes. They are not two independently sampled industrial applications. The CVC4 predecessor alias was checked in a post-collection lineage audit, with no matches in the recorded 852-file scope; that timing is explicit. Seeds do not multiply the independent-system count. All timings come from one host. Sixteen validation medians were just below the feasibility screen's 10 ms floor; the paired win rule did not include that floor and is not changed retrospectively. All validation MADs remained below 5%; the practical margin was 10%, distinct from earlier 1% studies.

The router transfers from a historical 20-search target to a 17-search-plus-three-validation target. Model families, quantization, constrained batch proposals, projection, fixed checkpoints and public-benchmark familiarity bound the claim. No population significance, formal reliability guarantee, full prior-method replication or industrial deployment benefit has been established. Further tuning on these outcomes would not fix those limitations.

**Most important next action: run a fixed, prospectively selected cohort of independent application workloads with the comparison set unchanged.** Admission must depend on source, license, fixed output correctness and measurement feasibility, not expected LLM gains. Independent-host replication follows. A narrowly scoped negative empirical paper is a reasonable direction to discuss with Tim Menzies; suitability still needs novelty and methodological review, and acceptance cannot be promised.

Evidence: [V159 report](solvers_v159.md), [source audit](source_audit_v156.md), [failed feasibility](solvers_v157.md), [revised feasibility](solvers_v158.md), [resume status](../STATUS.md).
