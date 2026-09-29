import itertools
from collections import Counter
import pytest
from escalation.core import State
from escalation.random_v31 import select, branch, MODES
from escalation.selection_null_v9 import uniform_minimum_distribution

@pytest.mark.parametrize('mode', MODES)
def test_random_controls_preserve_state_budget_and_label_blind_selection(mode):
    prefix = State(list(range(40)))
    for i in range(10): prefix.observe(i, [40-i], ('-',))
    saved = prefix.record(); pool = list(range(10,30)); chosen = select(prefix, pool, 'synthetic', 11, mode)
    altered = prefix.clone(); altered.labels = [[999] for _ in altered.ids]
    assert select(altered, pool[::-1], 'synthetic', 11, mode) == chosen
    accesses = []
    def acquire(i): accesses.append(i); return [40-i]
    final, selection = branch(prefix, pool, 'synthetic', 11, mode, ('-',), acquire)
    assert selection == chosen and accesses == chosen['selected']
    assert len(accesses) == len(set(accesses)) == 10 and not set(accesses)&set(prefix.ids)
    assert prefix.record() == saved and final.ids[:10] == prefix.ids and len(final.ids) == 20
    if mode == 'random_shortlist': assert set(accesses) <= set(pool)

def test_random_rejects_contaminated_pool():
    prefix = State(list(range(40)), ids=list(range(10)))
    with pytest.raises(ValueError): select(prefix, list(range(9,29)), 'synthetic', 11, 'random_shortlist')
    with pytest.raises(ValueError): select(prefix, list(range(10,30)), 'synthetic', 11, 'unknown')

@pytest.mark.parametrize('values,incumbent,k', [([1,1,2,4,9],3,2),([9,9,9],2,2),([1,2,3],4,3)])
def test_exact_random_formula_matches_exhaustive_tied_and_clipped_fixtures(values, incumbent, k):
    expected = Counter(min(incumbent,min(values[i] for i in ids)) for ids in itertools.combinations(range(len(values)),k))
    result = uniform_minimum_distribution(values,incumbent,k)
    assert {r['loss']:r['subsets'] for r in result['support']} == expected
