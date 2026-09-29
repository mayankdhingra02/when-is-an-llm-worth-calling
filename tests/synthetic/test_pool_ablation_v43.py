"""Synthetic only: no fixture is a research result."""
import pytest
from escalation.core import initial_state
from escalation.finite_domain import FiniteCandidates
from escalation.pool_ablation_v43 import pools, partition
from escalation.transfer_v41 import rank


def fixture(direction="-"):
    c = FiniteCandidates(tuple("abcdef"),
        tuple(tuple((i >> j) & 1 for j in range(6)) for i in range(64)),
        ("y",), (direction,), tuple(range(2, 66)))
    p = initial_state(c, 11)
    for i in p.order[:10]:
        p.observe(i, [float(i + 1)], c.directions)
    return c, p, p.order[10:30]


@pytest.mark.parametrize("direction", ["-", "+"])
def test_pool_partition_budget_prefix_and_repeatability(direction):
    c, p, original = fixture(direction)
    before = p.record()
    result = pools(c, p, original, 11)
    assert result == pools(c, p, original, 11)
    assert p.record() == before
    assert result["retained10_diverse10"][:10] == rank(c, p, original)[:10]
    for pool in result.values():
        assert len(pool) == len(set(pool)) == 20
        assert not set(pool) & set(p.ids)
        arms = partition(c, p, pool)
        assert all(len(rows) == 10 for rows in arms.values())
        assert not set(arms["batch_3nn"]) & set(arms["coverage_complement"])
        assert set(sum(arms.values(), [])) == set(pool)


def test_farthest_selection_matches_independent_scalar_distances():
    c, p, original = fixture()
    chosen = pools(c, p, original, 11)["retained10_diverse10"]
    selected = chosen[:10]
    for actual in chosen[10:]:
        unused = [i for i in p.order if i not in p.ids + selected]
        def score(i):
            return min(sum(a != b for a, b in zip(c.x[i], c.x[j]))
                       for j in p.ids + selected)
        assert actual == max(unused, key=score)
        selected.append(actual)


def test_uniform_pool_does_not_use_labels():
    c, p, original = fixture()
    altered = p.clone()
    altered.labels = [[1000. - y[0]] for y in p.labels]
    assert pools(c, p, original, 11)["uniform20"] == pools(c, altered, original, 11)["uniform20"]


def test_rejects_overlap_and_incomplete_pool():
    c, p, original = fixture()
    for bad in (original[:19], [p.ids[0], *original[:19]]):
        with pytest.raises(ValueError): pools(c, p, bad, 11)
        with pytest.raises(ValueError): partition(c, p, bad)
