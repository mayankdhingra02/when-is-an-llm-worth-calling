"""Synthetic integrity/guard tests. No timing results enter research aggregates."""
import json,os,sys
import pytest
from escalation.live_compression_v15 import settings,schedule,commands,exact_roundtrip,isolated_trial,validate_setting


def test_real_parameter_grid_and_fixed_order_have_complete_denominator():
    grid=settings();assert len(grid)==96 and len({r['config_id'] for r in grid})==96
    assert all(sum(r['family']==f for r in grid)==32 for f in ('zlib','zstd','lz4'))
    trials=schedule();assert len(trials)==288 and trials==schedule()
    assert sorted(t['trial_id'] for t in trials)==list(range(288))
    for rep in range(3):assert {t['setting']['config_id'] for t in trials if t['repetition']==rep}=={r['config_id'] for r in grid}


def test_wrong_roundtrip_never_reports_success():
    with pytest.raises(ValueError,match='differ'):exact_roundtrip(b'abc',b'abd')


def test_unknown_setting_and_shell_text_cannot_enter_commands():
    setting=dict(settings()[0],level='9; echo not-allowed')
    with pytest.raises(ValueError):validate_setting(setting)
    with pytest.raises(ValueError):commands(setting,'/binary')


def test_cli_threads_and_checks_are_explicit():
    zs=next(r for r in settings() if r['family']=='zstd' and not r['checksum'])
    lz=next(r for r in settings() if r['family']=='lz4' and r['dependent'])
    assert '--single-thread' in commands(zs,'/binary')[0]
    assert '--no-check' in commands(zs,'/binary')[0]
    assert '-T1' in commands(lz,'/binary')[0] and '-BD' in commands(lz,'/binary')[0]


def test_timeout_kills_child_group_and_reaps_parent(tmp_path):
    # All dummy/sleep activity is synthetic, not a measured compressor trial.
    result=isolated_trial([sys.executable,'-c','import subprocess,time; subprocess.Popen(["/bin/sleep","5"]); time.sleep(5)'],b'',.15,str(tmp_path),{'PATH':'/usr/bin:/bin'})
    assert result['timed_out'] and result['returncode']!=0
