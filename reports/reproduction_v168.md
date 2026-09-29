# Replaying V166–V168

Read STATUS.md first. Collectors are create-once; do not rerun into existing results directories or delete them to make a command succeed. Historical data, protocol freezes and raw failures are evidence.

## Saved-data reproduction (no model or application execution)

From the project root with the existing project Python environment:

```sh
MPLCONFIGDIR=/tmp/mpl-v168 .venv/bin/python scripts/report_apps_v168.py
.venv/bin/python scripts/verify_apps_v168.py
.venv/bin/python scripts/cost_apps_v168.py
.venv/bin/python scripts/diagnose_apps_v168.py
.venv/bin/python scripts/reproduce_apps_v168.py
.venv/bin/pytest -q tests
.venv/bin/python scripts/seal_research_v168.py --verify-only
```

The reproduction command also regenerates both admission analyses and compares report/data/figure bytes. The verification command reconstructs native correctness, acquired-label-only classical decisions, projection, GP expected improvement, shared-prefix identity, charged validation, real-response provenance and frozen policy decisions. It checks retained inputs and the pinned local runtime. This is internal replay, not a second independently collected experiment.

## Dependencies and inputs

Base packages are pinned in requirements.lock.txt/pyproject.toml. The existing run uses Python3.10.13, NumPy2.2.6 and SciPy1.13.1. Additional owner wheels are pinned by SHA256 in configs/apps_v166.lock.txt. They were installed with no dependency resolution into `.local-runtime/apps-v166`; scripts prepend that target locally. Compatible ARM wheels and existing libomp20.1.3 were used. Runtime hashes and dependency linkage are recorded in artifacts/study_v166/runtime.json and hardware.json. An ARM Mac without libomp needs that external dependency provided explicitly; these scripts do not install or modify a system package manager.

The bounded source downloader is scripts/fetch_apps_v166.py. Its receipt retains exact URLs, sizes and hashes for registry metadata, three wheels, owner licenses/parameter documentation and official UCI Covertype. The exact offline install command and wheel digests are in artifacts/study_v166/install.json. Preparation is scripts/prepare_apps_v166.py. Existing flight CSVs and their independent query-reference contract are dependencies from V88. Source bytes reside in ignored artifacts/sources/v166; installed binaries reside in ignored .local-runtime/apps-v166. They are retained on this machine, not silently bundled into a public repository or remotely uploaded.

## Fresh collection

A fresh run needs a separate versioned output namespace, a new prospective protocol/cap and matching owner artifacts. Reproduce the frozen settings and retain all attempts, including invalid quality and runtime failures. Do not claim byte-identical timing or cross-host model determinism. V166 failed on a real null marker; V167 is the separately frozen schema repair. Repeating the repaired experiment does not erase those20 original failed attempts.

The V168 driver executes saved prefixes, classical search, the classical gate, real model calls, model search and fresh validation in that order. Models use existing pinned SmolLM3-3B/Qwen3-8B Q4_K_M and llama.cpp b11146, offline loopback only. Runtime caps enforce20 requests,800 outcomes,1600 query/training executions,1800 seconds,8GiB model-server RSS and zero paid/cloud use. No dashboard, service deployment or background automation is required.

The post-hoc break-even supplement is explicitly separate from the prospective primary analysis. Its first attempt to freeze before responses was rejected by its own guard because model responses already existed. It was relabeled exploratory; no collection/policy was changed.
