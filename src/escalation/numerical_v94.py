"""Fresh numerical-engine domains and independent solution certificates.

No objective table exists. Candidate construction and proposal policies cannot
read measurements; only the separate native acquisition worker runs solvers.
"""
from itertools import product
import numpy as np
from scipy.sparse import csc_matrix
from .finite_domain import FiniteCandidates

PERMUTATIONS = ('NATURAL', 'MMD_ATA', 'MMD_AT_PLUS_A', 'COLAMD')
DOMAINS = {
    'superlu': (('column_permutation_code', 'diagonal_pivot_threshold', 'relax', 'panel_size'),
                (range(4), (0., .01, .1, .5, 1.), (1, 2, 4, 8, 16), (4, 8, 16, 32))),
    'highs': (('presolve_on', 'simplex_scale_strategy', 'simplex_dual_edge_weight_strategy',
               'simplex_update_limit', 'simplex_permute_strategy'),
              ((0, 1), (0, 2, 3, 4), (0, 1, 2), (10, 25, 50, 100, 200), (0, 1))),
}

def candidates(family):
    names, levels = DOMAINS[family]
    rows = tuple(product(*levels))
    return FiniteCandidates(names, rows, ('validated_solve_seconds',), ('-',), tuple(range(len(rows))))

def options(family, row):
    c = candidates(family)
    if tuple(row) not in c.x:
        raise ValueError('Configuration outside frozen domain')
    if family == 'superlu':
        return dict(permc_spec=PERMUTATIONS[int(row[0])], diag_pivot_thresh=float(row[1]),
                    relax=int(row[2]), panel_size=int(row[3]))
    return dict(presolve='on' if row[0] else 'off', simplex_scale_strategy=int(row[1]),
                simplex_dual_edge_weight_strategy=int(row[2]), simplex_update_limit=int(row[3]),
                simplex_permute_strategy=int(row[4]))

def linear_certificate(a, b, x, truth):
    residual = float(np.max(np.abs(a @ x - b)) / max(1., np.max(np.abs(b))))
    forward = float(np.max(np.abs(x - truth)) / max(1., np.max(np.abs(truth))))
    valid = bool(np.isfinite(x).all() and residual <= 1e-8 and forward <= 1e-6)
    return dict(valid=valid, scaled_residual=residual, relative_forward_error=forward)

def lp_arrays(lp):
    a = csc_matrix((lp.a_matrix_.value_, lp.a_matrix_.index_, lp.a_matrix_.start_),
                   shape=(lp.num_row_, lp.num_col_))
    return a, *(np.asarray(v, dtype=float) for v in
                (lp.col_cost_, lp.col_lower_, lp.col_upper_, lp.row_lower_, lp.row_upper_))

def lp_certificate(lp, x, y, z):
    """Primal bounds, dual stationarity/sign feasibility, and weak-duality gap.

    HiGHS minimization convention: positive duals attach to lower bounds;
    negative duals attach to upper bounds. Never multiply zero by infinity.
    """
    a, c, lo, hi, rl, ru = lp_arrays(lp)
    x, y, z = map(lambda v: np.asarray(v, dtype=float), (x, y, z))
    if not all(np.isfinite(v).all() for v in (x, y, z)):
        return {'valid': False, 'reason': 'nonfinite solution'}
    activity = a @ x
    def violation(v, lower, upper):
        scores = [0.]
        for bounds, delta in ((lower, lower-v), (upper, v-upper)):
            mask = np.isfinite(bounds)
            scores.extend((np.maximum(0., delta[mask]) / (1.+np.abs(bounds[mask]))).tolist())
        return max(scores)
    primal_error = max(violation(x, lo, hi), violation(activity, rl, ru))
    aty = a.T @ y
    stationarity = float(np.max(np.abs(c-aty-z)/(1.+np.abs(c)+np.abs(aty)+np.abs(z))))
    bound_terms, sign_error = [], 0.
    for duals, lower, upper in ((y, rl, ru), (z, lo, hi)):
        for dual, lb, ub in zip(duals, lower, upper):
            if dual == 0.: continue
            bound = lb if dual > 0 else ub
            if not np.isfinite(bound):
                sign_error = max(sign_error, abs(float(dual)))
            else: bound_terms.append(float(dual*bound))
    primal = float(c @ x + lp.offset_)
    dual = float(sum(bound_terms) + lp.offset_)
    gap = abs(primal-dual)/(1.+abs(primal))
    valid = max(primal_error, stationarity, sign_error, gap) <= 1e-6
    return dict(valid=bool(valid), scaled_primal_violation=float(primal_error),
                scaled_stationarity=stationarity, dual_sign_error=sign_error,
                relative_duality_gap=gap, primal_objective=primal, dual_objective=dual)
