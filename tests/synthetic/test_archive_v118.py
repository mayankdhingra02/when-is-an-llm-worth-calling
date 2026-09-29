"""Synthetic feature-only archive fixtures, excluded from measured results."""
import io,sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from audit_archive_v118 import feature_census,signature,safe_member


def test_poisoned_objectives_not_interpreted():
    a=feature_census(io.StringIO('a,b,throughput,latency\n1,2,POISON,SECRET\n3,4,x,y\n'))
    b=feature_census(io.StringIO('a,b,throughput,latency\n1,2,-100,999\n3,4,999,-100\n'))
    assert a==b


def test_feature_signature_ignores_row_column_order_and_duplicates():
    assert signature(['A','buffer-size'],[(1.,2.),(3.,4.)])==signature(['Buffer_size','a'],[(4.,3.),(2.,1.),(2.,1.)])


def test_archive_members_must_be_relative():
    with pytest.raises(ValueError):safe_member('bo4co_dataset/../../a.csv')
    with pytest.raises(ValueError):safe_member('/bo4co_dataset/a.csv')
    assert not safe_member('__MACOSX/bo4co_dataset/._a.csv')


def test_nonfinite_features_fail_closed():
    with pytest.raises(ValueError):feature_census(io.StringIO('a,throughput,latency\ninf,x,y\n'))
