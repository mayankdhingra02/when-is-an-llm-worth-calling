"""Synthetic fixtures only; never research performance observations."""
import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from analyze_influence_v117 import analyze,grouped


def rows():
    return [{'family':'a','base_key':'a1','gain':.1},{'family':'a','base_key':'a1','gain':.3},
            {'family':'a','base_key':'a2','gain':-.2},{'family':'b','base_key':'b1','gain':.4}]


def test_nesting_prevents_replica_weight_inflation():
    r=rows();g=grouped(r)
    assert g==pytest.approx({'a':0,'b':.4})
    # Doubling a complete replica set at one prefix must not change its weight.
    assert grouped(r+r[:2])==pytest.approx(g)
    assert analyze(r)['mean']==pytest.approx(.2)


def test_oracle_is_per_replica_clipping_not_best_sample():
    a=analyze(rows())
    assert a['nondeployable_oracle_headroom_mean']==pytest.approx(.25)
    assert a['nondeployable_oracle_positive_choices']==3
    assert a['leave_one_group_out']==pytest.approx({'a':.4,'b':0})
