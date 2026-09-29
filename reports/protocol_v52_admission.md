# V52 — prospective application admission, before new objective inspection

Date: 2026-09-25. This is a source/feature audit, not an LLM experiment.
Motivation: V50/V51 exhausted useful headroom in the small compression workload.
Do not select another task by first looking for favorable measured outcomes.

## Scope and bounds

Audit the eight unused non-compression families already identified in V47:
dconvert, deeparch, exastencils, fastdownward, javagc, mongodb, redis, storm.
Exclude hardware tasks and keep compression retired. Use the pinned V5 registry
and primary author/owner papers, metadata, feature models and harness code.
Maximum new source payload: 20 MiB within the existing persistent download cap;
no models, packages, installs, paid calls or physical benchmark executions.
No raw objective values may enter this audit, including validation labels.
Previously downloaded source papers are allowed; their published aggregate
results do not serve as task selection evidence. Do not execute upstream scripts.

## Admission gates

Each gate has status verified, unresolved or contradicted, plus source references.
All gates must be verified before running a performance screen:

1. Identity: fixed software release, workload, table lineage and measurement units
   and direction; ambiguous transformed headers are insufficient.
2. Equivalent utility: the workload stays fixed and correctness/quality requirements
   are stated. Output-affecting options need a feature-only fixed contract or a
   measured quality constraint. Runtime alone cannot certify neural-model accuracy,
   image quality, solver solutions or storage durability.
3. Validation: primary measurement/harness evidence describes a correctness check
   and treatment of failed/timed-out runs for the exact archived task. A modern
   harness's validation capability is not proof it was enabled in an old run.
4. Feasibility: at least 40 unique configurations after outcome-blind restrictions;
   all controllable variables have described domains, no workload size as an
   optimization knob, all seeds/versions remain in a single system group.
5. Reproducibility: source bytes/version pinned, reuse terms recorded; any missing
   data license prevents redistribution, not private inspection. Do not equate a
   repository code license with independently proven third-party data rights.

An unresolved gate means quarantined for this stronger study, not proof the
historical dataset is invalid. Record observed schema concerns separately from
confirmed upstream defects. Never infer that a direction suffix is wrong merely
because another paper reports throughput: a transformation might have occurred.

## Splits and conditional next execution

Before any new performance access, reserve mongodb, redis and storm as future
evaluation families. This is a prospective reservation, not a claim their old
outcomes have never been exposed; admission still requires a history audit.
All other five families are development candidates. No score-based reassignment.
If any development family passes all gates, freeze a separate executable protocol
before its classical screen: seeds 11/23/37/53/71, prefix10, total20, shared prefix,
random plus mixed-domain surrogate search. Include a random-forest uncertainty
acquisition baseline and an acquired-only nearest-neighbor baseline. No favorable
surrogate or seed selection after results. This document authorizes no objective
reads by itself. No LLM trial until a separate frozen headroom decision is met.

## Deliverables

Executable fail-closed admission validator, synthetic guard tests, pinned source
manifest, all eight family decisions and precise remediation, feature-only counts
where useful, audit report, execution receipt and updated STATUS. If none pass,
report zero eligible tasks honestly and identify the smallest missing evidence or
fresh measurement that resolves the best candidate. Do not manufacture results.
