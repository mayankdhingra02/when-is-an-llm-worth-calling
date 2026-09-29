# Status — 2026-09-24, ambiguity audit complete; three-call extension ready

## Resume here / next action

Read reports/rule_identifiability_v20.md and reports/nonmonotone_probe_v21.md. Independent unblocked work is complete. **Request approval for three additional local attempts, cap137→140, with1800seconds andUSD0 unchanged.** configs/authorization_v21.json remains denied. Do not silently increase limits or start another audit instead of resolving this concrete blocker.

If the user approves this precise three-call request, record their response/time, set granted=true/request_cap140 (retain additional_requests3,runtime1800,spend0), then execute:

```sh
.venv/bin/python scripts/run_nonmonotone_v21.py
.venv/bin/python scripts/analyze_nonmonotone_v21.py
```

A direct continuation reply to the specific approval question authorizes that bounded proposal only; generic continuation elsewhere is not an open-ended cap increase. No ledger reset. Stop after three attempts irrespective of outcome. Started runs require audit before retry. If less than22 runtime seconds remain, stop rather than extend the cap.

## What actually ran this continuation

V20 audited all15 V8 and9 V19 actual saved responses against four fixed post-hoc rules; all96 comparisons retained and exact replay passed. First-display-ten and endpoint-ID-sequence rules both match24/24 outputs; lowest IDs match18/24, highest IDs6/24. Report them by source study (15/15 and9/9 versus15/15 and3/9 etc.), not as independent samples. Only ascending/descending ID orders were tested. V19's observed display-order effect remains valid; a unique internal mechanism is not identified.

V21 prepared a separating condition: IDs0,J,1,I,…,9,A while preserving original feature order/observations for MySQL/lrzip/Brotli seed11. First-display and endpoint-sequence rules disagree on these prompts, but **no V21 model output exists**. Exact prompts/mappings were tokenizer-checked and frozen. The model's behavior is unknown.

**140 tests passed** (139 after audit,140 after extension code). Compilation checks passed. Actual unapproved runner returned expected status2 before model loading/measured directory creation. No new model call, objective acquisition, physical trial, download or spending occurred.

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/audit_rules_v20.py
.venv/bin/python scripts/audit_rules_v20.py --verify-only
.venv/bin/python scripts/prepare_nonmonotone_v21.py
.venv/bin/python scripts/run_nonmonotone_v21.py
```

All succeeded except the last, which correctly blocked on permission. The real V21 provider path/response analyzer remain untested end-to-end for this permutation. Synthetic rule predictions are not experimental responses.

## Evidence

- Completed post-hoc audit: results/v20_rule_audit/summary.json, rule_matches.csv; logs under artifacts/study_v20/; protocol_v20_rules.md/.freeze.json (10 files).
- Unexecuted design examples: artifacts/study_v20/unexecuted_designs.json, explicitly not measured outputs.
- Prepared actual prompts: data/nonmonotone_probe_v21.json; reports/protocol_v21_nonmonotone.md/.freeze.json (27 files).
- Permission/guards: configs/authorization_v21.json; scripts/run_nonmonotone_v21.py; analyzer scripts/analyze_nonmonotone_v21.py.
- Tests/tokenizer/blocked launch: artifacts/study_v21/tests.log, tokenizer_preflight.json, denied_run.log, preflight.json.
- Prior current review docs: artifacts/history/v20_before_rule_audit/.

## Current bounds

Inference **137/137 exhausted**,237 historical attempts. Runtime **1776.3840/1800seconds**, **23.6160seconds remaining**, active_since null. V20 audit/replay0.0087seconds, V21 tokenizer preparation2.7895seconds. No additional models/outcomes/spend; historical1134 physical trials +5408 recorded objective acquisitions, distinct types. Download ledger1415316681bytes/model999602607bytes unchanged.

Proposed V21: three requests only, existing pinned Qwen0.5B CPUfloat32/greedy/four threads; inherited V19 provider/grammar unchanged.14-second work/polling deadline,≤0.75second cleanup,6second request timeout,20token output maximum,zero retries,22second startup reserve including later analysis. Runtime/spending cannot increase. No new fresh-original repeats in this extension; comparisons to V19 originals are across sessions.

## Prior result and remaining limits

V19 actually completed9/9 calls: all selected first displayed ten; display reversal changed all ten configurations and ID reassignment preserved all ten in each case. V20 narrows interpretation because first-displayed copying and ID-sequence continuation coincide on those monotone lists. No useful optimization or benefit-router advantage demonstrated. V6 selected zero escalation, V17/V18 showed little recorded task headroom. All prior sources/results/failures/freezes retained.

Untested: V21 responses, broader permutations/prompts/models, untouched groups, selection-quality consequences, application utility, live routing benefit. New three-call authorization is the single pending action; no other experiment is proposed to run automatically. No active worker, scheduled followup, paid/cloud access, install, credentials, contact or publication.
