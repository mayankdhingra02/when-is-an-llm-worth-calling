# Next step after V172

The V171 version of this file, which recommended the V172 model-scale test, is preserved in `artifacts/study_v172/previous_snapshot/reports/next_experiment.md`.

V172 ran that test under a frozen protocol and gave `close_router_question`:
- Qwen3-14B had LLM-specific wins in 1 of 7 ecosystems, against a threshold of 2.
- SmolLM3-3B, the historical Qwen3-8B draw and a partial Qwen3-8B re-draw had none.
- Details: `reports/research_assessment_v172.md`.

**Recommended next step: synthesis and write-up, not collection.** The paper-shaped contribution is a bounded boundary result with a methodological lesson:

1. **Design.** Paired-prefix escalation with charged budgets, hidden-label isolation, complete failure denominators and separate collection and deployment costs.
2. **Always-call is dominated.** Always calling the LLM is beaten by cheap continuations across 7 recorded ecosystems and 6 native implementations.
3. **No LLM-specific headroom from 3B to 14B.** Wins appear in at most one ecosystem, and one of the two 14B wins is matched by random proposals through the same interface.
4. **Routers are non-identifiable here.** With positives concentrated in one group, leave-one-group-out router evaluation cannot be informative. Zero-call routers are correct abstention, not failed prediction.
5. **Methodology.** Escalation benefit must be measured against the best pre-specified cheap switch, and headroom must be established in several independent groups before any router is trained.

Report every arm, stage failure and amendment (V172 amendments 1–4), and disclose the V1–V172 development history.

**Not recommended with current resources:**
- more seeds, prompts or interfaces on these exposed tasks (forking-path exploration);
- a second host, which cannot change "nothing wins robustly" and cannot affect recorded-table evidence;
- a router study, which has no positive-bearing groups to learn from.

**The only substantive open lever** is a much larger model, such as SNAP2's gpt-oss-120b, or a model with different training. It does not fit this 18 GB machine and would need new, explicit owner decisions on hardware or paid inference, which are not authorized. If pursued, it should reuse the V172 design:
- same prompts and switch set;
- the same ecosystem-level estimand and threshold, fixed before collection;
- a complete re-draw of the comparator model with memory caps sized from V172's observations.

Counters after V172: 4,973 cumulative model starts; 43,013 recorded-table charges plus two historical incidental exposures; retained downloads 19,381,944,226 of the V172-approved 20 GiB; model payload 18,128,110,983 of the V172-approved 19 GiB. The V172 cap increases are not standing permission.
