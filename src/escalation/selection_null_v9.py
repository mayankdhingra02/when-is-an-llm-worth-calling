"""Post-hoc evaluator mathematics, never imported by an optimizer or model adapter."""
import math
from collections import defaultdict


def uniform_minimum_distribution(candidate_losses, incumbent_loss, count):
    """Exact subset counts for min(incumbent, min(k of n without replacement)).

    When sorted position j is the lowest selected position, the other k-1
    positions come from n-j-1 later positions. Tied loss values are aggregated.
    Counts are exact integers; loss/expectation arithmetic uses Python floats.
    """
    values=sorted(float(x) for x in candidate_losses)
    if type(count) is not int or not 1<=count<=len(values):
        raise ValueError('selection count outside candidate pool')
    if not math.isfinite(incumbent_loss) or not all(math.isfinite(v) for v in values):
        raise ValueError('finite retrospective losses required')
    frequencies=defaultdict(int)
    for j in range(len(values)-count+1):
        frequencies[min(float(incumbent_loss),values[j])]+=math.comb(len(values)-j-1,count-1)
    total=math.comb(len(values),count)
    if sum(frequencies.values())!=total:raise AssertionError('subset counts do not sum')
    return {'pool_size':len(values),'selection_count':count,'subsets':total,
        'support':[{'loss':loss,'subsets':n,'probability':n/total} for loss,n in sorted(frequencies.items())],
        'expected_loss':math.fsum(loss*n/total for loss,n in frequencies.items())}


def event_probability(distribution, predicate):
    return sum(r['subsets'] for r in distribution['support'] if predicate(r['loss']))/distribution['subsets']


def quantile(distribution, probability):
    if not 0<=probability<=1:raise ValueError('probability outside unit interval')
    seen=0
    for r in distribution['support']:
        seen+=r['subsets']
        if seen>=probability*distribution['subsets']:return r['loss']
    return distribution['support'][-1]['loss']
