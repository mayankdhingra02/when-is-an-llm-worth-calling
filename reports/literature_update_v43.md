# Candidate generation versus selection: bounded primary-source check

Read 2026-09-25 to position V42/V43, not to certify novelty. Search terms included
LLM Bayesian optimization candidate generation ablations, shortlist ceilings,
and the exact SNAP2 title. No external code executed, credentials used or authors
contacted.

- **Liu, Astorga, Seedat and van der Schaar**, *Large Language Models to Enhance
  Bayesian Optimization*, [arXiv2402.03921v2, 8 March2024](https://arxiv.org/html/2402.03921v2),
  §6: separately tests candidate generation, including desired-outcome conditioning,
  candidate quality and diversity, against TPE/random alternatives. It already
  distinguishes generation from surrogate selection. Our inference: changing
  the search region is not a new idea; our fixed-pool ceiling is a local audit
  of this adaptation, not a criticism that LLAMBO only ranks a cheap shortlist.
  Status: relevant methods read; not executed here.
- [Author LLAMBO repository](https://github.com/tennisonliu/LLAMBO),
  [acquisition function](https://github.com/tennisonliu/LLAMBO/blob/master/llambo/acquisition_function.py):
  inspected desired-value prompting, candidate filtering and bounded retry code.
  [License](https://github.com/tennisonliu/LLAMBO/blob/master/LICENSE) is MIT,
  copyright2024Tennison Liu. No code copied. The GitHub API commit lookup failed
  through the web tool; this inspection used the moving master page, so it is
  not a pinned executable artifact. Do not treat it as an executed comparison.
- **Srinivasan and Menzies**, *Better Together, in the Right Order: Classical-then-LLM
  Optimization for SE*, [arXiv2607.02583v1](https://arxiv.org/html/2607.02583v1),
  methods and limitations: proposed configurations are projected to measured
  rows by feature distance. That permits pointing to regions of the table; it
  differs materially from forcing the model to choose from our fixed20-row pool.
  Hence our ceiling does not bound SNAP2. Exact SNAP2 code remains unverified.

The primary sources support component separation and finite-table limitations.
They do not establish that our particular six-family finding is new. A plausible
contribution must be narrower: audited paired escalation under cheap controls,
including where shortlist construction suppresses headroom and where newly
available headroom remains hard to exploit. Such a contribution still needs
stronger predictive-routing evidence or a compelling validated negative result,
independent software groups/models and equal application-utility constraints.
No journal quartile can be inferred from this bounded search.
