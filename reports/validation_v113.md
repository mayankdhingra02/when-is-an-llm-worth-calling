# V113: fresh validation exposes material timing variation

All **90/90** new native acquisitions completed; all **270/270** saved solution certificates passed independent recomputation. Zero failures or missing attempts, zero new model requests/downloads/spending. Collection took47.387s. This remeasures the configurations selected in V94; it does not rerun an optimizer or generate new LLM choices.

## Primary frozen comparison

|Engine|Mean LLM gain vs batch3NN|Mean LLM gain vs sequential3NN|
|---|---:|---:|
|superlu|-17.60%|-26.39%|
|highs|-12.50%|-13.83%|

None of ten cases beat both controls at the frozen5%margin; the same zero count holds on the descriptive0/2/10%grid. These values are observed contrasts, not causal estimates of an LLM penalty. The complete cases and all three fresh labels per arm are in the saved JSON/CSV. No seed or failed historical acquisition was removed.

## The important qualification

Posthoc, **8** LLM/control contrasts selected exactly the same configuration. **5of8** nevertheless show apparent differences of at least5%; the largest is **23.68%**. Configuration selection cannot explain a difference when the settings are identical. The contrasts are dependent and are not an estimated population false-positive rate.

Across30frozen incumbents, median(maximum-minimum)/mean over three fresh acquisition labels is **35.92%**; 26/30exceed10%. These descriptive ranges are not confidence intervals. Each acquisition itself aggregates three physical solves; the spread across acquisitions shows that those internal repeats were insufficient for stable5%comparisons in this session.

This audit therefore **weakens confidence in precise native-runtime effect magnitudes**, even though the observed direction still supplies no evidence of useful escalation. It does not establish LLM harm, equivalence, or a useful router. The recorded-table studies are a separate evidence stream; this timing check neither remeasures their original software runtimes nor invalidates their trace-replay findings.

## Budget and scope

The30incumbents were frozen before these outcomes: two exposed engines×five seeds×three arms. Each gets3new validation acquisitions×3physical solves. V94search staysB20; search-plus-validation for one arm is23acquisitions/69physical solves, not20. Actual research collection across V94and this check is590native acquisitions plus the original100real model requests. The new90acquisitions are validation overhead, not free budget. No new deployment saving is claimed; electricity/hardware costs remain unknown.

The schedule interleaved arms within pre-shuffled case blocks across three rounds. Same machine, same datasets, same selected configurations, no independent hardware or software groups. The initial motivation was post-selection measurement bias; all analyses are explicitly exploratory. HistoricalSuperLUcrashes remain in V94and were not fixed or excused by the absence of crashes among these selected incumbents.

## Next action

Independently replicate the frozen selected configurations on a separate, otherwise quiet host, retaining correctness checks and identical-configuration negative controls. Establish measurement repeatability before interpreting a5%native effect. Do not select a nicer threshold, delete equal-configuration contrasts, or spend more model calls on this noisy workload. No second host is available in this project; a compatible local/remote machine supplied by the user is needed. Paid provisioning is not authorized.

![All contrasts, with equal configurations marked](../results/v113_analysis/validation.png)
