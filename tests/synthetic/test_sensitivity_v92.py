"""Synthetic guard checks; never included in measured research aggregates."""
import importlib.util
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('v92_config', ROOT / 'scripts/validate_sensitivity_v92.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

@pytest.mark.parametrize('key,value', [
    ('new_generation_request_cap', 1081), ('scientific_request_cap', 1081),
    ('compatibility_request_cap', 1), ('max_generation_stage_seconds', 1801),
    ('max_server_rss_bytes', 8589934593), ('max_external_spend_usd', 1),
    ('allow_paid_api', True), ('allow_cloud', True), ('host', 'example.org'),
    ('retries', 1), ('stage_download_cap_bytes', 1),
    ('max_new_recorded_objective_acquisitions', 1), ('context_tokens', 8192),
    ('scientific_case_source', 'heldout.json'), ('cases', 109),
])
def test_resource_or_scientific_scope_expansion_rejected(key, value):
    cfg = json.loads((ROOT / 'configs/study_v92.json').read_text())
    cfg[key] = value
    with pytest.raises(ValueError):
        mod.validate(cfg)

def test_prospective_configuration_is_valid():
    mod.validate(json.loads((ROOT / 'configs/study_v92.json').read_text()))
