# V46 — SmolLM3 local feasibility, not an optimization experiment

User authorized installing SmolLM3 and a small local memory/speed test, then
explicitly resumed after stopping Next.js and Docker to recover memory.
This new setup scope uses `configs/local_feasibility_v46.json`: at most 3 GiB
additional downloads, two real generations (including failures, no retries),
128 generated tokens each, and a 180-second inference stage. No objective
labels, paid services, cloud resources, credentials, or held-out research data.
The old 350-request research ledger and scientific stopping decision are
preserved. Setup calls are separately recorded and must be added when reporting
all historical model usage.

Model: ggml-org/SmolLM3-3B-GGUF, revision
4965cb60b150737b68a0408c36aeefb65078f894, SmolLM3-Q4_K_M.gguf.
Artifact SHA256: 8334b850b7bd46238c16b0c550df2138f0889bf433809008cc17a8b05761863e.
Publisher: llama.cpp maintainers; explicitly included in original model owner's
collection https://huggingface.co/collections/HuggingFaceTB/smollm3.
Original model: https://huggingface.co/HuggingFaceTB/SmolLM3-3B.
Quantized model is an adaptation; precise upstream weights revision is not
specified by the quantization card. This limits upstream reproduction even
though the downloaded GGUF is byte pinned. Model license: Apache-2.0.
Runtime: official ggml-org/llama.cpp b11146 macOS ARM64 release, linked from
v0.5.0 release notes. Archive is publisher-SHA256 verified. Project-local install.
No shell installer, dependency updates, or system settings changes.

Predeclared feasibility checks: successful GPU loading and two bounded outputs;
record actual tokens, raw output, elapsed time, and process memory where
observable. Use greedy sampling, seed 11, context 4096, disable extended
thinking using supported template configuration. No cross-hardware bitwise
reproducibility claim. One short ordinary prompt and one longer explicitly
synthetic configuration prompt test basic generation and prompt handling.
Synthetic input is a hardware fixture only; its real generated response and
hardware costs are NOT research optimization outcomes. Do not infer superiority
from either answer. Save the precise prompt and command before starting.

Stop all inference processes after completion or timeout. Report cold-load and
generation timing separately where available; OS peak resident memory and GPU
buffers are different measurements and must not be conflated. A future research
comparison requires its own frozen protocol and budget; V46 authorizes none.
