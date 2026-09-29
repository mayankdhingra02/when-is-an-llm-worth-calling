# V41 local results review kit

Start with reports/models_v41.md. Run:

    python3 -I -S scripts/verify_review_bundle_v41.py

This uses only the Python standard library, verifies every bundled evidence hash, and independently replays420exact comparisons and108policy means from acquired records. It makes no model call or new objective acquisition.

This is a results-replay subset of the local repository, not the full inference environment. Full source tables, model weights and third-party papers are deliberately omitted. Manifest URLs/hashes and model identities preserve provenance. Reproducing fresh inference and source-row authenticity checks needs those original inputs and the full project. Bundled source-check receipts document what ran locally; they do not make omitted source files independently verifiable inside this kit.

All60model cases are retained, including original infrastructure-failure logs and recovery metadata. Synthetic fixtures are not research outputs. No new-model generalization, application-utility validation, or journal acceptance is established. This local artifact has not been uploaded or published. Review dataset licensing before external redistribution.
