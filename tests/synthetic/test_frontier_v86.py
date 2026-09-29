"""Synthetic arithmetic fixtures only; not research measurements."""
import importlib.util,itertools,math
from fractions import Fraction as F
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location('frontier_v86',Path(__file__).resolve().parents[2]/'scripts/analyze_frontier_v86.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def test_exact_frontier_matches_independent_combinations():
    gs=[F(1,7),F(-2,9),F(0),F(1,5)];cost=[F(3),F(2),F(5),F(7)]
    rows,sums,costs=m.frontier(gs,cost)
    for k,row in enumerate(rows):
        direct=[sum((gs[i] for i in c),F(0)) for c in itertools.combinations(range(4),k)]
        assert row['number_of_masks']==math.comb(4,k)
        assert row['hindsight_best_mean_gain']==float(max(direct)/4)
        assert row['hindsight_worst_mean_gain']==float(min(direct)/4)
        assert row['random_expected_mean_gain']==float(sum(direct,F(0))/len(direct)/4)

def test_exact_cancellation_and_zero_no_positive_mask():
    _,sums,_=m.frontier([F(-1,3),F(0),F(-1,5)],[F(1)]*3)
    assert all(s<=0 for s in sums) and sum(s==0 for s in sums)==2
    rows,_,_=m.frontier([F(1,10),F(-1,10)],[F(2),F(2)])
    assert rows[2]['random_expected_mean_gain']==0

def test_repeat_range_is_not_point_estimate():
    case={'arms':{'llm':{'repeats':[9,10,11]},'rf_lcb':{'repeats':[9,10,11]}}}
    point,lo,hi=m.gains(case,'rf_lcb');assert point==0 and lo==F(-2,9) and hi==F(2,11)

def test_denominator_cannot_be_truncated():
    with pytest.raises(AssertionError):m.validate_records([])

def test_declared_size_cap():
    with pytest.raises(AssertionError):m.frontier([F(0)]*16,[F(0)]*16)
