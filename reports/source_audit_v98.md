# V98 primary-source check

Niklas Muennighoff, Zitong Yang, Weijia Shi, Xiang Lisa Li, Li Fei-Fei,
Hannaneh Hajishirzi, Luke Zettlemoyer, Percy Liang, Emmanuel Candès and Tatsunori
Hashimoto: [s1: Simple test-time scaling](https://arxiv.org/abs/2501.19393v3),
arXiv2501.19393v3,1March2025. The abstract describes shortening or extending
reasoning with budget forcing. The [author repository](https://github.com/simplescaling/s1)
shows separate thinking and final-answer generation and a reserved answer
allowance. These primary pages were opened in this session. This establishes
the method as prior work, not an expected improvement on software configuration.
No s1 code, trained model or dataset is copied or executed here.

The pinned [llama.cpp b11146 server documentation](https://raw.githubusercontent.com/ggml-org/llama.cpp/b11146/tools/server/README.md)
was opened and inspected: `/apply-template` produces a prompt that may be
modified before `/completion`; stop strings terminate completion and are
excluded from returned content; `stop_type` distinguishes EOS, limit and word;
`truncated` indicates context overflow; returned usage/settings are available
for audit. V98 uses these documented native primitives rather than assuming
an unverified per-request reasoning-budget option applies to this endpoint.

Qwen's version-pinned owner README, already saved in
`artifacts/sources/v91/README.md`, remains the sampling/model provenance source.
V98 follows its mode-specific temperature/top-p settings but uses much shorter
output allowances and an explicit two-request intervention. It is an adaptation,
not unrestricted owner-recommended reasoning or an exact s1 replication.

No new source/model/package payload was downloaded into the repository; browsing
was read-only verification. No installation, account setup, credentials or
external spending. All implementation is project-authored; existing third-party
model/runtime licenses and dataset provenance still apply.
