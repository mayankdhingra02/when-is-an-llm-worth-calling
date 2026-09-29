"""Independent Decimal reconstruction from source targets and real request logs."""
import csv,json
from decimal import Decimal,getcontext
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];getcontext().prec=45
def read(p):return json.loads((ROOT/p).read_text(),parse_float=Decimal)
def avg(xs):return sum(xs,Decimal(0))/len(xs)
def threshold(g,c):return c/g if g>0 else None
checks=0
def close(a,b):
    global checks
    checks+=1
    if a is None or b is None:
        assert a is b;return
    assert abs(a-b)<=max(Decimal('1e-10'),abs(a)*Decimal('1e-11')),(a,b)

def main():
    result=read('results/v33_amortization/summary.json');m=read('data/manifest_v8.json');targets={}
    for spec in m['datasets']:
        values=[];seen=set()
        with (ROOT/spec['path']).open(newline='') as f:
            for row in csv.DictReader(f,delimiter=spec['delimiter']):
                if any(row[k]!=str(v) for k,v in spec['filters'].items()):continue
                x=tuple(Decimal(row[k]) for k in spec['feature_names'])
                if x in seen:continue
                seen.add(x);values.append(Decimal(row[spec['primary_objective']]))
        assert len(values)==spec['rows'];targets[spec['id']]=values
    requests={r['job_id']:r for r in [json.loads(s,parse_float=Decimal) for s in (ROOT/'results/v22_larger/requests.jsonl').read_text().splitlines()]}
    def target(state,dataset):
        values=targets[dataset];assert state['labels']==[[values[i]] for i in state['ids']]
        return min(values[i] for i in state['ids'])
    records=[]
    for row in result['records']:
        dataset=row['dataset'];key=f"{dataset}_{row['seed']}";base=row['baseline']
        if base=='full_classical':state=read(f'results/v6/classical/{key}.json')['arms']['centroid_nominal']['state']
        else:
            path={'static_rank':f'results/v8/static_rank/{key}.json','centroid_shortlist':f'results/v25_shortlist/arms/{key}.json',
                'sequential_3nn':f'results/v29_neighbors/arms/{key}_sequential_3nn.json'}[base]
            state=read(path)['state']
        b=target(state,dataset);arm=read(f"results/v22_larger/arms/{row['job_id']:02d}_llm.json");l=target(arm['state'],dataset)
        req=requests[row['job_id']];cost=req['wall_seconds'];gain=(b-l)/b
        assert row['cache_key']==req['cache_key'] and row['request_id']==req['request_id']
        for k,v in [('baseline_target',b),('llm_target',l),('gain',gain),('request_seconds',cost),('recovery_baseline_work_seconds',threshold(gain,cost))]:close(v,row[k])
        records.append({**row,'gain':gain,'request_seconds':cost})
    cases=[]
    for c in result['cases']:
        rows=[r for r in records if r['dataset']==c['dataset'] and r['seed']==c['seed'] and r['baseline']==c['baseline']]
        assert len(rows)==3
        assigned=next(r for r in rows if r['condition']=='assigned_ids');g=avg([r['gain'] for r in rows]);cost=avg([r['request_seconds'] for r in rows])
        ts=[threshold(r['gain'],r['request_seconds']) for r in rows]
        values={'assigned_gain':assigned['gain'],'assigned_request_seconds':assigned['request_seconds'],
            'assigned_recovery_seconds':threshold(assigned['gain'],assigned['request_seconds']),
            'uniform_presentation_mean_gain':g,'uniform_presentation_mean_request_seconds':cost,'uniform_presentation_recovery_seconds':threshold(g,cost),
            'all_three_recovery_seconds':max(ts) if all(t is not None for t in ts) else None}
        for k,v in values.items():close(v,c[k])
        assert c['all_three_positive']==all(r['gain']>0 for r in rows)
        assert c['any_gain']==any(r['gain']>0 for r in rows) and c['any_harm']==any(r['gain']<0 for r in rows)
        cases.append({**c,**values})
    def group_mean(values):
        return avg([avg([v for v,g in values if g==family]) for family in sorted({g for v,g in values})])
    for row in result['curves']:
        cs=[c for c in cases if c['baseline']==row['baseline']];prefix='assigned' if row['scenario']=='assigned_ids' else 'uniform_presentation_mean'
        values=[(row['baseline_work_seconds_per_case']*c[prefix+'_gain']-c[prefix+'_request_seconds'],c['system_group']) for c in cs]
        close(group_mean(values),row['always_call_mean_net_seconds'])
        close(group_mean([(max(Decimal(0),v),g) for v,g in values]),row['hindsight_mean_net_seconds'])
        assert row['hindsight_calls']==sum(v>0 for v,g in values)
        assert row['never_call_mean_net_seconds']==row['never_calls']==0 and row['always_calls']==15
    for s in result['summaries']:
        cs=[c for c in cases if c['baseline']==s['baseline']]
        assert s['assigned_positive']==sum(c['assigned_gain']>0 for c in cs)
        assert s['assigned_ties']==sum(c['assigned_gain']==0 for c in cs)
        assert s['assigned_harms']==sum(c['assigned_gain']<0 for c in cs)
        assert s['uniform_mean_positive']==sum(c['uniform_presentation_mean_gain']>0 for c in cs)
        assert s['positive_under_all_three']==sum(c['all_three_positive'] for c in cs)
        for row in s['scenarios']:
            prefix='assigned' if row['scenario']=='assigned_ids' else 'uniform_presentation_mean'
            g=group_mean([(c[prefix+'_gain'],c['system_group']) for c in cs]);cost=group_mean([(c[prefix+'_request_seconds'],c['system_group']) for c in cs])
            close(g,row['equal_family_gain']);close(cost,row['equal_family_request_seconds']);close(threshold(g,cost),row['always_call_recovery_baseline_work_seconds_per_case'])
    history=result['historical_v22_collection'];assert history['actual_requests']==len(requests)==60
    close(sum(r['wall_seconds'] for r in requests.values()),history['request_wall_seconds'])
    assert sum(r['input_tokens'] for r in requests.values())==history['input_tokens']
    assert sum(r['output_tokens'] for r in requests.values())==history['output_tokens']
    assert len(records)==180 and len(cases)==60 and len(result['curves'])==56
    print(json.dumps({'verified':True,'source_paired_comparisons':len(records),'case_scenarios':len(cases),
        'work_grid_rows':56,'decimal_values_checked':checks,'aggregate_count_checks':20,'model_cost_requests_reconciled':60,
        'new_model_calls':0,'new_objective_acquisitions':0,'new_physical_trials':0},indent=2))

if __name__=='__main__':main()
