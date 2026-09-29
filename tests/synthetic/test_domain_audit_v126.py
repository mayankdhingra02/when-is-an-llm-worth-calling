"""Synthetic feasibility tests; no measured objectives or model outputs."""
import sys
from pathlib import Path
from fractions import Fraction
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from domain_audit_v126 import plan,optimum,exact_gain

def test_coverage_uses_ids_only_and_respects_budget():
    class Poison:
        def __iter__(self):raise AssertionError('Labels must not be inspected')
    p={'ids':list(range(0,20,2)),'order':list(range(37)),'labels':Poison()}
    chunks=plan(p);flat=[i for c in chunks for i in c]
    assert flat==[i for i in range(37) if i not in p['ids']]
    assert len(flat)==len(set(flat))==27
    assert [len(c) for c in chunks]==[10,10,7]
    assert all(len(p['ids'])+len(c)<=20 for c in chunks)

@pytest.mark.parametrize('ids,order',[(list(range(9)),list(range(30))),([0]*10,list(range(30))),(list(range(10)),list(range(30))+[0]),(list(range(10)),list(range(1,30)))])
def test_bad_prefix_rejected(ids,order):
    with pytest.raises(ValueError):plan({'ids':ids,'order':order})

@pytest.mark.parametrize('direction,values,expected',[('-', [100,95,105],95),('+',[100,95,105],105)])
def test_direction_and_exact_five_percent_boundary(direction,values,expected):
    assert optimum(values,direction)==expected
    assert exact_gain(100,expected,direction)==Fraction('0.05')
    assert exact_gain(100,100,direction)==0
    assert exact_gain(100,105 if direction=='-' else 95,direction)<0

@pytest.mark.parametrize('direction,ref,value',[('?',1,2),('-',0,1),('+',1,0)])
def test_invalid_objective_contract(direction,ref,value):
    with pytest.raises(ValueError):exact_gain(ref,value,direction)
