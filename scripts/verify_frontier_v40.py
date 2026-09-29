"""Independent integer-scaled exhaustive check; stdlib only; no experiment imports."""
import hashlib,json,math
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def require(ok,message):
    if not ok:raise ValueError(message)
def main():
    for p,h in read('reports/protocol_v40_frontier.freeze.json')['sha256'].items():require(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,'Frozen input')
    original=read('results/v38_size_prompt/summary.json');saved=read('results/v40_frontier/summary.json')
    vals={(p['dataset'],p['seed'],p['condition'],p['baseline']):1-F(p['size_aware_runtime'])/F(p['baseline_runtime']) for p in original['comparisons']}
    cases=[(r['dataset'],r['seed']) for r in saved['cases']];n=len(cases);require(n==10,'Ten cases')
    require(len(saved['scenarios'])==30,'Thirty scenarios');checked=0;allocations=0
    for scenario in saved['scenarios']:
        base,kind=scenario['baseline'],scenario['scenario'];gains=[]
        for d,s in cases:
            vv=[vals[(d,s,c,base)] for c in ('assigned_ids','reverse_display','reassigned_ids')]
            if kind=='uniform_presentation_mean':v=sum(vv)/3
            elif kind=='worst_tested_presentation':v=min(vv)
            elif kind=='best_tested_presentation_hindsight':v=max(vv)
            else:v=vals[(d,s,kind,base)]
            gains.append(v)
        scale=math.lcm(*(v.denominator for v in gains));integers=[v.numerator*(scale//v.denominator) for v in gains]
        require([str(v) for v in gains]==scenario['case_gains_fraction'],'Case gains')
        maxima=[]
        for k in range(n+1):
            sums=[sum(integers[i] for i in indices) for indices in combinations(range(n),k)];r=scenario['curves'][k]
            require(r['calls']==k and r['subsets']==len(sums),'Call budget')
            maximum=F(max(sums),scale*n);maxima.append(maximum)
            require(maximum==F(r['oracle_gain_fraction']) and F(min(sums),scale*n)==F(r['worst_gain_fraction']),'Extrema')
            require(F(sum(sums),len(sums)*scale*n)==F(r['random_expected_fraction']),'Random expectation')
            require(F(sum(v>0 for v in sums),len(sums))==F(r['positive_allocation_probability_fraction']),'Allocation probability')
            ii=r['oracle_indices'];require(len(ii)==len(set(ii))==k and sum((gains[i] for i in ii),F(0))/n==maximum,'Oracle subset')
            checked+=1;allocations+=len(sums)
        require(max(maxima)==F(scenario['maximum_gain_fraction']) and maxima.index(max(maxima))==scenario['fewest_calls_at_maximum'],'Best call budget')
    require(checked==330 and allocations==30720,'Complete enumeration')
    strong=[v for key,v in vals.items() if key[-1]=='runtime_3nn'];require(len(strong)==30 and max(strong)==0,'Pointwise dominance')
    print(json.dumps({'verified_curve_rows':checked,'enumerated_allocations':allocations,'integer_arithmetic_check':True,'runtime3nn_positive_cases':sum(v>0 for v in strong),'runtime3nn_ties':sum(v==0 for v in strong),'runtime3nn_negative_cases':sum(v<0 for v in strong),'new_requests':0,'new_acquisitions':0},indent=2))
if __name__=='__main__':main()
