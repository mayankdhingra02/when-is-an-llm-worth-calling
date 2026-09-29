"""Synthetic helpers only; never included as experimental cases."""
import importlib.util
from pathlib import Path
import pytest
p=Path(__file__).resolve().parents[2]/'scripts/verify_reproduction_v35.py'
spec=importlib.util.spec_from_file_location('v35',p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

def test_acquired_size_controls_choice_and_cap_equality():
    x=[(0,),(1,),(2,),(3,),(0,),(3,)]
    assert v.choose_joint(x,[4,5],[0,1,2,3],[[1,20],[5,10],[5,10],[6,1]],10)==5

def test_runtime_uses_acquired_runtime_only_and_stable_order():
    x=[(i,) for i in range(6)]
    assert v.choose_runtime(x,[5,4],[0,1,2],[[1,99],[2,99],[3,99]],[4,5])==5

def test_terminal_keeps_feasible_incumbent_and_counts_infeasible():
    ids=list(range(20));y=[[10,5]]*10+[[1,6]]*10
    result=v.selected_metrics(ids,y,5)
    assert result['best_row']==0 and result['best_runtime']==10
    assert result['infeasible_new_acquisitions']==10 and result['runtime_only_best_violates_cap']

@pytest.mark.parametrize('ids',[list(range(19)),list(range(19))+[0]])
def test_terminal_rejects_non_twenty_unique_budget(ids):
    with pytest.raises(ValueError,match='Twenty unique'):v.selected_metrics(ids,[[1,1]]*len(ids),1)

def test_terminal_rejects_no_feasible_acquired_incumbent():
    with pytest.raises(ValueError,match='Feasible incumbent'):v.selected_metrics(list(range(20)),[[1,2]]*20,1)
