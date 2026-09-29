# When Is an LLM Worth Calling? Replication package

This is the replication package for the paper *When Is an LLM Worth Calling? Rare, Concentrated Gains from Escalating Classical Configuration Search to Large Language Models* (Mayank Dhingra). The manuscript source is in [`paper/overleaf_v180/`](../paper/overleaf_v180/).

The study asks whether, after ten evaluations of a classical configuration optimizer, calling a large language model to propose the next ten configurations is worth it, and whether a small controller can tell in advance. The package lets you recompute every result table from the saved records, offline. It also contains independent verifiers that replay the saved model responses and charged acquisitions.

## Reproduce the results

Requirements: Python 3.10 (the study used 3.10.13), about 2 GB of disk space, and network access for steps 2 and 3 only.

```sh
git clone https://github.com/mayankdhingra02/when-is-an-llm-worth-calling.git
cd when-is-an-llm-worth-calling
python3.10 -m venv .venv
.venv/bin/python -m pip install -r requirements-bundle-v178.txt     # 2. pinned packages
.venv/bin/python scripts/fetch_third_party_v181.py                  # 3. third-party tables (see below)
.venv/bin/python scripts/reproduce_bundle_v178.py                   # 4. offline reproduction, about 2 minutes
```

Step 4 runs 31 checks, and a host-dependent one if Python 3.13 is available. It then confirms that every file is byte-identical to the sealed package.
- Each command runs under a guard that blocks all network access.
- Byte-identical outputs and exact replays are expected only with Python 3.10 and the pinned packages. Other versions can differ in the last floating-point digits.
- [`BUNDLE_V178_README.md`](../BUNDLE_V178_README.md) explains each check, and what cannot be reproduced from the package and why.
- [`TABLE_MAP_V178.md`](../TABLE_MAP_V178.md) maps every table in the paper to the script, input files and output fields that produce it.

## Third-party data that is fetched, not included

The repositories behind three measurement sources declare no licence (DeepPerf, Tuneful) or a copyleft licence (Performance Evolution, GPL-2.0), so their tables are not redistributed here. Step 3 does three things:
1. It downloads 11 tables (about 11 MB) from the owners' repositories, at the exact commits the study used.
2. It checks each table against the SHA-256 hash recorded when the study ran.
3. It rebuilds 8 small "source extract" files from those tables. These hold the header and the rows the study acquired, and the repository stores only their line numbers.

If any hash differs, nothing is written.

| Source | Used for | In this repository |
|---|---|---|
| DeepPerf / SPLConqueror (BerkeleyDB, DUNE, HIPAcc, LLVM, SaC) | recorded cohort | fetched from `DeepPerf/DeepPerf` |
| Performance Evolution (OpenVPN) | recorded cohort | fetched from `ChristianKaltenecker/PerformanceEvolution_Website` |
| Tuneful (Spark) | recorded cohort | fetched from `ayat-khairy/tuneful-data` |
| Scout (Hadoop) | recorded cohort | included (MIT licence included) |
| EZR 0.9.4 | classical baseline | included (MIT licence included) |
| CPython 3.10.13 source subset | ripgrep search corpus | included (PSF licence included) |

`BUNDLE_V178_README.md` describes the package it was written for as a "private review copy". That notice applied to the full package, which contained the tables above. This public version leaves them out and fetches them instead.

## Licence

- **Code** written for this study is under the MIT licence ([`LICENSE`](../LICENSE)).
- **Data and documentation** produced by this study (saved observations, model responses, logs, results, reports and figures) are under CC BY 4.0 ([`LICENSE-DATA`](../LICENSE-DATA)).
- **Third-party files** keep their own licences. See [`THIRD_PARTY.md`](../THIRD_PARTY.md) and the licence files beside them. The fetched tables stay under their owners' terms.
- **The manuscript** in `paper/` is not licensed for reuse.

If you use this package, please cite the paper.

## Notes

- **Binaries.** Three small binaries are included only so the verifiers can check their recorded hashes; nothing runs them. They are the llama.cpp `llama-server` launcher (MIT), ripgrep 15.2.0 (MIT/Unlicense) and a compiled hnswlib worker. No model weights or API credentials are included.
- **Absolute paths.** Logs and recorded commands contain absolute paths from the machine the study ran on. They are sealed records and have not been rewritten.
- **AI assistance.** The project was carried out with substantial help from AI assistants, as the paper's acknowledgements describe. Some reports in `reports/` refer to them.
- **Integrity.** Integrity manifests for every stage of the study are in `artifacts/*/evidence_manifest.json`.
