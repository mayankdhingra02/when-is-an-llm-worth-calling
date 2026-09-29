"""Restricted acquired-label classical continuation; no label-table/provider imports."""
from .finite_domain import recommend

def restrict(prefix, pool):
    if len(prefix.ids)!=10 or len(set(prefix.ids))!=10 or len(pool)!=20:
        raise ValueError('Need ten acquired rows and twenty distinct candidates')
    if len(pool)!=20 or len(set(pool))!=20 or set(pool)&set(prefix.ids):
        raise ValueError('Invalid or acquired shortlist row')
    if not set(pool)<=set(prefix.order):raise ValueError('Unknown shortlist row')
    state=prefix.clone();allowed=set(pool)|set(prefix.ids)
    state.order=[i for i in prefix.order if i in allowed]
    return state

def continue_branch(candidates,prefix,pool,acquire,checkpoint=lambda state:None):
    state=restrict(prefix,pool)
    while len(state.ids)<20:
        row=recommend(candidates,state)
        if row not in pool or row in state.ids:raise ValueError('Selection outside unacquired shortlist')
        state.observe(row,acquire(row),candidates.directions);checkpoint(state)
    return state
