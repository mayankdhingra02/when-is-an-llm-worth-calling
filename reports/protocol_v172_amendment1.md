# V172 amendment 1: pre-start port failure in stage A1

Written 2026-09-28, after stage A1 failed and **before any Qwen3-14B scientific request, response or V172 recorded acquisition existed**. The original protocol and `artifacts/study_v172/freeze.json` are unchanged and remain the pre-collection record. Hashes of the amended files are in `artifacts/study_v172/freeze_amendment1.json`.

## What happened

- Preflight P passed and closed its Qwen3-14B server on loopback port 18721 at 18:57:01 UTC.
- Stage A1 started 11 seconds later on the same port.
- The runtime's pre-start `bind` probe raised `OSError(48, 'Address already in use')`. Sockets from P's closed connections were still in TIME_WAIT, and the probe does not set `SO_REUSEADDR`.
- The stage stopped before launching a server. It made zero generation requests, returned zero responses, allocated zero output tokens and charged zero acquisitions.
- The complete failed stage is retained in `results/v172_models/A1/` (`errors.jsonl`, `summary.json`, `ledger.json`).
- The same failure class occurred historically in V141/V142, where a pre-start socket failure was repaired under a pre-outcome amendment using the unused allowance.

## Why a repair does not bias the result

No Qwen3-14B scientific output and no V172 target had been observed; P's only output was a synthetic compatibility string. The repair therefore cannot depend on outcomes. Leaving A1 as-is would turn half the 14B arm into forced fallbacks from an infrastructure fault unrelated to the model. The frozen rule against additional stages exists to stop outcome-dependent reruns, which this is not.

## Amended procedure

1. **New stage A1R.** It runs exactly the 35 split-1 jobs of A1, with the same model, seeds, prompts, payloads and 1,800 s cap. It uses A1's unused allowance of 35 requests and 35,840 output tokens. Total authorized requests stay at 140 scientific plus 1 compatibility. A1R is the stage of record for the Qwen3-14B split 1. A1 stays in the evidence as a failed stage with zero requests.
2. **Port wait.** Before every server start, the runtime polls the pre-start `bind` probe once per second for up to 120 s and records the wait. If the port is still unavailable, the stage fails as before, with its denominator intact.
3. **Stage order.** P, A1 (failed), A1R, A2, B1, B2, then E.
4. **Code changes, nothing else.**
   - Stage bookkeeping in `common_v172.py`.
   - The port wait in `runtime_v172.py`.
   - `collect_models_v172.py`, `evaluate_v172.py`, `analyze_v172.py` and `verify_v172.py` read stages of record from `common_v172.STAGES` and report the failed A1 separately.
   - `tests/synthetic/test_v172.py` gains port-wait and stage-map tests.
   - Payload, parsing, projection, oracles, estimand and decision rule are unchanged.
5. **No further repairs.** Any other stage failure keeps its unattempted jobs in the denominator.

Model starts: P and A1's aborted launch attempt made no generation request. Both are reported as operational events; only generation requests count toward the project's model-start counter.
