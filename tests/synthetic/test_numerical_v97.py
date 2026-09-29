import pytest
from escalation.numerical_v97 import candidates, options
from escalation.numerical_v94 import candidates as original
from escalation.core import initial_state
from escalation.finite_domain import recommend
from escalation.selection_v8 import shortlist
from escalation.transfer_v41 import messages

def test_restricted_domain_preserves_original():
    c = candidates('superlu')
    assert len(c.x) == len(set(c.x)) == 240
    assert len(original('superlu').x) == 400
    assert set(r[2] for r in c.x) == {1,2,4,8}
    assert set(r[3] for r in c.x) == {4,8,16}
    for row in [(2,.1,4,32),(2,.1,16,16)]:
        with pytest.raises(ValueError): options('superlu',row)
    with pytest.raises(ValueError): candidates('highs')

@pytest.mark.parametrize('seed',[11,23,37,53,71])
def test_prefix_replay_clone_and_prompt(seed):
    c = candidates('superlu'); s = initial_state(c,seed)
    for step in range(10):
        row = recommend(c,s); s.observe(row,[.01+step*.001],c.directions)
    pool = shortlist(c,s,seed)
    assert len(pool['ranked']) == 20 and not set(pool['ranked']) & set(s.ids)
    assert messages(c,s,pool) == messages(c,s.clone(),pool)
    clone = s.clone(); row = pool['ranked'][0]; clone.observe(row,[.001],c.directions)
    assert len(s.ids) == 10 and len(clone.ids) == 11
