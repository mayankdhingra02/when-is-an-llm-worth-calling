"""Fixed classical policies; inputs are features and acquired observations only."""
import numpy as np
from sklearn.ensemble import RandomForestRegressor


def encode(configurations):
    x = np.log2(np.asarray(configurations, dtype=float))
    return (x - np.array([0., 0., 1.])) / np.array([3., 3., 2.])


def choose(x, observations, method, seed, rng=None):
    ids = [o['config_id'] for o in observations]
    remaining = [i for i in range(len(x)) if i not in ids]
    if not remaining: raise ValueError('no unobserved configurations')
    if method == 'random': return rng.choice(remaining)
    y = np.array([o['value_ms'] for o in observations])
    if method == 'nn':
        distance = np.abs(x[remaining, None, :] - x[ids][None, :, :]).mean(axis=2)
        near = np.argsort(distance, axis=1, kind='stable')[:, :3]
        score = y[near].mean(axis=1)
    elif method == 'rf_lcb':
        model = RandomForestRegressor(n_estimators=64, min_samples_leaf=1,
                                      max_features=1.0, bootstrap=True, n_jobs=1,
                                      random_state=seed * 100 + len(ids))
        model.fit(x[ids], y)
        predictions = np.array([tree.predict(x[remaining]) for tree in model.estimators_])
        score = predictions.mean(axis=0) - predictions.std(axis=0)
    else: raise ValueError(method)
    return remaining[int(np.argmin(score))]


class RecordedOracle:
    def __init__(self, values):
        self.__values = tuple(values)
        self.events = []

    def acquire(self, config_id, observations, case, arm):
        if len(observations) >= 20: raise ValueError('inclusive20 budget exceeded')
        if config_id in [o['config_id'] for o in observations]: raise ValueError('duplicate acquisition')
        if len(self.events) >= 200: raise ValueError('collection cap exceeded')
        if not 0 <= config_id < len(self.__values): raise ValueError('invalid configuration')
        event = {'event_id': len(self.events), 'case': case, 'arm': arm,
                 'config_id': config_id, 'inclusive_step': len(observations) + 1}
        self.events.append(event)  # Charge before reading the hidden value.
        value = float(self.__values[config_id])
        event['value_ms'] = value
        return dict(config_id=config_id, value_ms=value, source_event_id=event['event_id'])
