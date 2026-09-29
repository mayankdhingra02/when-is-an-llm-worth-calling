# V58 — retrospective configuration-ID sensitivity on exposed recorded tables

Freeze before generating perturbed-order results. Both V54 Java/default and V56
planning/p05 are already exposed development tables. This is an exploratory
robustness diagnostic, not new held-out evidence, new physical runs or LLM output.
It addresses the untested effect of lowest-ID tie-breaking noted in V56.

Twenty permutations of all48 configuration IDs: Python Random(58000+i), i0..19.
Apply same permutation indices to each separate table; no task mixing or relabeling
of objective/feature pairs. For each permutation/family run seeds11,23,37,53,71.
Hold the FOUR initial physical configurations fixed to the original seed's draw;
map them through the inverse permutation. This isolates ID-order/tie consequences
beyond initialization, rather than also changing which configurations were sampled.
One shared prefix10 per case (four fixed initial +six3NN), then random/3NN/RF-LCB
continuations10 each,20 inclusive outcomes per arm. Same original feature encoders,
classical code, RFparameters and seeds. Random continuation samples the permuted
ID list, so it is a distributional reference, not identical physical random draws.

Only features, ID ordering and acquired values go into each optimizer. Source
row IDs map lineage, not controller features. Hash original tables, save all forty
permutation/family schedules,200prefixes,600arms and8,000 charged recorded accesses.
A new oracle is isolated per permutation/family with its original200-event cap;
overall8,000-event cap enforced. Physical research collection cost remains the
historical144+144 trials; these accesses cost replay compute, not new application
measurements. Do not describe a cached outcome as a freshly observed physical trial.
No model request, downloads, spending or parameter search. Stage180s;
if incomplete, retain cases and do not silently reduce denominator.

After all choices are saved, evaluator computes prefix/arm best recorded penalized
runtime and percentage headroom to that family's recorded minimum. Reuse original
fixed gates: V54 max(5%,2*its medianCV) and V56 equivalent noise threshold (fully
valid settings for CV). Report per-family100-case distributions, per-method exact
minimum counts, max/median headroom, and number of20 permutations whose hindsight
best-of-three portfolio crosses its threshold in >=2/5seeds. A portfolio is not
an achieved policy. No retuning or rerunning another set of permutations to improve
outcomes. Do not interpret100cases as100independent systems or use population
significance tests. Existing-table minima/noise/measurement limitations stand.

If failure of the original headroom screen changes under ID relabeling, report it
as sensitivity and retire strong robustness claims. If it does not, this removes
one possible explanation on these two exposed tables only. It cannot establish
absence of LLM benefit in different workloads, costs, models or independent groups.
