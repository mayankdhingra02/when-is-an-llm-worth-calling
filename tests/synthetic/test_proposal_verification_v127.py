"""Synthetic regression for independent baseline tie reconstruction."""
import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from verify_proposal_v127_fixed import independent_batch

@pytest.mark.parametrize('direction',['-','+'])
def test_equal_prediction_ties_follow_candidate_order_not_numeric_id(direction):
 xs=[tuple((i>>k)&1 for k in range(5)) for i in range(32)]
 p={'ids':list(range(10)),'labels':[[1.0] for _ in range(10)],'order':list(reversed(range(32)))}
 assert independent_batch(xs,p,direction)==list(range(31,21,-1))
