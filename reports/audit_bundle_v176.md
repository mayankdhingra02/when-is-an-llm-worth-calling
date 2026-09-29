# V176: wording fixes, table checker, reviewer audit bundle and draft repeat plan

No objective acquisition, model request, dataset or model download, paid call or remote publication. The only network use was installing the bundle's pinned Python packages from PyPI into a throwaway test environment.

## Manuscript

**Three wording corrections from the external review:**

- The introduction now says the 3B and 8B models "never achieved a baseline-set win, that is, never beat every prespecified classical baseline by more than 1%".
- The DUNE statement is limited to mean losses: "each [continuation] in Table 4 has a mean loss of more than 11%". The earlier "nothing comes within 10%" was false at the case level; the adaptive neighbour rule gains +2.7% on one DUNE case.
- The useful-case counts are stated: random search 11, SmolLM3-3B 10, Qwen3-8B 5.

**A table checker, and four double-rounding errors it found.** `scripts/check_tables_v176.py` recomputes or looks up every row of the 11 numeric result tables (80 rows) and 12 headline numbers in the text. It then requires each to appear verbatim in `main.tex`. Its first run found four values that had been rounded twice. All are corrected in the tables and in the text that quotes them:

| Value | Exact | Was | Now |
|---|---:|---:|---:|
| gpt-oss-120b draw 1 hindsight headroom (Tables 3, 11) | 0.52498% | 0.53% | 0.52% |
| gpt-oss-120b loop hindsight headroom (Tables 3, 11; text) | 0.86462% | 0.87% | 0.86% |
| gpt-oss-120b loop log-ratio (Table 3) | −2.48472% | −2.49% | −2.48% |
| Native cvc5, Qwen3-8B (Table 6) | +0.16460% | +0.17% | +0.16% |

The checker now reports 0 mismatches. The V175 manuscript is kept at `paper/overleaf_v173/previous/main_before_audit_wording.tex`.

## Reviewer audit bundle

`output/llm_escalation_audit_v176.zip`. Its hash, size and counts are in `artifacts/study_v176/bundle_receipt.json`, outside the bundle. The README for reviewers is `BUNDLE_V176_README.md`; the table-to-source map is `TABLE_MAP_V176.md`.

### How the contents were chosen

1. **Traced inputs.** `scripts/trace_inputs_v176.py` runs the bundle's whole command suite in an APFS copy-on-write clone of the project. The clone leaves out model weights, runtimes and native build trees. A file-access tracer records every file each process opens, globs or lists, the subprocesses it starts, and any network event. All 30 commands passed in the clone, with 0 network events. The result is `artifacts/study_v176/traced_inputs.json`.
2. **Added material.** The bundle adds everything Codex listed:
   - all project code, configs, reports and manuscript versions;
   - every evidence manifest, freeze record and `previous_snapshot`, plus every earlier-version copy the V175 seal redirects to (old STATUS and README copies);
   - small artifact files of the studies behind the paper;
   - the complete raw model responses and acquisition logs of V141–V175;
   - the complete native measurement records (V153, V159, V163–V165, V168–V170).
3. **Exclusions.** Model weights, credentials, runtimes and native build trees, earlier bundles, caches, and the agent workflow notes (`AGENTS.md`, `CLAUDE_HANDOFF.md`, `START_HERE.md`) are left out. Four runtime files are the exception. The verifiers hash them against recorded pins, and no bundle command executes them:
   - the llama.cpp `llama-server` launcher (50 KB, MIT);
   - the ripgrep 15.2.0 binary (MIT/Unlicense);
   - the project-compiled `hnsw_worker_v161`;
   - a CPython 3.10.13 source subset used as the search corpus (PSF).

   Their licences are included beside them.
4. **Credential scan.** The build aborts on any credential-like pattern. The only hit was the PEM placeholder in CPython's `ssl.rst` documentation. It is allowed by path, pattern and exact file hash. Your e-mail address appears in no bundled file. Absolute paths containing the local username do appear, in 5,832 files (logs, recorded commands). They are sealed records and were not rewritten.

### Integrity

`scripts/verify_bundle_v176.py`:

- confirms every bundled file against `BUNDLE_MANIFEST_V176.json`;
- confirms that the V175 manifest and the 74 earlier manifests it names by hash are present unmodified: 86 manifests, a chain of 75 checkpoints;
- classifies every file those manifests seal.

Of the sealed file entries:

- 12,721 are present with the sealed hash;
- 63,305 are absent, each listed with its sealed hash in `EXCLUDED_FROM_BUNDLE_V176.tsv`:

  | Category | Entries |
  |---|---:|
  | Earlier or unrelated iterations | 51,723 |
  | Earlier packaged bundles | 8,835 |
  | Third-party runtimes and native builds | 1,518 |
  | Third-party source archives | 1,140 |
  | Other files not needed for the paper | 72 |
  | Model weights | 12 |
  | Workflow notes | 5 |

- 0 are integrity failures.

On the full workspace, where every sealed file exists, the same check verified all 76,025 entries. The only exception was that day's edited `main.tex`, whose sealed version is kept as a snapshot.

### Reproduction from the unpacked ZIP

The ZIP was unzipped into a scratch folder. A new Python 3.10.13 environment was created from `requirements-bundle-v176.txt` alone, and `scripts/reproduce_bundle_v176.py` was run there. The network guard was active, so no connection was possible.

- **Checks:** all 29 core commands passed, as did the host-dependent EZR bridge tests (7) and the bundle verifier.
- **Tests:** pytest passed 140, with 1 location-dependent case deselected.
- **Files:** every file listed in `BUNDLE_MANIFEST_V176.json` was byte-identical after the run, including every regenerated report, JSON output and figure.
- **Time:** under two minutes.
- **Records:** result, log and environment are in `artifacts/study_v176/bundle_reproduction_*`.

### What the bundle cannot reproduce

- **LLM generation.** Responses are replayed from saved raw outputs.
- **Native timings.** They depend on the machine.
- **Four verifiers that need runtimes or binaries not included.** They passed in the workspace, and their receipts are bundled.
  - `verify_native_study_v153`: memcached and libevent binaries.
  - `verify_apps_v168`, `verify_ezr_v169` and `verify_ezr_v170`: the 125 MB Polars/XGBoost native runtime, plus the Covertype and flights data.
- **`seal_research_v175 --verify-only`.** It needs every file ever sealed, including model weights.
- **One pytest case.** It compares an absolute path. The equivalent comparison runs relocated inside `verify_v172_relocated_v176.py`, which recovers the original root from the recorded commands.
- **The compiled PDF.** No LaTeX toolchain is available locally.

### Licensing: private review copy

The bundle redistributes the raw tables the checks need. `THIRD_PARTY.md` records unresolved redistribution rights for the DeepPerf tables (no licence found) and the Tuneful Spark tables (the project had committed to no public redistribution). The bundle is therefore a private review copy, like the earlier V113 packet: share it privately with reviewers, and do not post it publicly. A public release would need those rights resolved, or would need to replace the tables with fetch-by-hash instructions.

## Draft repeat plan

`reports/proposal_v176_matched_repeat.md`: a full-cohort matched repeat, with 2 new one-shot and 2 new loop draws of gpt-oss-120b, interleaved, on the same 70 prefixes. It fixes:

- the estimand;
- a descriptive decision rule, which allows "no reliable difference";
- a stopping rule with no outcome-based stops;
- a cost of about $2.27 expected, with a $3.00 hard cap.

It is a draft: not frozen, not authorized, not executed. The cap was not raised.
