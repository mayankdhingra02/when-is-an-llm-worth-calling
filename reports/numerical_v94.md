# V94: fresh numerical-engine results

The fixed Qwen3 policy was evaluated prospectively on two new native engine groups. This is not a learned-router validation or evidence of journal acceptance.

| Engine | vs batch 3NN mean | vs sequential 3NN mean | vs random mean |
|---|---:|---:|---:|
| superlu | -0.29% | -10.21% | -7.52% |
| highs | -2.10% | -9.69% | -10.08% |

Positive gain means a faster validated incumbent. Every seed is retained in `results/v94_analysis/summary.json`; the 5% practical threshold was fixed before measurements. No group confidence interval is warranted with two engines.

## What actually ran

{
  "acquisitions": 500,
  "valid_acquisitions": 485,
  "physical_starts": 1474,
  "physical_return_events": 1459,
  "certificates_recomputed": 1455,
  "failed_worker_acquisitions": 15,
  "generation_requests": 100,
  "responses": 100,
  "returned_generated_tokens": 100,
  "full_context_tokens_summed": 70620,
  "native_stage_seconds": 272.822869583033,
  "model_stage_seconds": 37.44918945804238,
  "peak_native_sampled_rss_bytes": 102416384,
  "peak_model_rss_bytes": 6721028096,
  "external_spend_usd": 0,
  "unobserved_request_usage_unknown": 0
}

Each of 10 shared prefixes acquired ten labels. Four continuations acquired ten labels each: 500 actual configuration acquisitions, versus 20 logical labels for deployment of any one branch. Each acquisition planned three physical solves. Native failures remain charged and penalized; physical starts/returns are reported separately, and missing executions are unknown. The verification recomputes solution certificates from saved vectors and reconstructs every classical/LLM selection.

## Costs and interpretation

Actual collection includes all four continuations, all real model requests and native/model lifecycle time. A deployed policy would use its shared prefix plus one branch and pay model cost only on escalation. External spending is zero; electricity and hardware costs are unknown. The per-case inference-only break-even reuse count divides measured model case time by positive incumbent runtime savings. It excludes startup and different search costs, so it is a scenario, not demonstrated deployment savings.

## Limitations

Two engine groups, one input per engine, one machine, three timing repetitions per acquired configuration, and selection on noisy measured minima. Repeated seeds are not independent systems. Public benchmarks may be in model pretraining. Native and wrapper versions are pinned, but a clean-machine replication has not run. SuperLU worker crashes are actual runtime failures, not filtered observations; the cause is not yet established by a native debugger. The freeze remains unchanged. The constructed RHS is disclosed. Historical dataset redistribution terms remain unresolved. New router thresholds were not fit or assessed on these held-out outcomes.

Reproduce analysis: `.venv/bin/python scripts/analyze_numerical_v94.py`. Raw records: `results/v94_native/`, `results/v94_qwen/`. Freeze: `reports/protocol_v94.freeze.json`.
