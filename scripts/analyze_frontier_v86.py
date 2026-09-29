"""Standard-library, exact finite-policy analysis of measured saved outcomes."""
import argparse,csv,hashlib,json,math,statistics,time
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def frac(v):return F(str(v))
def write(p,v):p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def normalize(root):
    records=[]
    r=read(root/'results/v72_rocksdb_analysis/summary.json');costs=[json.loads(s) for s in (root/'results/v72_rocksdb_paired/selection_costs.jsonl').read_text().splitlines()]
    assert r['actual_new_physical_evaluations']==150 and r['valid_model_responses']==35 and len(r['rows'])==15
    for seed in [11,23,37,53,71]:
        arms={}
        for arm in ['rf_lcb','domain_prior','llm']:
            a=next(a for a in r['rows'] if a['seed']==seed and a['method']==arm);assert a['inclusive_budget']==20 and len(a['confirmation_ms'])==3 and statistics.median(a['confirmation_ms'])==a['confirmed_median_ms']
            arms[arm]={'repeats':a['confirmation_ms'],'selection_seconds':sum(c['seconds'] for c in costs if c['seed']==seed and c['arm']==arm),'config_id':a['selected_config_id']}
        records.append({'family':'RocksDB','workload':'generated_read','seed':seed,'unit':'ms','margin':'0.05','prior_arm':'domain_prior','prior_scope':'shared-prefix continuation,20logical','arms':arms})
    k=read(root/'results/v80_kanzi_analysis/summary.json');costrows=list(csv.DictReader((root/'results/v80_kanzi_analysis/cases.csv').open()))
    assert k['requests']==k['intended_requests']==105 and k['invalid_responses']==0 and k['new_physical_trials']==450 and len(k['cases'])==15
    for c in k['cases']:
        arms={}
        for arm in ['rf_lcb','preset','llm']:
            a=c['arms'][arm];assert len(a['confirmation_bytes'])==3 and statistics.median(a['confirmation_bytes'])==a['median_bytes']
            cost=next(r for r in costrows if r['workload']==c['workload'] and int(r['seed'])==c['seed'] and r['method']==arm)
            assert int(cost['confirmed_bytes'])==a['median_bytes']
            arms[arm]={'repeats':a['confirmation_bytes'],'selection_seconds':float(cost['decision_seconds']),'config_id':a['config_id']}
        records.append({'family':'Kanzi','workload':c['workload'],'seed':c['seed'],'unit':'bytes','margin':'0.01','prior_arm':'preset','prior_scope':'shared-prefix continuation,20logical','arms':arms})
    h=read(root/'results/v85_h2_analysis/summary.json');assert h['complete'] and h['generation_requests']==35 and h['new_physical_trials']==115 and len(h['cases'])==5
    for c in h['cases']:
        arms={}
        for arm,a in c['arms'].items():
            assert len(a['confirmation_seconds'])==3 and statistics.median(a['confirmation_seconds'])==a['median_seconds'] and a['logical_evaluations']==(3 if arm=='prior' else 20)
            arms[arm]={'repeats':a['confirmation_seconds'],'selection_seconds':a['selection_seconds'],'config_id':a['config_id']}
        records.append({'family':'H2','workload':'generated_queries','seed':c['seed'],'unit':'seconds','margin':'0.10','prior_arm':'prior','prior_scope':'standalone fixed prior,3logical;not paired continuation','arms':arms})
    validate_records(records)
    return records

def validate_records(records):
    expected={'RocksDB':{'generated_read'},'Kanzi':{'dickens','sao','xml'},'H2':{'generated_queries'}}
    assert len(records)==25 and len({(r['family'],r['workload'],r['seed']) for r in records})==25
    for family,workloads in expected.items():
        subset=[r for r in records if r['family']==family]
        assert {(r['workload'],r['seed']) for r in subset}=={(w,s) for w in workloads for s in [11,23,37,53,71]}
        for r in subset:
            assert set(r['arms'])=={'rf_lcb','llm',r['prior_arm']}
            for a in r['arms'].values():assert len(a['repeats'])==3 and all(math.isfinite(x) and x>0 for x in a['repeats']) and math.isfinite(a['selection_seconds']) and a['selection_seconds']>=0

def gains(case,control):
    l=list(map(frac,case['arms']['llm']['repeats']));c=list(map(frac,case['arms'][control]['repeats']))
    return (1-statistics.median(l)/statistics.median(c),1-max(l)/min(c),1-min(l)/max(c))

def frontier(gs,extra):
    n=len(gs);assert n and len(extra)==n and n<=15
    sums=[F(0)]*(1<<n);costs=[F(0)]*(1<<n);buckets=[[] for _ in range(n+1)]
    for mask in range(1<<n):
        if mask:
            bit=mask&-mask;i=bit.bit_length()-1;previous=mask^bit;sums[mask]=sums[previous]+gs[i];costs[mask]=costs[previous]+extra[i]
        buckets[mask.bit_count()].append(mask)
    rows=[]
    for k,masks in enumerate(buckets):
        best=max(sums[m] for m in masks);worst=min(sums[m] for m in masks);mean=sum((sums[m] for m in masks),F(0))/len(masks);mean_cost=sum((costs[m] for m in masks),F(0))/len(masks)
        assert len(masks)==math.comb(n,k) and best==sum(sorted(gs,reverse=True)[:k],F(0)) and worst==sum(sorted(gs)[:k],F(0))
        assert mean==F(k,n)*sum(gs,F(0)) and mean_cost==F(k,n)*sum(extra,F(0))
        rows.append({'escalated_cases':k,'cases':n,'model_requests':7*k,'number_of_masks':len(masks),'random_expected_mean_gain':float(mean/n),'hindsight_best_mean_gain':float(best/n),'hindsight_worst_mean_gain':float(worst/n),'random_expected_added_selection_seconds_per_case':float(mean_cost/n)})
    return rows,sums,costs

def analyze(records,out):
    validate_records(records);summary=[];curves=[];pairrows=[];start=time.monotonic();out.mkdir(parents=True,exist_ok=True)
    for family in ['RocksDB','Kanzi','H2']:
        cases=sorted([r for r in records if r['family']==family],key=lambda r:(r['workload'],r['seed']));n=len(cases)
        for label in ['rf_lcb','cheap_prior']:
            ctr=label if label=='rf_lcb' else cases[0]['prior_arm'];triples=[gains(r,ctr) for r in cases];gs=[t[0] for t in triples];extra=[frac(r['arms']['llm']['selection_seconds'])-frac(r['arms'][ctr]['selection_seconds']) for r in cases]
            rows,sums,costs=frontier(gs,extra)
            for row in rows:curves.append({'family':family,'control':label,**row})
            with (out/f'masks_{family.lower()}_{label}.csv').open('w') as f:
                writer=csv.writer(f);writer.writerow(['mask_lsb_in_case_order','escalated_cases','gain_fraction_sum','mean_relative_gain','added_selector_seconds_sum'])
                for m,g in enumerate(sums):writer.writerow([format(m,f'0{n}b')[::-1],m.bit_count(),str(g),float(g/n),float(costs[m])])
            summary.append({'family':family,'control':label,'cases':n,'case_order':[[r['workload'],r['seed']] for r in cases],'mask_count':len(sums),'observed_oracle_gain_pct':100*float(sum((max(F(0),g) for g in gs),F(0))/n),'repeat_range_oracle_lower_pct':100*float(sum((max(F(0),t[1]) for t in triples),F(0))/n),'repeat_range_oracle_upper_pct':100*float(sum((max(F(0),t[2]) for t in triples),F(0))/n),'material_case_count':sum(g>=frac(r['margin']) for g,r in zip(gs,cases)),'original_margin_pct':100*float(frac(cases[0]['margin'])),'strict_benefit_cases':sum(g>0 for g in gs),'same_configuration_cases':sum(r['arms']['llm']['config_id']==r['arms'][ctr]['config_id'] for r in cases),'masks_strictly_better_than_never':sum(s>0 for s in sums),'masks_equal_to_never':sum(s==0 for s in sums),'always_mean_gain_pct':100*float(sum(gs,F(0))/n),'mean_added_selector_seconds':float(sum(extra,F(0))/n),'control_scope':'shared-prefix20logical' if label=='rf_lcb' else cases[0]['prior_scope']})
            for r,t,e in zip(cases,triples,extra):pairrows.append({'family':family,'workload':r['workload'],'seed':r['seed'],'control':label,'gain_pct':100*float(t[0]),'repeat_range_lower_pct':100*float(t[1]),'repeat_range_upper_pct':100*float(t[2]),'extra_selector_seconds':float(e)})
            assert time.monotonic()-start<600,'analysis cap'
    for name,rows in [('frontiers.csv',curves),('paired.csv',pairrows)]:
        with (out/name).open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    write(out/'summary.json',{'scope':'retrospective exact observed-outcome upper references; no fitted policy or independent validation','families':3,'paired_cases':25,'new_generations':0,'new_native_trials':0,'historical_selected_batch_generations':175,'historical_selected_batch_physical_trials':715,'enumerated_masks':sum(x['mask_count'] for x in summary),'comparisons':summary,'repeat_sensitivity':'observed-range extremes; not confidence intervals','selection_cost_only':True})
    write(out/'normalized_cases.json',records)
    return summary

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='results/v86_frontier');p.add_argument('--root',default=str(ROOT));a=p.parse_args();root=Path(a.root)
    freeze=read(root/'reports/protocol_v86.freeze.json')
    for n,d in freeze['sha256'].items():assert sha(root/n)==d,n
    result=analyze(normalize(root),root/a.out);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
