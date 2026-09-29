"""Synthetic mathematical fixtures only; no model outputs or empirical cases."""
import itertools,collections,math
import pytest
from escalation.selection_null_v9 import uniform_minimum_distribution,event_probability,quantile

@pytest.mark.parametrize('values,incumbent,k',[
    ([1,2,3,4,5],9,2),([1,1,2,3,3],2,3),([1,2,3],0,2),
    ([2,2,2,2],2,1),([1,2,3,4],9,4),([-3,-2,0,1],-1,2)])
def test_exact_counts_equal_brute_force(values,incumbent,k):
    dist=uniform_minimum_distribution(values,incumbent,k)
    brute=collections.Counter(min(incumbent,min(c)) for c in itertools.combinations(values,k))
    assert {r['loss']:r['subsets'] for r in dist['support']}==brute
    assert dist['subsets']==sum(brute.values())==math.comb(len(values),k)
    assert math.isclose(dist['expected_loss'],sum(x*n for x,n in brute.items())/sum(brute.values()),abs_tol=1e-14)
    assert quantile(dist,0)==min(brute) and quantile(dist,1)==max(brute)
    assert event_probability(dist,lambda loss:True)==1
    assert event_probability(dist,lambda loss:False)==0


def test_reference_twenty_choose_ten_and_budget():
    d=uniform_minimum_distribution(list(range(20)),100,10)
    assert d['subsets']==184756 and len(d['support'])==11
    assert d['support'][0]['probability']==.5
    assert math.isclose(d['expected_loss'],10/11)
    assert event_probability(d,lambda loss:loss<0)==0
    assert event_probability(d,lambda loss:loss<=0)==.5

@pytest.mark.parametrize('values,incumbent,k',[([],0,1),([1],0,0),([1],0,2),([1],0,1.0),([float('nan')],0,1),([1],float('inf'),1)])
def test_invalid_inputs(values,incumbent,k):
    with pytest.raises(ValueError):uniform_minimum_distribution(values,incumbent,k)
