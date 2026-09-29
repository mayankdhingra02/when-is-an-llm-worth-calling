# V94 admission audit

Prior registry families were exposed or had unresolved workload/correctness
contracts; see V41/V52/V73 admission audits. This stage adds two numerical
engines rather than counting another workload as a new software family.
The structured-record exposure scan and its exact scope are saved in
`artifacts/study_v94/exposure_audit.json`; this is a repository audit, not proof
that the foundation model never saw these public benchmarks during training.

- SuperLU: installed SciPy 1.13.1; [version-tagged bundled README](https://github.com/scipy/scipy/blob/v1.13.1/scipy/sparse/linalg/_dsolve/SuperLU/README)
  and header identify 6.0.1. [SciPy wrapper](https://github.com/scipy/scipy/blob/v1.13.1/scipy/sparse/linalg/_dsolve/_superluobject.c)
  forwards panel size and relax to gstrf. The downloaded dgstrf source documents
  these parameters; the Python wrapper documents permutation and pivot choices.
  SciPy BSD licensing and SuperLU's BSD notice apply; source files are retained
  for provenance, no native source was compiled or installed system-wide.
- [HB/orsreg_1](https://sparse.tamu.edu/HB/orsreg_1): owner metadata identifies
  a 1984 R. Grimes oil-reservoir problem, full numerical rank, moderate condition.
  Official Matrix Market archive retained with hash. Matrix-specific redistribution
  terms were not located; use is local research, no public redistribution is
  authorized by this audit. The matrix author is not a coauthor of this study.
  Boeing/bcsstk38 was considered from metadata but not selected because its
  published numerical rank/conditioning is unsuitable for this forward-error
  contract. No benchmark timing was used to make this choice.
- [HiGHS v1.7.2](https://github.com/ERGO-Code/HiGHS/tree/v1.7.2): MIT engine;
  [version-pinned options](https://github.com/ERGO-Code/HiGHS/blob/v1.7.2/src/lp_data/HighsOptions.h)
  inspected. PyPI highspy 1.7.2 macOS arm64 CPython 3.10 wheel SHA checked
  against registry metadata; installed only into `.venv`, with no dependency
  resolution. Installed API returns version 1.7.2. Actual option round-trips
  passed before any solve. Wheel, MIT text, registry metadata and source are
  retained locally. The existing SciPy HiGHS wrapper was inspected but is NOT
  the HiGHS engine used here; its bundled version must not be conflated.
- [25fv47.mps](https://github.com/ERGO-Code/HiGHS/blob/v1.7.2/check/instances/25fv47.mps):
  real public continuous LP distributed in owner tests. Native metadata read
  confirmed 821 constraints, 1,571 variables, minimization, no integer columns.
  No solver run or objective score was acquired during admission. Historical
  Netlib instance authorship/standalone dataset licensing remain less clear than
  engine licensing; no claim that engine MIT settles all upstream data rights.

Every retrieved response is recorded with URL, redirect target, byte count,
SHA256 and UTC time in `artifacts/sources/v94/fetch.jsonl`. Public retrievals
used normal HTTPS; no credentials, accounts, installers from webpages, or
paid services. Native runtime and model files are pinned separately.
