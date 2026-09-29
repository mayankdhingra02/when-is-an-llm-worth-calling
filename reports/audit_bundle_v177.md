# V177: manuscript–package consistency, cited earlier experiments, revised repeat plan

This responds to the third external review. No objective acquisition, model request, dataset or model download, paid call or publication was made. The only network use was installing the bundle's pinned Python packages from PyPI into a throwaway test environment.

## Manuscript (`paper/overleaf_v173/main.tex`; V176 version kept at `previous/main_before_package_wording.tex`)

- **What the package contains.** The review had flagged two sentences:
  - "the replication package contains them all" (section *How the study evolved*);
  - "for all experiments" (*Data Availability*).

  Both overstated what the bundle contains, because it omits the raw records of early iterations. They now distinguish:
  - the project archive, which keeps everything;
  - the review package, which holds protocols and freeze records of every iteration, plus the records behind every reported result;
  - the omitted earlier-iteration records, listed with their recorded hashes;
  - the four raw re-validation checks that need runtimes the package lacks.
- **Controller transfer history.** Checking which records back each claim found an inaccuracy. The paper said the Table 10 controllers were transferred to WavPack, FFTW, Hadoop, Memcached and the native systems. In fact:
  - an earlier version frozen at V132 was applied to WavPack and FFTW;
  - a version fitted on seven families (V147) was applied to Hadoop (V148);
  - the Table 10 version was applied to Memcached and the six native systems.

  All of these benefit controllers made no calls, so the result stands, but the paper now attributes each to the right version. Sources: `reports/router_v132.md`, `reports/hadoop_v148.md`, `reports/native_study_v153.md`, `reports/solvers_v159.md`.
- **Table 11 width.** `\tabcolsep` is reduced to 4pt to remove the overfull-box warning the reviewer saw when compiling.

## Evidence for the double-rounding explanation (V176 corrections)

The generated reports print three decimals: `reports/snap2_model_v173.md` shows +0.525%, −2.485% and +0.865%, and `reports/ezr_synthesis_v170.md` shows +0.165%. The draft had rounded these printed values again, to 0.53, −2.49, 0.87 and 0.17. Rounding the full-precision outputs once gives different values:

| Output | Full precision | Correct |
|---|---:|---:|
| `results/v173_analysis/analysis.json`: gpt-oss draw 1 headroom | 0.524978% | 0.52 |
| same file: loop headroom | 0.864623% | 0.86 |
| same file: loop log-ratio | −2.484722% | −2.48 |
| `artifacts/study_v170/synthesis.json`: cvc5 / Qwen3-8B | 0.164599% | 0.16 |

## Package (V177)

The package adds the records of the two earlier experiments the paper cites in its text:

- V131 proposals, V132 controller decisions and V134 attribution (WavPack/FFTW transfer);
- V136 masked-feedback responses, acquisitions and arms.

It also adds their independent verifiers, `verify_router_v132` and `verify_feedback_v136 --compact`, to the offline suite. Both pass without runtimes or weights. The raw native logs of V130–V135 (up to 460 MB per study) stay in the project archive and are listed with hashes.

**Receipt-only checks.** The four checks that need omitted runtimes are now reported as "not rerun by this offline workflow; original-workspace execution receipt included". The reproduction never reports them as passed. The README also states that a listed hash of an omitted file says what the file should contain, but does not verify it.

`BUNDLE_V177_README.md` and `TABLE_MAP_V177.md` replace the V176 versions inside the package.

## Revised repeat plan (`reports/proposal_v177_matched_repeat.md`)

This supersedes the V176 draft, which is kept. It adds:

- **Primary comparison:** only the four new balanced draws; pooling with the three earlier draws is a separate, labelled secondary analysis.
- **Unit of completion:** a case with all four new arms.
- **Early stop:** no primary estimate, and partial cases are listed and kept in the denominators.
- **Retries:** loop retries count toward the cap.
- **In-flight requests:** each request's maximum cost is reserved before sending, so the cap cannot be exceeded, and a request still in flight is recorded as unknown cost, not zero.
- **Budget check:** the run does not start if expected cost exceeds 80% of the cap.

It is still not frozen, not authorized and not run.
