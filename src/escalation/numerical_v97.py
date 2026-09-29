"""Restricted V97 domain; original V94 remains unchanged."""
from itertools import product
from .finite_domain import FiniteCandidates
from .numerical_v94 import PERMUTATIONS, linear_certificate, lp_certificate

def candidates(family):
    if family != 'superlu':
        raise ValueError('Only the predeclared exposed SuperLU family is eligible')
    levels = (range(4), (0., .01, .1, .5, 1.), (1, 2, 4, 8), (4, 8, 16))
    rows = tuple(product(*levels))
    return FiniteCandidates(('column_permutation_code', 'diagonal_pivot_threshold', 'relax', 'panel_size'),
        rows, ('validated_solve_seconds',), ('-',), tuple(range(len(rows))))

def options(family, row):
    if tuple(row) not in candidates(family).x:
        raise ValueError('Configuration outside restricted domain')
    return dict(permc_spec=PERMUTATIONS[int(row[0])], diag_pivot_thresh=float(row[1]),
                relax=int(row[2]), panel_size=int(row[3]))
