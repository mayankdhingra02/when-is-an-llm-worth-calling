"""Synthetic headroom checks, separate from measured results."""
import pytest
from escalation.headroom_v10 import bounds,material,relative_improvement
from escalation.core import losses


def test_incumbent_clipping_and_restricted_vs_global():
    assert bounds([.3,.4,.2,0.],[0],[1,2])=={'shortlist':.2,'full_table':0.}
    assert bounds([0.,.3,.4],[0],[1,2])=={'shortlist':0.,'full_table':0.}


def test_orientation_uses_existing_loss_definition():
    assert bounds(losses([[1],[2],[3]],['-']),[1],[0])=={'shortlist':0.,'full_table':0.}
    assert bounds(losses([[1],[2],[3]],['+']),[1],[0])=={'shortlist':.5,'full_table':0.}
    assert relative_improvement(10,5,'-')==.5
    assert relative_improvement(10,15,'+')==.5


def test_strict_margin_and_unrestricted_baseline_can_be_better():
    assert not material(.02) and material(.020001)
    assert not material(-.01)
    assert relative_improvement(0,0,'-') is None
    assert relative_improvement(-1,-2,'-') is None

@pytest.mark.parametrize('scores,prefix,pool',[([],[],[]),([0,1],[0],[0]),([0,1],[0],[2]),([0,float('nan')],[0],[1])])
def test_invalid_bounds(scores,prefix,pool):
    with pytest.raises(ValueError):bounds(scores,prefix,pool)
