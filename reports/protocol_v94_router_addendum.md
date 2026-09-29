# V94 secondary router transfer, before continuation outcomes

The primary V94 protocol is unchanged. This secondary analysis is added after
prefix collection and model-choice generation, but BEFORE any continuation
objective is measured. It does not use model choices or new-family labels for
training or tuning. It is explicitly an exploratory protocol extension, not an
originally registered confirmatory claim. Timing of this addition is disclosed.

Reuse the 30 existing V91 Qwen3 paired outcomes from six exposed engine groups
as DEVELOPMENT data. Repeated seeds remain inside their system group. Target
is relative gain over full-domain sequential 3NN. Use the existing nine V6
acquired-prefix features, no family identity or model outputs. Fixed ridge
alpha=1, standardized with training-group means/scales. Produce development
predictions by leave-one-system-out fitting; no row-wise split. Pick the
benefit threshold from {-0.1,-0.05,0,0.01,0.05,0.1,never} to maximize group-mean
OOF gain minus 0.05 per escalation. This penalty is a labeled quality preference,
not USD or measured latency. Ties prefer fewer calls, then larger threshold.
Refit coefficients on all six DEVELOPMENT groups only.

Uncertainty-only threshold comes from development feature quantiles
{0,0.25,0.5,0.75,1} and never, maximizing the same criterion. Its values and
targets are development-only; there is no fitted scaler. Strict greater-than
threshold. Freeze all ten new-family masks before collecting continuations.
Compare never, always, benefit, uncertainty, deterministic random at the
development selected rate, and random at each new-cohort matched count
(explicit retrospective cohort-rate diagnostic, no outcome use). Hindsight
oracle selects positive measured gains, diagnostic only.

Report per-group quality gain, calls saved, useful escalations missed (>5%),
harmful calls (<-5%), actual selected model usage, and 20 objective labels per
deployed case. No refitting or threshold changes after new outcomes. Six
development and two test groups are too few for credible population routing
claims; native timing noise and transfer from recorded to measured workloads
are additional limitations. A never-escalate result may be the correct choice.
