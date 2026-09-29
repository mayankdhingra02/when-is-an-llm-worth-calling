"""Synthetic log parser tests, excluded from real measurements."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('v53', Path(__file__).resolve().parents[2] / 'scripts/run_java_feasibility_v53.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def test_only_complete_validated_run_succeeds():
    text = '===== DaCapo 9.12-MR1 xalan completed warmup 1 in 123 msec =====\n===== DaCapo 9.12-MR1 xalan PASSED in 100 msec ====='
    assert m.parse_status(text)['success_markers']
    assert not m.parse_status(text + '\nException')['success_markers']
    assert not m.parse_status(text + text)['success_markers']
    assert not m.parse_status('Normal completion.')['success_markers']
