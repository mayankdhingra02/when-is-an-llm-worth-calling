import random
import pytest
from escalation.classical_java_v54 import RecordedOracle, choose, encode


def test_budget_duplicate_and_branches():
    oracle = RecordedOracle(range(48))
    prefix = [oracle.acquire(i, [], 'test', 'prefix') for i in range(10)]
    one = [dict(x) for x in prefix]; two = [dict(x) for x in prefix]
    one.append(oracle.acquire(10, one, 'test', 'one'))
    two.append(oracle.acquire(11, two, 'test', 'two'))
    assert len(prefix) == 10 and one[-1]['config_id'] != two[-1]['config_id']
    with pytest.raises(ValueError): oracle.acquire(0, prefix, 'test', 'bad')
    with pytest.raises(ValueError): oracle.acquire(21, [{'config_id': i} for i in range(20)], 'test', 'bad')


def test_policy_inputs_are_acquired_only_and_deterministic():
    x = encode([(1, 1, 2), (2, 2, 4), (4, 4, 8), (8, 8, 8)])
    obs = [{'config_id': 0, 'value_ms': 100}, {'config_id': 1, 'value_ms': 80}]
    for method in ['nn', 'rf_lcb', 'random']:
        a = choose(x, obs, method, 11, random.Random(1))
        b = choose(x, obs, method, 11, random.Random(1))
        assert a == b and a in [2, 3]
