# Research assessment after V97

The restricted-domain follow-up supplies a complete, reproducible result:
250/250 configuration acquisitions valid,750/750 physical solves returned and
independently certified,50/50 real local-model requests returned valid choices.
There were no retries, downloads, paid calls or removed outcomes.

The observed Qwen3 mean relative gain was−1.52% versus same-pool batch3NN,
−2.77% versus full-domain sequential3NN and+12.62% versus random. None of the
five paired cases improved by at least5% against either strong control.
The hindsight oracle gained only0.41% on average against sequential3NN;
this is a non-deployable upper reference, below the scale of the descriptive
timing variation. The two observed positive LLM-versus-sequential gains were
each below5%, and there is no population-level interval from one system.

This adds a cleaner exploratory SuperLU comparison after the V96 qualification.
It is not a repaired held-out test: the system had been examined, the search
space changed, and every new prefix/continuation was measured afresh. Do not
pool V94 and V97 as independent families or attribute their mean difference
solely to the removed settings. Both original and follow-up remain available.

The original benefit-aware routing hypothesis is still unsupported. Both
previously fitted thresholds make no calls, matched-rate random also makes no
calls, and no>=5% benefits are missed here. That is evidence of low measured
routing headroom under this procedure, not a predictive advantage.

For the candidate negative-result paper, a defensible claim is that these
specific local-model selection procedures have not shown a practically useful
advantage over the strong classical controls in the measured setting. Beating
random search alone does not justify escalation. Reliability of response format
and better objective selection are separate outcomes.

Q2 readiness remains unestablished. Independent-machine replication, a stronger
test of reasoning with a final-answer reserve, more independent software systems,
and a current venue-specific novelty assessment are still missing. The next
locally actionable experiment is a bounded development-only final-answer-reserve
procedure, frozen before model calls, with all raw outputs and failures retained.
No positive-result stopping rule or test-set tuning is justified.
