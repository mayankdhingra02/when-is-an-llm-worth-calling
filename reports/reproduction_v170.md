# Reproduce V169–V170 without new collection

Use the project root and retained, hash-pinned artifacts. The main environment is `.venv` (Python 3.10.13 with the existing locked dependencies). Literal upstream EZR replay additionally uses the existing Python 3.13.3 interpreter recorded in `artifacts/study_v169/runtime.json`; its source syntax is incompatible with Python 3.10. No global installation was performed. Native source/input/binary pins are inherited from the V159, V163 and V168 freezes. Replay requires retained raw outputs and source/input data, not model servers or fresh inference.

```sh
MPLCONFIGDIR=/tmp/mpl-v169 .venv/bin/python scripts/reproduce_ezr_v169.py
MPLCONFIGDIR=/tmp/mpl-v170 .venv/bin/python scripts/reproduce_ezr_v170.py
.venv/bin/pytest -q tests
.venv/bin/python scripts/seal_research_v170.py --verify-only
```

The first two commands regenerate reports, figures, source-choice replay and synthesis, then compare their bytes with the existing artifacts. They acquire no new objective labels or model outputs. Source replay executes the same upstream implementation; separate objective checks validate retained native outputs. V170 also verifies solver assignments and independently calculated text/ANN references. Reproduction is deterministic analysis of saved evidence, not fresh runtime replication.

Collection is create-once: do not rerun `collect_ezr_v169.py`, `collect_ezr_v170.py`, preparation or adapter-generation scripts into completed directories. Fresh measurements require a new protocol, manifest, output namespace and bounded counters. A different host requires explicit runtime pinning and a prospective replication protocol; do not change historical hashes to make it pass.

Reports: `reports/ezr_v169.md`, `reports/ezr_v170.md`, `reports/ezr_synthesis_v170.md`. Raw searches, acquisition receipts, fixed selections, randomized validation plans and outputs are under `results/v169_ezr` and `results/v170_ezr`. `artifacts/study_v170/evidence_manifest.json` seals both extensions and verifies prior history with root-file snapshot redirects. Exact manifest hash is in `seal_verification.json`, excluded from the manifest to avoid a self-reference.
