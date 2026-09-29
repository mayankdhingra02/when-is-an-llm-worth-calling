"""Exact finite-population allocation diagnostics, never a deployable router."""
import math
from statistics import mean

def frontier(gains):
    n = len(gains)
    if not 1 <= n <= 15 or not all(math.isfinite(x) for x in gains):
        raise ValueError('Need 1..15 finite gains')
    order = sorted(range(n), key=lambda i: (-gains[i], i))
    distributions = [[] for _ in range(n+1)]
    # Exhaustive verification uses bit membership, independent of sorted prefixes.
    for mask in range(1 << n):
        ids = [i for i in range(n) if mask & (1 << i)]
        distributions[len(ids)].append(math.fsum(gains[i] for i in ids)/n)
    rows = []
    for k, values in enumerate(distributions):
        selected = order[:k]; best = math.fsum(gains[i] for i in selected)/n
        random_mean = mean(values)
        if not math.isclose(best, max(values), abs_tol=1e-12): raise ValueError('Oracle enumeration mismatch')
        if not math.isclose(random_mean, k/n*mean(gains), abs_tol=1e-12): raise ValueError('Random expectation mismatch')
        rows.append({'calls':k, 'oracle_gain':best, 'oracle_selected_indices':selected,
                     'random_expected_gain':random_mean, 'random_min_gain':min(values),
                     'random_max_gain':max(values), 'enumerated_subsets':len(values)})
    maximum=max(r['oracle_gain'] for r in rows)
    best=next(r for r in rows if r['oracle_gain']>=maximum-1e-12)
    return {'curves':rows,'maximum_oracle_gain':maximum,'fewest_calls_at_maximum':best['calls'],
            'enumerated_subsets':sum(len(x) for x in distributions)}
