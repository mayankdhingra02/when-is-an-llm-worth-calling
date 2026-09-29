# Research evidence after V94

There is now a concrete negative-result paper candidate: for the fixed local Qwen3 procedure, cheap full-domain sequential 3NN has a better mean final incumbent in all eight evaluated system groups. Six groups are historical/exposed recorded-data comparisons; two are the new prospective native-engine extension. This is 40 paired cases, not 40 independent systems, and not eight untouched test groups.

| System | Evidence stage | LLM mean gain vs sequential 3NN |
|---|---|---:|
| berkeleydb | V91 exposed recorded-data comparison | -0.02% |
| dune_hsmgp | V91 exposed recorded-data comparison | -8.94% |
| hipacc | V91 exposed recorded-data comparison | -1.23% |
| llvm | V91 exposed recorded-data comparison | -1.99% |
| openvpn | V91 exposed recorded-data comparison | -6.63% |
| sac | V91 exposed recorded-data comparison | -0.40% |
| superlu | V94 fresh native-engine comparison | -10.21% |
| highs | V94 fresh native-engine comparison | -9.69% |

The aggregate is descriptive. No new p-value or pooled confidence interval is used to turn an adaptively expanded study into a confirmatory result. Earlier paired studies and prompt diagnostics remain separate evidence.

## Defensible claim

In these finite-domain adaptations with a 10-label checkpoint and 20-label budget, calling this quantized local model is not justified by improved mean solution quality relative to the strong sequential 3NN control. The fresh-engine test delivered zero >=5% LLM improvements in ten pairs. Development-trained routing rules selected never-call and missed no >=5% benefit there. This is evidence for checking LLM headroom before learning a router; it is not evidence that the new benefit predictor beats uncertainty or random routing.

## Reliability and cost

The new batch had 100/100 valid real model responses and 15 charged native SuperLU worker crashes. A posthoc audit associates all 15 crashes with panel size 32 (44 attempted acquisitions at that level); this is not a causal diagnosis. All 250 HiGHS acquisitions were valid. Native collection took 272.823 seconds and model lifecycle 37.449 seconds, with zero external spending. Raw logs retain failed starts and unknown durations. SuperLU within-acquisition timing range was about 4% at the median, versus 1.2% for HiGHS; tiny apparent improvements must not be treated as robust benefits. Even the two sub-5% LLM wins would need roughly 38,691 and 9,707 repeated uses merely to amortize measured inference time under an optimistic fixed-runtime scenario excluding startup and search-cost differences.

## What this does not establish

No general claim about LLMs, reasoning-enabled models, different prompts or native semantic representations; no exact SNAP2 replication; no positive learned-router advantage; no clean-machine or independent-hardware replication; no established novel contribution or journal acceptance. A Q2 label is not a measurable stopping criterion. The present result is worth technical review as a scoped negative study, but a confident claim of Q2 readiness would overstate the evidence.

## Prioritized next experiment

First independently replicate the frozen strong-control comparison on a second environment, preserving all configurations and failures. Investigate the SuperLU crash separately without deleting failed observations or rewriting the V94 domain. Then admit further genuinely independent systems before using any revised prompt/controller as a confirmatory evaluation. More seeds on these two engines do not create more systems. A useful router requires demonstrable, predictable LLM gains on development groups; the current data do not supply that signal. No additional inference batch or automatic background run is pending.
