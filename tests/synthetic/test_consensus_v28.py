import pytest
from escalation.consensus_v28 import select, continue_branch
from escalation.core import State


def test_votes_and_static_rank_tie_break_hand_example():
    pool = list(range(20))
    result = select(pool, [list(range(10)), list(range(5, 15)), list(range(10, 20))])
    assert result['selected'] == list(range(5, 15))
    assert result['boundary_vote_count'] == 2
    assert result['tie_break_decides_membership'] is False
    a = list(range(10)); b = list(range(10, 20)); c = list(range(0, 20, 2))
    result = select(pool, [a, b, c])
    assert result['selected'] == c


def test_boundary_ties_use_rank_not_ballot_or_proposal_order():
    pool = list(range(20))
    ballots = [list(range(10)), list(range(5, 15)), list(range(0, 5))+list(range(10, 15))]
    result = select(pool, ballots)
    assert result['selected'] == list(range(10))
    assert result['tie_break_decides_membership'] and result['boundary_tie_size'] == 15
    assert select(pool, [list(reversed(b)) for b in reversed(ballots)]) == result
    # Three identical ballots retain that set, with output ordered by static rank.
    assert select(pool, [list(range(19, 9, -1))]*3)['selected'] == list(range(10, 20))


@pytest.mark.parametrize('ballots', [[list(range(10))]*2, [[0]*10]*3, [list(range(11))]*3,
                                    [list(range(11, 21))]*3])
def test_malformed_ballots_fail(ballots):
    with pytest.raises(ValueError): select(list(range(20)), ballots)


def test_branch_isolation_budget_and_label_independent_batch():
    prefix = State(list(range(30)))
    for i in range(10): prefix.observe(i, [float(i+1)], ['-'])
    before = prefix.record(); chosen = list(range(10, 20)); seen = []
    def acquire(i): seen.append(i); return [1000.0-i]
    out = continue_branch(prefix, chosen, ['-'], acquire)
    assert seen == chosen and prefix.record() == before
    assert len(out.ids) == 20 and out.ids[:10] == prefix.ids
    other = continue_branch(prefix, chosen, ['-'], lambda i: [1e9+i])
    assert other.ids == out.ids
    with pytest.raises(ValueError):
        continue_branch(prefix, list(range(9, 19)), ['-'], lambda i: pytest.fail('Unexpected acquisition'))
