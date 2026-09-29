import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from audit_cost_proposal_v128 import usage
def test_unreturned_and_missing_usage_are_unknown():
    assert usage(3,[{'tokens':4},{}],'tokens')=={'observed_sum':4,'missing_responses':2}
    assert usage(1,[],'tokens')=={'observed_sum':0,'missing_responses':1}
    assert usage(0,[],'tokens')=={'observed_sum':0,'missing_responses':0}
def test_usage_is_not_invented_from_bad_receipts():
    for value in [-1,True,'2',1.5]:
        with pytest.raises(ValueError):usage(1,[{'tokens':value}],'tokens')
    with pytest.raises(ValueError):usage(0,[{'tokens':2}],'tokens')
