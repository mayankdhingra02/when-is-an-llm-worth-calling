import importlib.util,json
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('gate_v91',ROOT/'scripts/check_resources_v91.py');gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
def proposal():return json.loads((ROOT/'configs/resource_proposal_v91.json').read_text())
@pytest.mark.parametrize('approval',[None,{}, {'explicit_resource_change_approved':True,'proposal_sha256':'wrong','user_message':'synthetic','at_utc':'fixture'}])
def test_missing_or_mismatched_permission(approval):
    with pytest.raises(PermissionError):gate.validate(proposal(),approval,'expected')
def test_exact_synthetic_approval():
    assert gate.validate(proposal(),{'explicit_resource_change_approved':True,'proposal_sha256':'expected','user_message':'synthetic fixture only','at_utc':'fixture'},'expected')
def test_paid_disabled():
    p=proposal();p['allow_paid_api']=True
    with pytest.raises(AssertionError):gate.validate(p,None,'expected')
