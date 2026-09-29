# V39.2 test-harness expectation correction

The V39.1 ZIP passes clean isolated Python3.10 and3.12 reconstruction with identical scientific outputs. Its checksum negative control is correctly rejected by the frozen-source hash check, which runs before the per-file bundle checksum. The harness incorrectly expected only the later error string and marked validation failed. Preserve those receipts under artifacts/reproduction_v39_1/.

Change only that expected failure message in the test harness. Use the identical V39.1 archive and verifier. No scientific or verification semantics change; no new archive needed. Freeze the corrected harness, rerun the same complete two-interpreter/ten-corruption/restoration/determinism sequence, preserve both failures in the report. No inference, acquisitions or resource increase.
