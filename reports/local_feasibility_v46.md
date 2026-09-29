# SmolLM3 runs locally — V46 hardware feasibility

Completed on 2026-09-25 on the user's Apple M3 Pro / 18 GB Mac after the
user requested stopping Next.js and Docker. Installed the pinned SmolLM3-3B
Q4_K_M GGUF and official llama.cpp b11146 runtime inside this repository.
Two real offline generations completed; no research configurations evaluated.

| Check | Short prompt | Longer synthetic prompt |
|---|---:|---:|
| Wall time including process/model startup | 19.30 s | 5.44 s |
| Reported generation speed | 54.4 tokens/s | 50.6 tokens/s |
| Reported prompt processing speed | 243.7 tokens/s | 510.8 tokens/s |
| Peak resident memory | 2.2053 GiB | 2.2051 GiB |
| Exit code | 0 | 0 |

The runtime reports an available Metal Apple M3 Pro device outside the sandbox;
both commands requested full GPU offload. The CLI suppressed layer-placement
logs, so the exact number of GPU-resident layers was not independently observed.
A sandboxed device query returned no named Metal device; its original output is
preserved in `devices.txt`, and the host query in `devices_host.txt`.

Peak resident memory is approximately 2.37 decimal GB. It is not total system
memory consumption or an independently measured GPU allocation. Do not add the
OS footprint number and RSS together. Initial and subsequent startup timings
can differ due to OS caches and first-run initialization; load time was not
separately exposed. CLI rates are rounded, not exact token totals. Exact input
and output counts remain unknown. Both calls used greedy decoding, seed 11,
4096-token context, at most 128 generated tokens, thinking off, and warmup off.
The longer answer ends mid-sentence under that cap. Neither answer is an
optimization-quality result or a meaningful instruction-following benchmark.

## Provenance and cost

Original owner: [HuggingFaceTB/SmolLM3-3B](https://huggingface.co/HuggingFaceTB/SmolLM3-3B).
Downloaded quantization: [ggml-org/SmolLM3-3B-GGUF](https://huggingface.co/ggml-org/SmolLM3-3B-GGUF),
linked by the [original owner's collection](https://huggingface.co/collections/HuggingFaceTB/smollm3).
Quantization revision `4965cb60b150737b68a0408c36aeefb65078f894`,
SHA256 `8334b850b7bd46238c16b0c550df2138f0889bf433809008cc17a8b05761863e`.
Its card does not pin the source weights revision. Label this quantized-model
adaptation accordingly. Model Apache-2.0; runtime MIT license copied locally.
Runtime b11146 / commit prefix `7fe450e19`, version `0.5.0-dev`.
Both downloaded payloads match publisher-provided SHA256 digests.

Downloaded payloads: 1,926,495,026 bytes (about 1.79 GiB), plus metadata conservatively
reserved at 1 MiB. Setup download wall time 42.07 seconds, separately recorded.
Inference stage: 24.746 seconds; two requests, zero retries, failures, or objective
accesses. External spend $0. Local electricity/hardware cost is unmeasured.
The separate new 3-GiB/two-request setup allowance comes from the user's explicit
local-install/test approval; the old research request cap remains exhausted at
350/350. Including setup, follow-up requests now total 352, or 452 including the
original 100-request stage. Old research ledger and raw evidence are unchanged.
No inference process or endpoint remains running.

## Reproduction and evidence

- `configs/local_feasibility_v46.json`: bounded setup scope.
- `reports/protocol_v46_local_feasibility.md`: pre-run design.
- `artifacts/study_v46/feasibility/`: exact commands, prompts, raw stdout/stderr,
  timestamps and actual request ledger. Synthetic prompt is explicitly segregated
  here and excluded from research aggregates.
- `artifacts/study_v46/downloads.json`: payload hashes, byte counts and URLs.
- `artifacts/study_v46/verified_measurements.json`: parsed trace measurements.
- `scripts/setup_smollm_v46.py`: pinned download and verification script.
- `scripts/run_smollm_feasibility_v46.py`: bounded runner, refuses existing run.
- `scripts/verify_smollm_feasibility_v46.py`: verification without new inference.

Read-only verification command:

```sh
.venv/bin/python scripts/verify_smollm_feasibility_v46.py
```

The run command was `.venv/bin/python scripts/run_smollm_feasibility_v46.py`.
It now refuses another run to preserve evidence and prevent extra requests.
Do not delete its evidence to bypass the consumed two-request allowance.
Exact commands can be reused only under a newly accounted run allowance.

Next action: freeze a separate SmolLM3-versus-Qwen study that separates model
family, quantization/runtime, and intervention changes and identifies independent
evaluation groups. Hardware feasibility is established for these short prompts;
useful optimization, reliability over many requests, long-context memory needs,
and publication readiness remain untested.

Validation: two new tests passed (raw-trace checks and refusal to rerun a consumed
allowance). Receipt: `artifacts/study_v46/tests.txt`. Evidence hashes are saved
in `artifacts/study_v46/evidence_manifest.json`. Existing research suite was not
rerun; no previous research implementation changed.
