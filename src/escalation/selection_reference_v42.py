"""Exact finite random-selection reference; evaluation only, never an optimizer."""
from collections import defaultdict
from fractions import Fraction as F
from math import comb

def best(values,direction):
    if direction not in ('-','+'):raise ValueError('Direction required')
    if not values or any(v<=0 for v in values):raise ValueError('Positive recorded targets required')
    return (min if direction=='-' else max)(values)

def gain(reference,treatment,direction):
    if reference<=0 or treatment<=0:raise ValueError('Positive targets required')
    return (reference-treatment)/reference if direction=='-' else (treatment-reference)/reference

def random_distribution(values,prefix_best,direction,k=10):
    """Probability by order statistic, including ties and prefix clipping.

    A fixed sorted rank r is the first selected rank in C(n-r-1,k-1)
    subsets. Stable tie ranks partition subsets; equal values are combined.
    """
    if not 1<=k<=len(values):raise ValueError('Invalid sample size')
    best([prefix_best,*values],direction)
    ordered=sorted(values,reverse=direction=='+');counts=defaultdict(int)
    for r in range(len(values)-k+1):
        result=best([prefix_best,ordered[r]],direction)
        counts[result]+=comb(len(values)-r-1,k-1)
    denominator=comb(len(values),k)
    if sum(counts.values())!=denominator:raise AssertionError('Subset partition')
    return {'counts':dict(counts),'denominator':denominator,'ceiling':best([prefix_best,*values],direction)}

def compare(distribution,model_best,direction):
    counts=distribution['counts'];denominator=distribution['denominator']
    effects={target:gain(target,model_best,direction) for target in counts}
    return {'expected_relative_gain':sum(counts[t]*effects[t] for t in counts)/denominator,
        'probability_model_strictly_better':F(sum(counts[t] for t,g in effects.items() if g>0),denominator),
        'probability_tie':F(sum(counts[t] for t,g in effects.items() if g==0),denominator),
        'probability_random_strictly_better':F(sum(counts[t] for t,g in effects.items() if g<0),denominator),
        'probability_random_matches_or_beats':F(sum(counts[t] for t,g in effects.items() if g<=0),denominator)}
