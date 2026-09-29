"""Exploratory candidate-pool interventions using predecision information only."""
import random

import numpy as np

from .transfer_v41 import rank


def pools(candidates, prefix, original_pool, seed):
    """Return two fixed-size alternatives; no objective oracle is accepted."""
    if len(prefix.ids) != 10 or len(set(original_pool)) != 20:
        raise ValueError("Require ten-label prefix and twenty distinct candidates")
    if set(original_pool) & set(prefix.ids):
        raise ValueError("Pool overlaps prefix")
    available = [i for i in prefix.order if i not in set(prefix.ids)]
    if len(available) < 20 or not set(original_pool) <= set(available):
        raise ValueError("Invalid candidate domain")
    uniform = random.Random(seed + 43000).sample(available, 20)
    # Preserve the primary batch baseline's entire ten-candidate selection.
    hybrid = rank(candidates, prefix, original_pool)[:10]
    x = np.asarray(candidates.x)
    distance = np.min(
        np.sum(x[:, None, :] != x[prefix.ids + hybrid][None, :, :], axis=2), axis=1
    )
    for _ in range(10):
        unused = [i for i in available if i not in set(hybrid)]
        row = max(unused, key=lambda i: int(distance[i]))
        hybrid.append(row)
        distance = np.minimum(distance, np.sum(x != x[row], axis=1))
    return {"uniform20": uniform, "retained10_diverse10": hybrid}


def partition(candidates, prefix, pool):
    """Two separately budgeted arms cover a pool without sharing new labels."""
    if len(pool) != 20 or len(set(pool)) != 20 or set(pool) & set(prefix.ids):
        raise ValueError("Invalid pool")
    selected = rank(candidates, prefix, pool)[:10]
    return {"batch_3nn": selected,
            "coverage_complement": [i for i in pool if i not in set(selected)]}
