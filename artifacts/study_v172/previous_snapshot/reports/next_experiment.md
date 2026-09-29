# Next experiment after the V171 audit

The V170 version of this file, which prioritized a second physical host, is preserved in `artifacts/study_v171/previous_snapshot/reports/next_experiment.md`. The V171 audit (`reports/audit_v171.md`) revises that priority for three reasons:

- **No LLM-specific headroom so far.** Neither SmolLM3-3B nor Qwen3-8B beat the pre-specified cheap switches (sequential, random-full, adaptive neighbor, GP-EI) by >1% in any of 140 recorded or 60 native model-cases.
- **The router tests could not show skill.** Positives were concentrated in a single ecosystem, so the leave-one-group-out tests could not have demonstrated predictive skill.
- **A second host changes nothing here.** It cannot affect recorded-table evidence and would not change the native conclusion that no arm wins robustly.

**First priority: V172, a model-scale test of LLM-specific headroom** (`reports/proposal_v172.md`, `configs/proposal_v172.json`, hash-frozen in `artifacts/study_v171/freeze.json`).
- **Design.** Replay the 70 saved recorded-cohort message lists with Qwen3-14B Q4_K_M from `Qwen/Qwen3-14B-GGUF`, keeping the same grammar, seeds, projection and B20 accounting.
- **Primary estimand.** Ecosystems with an LLM-specific win.
- **Decision rule.** At least 2 of 7 ecosystems makes a router study testable; otherwise close the router question for local models on this hardware.
- **Prerequisites.** Owner authorization to raise the retained-download cap (357,259,054 bytes remain) and the model-payload cap (9 GiB, 9,126,358,023 bytes used), and at least 25 GiB of free disk (about 12 GiB now).

**Conditional second priority.** Only if V172 meets its rule: a prospectively admitted, headroom-gated cohort of fresh large-domain systems.
- Domains should have roughly ≥500 valid settings, and headroom should be measured before any LLM call.
- The switch-set counterfactual and log-ratio primary metric should be frozen before collection.
- At the V171 upper bound, expecting five positive-bearing held-out groups needs at least 15 systems, and 50–100 at plausible rates.
- The admissible unexposed recorded-table pool is nearly exhausted, so this would mean native task construction.

**Last priority: second-host replication.** Worthwhile only if a paper reports native effect sizes as findings.

If V172 is not authorized, the evidence does not justify further collection with the current models. The productive next step is writing up the bounded boundary result and methodological lesson in `reports/audit_v171.md` §4.

Counters are unchanged by V171: 4,855 cumulative model starts; 41,613 recorded-table charges plus two historical incidental exposures; native counters separate. No paid or cloud use, downloads, weights, installations, publishing, contact or remote push.
