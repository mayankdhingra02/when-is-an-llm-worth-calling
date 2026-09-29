"""Modeled amortization from real records, no additional objective/model calls."""
import math,statistics
from collect_smollm_v47 import ROOT,read,write,sha
O=ROOT/'results/v168_native';M=ROOT/'results/v168_models';A=ROOT/'artifacts/study_v168'
def main():
    for n,h in read(A/'cost.freeze.json')['sha256'].items():assert sha(ROOT/n)==h
    result=read(O/'comparison.json');acq=[read(p) for p in sorted((O/'acquisitions').glob('*.json'))];rows=[]
    for case in result['cases']:
        key=case['case'];model=case['model'];arms={a['arm']:a for a in result['arms'] if a['case']==key};base=arms['sequential_3nn'];chosen=arms[model]
        responses=[__import__('json').loads(x) for x in (M/model/'responses.jsonl').read_text().splitlines()];request=next((r for r in responses if r['key']==key),None)
        branch={arm:sum(a['collection_seconds'] for a in acq if a['case']==key and a['arm']==arm) for arm in [model,'sequential_3nn']}
        warm=None if request is None else branch[model]-branch['sequential_3nn']+request['wall_seconds']
        startup=result['model_costs'][model]['ledger'].get('startup_seconds');cold=None if warm is None or startup is None else warm+startup
        saving=base['median']-chosen['median'];eligible=base['quality_feasible'] and chosen['quality_feasible'] and base['row_id']!=chosen['row_id'] and saving>0
        rows.append({'case':key,'engine':case['engine'],'model':model,'saving_per_future_bundle_seconds':saving,'different_configuration':base['row_id']!=chosen['row_id'],'quality_valid_pair':base['quality_feasible'] and chosen['quality_feasible'],'stable_pair':base['stable'] and chosen['stable'],'robust_practical_gain_vs_sequential':case['robust_practical_wins']['sequential_3nn'],'warm_marginal_optimization_seconds':warm,'cold_marginal_optimization_seconds':cold,'warm_break_even_bundles':math.ceil(max(0,warm)/saving) if eligible and warm is not None else None,'cold_break_even_bundles':math.ceil(max(0,cold)/saving) if eligible and cold is not None else None,'warm_net_seconds_by_future_bundles':{str(n):n*saving-warm for n in [1,10,100,1000,10000]} if eligible and warm is not None else None})
    write(O/'cost_diagnostic.json',{'scope':'post-hoc modeled deployment, not measured savings','primary_comparator':'sequential_3nn','rows':rows})
    text=['# V168 exploratory modeled break-even diagnostic','','Each number is an estimate from measured branch/request costs and fresh-validation medians. It assumes repeating this same workload. No production workload or deployment savings were measured. Null means no positive break-even claim under the fixed rule. Cold startup is charged once per hypothetical case.','','| Case | Model | Robust gain vs sequential | Warm marginal seconds | Warm break-even bundles | Cold break-even bundles |','|---|---|---|---:|---:|---:|']
    for r in rows:text.append(f"| {r['case']} | {r['model']} | {r['robust_practical_gain_vs_sequential']} | {r['warm_marginal_optimization_seconds']} | {r['warm_break_even_bundles']} | {r['cold_break_even_bundles']} |")
    text+=['','Break-even does not establish a reliable controller, superiority to GP, or a positive amortized result for a different workload. Full noise, quality, same-setting, costs and fixed-count net-time projections are retained in results/v168_native/cost_diagnostic.json. Actual source, failed admission and all-branch collection costs remain separate.']
    (ROOT/'reports/cost_v168.md').write_text('\n'.join(text)+'\n')
    print('Saved20modeledcostcases;zeroadditionalmeasurement')
if __name__=='__main__':main()
