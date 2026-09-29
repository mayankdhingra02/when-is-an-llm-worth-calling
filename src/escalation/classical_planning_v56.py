"""Fixed feature-only grid and classical controls for V56."""
import itertools
import numpy as np
from escalation.classical_java_v54 import choose, RecordedOracle

LEVELS = [('lmcut','hmax'), ('null','stubborn_sets_simple','stubborn_sets_ec','atom_centric_stubborn_sets'),
          ('true','false'), ('low_h','low_g','fifo')]

def grid():
    return list(itertools.product(*LEVELS))

def encode(configurations):
    # Equal contribution per categorical dimension to mean absolute distance.
    return np.array([[float(value == level) for value, levels in zip(c, LEVELS) for level in levels]
                     for c in configurations])

def options(config):
    heuristic, pruning, cache, tie = config
    if tuple(config) not in grid():
        raise ValueError('Unknown configuration')
    evaluations = 'sum([g(),h])' + {'low_h':',h','low_g':',g()','fifo':''}[tie]
    return ['--evaluator',f'h={heuristic}(cache_estimates={cache})', '--search',
            f'eager(tiebreaking([{evaluations}],unsafe_pruning=false),reopen_closed=true,'
            f'f_eval=sum([g(),h]),pruning={pruning}(),cost_type=normal)']
