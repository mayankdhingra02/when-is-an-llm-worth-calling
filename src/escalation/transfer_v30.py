"""Admission guards and fixed classical branches; no hidden target access."""
from .core import State
from .finite_domain import recommend
from .neighbors_v29 import continue_branch as neighbors
from .shortlist_v25 import continue_branch as centroid
from .consensus_v28 import continue_branch as fixed_batch

MODES = ('full_classical', 'static_rank', 'centroid_shortlist', 'batch_3nn', 'sequential_3nn')


def validate_admission(specs, exposed):
    if len(specs) != 2 or {s['system_group'] for s in specs} != {'opus', 'z3'}:
        raise ValueError('This fixed transfer study requires exactly Opus and z3')
    if {s['system_group'] for s in specs} & set(exposed):
        raise ValueError('Previously exposed family cannot be admitted as fresh')
    for s in specs:
        if s['direction'] != '-' or s['split'] != 'prospective_transfer' or s['rows'] < 30:
            raise ValueError('Unsupported direction, split or candidate count')
        if not s.get('evidence') or not s.get('sha256'):
            raise ValueError('Pinned source evidence required')


def branch(candidates, prefix, pool, mode, acquire, checkpoint=lambda state, trace: None):
    if mode not in MODES:
        raise ValueError('Unknown fixed arm')
    if mode in ('batch_3nn', 'sequential_3nn'):
        return neighbors(candidates, prefix, pool, mode, acquire, checkpoint)
    if mode == 'static_rank':
        result = fixed_batch(prefix, pool[:10], candidates.directions, acquire,
                             lambda s: checkpoint(s, []))
    elif mode == 'centroid_shortlist':
        result = centroid(candidates, prefix, pool, acquire, lambda s: checkpoint(s, []))
    else:
        if len(prefix.ids) != 10:
            raise ValueError('Ten-label prefix required')
        result = prefix.clone()
        for _ in range(10):
            row = recommend(candidates, result)
            result.observe(row, acquire(row), candidates.directions)
            checkpoint(result, [])
    return result, []
