"""Fixed votes plus classical tie-break; no objective table or provider inputs."""
from collections import Counter


def select(pool, ballots):
    if len(pool) != 20 or len(set(pool)) != 20 or len(ballots) != 3:
        raise ValueError('Need twenty unique ranked candidates and three ballots')
    for ballot in ballots:
        if len(ballot) != 10 or len(set(ballot)) != 10 or not set(ballot) <= set(pool):
            raise ValueError('Each ballot must select ten distinct shortlist rows')
    votes = Counter(i for ballot in ballots for i in ballot)
    ranked = sorted(pool, key=lambda i: (-votes[i], pool.index(i)))
    cutoff = votes[ranked[9]]
    tied = [i for i in pool if votes[i] == cutoff]
    return {'selected': ranked[:10], 'votes': [{'row_id': i, 'votes': votes[i]} for i in pool],
            'boundary_vote_count': cutoff, 'boundary_tie_size': len(tied),
            'boundary_selected': sum(votes[i] == cutoff for i in ranked[:10]),
            'tie_break_decides_membership': votes[ranked[9]] == votes[ranked[10]]}


def continue_branch(prefix, selected, directions, acquire, checkpoint=lambda state: None):
    if len(prefix.ids) != 10 or len(selected) != 10 or len(set(selected)) != 10:
        raise ValueError('Need ten-prefix and ten distinct proposals')
    if set(selected) & set(prefix.ids) or not set(selected) <= set(prefix.order):
        raise ValueError('Invalid or previously acquired proposal')
    state = prefix.clone()
    for row in selected:
        state.observe(row, acquire(row), directions)
        checkpoint(state)
    return state
