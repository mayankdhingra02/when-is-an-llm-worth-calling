"""Read-only checks over V46 traces; these never issue model requests."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_existing_run_cannot_consume_more_requests():
    summary = ROOT/'artifacts/study_v46/feasibility/summary.json'
    before = summary.read_bytes()
    result = subprocess.run([sys.executable, str(ROOT/'scripts/run_smollm_feasibility_v46.py')],
        capture_output=True, text=True, timeout=10)
    assert result.returncode != 0
    assert 'Preserve previous run; no implicit retry' in result.stderr
    assert summary.read_bytes() == before

def test_measurements_match_raw_traces():
    result = subprocess.run([sys.executable, str(ROOT/'scripts/verify_smollm_feasibility_v46.py')],
        capture_output=True, text=True, timeout=10)
    assert result.returncode == 0, result.stderr
    measured = json.loads(result.stdout)
    assert measured['verified'] and len(measured['measurements']) == 2
    assert measured['research_outcomes'] == 0
    assert all(x['input_tokens'] is None and x['output_tokens'] is None for x in measured['measurements'])
