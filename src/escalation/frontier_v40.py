"""Finite recorded-case upper bounds, not deployable routing policies."""
from fractions import Fraction as F
from math import comb

def allocation_frontier(gains):
    values=[F(x) for x in gains];n=len(values)
    if not 1<=n<=15:raise ValueError('One to fifteen recorded cases required')
    order=sorted(range(n),key=lambda i:(-values[i],i));rows=[]
    for k in range(n+1):
        selected=order[:k];oracle=sum((values[i] for i in selected),F(0))/n
        rows.append({'calls':k,'oracle_gain_fraction':str(oracle),'oracle_gain':float(oracle),'oracle_indices':selected,
                     'random_expected_fraction':str(F(k,n)*sum(values,F(0))/n),
                     'random_expected_gain':float(F(k,n)*sum(values,F(0))/n),
                     'worst_gain_fraction':str(sum(sorted(values)[:k],F(0))/n),'subsets':comb(n,k)})
    best=max(F(r['oracle_gain_fraction']) for r in rows)
    return {'curves':rows,'maximum_gain_fraction':str(best),'maximum_gain':float(best),
            'fewest_calls_at_maximum':next(r['calls'] for r in rows if F(r['oracle_gain_fraction'])==best),
            'positive_cases':sum(v>0 for v in values),'ties':sum(v==0 for v in values),'negative_cases':sum(v<0 for v in values)}
