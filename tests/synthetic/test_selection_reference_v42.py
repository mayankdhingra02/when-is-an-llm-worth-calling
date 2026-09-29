"""Synthetic mathematical fixtures; never model evidence."""
import itertools
from collections import Counter
from fractions import Fraction as F
import pytest
from escalation.selection_reference_v42 import random_distribution,compare,best

@pytest.mark.parametrize('direction',['-','+'])
@pytest.mark.parametrize('values,prefix,k',[([1,2,3,4],9,2),([1,1,3,4],2,2),([1,1,1,1],1,3),([1,2,3,4],F(5,2),1),([1,2,3,4],3,4)])
def test_exact_distribution_matches_all_subsets(direction,values,prefix,k):
    values=list(map(F,values));prefix=F(prefix)
    expected=Counter(best([prefix,*(values[i] for i in subset)],direction) for subset in itertools.combinations(range(len(values)),k))
    result=random_distribution(values,prefix,direction,k)
    assert result['counts']==expected and sum(expected.values())==result['denominator']

def test_expectation_of_ratio_is_not_ratio_of_expectation():
    d=random_distribution([F(1),F(3)],F(5),'-',1);r=compare(d,F(1),'-')
    assert r['expected_relative_gain']==F(1,3)
    assert r['expected_relative_gain']!=(F(2)-F(1))/F(2)
    assert r['probability_model_strictly_better']==F(1,2) and r['probability_tie']==F(1,2)

def test_prefix_already_optimal_and_exact_half_selection():
    d=random_distribution(list(map(F,range(1,21))),F(1),'-')
    assert compare(d,F(1),'-')['probability_random_matches_or_beats']==1
    d=random_distribution(list(map(F,range(1,21))),F(21),'-')
    assert compare(d,F(1),'-')['probability_random_matches_or_beats']==F(1,2)

@pytest.mark.parametrize('values,prefix,k',[([],1,1),([1],0,1),([1],1,2)])
def test_invalid_population_rejected(values,prefix,k):
    with pytest.raises(ValueError):random_distribution(list(map(F,values)),F(prefix),'-',k)
