"""Regression for mutable-prefix aliasing, synthetic data only."""
import copy
import pytest


@pytest.mark.parametrize("direction", ["-", "+"])
def test_two_pool_replays_keep_original_prefix_unchanged(monkeypatch, direction):
    monkeypatch.syspath_prepend("scripts")
    from analyze_pool_models_v44_fixed import fresh_state
    from escalation.core import State
    p = State(list(range(40)))
    for i in range(10):
        p.observe(i, [float(i + 1)], (direction,))
    saved = p.record()
    before = copy.deepcopy(saved)
    left, right = fresh_state(saved), fresh_state(saved)
    for i in range(10, 20):
        left.observe(i, [float(i + 1)], (direction,))
    for i in range(20, 30):
        right.observe(i, [float(i + 1)], (direction,))
    assert saved == before
    assert left.ids[:10] == right.ids[:10] == before["ids"]
    assert left.labels[:10] == right.labels[:10] == before["labels"]
    assert len(left.ids) == len(right.ids) == 20
    left.best.append(999)
    left.rest.append(998)
    left.order.reverse()
    assert saved == before and right.order == before["order"]
