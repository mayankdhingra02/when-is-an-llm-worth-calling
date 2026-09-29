from types import SimpleNamespace
import pytest
from escalation.core import State
from escalation.neighbors_v29 import rank, continue_branch


def test_neighbor_ties_prediction_and_seeded_candidate_order():
    # All distances tied: earliest three observations (targets3,6,9) predict6.
    c = SimpleNamespace(x=[(0,)]*23)
    state = State([0, 1, 2]+list(reversed(range(3, 23))), ids=[0, 1, 2], labels=[[3.], [6.], [9.]])
    rows = rank(c, state, list(range(3, 23)))
    assert [r['row_id'] for r in rows] == list(reversed(range(3, 23)))
    assert all(r['neighbor_ids'] == [0, 1, 2] and r['predicted_target'] == '6.0' for r in rows)


def fixture():
    c = SimpleNamespace(x=[(i,) for i in range(40)], directions=('-',))
    prefix = State(list(range(40)))
    for i in range(10): prefix.observe(i, [float(i+1)], c.directions)
    return c, prefix, list(range(10, 30))


def test_batch_acquires_ten_and_cannot_use_new_labels_to_change_selection():
    c, p, pool = fixture(); before = p.record(); seen = []
    def acquire(i): seen.append(i); return [float(100-i)]
    state, trace = continue_branch(c, p, pool, 'batch_3nn', acquire)
    other, other_trace = continue_branch(c, p, pool, 'batch_3nn', lambda i: [1e9+i])
    assert len(seen) == len(set(seen)) == 10 and len(state.ids) == 20
    assert p.record() == before and state.ids == other.ids and trace == other_trace
    assert all(set(r['neighbor_ids']) <= set(p.ids) for r in trace)


def test_sequential_neighbors_can_use_newly_acquired_rows():
    c, p, pool = fixture()
    # Row10 and later shortlist rows share a level; acquired prefix rows do not.
    c.x = [(0,)]*10+[(1,)]*30
    state, trace = continue_branch(c, p, pool, 'sequential_3nn', lambda i: [.1])
    assert 10 in trace[1]['neighbor_ids'] and trace[1]['predicted_target'] != trace[0]['predicted_target']
    assert len(state.ids) == 20 and state.ids[:10] == p.ids


@pytest.mark.parametrize('pool', [list(range(9, 29)), [10]*20, list(range(10, 29)), list(range(30, 50))])
def test_bad_pools_fail_before_acquisition(pool):
    c, p, _ = fixture()
    with pytest.raises(ValueError):
        continue_branch(c, p, pool, 'batch_3nn', lambda i: pytest.fail('Unexpected label access'))


def test_labels_are_required_but_unacquired_targets_not_an_input():
    c, p, pool = fixture(); before = rank(c, p, pool)
    c.hidden_targets = [-1e9]*40
    assert rank(c, p, pool) == before
    p.labels[0] = [float('nan')]
    with pytest.raises(ValueError): rank(c, p, pool)
