> **Schema correction:** the original SQLite run dropped a real INDEX option. Earlier full-schema counts/claims are superseded; see [schema_erratum.md](schema_erratum.md). Original measured logs are preserved. Use the corrected v3 report for current conclusions.

# Source audit — 2026-09-24

The supplied reading/deep-research.md was read once as discovery material. Its SHA-256 is recorded in artifacts/source_manifest.json. It is not evidence of replication or novelty. Primary pages were checked directly; repository files were fetched from pinned owner URLs. Status below separates reading, inspection, and execution.

| Source | Verified version/authors | Evidence used / status |
|---|---|---|
| [Better Together, in the Right Order: Classical-then-LLM Optimization for SE](https://arxiv.org/html/2607.02583v1) | Srinath Srinivasan, Tim Menzies; v1, 2026-07-01 | Methods §§III–IV and limitations/future work §VI read. Algorithms 1–2, centroid acquisition, 10/20 handoff, two proposals/call, d2h/Delta and conditional escalation checked. Paper reports gpt-oss-120b/OpenRouter; this pilot does not replicate that model. |
| [Can AI be Easy? Lessons Learned from the EZR.py Toolkit](https://arxiv.org/html/2606.03640v2) | Tim Menzies, Srinath Srinivasan, Kishan Ganguly; v2, 2026-09-14 | Active-learning code and Appendix A inspected. The paper identifies v0.9.4 and [Zenodo DOI](https://doi.org/10.5281/zenodo.22554751); archive itself not retrieved. |
| [MOOT: a Repository of Many Multi-Objective Optimization Tasks](https://arxiv.org/html/2511.16882v2) | Tim Menzies, Tao Chen, Yulong Ye, Kishan Kumar Ganguly, Amirali Rayegan, Srinath Srinivasan, Andre Lustosa; v2, 2026-02-06 | Paper task catalogue, repo README, config README, license and selected CSV schemas inspected. Repository CITATION.cff lists six authors; paper lists seven. Cite the paper's authors for the paper. |

## Artifact mapping and caveats

[EZR](https://github.com/timm/ezr/tree/bfda80b3b797d142378f7fb8746c3485610fb17e), commit bfda80b3b797d142378f7fb8746c3485610fb17e, declares version 0.9.4, Python >=3.12, MIT copyright 2026 Tim Menzies. Source downloaded and inspected; not executed. `norm` uses clipped logistic z-scores, `acquire` consumes a warm start plus a loop budget, and structures contain objective columns. Passing complete tables through that API would not create an enforced hidden-label boundary. This pilot independently implements the centroid procedure with feature-only candidates, a charged oracle, acquired-only min/max scaling and an inclusive budget. It is `ezr_centroid_adapted`, not a validated upstream numerical reproduction.

[MOOT](https://github.com/timm/moot/tree/90803be51b00f881305db45aa0cf6a3b5340804f), commit 90803be51b00f881305db45aa0cf6a3b5340804f (2026-08-10), carries an MIT repository license. Only three selected CSVs downloaded, from optimize/config. They are named Apache, SQL and X264 in upstream documentation; SQLite-specific option names establish the SQL family mapping. Row-level original collection versions, machine details and workload units are not supplied in these CSVs. Treat Performance- as an upstream minimization target, not a newly measured latency unit. All original data are kept outside shareable Git history by default despite the repository-level license, and per-file attribution/manifests remain available.

No exact SNAP2 repository or released cache was located in the paper's artifact statements, [author's page](https://timm.fyi/snap2.html), or targeted web searches on 2026-09-24. This is a bounded unsuccessful search, not proof that no artifact exists. No unrelated repository was substituted. The prompt, parser and fallback behavior here are original adaptations. Primary pseudocode has a sorting-direction inconsistency relative to its textual prompt; lower loss is used consistently here. The paper's common-completion subset can exclude timeout-prone tasks; this pilot retains all intended runs, including failures.

## Closest conceptual leads checked

| Primary source | What was verified; status |
|---|---|
| [Which Optimizer, At What Budget? A Tournament of Optimizers for Search-Based SE](https://arxiv.org/abs/2607.11705v1) — Kishan Kumar Ganguly, Tim Menzies, 2026-07-13 | Metadata/abstract verified: budget and task attributes motivate the small feature set. No tournament rerun; no direct router guarantee inferred. |
| [Is Model Instability just Noise to be Tolerated or a Property that can be Managed?](https://arxiv.org/abs/2607.10420v1) — Amirali Rayegan, Lunxiao Li, Tim Menzies, 2026-07-11 | Metadata/abstract verified; supports measuring instability, not assuming it predicts LLM benefit. No code reused. |
| [Consistent Estimators for Learning to Defer to an Expert](https://arxiv.org/abs/2006.01862v3) — Hussein Mozannar, David Sontag, ICML 2020; v3 2021-01-25 | Metadata/abstract verified. Deferral depends on relative competence. Our ridge model is not their consistent estimator. |
| [RouteLLM: Learning to Route LLMs with Preference Data](https://arxiv.org/abs/2406.18665v4) — Isaac Ong, Amjad Almahairi, Vincent Wu, Wei-Lin Chiang, Tianhao Wu, Joseph E. Gonzalez, M Waleed Kadous, Ion Stoica; v4 2025-02-23 | Metadata/abstract verified. Strong/weak model routing is prior art; no code reused. |
| [SCOPE: Cost-Efficient Model Selection for Compound AI Systems under Quality Constraints](https://arxiv.org/abs/2606.00774v2) — Yiqian Huang, Shiqi Zhang, Tianyuan Jin, Xiaokui Xiao; v2 2026-06-13 | Metadata/abstract verified: constrained quality/cost selection. Its formal guarantees are not claimed for this pilot. |

The audit is not an exhaustive novelty review. Other starter-report entries remain leads; their quantitative claims are not adopted. Searches for direct SNAP2 benefit-escalation follow-ups returned the original paper/author page and unrelated uses of “SNAP2,” not a verified direct successor. Conditional escalation itself is already explicit prior work.

## Local model and environment

[Qwen/Qwen2.5-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/tree/7ae557604adf67be50417f59c2c2f167def9a775), official owner, revision 7ae557604adf67be50417f59c2c2f167def9a775. Model card and Apache-2.0 license inspected. Downloaded safetensors plus tokenizer/config; no remote code, login, credential access or new service terms. File hashes and exact bytes are in artifacts/model_manifest.json. This very small model was chosen for bounded local feasibility, not to represent all LLMs.

Apple M3 Pro, 11 CPU cores, 14 GPU cores, 18 GB unified RAM, ~32 GiB initially free. Python 3.10.13 project venv. No Ollama/llama-server executable or responding localhost model endpoint found at standard Ollama/LM Studio ports; no personal model directories searched. MPS appears unavailable inside the restricted shell but available under authorized local GPU execution. No paid endpoint is implemented.

First model initialization failed before requests: SciPy 1.15.3 PROPACK binary was rejected by this macOS loader. [Upstream issue 25635](https://github.com/scipy/scipy/issues/25635) describes this failure. Pinned SciPy 1.13.1 passed actual SciPy/sklearn/transformers import checks. Failure log retained; cumulative experiment time includes failed startup. This dependency correction preceded model output and changed no scientific settings.
