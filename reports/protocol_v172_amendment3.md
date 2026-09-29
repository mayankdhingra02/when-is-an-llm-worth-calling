# V172 amendment 3: correction of the independent verifier's alphabet

Written 2026-09-28, **after** evaluation E and the frozen analysis had run. This amendment changes no collected data, selection, projection, oracle, analysis or decision. It corrects only the independent replay script.

## What happened

The first run of `scripts/verify_v172.py` failed. It reported "parse/fallback" and "selection" mismatches, and only for SAC and HIPAcc cases. Everything else matched: the primary estimand recomputed to 1 (Qwen3-14B) and 0 (re-draw), all 1,400 charges reconciled, and all four mutation checks were rejected. The failed output is preserved as `artifacts/study_v172/replay_initial_failed_verifier_alphabet.json` and `.log`.

## Cause

- The verifier's independently written parser used the alphabet digits, then lowercase letters.
- The frozen protocol grammar (`scripts/proposal_v127.py`, `ALPHABET`) uses digits, then **uppercase**, then lowercase.
- Domains with more than 10 levels therefore failed only in the verifier. SAC and HIPAcc have up to 19 levels. The collector and evaluator used the frozen parser and were correct.
- The earlier synthetic parser test used only 2–3-level domains, so it missed the bug.

## Correction

- `scripts/verify_v172.py` now uses the grammar's alphabet order.
- A new regression test checks the verifier alphabet against the frozen one and cross-parses a 19-level domain.
- `scripts/common_v172.py` adds `freeze_amendment3.json` to the ordered freeze overlay.
- The replay was then rerun unchanged in every other respect.

Correcting a verifier after seeing it fail can hide real errors. The mitigation: the corrected verifier must reproduce every other check, the full list of initial mismatches is preserved, and the mismatches are confined exactly to the >10-level families that the alphabet difference predicts.
