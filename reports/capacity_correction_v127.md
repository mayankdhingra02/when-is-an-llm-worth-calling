# V127 capacity correction and SAC-only repair bound

The five normal SAC responses and its one rotation probe all hit the512-token output limit. This is a design-caused failure, not evidence of poor model reasoning on SAC. The GGUF vocabulary audit establishes a conservative lower bound: each of ten setting strings has52binary-or-constant positions, hence≥520binary digits must be emitted. No vocabulary token compatible with the output character set encodes more than one such digit. Therefore≥520tokens are needed even before counting seven other positions per string, delimiters or EOS. The frozen512-token cap cannot emit any complete allowed SAC answer. The original all30-valid development screen was consequently unattainable. I should have checked output capacity before freezing it.

A separate actual offline-tokenizer check of a synthetic all-zero legal JSON string takes601tokens for SAC. This fixture is explicitly separate from generated model responses and optimization aggregates. An attempted live metadata check found the server had already shut down; all six connection failures are preserved. The existing offline tokenizer then completed all six fixture checks without generation, model-server restart or new outcomes.

Neither the cap nor the parser was enlarged after results. The original36requests, six incomplete responses, five normal fallback branches and900charged paired outcome accesses remain unchanged. The main report retains all30intended cases. A failed impossible-validity screen alone cannot establish optimizer inferiority. Independently, all five families whose normal outputs were valid have negative family-mean gain versus full-domain sequential3NN in this measured assay.

We can bound what repairing only SAC could change, without spending more LLM calls: replace its five fallback targets by the best attainable target in the already charged V126admitted domain, while keeping the other25actual outcomes fixed. This is a hindsight upper reference, not an achievable policy, generated response, corrected experiment or held-out estimate.

| Comparator | Mean gain with ideal SAC-only repair |
|---|---:|
| full_sequential_3nn | -4.718% |
| random_projection | -0.656% |
| full_batch_3nn | -0.366% |

Even this nondeployable repair has only1/6positive family means versus sequential. The unchanged25actual outcomes prevent a SAC-only output-budget repair from making the overall means positive against the primary controls. This does not rule out a genuinely different intervention across the other families. No repaired completion or score is substituted into the original results.

Before any future proposal collection, perform both input-context and output-capacity preflight for every schema using the actual tokenizer. A scalar output limit that is convenient for short binary configurations is unsuitable for a batch of ten59-field configurations. Keep a separate frozen diagnostic/quality criterion so representation infeasibility is not misreported as a scientific rejection of LLM optimization.
