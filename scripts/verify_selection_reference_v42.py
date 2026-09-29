"""Independent exhaustive subset enumeration, no optimization-library imports."""
import itertools,json,time
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    summary=json.loads((ROOT/'results/v42_selection_reference/summary.json').read_text());started=time.monotonic();subsets=0
    for case in summary['cases']:
        if time.monotonic()-started>80:raise RuntimeError('80-second verification bound')
        values=list(map(F,case['acquired_candidate_targets']));prefix=F(case['prefix_best']);sign=1 if case['direction']=='-' else -1
        # Exact rational targets receive integer desirability ranks; direct
        # enumeration then chooses the best of each ten-element subset.
        ordered=sorted(set(values+[prefix]),reverse=sign==-1);ranks={v:i for i,v in enumerate(ordered)}
        mapped=[ranks[v] for v in values];pr=ranks[prefix];hist=Counter()
        for chosen in itertools.combinations(mapped,10):hist[min(pr,min(chosen))]+=1
        actual={str(ordered[i]):count for i,count in hist.items()};expected={r['target']:r['subsets'] for r in case['distribution']}
        if actual!=expected or sum(hist.values())!=case['subset_denominator']:raise ValueError('Exact subset distribution mismatch')
        subsets+=sum(hist.values())
        for record in summary['model_comparisons']:
            if (record['dataset'],record['seed'])!=(case['dataset'],case['seed']):continue
            model=F(record['model_best']);total=case['subset_denominator'];effects={F(v):sign*(F(v)-model)/F(v) for v in actual}
            mean=sum(actual[str(v)]*g for v,g in effects.items())/total
            if mean!=F(record['exact']['expected_relative_gain']):raise ValueError('Mean-of-ratios mismatch')
            win=F(sum(actual[str(v)] for v,g in effects.items() if g>0),total)
            tie=F(sum(actual[str(v)] for v,g in effects.items() if g==0),total)
            lose=F(sum(actual[str(v)] for v,g in effects.items() if g<0),total)
            if win+tie+lose!=1 or win!=F(record['exact']['probability_model_strictly_better']) or tie!=F(record['exact']['probability_tie']) or lose!=F(record['exact']['probability_random_strictly_better']):raise ValueError('Probability mismatch')
    print(json.dumps({'distributions_verified':len(summary['cases']),'model_comparisons_verified':len(summary['model_comparisons']),
        'hypothetical_subsets_enumerated':subsets,'new_acquisitions':0,'new_model_requests':0,'scope':'Recorded-target enumeration, not repeated real experiments'},indent=2))
if __name__=='__main__':main()
