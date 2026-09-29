"""Exact feasibility checks on synthetic values; no measured observations."""
import sys
from pathlib import Path
from fractions import Fraction
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from audit_attainability_v125 import gain,attainable

def test_exact_boundary_and_one_blocking_control():
 assert attainable('95',{'a':'100','b':'100'},'0.05')
 assert not attainable('95.00000001',{'a':'100'},'0.05')
 assert not attainable('95',{'a':'100','b':'95'},'0.05')

def test_direction_and_negative_ceiling():
 assert gain('100','110')==Fraction('-0.1')
 assert gain('100','110','+')==Fraction('0.1')

@pytest.mark.parametrize('ref,target,direction',[('0','1','-'),('1','0','-'),('1','1','unknown')])
def test_invalid_contract(ref,target,direction):
 with pytest.raises(ValueError):gain(ref,target,direction)
