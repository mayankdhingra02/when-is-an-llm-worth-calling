"""Version-stable reduction regression; synthetic arithmetic, no measured result."""
import importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[2]/'scripts/verify_reproduction_v35_1.py'
spec=importlib.util.spec_from_file_location('v35_1',p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

def test_reduction_order_is_explicit_and_not_builtin_sum():
    assert v.left_fold([float(2**53),1.,1.])==float(2**53)
    assert v.left_fold([1.,1.,float(2**53)])==float(2**53)+2

def test_two_mathematically_equal_predictions_retain_frozen_binary64_order():
    x=[(0,0),(0,1),(1,1),(0,0),(1,1)]
    labels=[[float(2**53),1],[1.,1],[1.,1]]
    # First candidate in order has the higher sequentially rounded sum.
    # Source experiment's left-fold rule chooses row3 even though true sums tie.
    assert v.choose_joint(x,[4,3],[0,1,2],labels,1)==3
