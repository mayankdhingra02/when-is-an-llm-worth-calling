"""Synthetic structural tests only; no measured timings or model outputs."""
import json
from pathlib import Path
from collections import Counter
import pytest
from escalation.live_compression_v15 import settings as original
from escalation.live_compression_v17 import settings,schedule,commands,validate_setting
from escalation.offline_live_v17 import candidates


def test_grid_is_strict_superset_with_fixed_denominator_and_unique_features():
    grid=settings()
    assert Counter(r['family'] for r in grid)=={'zstd':96,'lz4':96,'zlib':90}
    assert len({r['config_id'] for r in grid})==282
    assert all(r in grid for r in original())
    planned=schedule()
    assert planned==schedule() and len(planned)==846
    assert [r['trial_id'] for r in planned]==list(range(846))
    for rep in range(3):assert len({r['setting']['config_id'] for r in planned if r['repetition']==rep})==282


def test_manifest_has_only_development_features_and_reference_in_each_grid():
    manifest=json.loads(Path('data/live_manifest_v17.json').read_text())
    for entry in manifest['datasets']:
        assert entry['split']=='development'
        c,ids,reference=candidates(entry)
        assert len(c.x)==len(ids)>20 and 0<=reference<len(ids)
        corrupted=dict(entry,configurations=entry['configurations'][:-1])
        with pytest.raises(ValueError,match='grid'):candidates(corrupted)


def test_new_parameter_extremes_are_explicit_and_invalid_settings_rejected():
    for family in ['zstd','lz4']:
        row=next(r for r in settings() if r['family']==family and r['level']==12)
        assert '-12' in commands(row,'/synthetic/binary')[0]
    with pytest.raises(ValueError):validate_setting(dict(settings()[0],level=99))


def test_budget_configuration_forbids_more_calls_and_preserves_denominator():
    c=json.loads(Path('configs/live_measurement_v17.json').read_text())
    assert c['allow_model_calls'] is False and c['request_cap_unchanged']==128
    assert c['stage_wall_seconds']==80 and c['global_runtime_seconds']==1800
    assert c['intended_physical_trials']==sum(c['settings_per_family'].values())*c['repetitions']==846
