# Research assessment after V165

**The new result narrows the explanation for the earlier negative findings.** The ANN task left very little observed opportunity by the B10 checkpoint, while text search retained a practical opportunity in a minority of cases. More model calls on these same small tasks would be weak evidence for a general routing method. This is a useful benchmark-validity diagnostic, not Q2 certification or a successful router.

## What actually changed

V164 had reduced duplicate/projection problems with an explicit catalog, without recovering a robust optimization gain. V165 then prospectively froze a different question: how close were the saved prefix incumbents to a good reference from the entire finite domain?

We executed every one of64 settings per application three times for selection, fixed a quality-feasible reference from those measurements, and executed every setting three more times for validation. That is768 new configuration outcomes and2,304 native invocations. All passed correctness/quality. There were no new LLM calls, downloads or paid services. These costs are outside the prior B20 policy budgets, and no optimizer or router received the exhaustive timing table.

## Result and its limits

At the original B10 checkpoint, text-search prefixes had mean observed improvement to the selected reference of5.293%, ranging0–12.695%. One of five cases met the frozen robust10% headroom rule; another above10% case had unstable validation and did not meet it. At B4/B7, two of five text cases met the robust rule. These checkpoints come from the same saved trajectories, not independent tasks or actual earlier LLM handoffs.

ANN had no robust10% B10 headroom against the selected reference. However, the selection winner ranked ninth on validation, and all B10 incumbents were slightly faster than it. This shows why a minimum selected from noisy measurements must not be treated as a proven optimum. The text reference ranked second on validation. Neither application's validation contained a setting robustly more than10% faster than its selected reference under the declared stability rule.

A separately labeled post-hoc sensitivity compares prefixes with the fastest *validation* setting. It is optimistically biased because it selects and scores on the same data, and it does not replace the primary reference. Even under that favorable finite-sample comparison, ANN's B10 observed gap was at most3.285% (mean1.618%). Text search still had a maximum12.973% gap (mean5.595%). This supports limited opportunity in ANN at B10 under this domain/input, not an assertion that ANN optimization is generally solved.

The distinction matters for the research question. A benefit-aware router has little opportunity to demonstrate selective escalation on tasks where inexpensive search already approaches the best observed setting. Text search shows that a complete lack of opportunity is not the sole explanation across all cases. Conversely, exhaustive opportunity does not establish that a method can discover the better setting within seven remaining search evaluations. No actual earlier-checkpoint LLM benefit has been measured here.

## Methodological value

The diagnostic separates three concerns: validity of model proposals (V164), budget-relative benefit of continuation (earlier paired experiments), and benchmark opportunity remaining at the handoff (V165). Repairing proposal defects did not supply practical quality gains, and a substantial part of this tiny cohort has little observed opportunity. This is a defensible qualification of a negative empirical result, rather than repeated prompting until a win appears.

The shared validation table gives identical values to identical configurations; previous primary experiments used separate arm validations and retained their timing variation. V165 does not retroactively erase that variation or overwrite those estimates. All90 prior V164 incumbent selections are mapped only as a labeled diagnostic. Full-space observations expose these domains for future development; they cannot become new held-out evidence.

## Checks and remaining work

All1,294 tests passed. Independent replay verifies all768 raw outcomes, acquisition/order/cost accounting, reference selection before validation,30 frozen prefix checkpoints and90 prior arm selections. It rejects corrupted utility, quality, configuration identity and reference ID. Post-hoc sensitivity arithmetic is independently checked too. Eight analysis/report/figure files regenerate byte-identically. These are internal checks on one Mac, not external replication. All collection finished in309.223s of an1800s cap.

The most useful next local research is a prospectively frozen benchmark expansion with larger realistic inputs and more varied configuration effects, selected by provenance and workload criteria before model gains. Headroom diagnosis belongs in development design; it must not be used to select favorable LLM outcomes or quietly discard easy/negative held-out cases. Independent-host replication remains valuable, but no second-machine access has been established. Full original-method replication, broader model families, production deployment, and a useful unseen-system router also remain untested.

**Single most important next action: freeze a broader, realistic workload cohort before any additional LLM outcome collection.** Do not keep tuning prompts on the now exhaustively exposed two-task cohort. The user has not authorized paid/cloud inference or external publication/contact; no such action occurred. A bounded negative paper is a reasonable discussion direction, but methodology, novelty and venue suitability still require review.

Evidence: [protocol](protocol_v165.md), [measured report](headroom_v165.md), [prefix figure](../results/v165_headroom/prefix_headroom.png), [post-hoc sensitivity](../results/v165_headroom/posthoc_validation_minimum.json), [STATUS](../STATUS.md).
