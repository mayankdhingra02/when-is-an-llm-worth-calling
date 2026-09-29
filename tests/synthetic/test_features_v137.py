"""Synthetic only: poisoned objective cells must not influence admission."""
import importlib.util
from pathlib import Path
import pytest
p=Path(__file__).resolve().parents[2]/'scripts/audit_features_v137.py'
s=importlib.util.spec_from_file_location('audit_v137',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def test_targets_never_parsed_or_reported():
 h=','.join(m.FEATURES['nodejs']+m.TARGETS['nodejs'])+'\n';features='0,1,0,1,0,1,'
 a=m.audit(h+features+'SECRET_POISON_TARGET\n','nodejs');b=m.audit(h+features+'NaN\n','nodejs')
 assert a==b and 'SECRET_POISON_TARGET' not in str(a) and a['objective_values_parsed']==0
def test_schema_and_missing_features_fail_closed():
 with pytest.raises(ValueError):m.audit('unapproved,ops\n0,SECRET\n','nodejs')
 h=','.join(m.FEATURES['nodejs']+m.TARGETS['nodejs'])+'\n'
 with pytest.raises(ValueError):m.audit(h+'0,0,0,0,,0,SECRET\n','nodejs')
def test_configuration_id_is_not_a_feature():
 h=','.join(['configurationID']+m.FEATURES['xz']+m.TARGETS['xz'])+'\n'
 r=m.audit(h+'a,50%,xz,3,1,POISON,POISON\nb,50%,xz,3,1,OTHER,OTHER\n','xz')
 assert r['unique_configurations']==1 and r['duplicate_feature_rows']==1 and not r['raw_coverage_pass']
