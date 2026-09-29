# STATUS — V36 exact-arithmetic ablation complete

Updated2026-09-25. Resume here and from [V36 report](reports/arithmetic_v36.md), [frozen protocol](reports/protocol_v36_arithmetic.md) and relevant code. Root documents and ledgers before this turn are in`artifacts/history/v36_before_execution/`.

**Concrete result:** exact arithmetic changes5of20search trajectories and3acquired sets, but **none of20final feasible runtimes**. All60cached-LLM comparisons retain scores and signs. Thus the V34 conclusion survives this particular numerical ablation; no new routing success is established.

## Actually executed

- Twenty new continuations on all10V34prefixes(two exposed families ×five seeds), two controls: joint3NN shortlist/full-domain.
- Exactly200new charged recorded runtime/size-vector acquisitions,20/20arms complete,20unique inclusive evaluations per arm with identical10prefix.
- Recommendations use exact Fraction sums of acquired values. Independent evaluator uses scaled integers; all200decisions/journal entries replayed.
- 246tests passed in1.24s;391inputs frozen before collection;3,149historical/current references verified.
- Standard-library isolated replays under Python3.10.13 and3.12.14 produce identical scientific hash`29154293e59585dd76f781c4e9ec8a222769aa2b99569b7fbe6688cd0e553b6a`.
- No collection/verification failures. Figure visually inspected. No new model calls,physical executions,downloads or external spending. No ongoing job.

## Commands and evidence

Prepare:`.venv/bin/python scripts/prepare_arithmetic_v36.py`.
Tests:`.venv/bin/python -m pytest -q`.
Collect:`.venv/bin/python scripts/run_arithmetic_v36.py`.
Analyze/render:`.venv/bin/python scripts/analyze_arithmetic_v36.py`.
Read-only replay:`.venv/bin/python -I -S scripts/verify_arithmetic_v36.py`(also executed with installed Python3.12).
Historical audit:`.venv/bin/python scripts/audit_history_v30.py`.

Report:`reports/arithmetic_v36.md`; protocol/freeze:`reports/protocol_v36_arithmetic.*`; exact prefix/source manifest:`data/arithmetic_v36.json`.
Raw traces/checkpoints/200-charge journal:`results/v36_arithmetic/`; tables:`arms.csv`,`llm_comparisons.csv`,`families.csv`; complete data:`summary.json`; PNG/SVG:`arithmetic_sensitivity.*`.
Logs,accounting,replays,final receipt:`artifacts/study_v36/`.

Frozen code/source/prior results are preserved. This is a versioned changed-arithmetic adaptation,not overwriting the historical algorithm. The V35.1 standalone ZIP remains a V34 snapshot and does not includeV36. Its cross-interpreter/corruption validation still holds for that snapshot.

## Scope and retained finding

The primary assigned-ID LLM feasible-runtime gain remains−0.3015% versus shortlist joint3NN(1win,6ties,3harms),and−1.6470% versus full-domain joint3NN. V34's positive comparison to static ranking and negative comparison to runtime3NN are unchanged historical results. All three presentations retained; no best presentation chosen.

Two already exposed systems; source measurements are not fresh physical executions. The size cap remains a research default. Runtime-only model prompts were not replaced with size-aware prompts. No untouched-system routing gain, application utility, correctness guarantee or measured deployment savings. The new arithmetic result does not establish robustness beyond these20arms.

## Remaining limits and next action

Runtime **2286.489703/3600s**; remaining **1313.510297s**. This stage added5.141951s of charged collection/analysis. Tests and read-only maintenance are separate.
Follow-up requests200/200(300includinginitial); recorded accesses **9,308**; physical trials1,274. Downloads unchanged4,518,268,306bytes total /4,098,574,535model bytes. USD0new external spend; no cloud,push,publish or contact.

**Single next action:** run the V35.1archive on a second machine for independent review before further collection. Scientific expansion remains`reports/next_experiment_v34.md`: set application quality/practical gain,freeze strong controls/reserve untouched groups,and obtain a new explicit bounded local inference allowance or truly compatible cache. Generic continuation does not expand200/200calls. Further numerical variants on these exposed cases would not add independent routing evidence.
