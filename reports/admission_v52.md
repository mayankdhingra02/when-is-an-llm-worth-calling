# V52 — new application admission result

Eight unused non-compression families were screened under prospective utility and
provenance rules. **None is currently admitted to the stronger study.** This is
an executed source and feature audit, not a performance experiment, not evidence that
these systems lack optimization opportunity, and not a claim their prior papers
are invalid. We did not read timings to find a task favorable to the hypothesis.

## Concrete findings

**DConvert cannot support this budget under our conservative same-output contract.**
The executable audit projected only configuration features from the pinned MOOT
table. Its 6,764 records contain 1,910 unique configurations. Fixing every option
except thread count gives 960 contracts: 950 have two settings and 10 have one.
The largest task therefore has two settings, below both the 40-setting admission
criterion and the 20-evaluation budget. Output formats, platforms, dimensions and
anti-aliasing cannot simply vary while claiming a fixed conversion job. Owner
documentation supports those option meanings; exact archived release mapping is
still unresolved. This does not rule out a separately defined quality-constrained
image-conversion problem.

**Two JavaGC archives must not be conflated.** The original FSE 2015 feature model
has 35 names, all matching our table after documented case/punctuation/XX-prefix
normalization. A later Distance-Based repository has 39 model names, 24 table-only
and 28 model-only names. More importantly, its setup explicitly describes Java 8,
DaCapo 9.12 xalan, interpreted execution,256 MiB–2 GiB heap, and GC time. The older
paper describes Java 7/DaCapo. The later setup is not a provenance certificate for
the earlier scalar runtime table. Feature-name agreement with the original model
does not establish objective transformations, workload identity or passed checks.

**DeepArch needs accuracy, not just timing.** The pinned owner training code
returns both a validation-accuracy field and inference time and saves training
histories. The local catalogue exposes only `Aws-theano-`. We have not linked
that column to the owner accuracy/history records or verified the positional
accuracy extraction. An empty `eval_model.py` in that revision supplies no extra
validation evidence. Architecture changes cannot be admitted on runtime alone.

## All decisions, including reserved families

| Family | Role before any new timings | Main unresolved issue / decision |
|---|---|---|
| DConvert | Development candidate | Fixed-output contract has at most 2 settings; reject this screen. |
| DeepArch | Development candidate | Missing linked accuracy constraint, workload and timing mapping. |
| ExaStencils | Development candidate | Original workload, numerical validator and runtime/compile target mapping unresolved. |
| FastDownward | Development candidate | Workload/releases known; plan validation, equal plan-cost contract, failure accounting and schema mismatch unresolved. |
| JavaGC | Development candidate | Original model matches; exact old workload/measurement/validation recipe unresolved. |
| MongoDB | Reserved for future evaluation | Fix durability/security semantics; locate request verification and workload. |
| Redis | Reserved for future evaluation | Establish workload, target units/direction and measurement harness. |
| Storm | Reserved for future evaluation | Fix payload/topology/delivery contract; establish target transformations and failures. |

The detailed machine-readable gate decisions are in
`data/admission_evidence_v52.json` and `results/v52_admission/summary.json`.
Reserved means no new objective access in this study. It does **not** certify that
all historical outcomes are untouched; a complete exposure audit remains required.
All variants and seeds must stay with their software family.

## Primary evidence and limits

- [DConvert owner documentation, pinned release](https://github.com/patrickfav/density-converter/blob/220d7d0f2f1a83699572493d821df4d9649f5b55/README.md).
  Tags do not resolve competing release descriptions in secondary catalogues.
- [Original FSE 2015 supplement](https://www.se.cs.uni-saarland.de/projects/splconqueror/esecfse2015.php),
  its JavaGC feature model, and the already archived paper, section 5.2. This
  establishes the earlier source, not per-run correctness.
- [Later JavaGC setup](https://github.com/se-passau/Distance-Based_Data/blob/d0056e12c77283a463051b14618e5db3e325aa1c/SupplementaryWebsite/MeasuredPerformanceValues/JavaGC/test_env.txt).
  GPL 2 repository license saved; do not transfer its experimental setup to 2015.
- [DeepArch training code](https://github.com/pooyanjamshidi/deeparch-xplorer/blob/01846a69b8f42e13147f41c17f7f4797ec3243af/mxplorer/train_model.py).
  MIT source license saved. Neither imported nor executed.
- [FastDownward measurement description](https://github.com/ChristianKaltenecker/PerformanceEvolution_Website/blob/4ee53dad6b81543c444d44282053def0d82d97b3/PerformanceEvolution_Data/FastDownward/README.md).
  Gives workload/releases, five repetitions and dispersion-based reruns; missing
  plan-validation evidence remains missing rather than presumed successful.
- [CM-CASL repository](https://github.com/xdbdilab/CM-CASL/tree/07ab1425e7130ac8862a606c9795799d6425222d).
  Retrieved tree/README contain learning implementations and data, but no
  measurement harness or LICENSE. This is a bounded inspection, not an exhaustive
  claim that no such artifact exists elsewhere.

The existing V5 registry remains immutable. MOOT/VEER headers and prior feature
aliases are evidence of schema, not independently verified objective orientation.
We have **not** established that Redis/Storm signs are wrong; a transformation
could explain the headers. ExaStencils/MongoDB/Storm gaps are limited to inspected
registry and source evidence, not a complete new literature search.

## Execution and reproducibility

Rules were SHA256-frozen before new retrieval; implementation/decision inputs and
source bytes were sealed before audit execution. Source manifests record URLs,
bytes and hashes. Initial GitHub access failed under the network sandbox and was
retried with approval; CM-CASL's nonexistent `master` request returned422, then
the actual default branch `main` was resolved and pinned. No fetched code ran.
Two initial GitHub commit responses include file-patch metadata; only their SHA
fields were projected, no patches inspected. Tree queries and raw source files
were used thereafter. CSV parsing reads records to project declared features;
no target cell is converted, exported, scored or used in any selection.

```sh
.venv/bin/python scripts/audit_admission_v52.py
.venv/bin/python scripts/verify_admission_v52.py
.venv/bin/python -m pytest -q tests
```

The audit is one-shot and refuses to overwrite its result. The independent
verifier reruns feature counts, checks both seals and all evidence paths, and
checks family reservations without reading performance values. Synthetic tests
exercise poisoned targets, missing evidence, failure-closed admission and duplicate
handling; these fixtures are separate from measured evidence. No plot is useful
for an eligibility table; the machine counts and source comparisons are retained.

Costs: zero new objective acquisitions, physical trials, model requests and paid
spending. Downloads have a separate 20 MiB audit cap within the existing persistent
cap. Exact source bytes, audit runtime and test counts are in the execution receipt.
Human/agent research time and electricity are not priced. Classical screening and
LLM comparisons were not run because no candidate met the frozen prerequisites.

## Next experiment, in priority order

1. Build a fresh correctness-checked JavaGC/DaCapo task if the old exact harness
   cannot be recovered: pin JDK/DaCapo versions and one workload, fix heap/CPU and
   validation settings, capture full pass/fail/timeout denominators, and optimize
   end-to-end application time rather than GC time alone. Verify local feasibility
   before collection; use a new prospective protocol and a development-only role.
2. Run fixed-budget random, mixed-domain nearest-neighbor and random-forest
   uncertainty baselines only after correctness and noise checks pass. Keep all
   cases and enforce a predeclared headroom rule before spending LLM calls.
3. Recover utility-valid independent families for router evaluation. One new
   JavaGC task cannot validate a cross-system learned controller or establish
   journal readiness. Preserve reserved families rather than selecting them by
   observed gains.

Follow-up: V53 and V54 subsequently completed the fresh Java task and its classical screen; see [V54](java_screen_v54.md) for the failed opportunity gate and updated next action.
