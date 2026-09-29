"""Independent stdlib replay: integer-scaled decimal sums, no Fraction/optimizer imports."""
import csv,hashlib,json,math,sys
from decimal import Decimal
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[1];OUT='results/v36_arithmetic';MODES=('joint_shortlist','joint_full')

def read(p):return json.loads((ROOT/p).read_text())
def lines(p):return [json.loads(l) for l in (ROOT/p).read_text().splitlines() if l.strip()]
def need(ok,message):
    if not ok:raise ValueError(message)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def fraction_string(n,d):
    g=math.gcd(n,d);n//=g;d//=g
    return str(n) if d==1 else f'{n}/{d}'

def integer_choice(xs,order,ids,labels,cap):
    values=[Decimal(v) for pair in labels for v in pair]+[Decimal(cap)]
    need(all(v.is_finite() and v>0 for v in values),'Finite positive acquired values')
    exponent=min(0,min(v.as_tuple().exponent for v in values));scale=10**(-exponent)
    def integer(v):
        t=v.as_tuple();n=int(''.join(str(i) for i in t.digits))
        return (-1 if t.sign else 1)*n*10**(t.exponent-exponent)
    z=[integer(v) for v in values];limit=z[-1];pairs=list(zip(z[:-1:2],z[1:-1:2]));est=[]
    for pos,i in enumerate(i for i in order if i not in ids):
        near=sorted(range(len(ids)),key=lambda j:(sum(a!=b for a,b in zip(xs[i],xs[ids[j]])),j))[:3]
        rt=sum(pairs[j][0] for j in near);size=sum(pairs[j][1] for j in near)
        est.append((i,pos,rt,size,[ids[j] for j in near]))
    feasible=[v for v in est if v[3]<=3*limit]
    chosen=min(feasible,key=lambda v:(v[2],v[1])) if feasible else min(est,key=lambda v:(v[3],v[2],v[1]))
    return {'row_id':chosen[0],'neighbor_ids':chosen[4],'runtime_sum_fraction':fraction_string(chosen[2],scale),
        'size_sum_fraction':fraction_string(chosen[3],scale),'predicted_feasible':chosen[3]<=3*limit}

def calculate():
    for p,h in read('reports/protocol_v36_arithmetic.freeze.json')['sha256'].items():need(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,'Frozen input: '+p)
    m=read('data/arithmetic_v36.json');old_manifest=read('data/constrained_v34.json');tables={}
    for d in m['datasets']:
        xs=[];ys=[];source=[];seen=set()
        with (ROOT/d['path']).open(newline='') as f:
            for line,row in enumerate(csv.DictReader(f,delimiter=d['delimiter']),2):
                if any(row[k]!=str(v) for k,v in d['filters'].items()):continue
                x=tuple(float(row[n]) for n in d['feature_names'])
                if x in seen:continue
                seen.add(x);xs.append(x);ys.append([row['performance'],row['size']]);source.append(line)
        need(len(xs)==d['rows'],'Source dimensions');tables[d['id']]=(xs,ys,source)
    records=[];comparisons=[];expected=[];old_prefix_events=lines('results/v34_constrained/acquisitions.jsonl')
    jobs=read('data/larger_probe_v22.json')['jobs'];requests=lines('results/v22_larger/requests.jsonl')
    for case in m['cases']:
        dataset=case['dataset'];seed=case['seed'];key=f'{dataset}_{seed}';xs,ys,source=tables[dataset];p=case['prefix'];cap=Decimal(p['size_cap'])
        v34=read(f'results/v34_constrained/prefixes/{key}.json')
        need(digest(p)==case['prefix_hash'] and v34['prefix_hash']==case['v34_prefix_hash'],'Prefix hashes')
        need(p['ids']==v34['prefix']['ids'] and p['order']==v34['prefix']['order'] and p['anchor_row']==v34['prefix']['anchor_row'],'Original prefix state')
        need(p['labels']==[ys[i] for i in p['ids']] and cap==Decimal(ys[p['anchor_row']][1]),'Source prefix/cap')
        events=[e for e in old_prefix_events if (e['dataset'],e['seed'],e['arm'])==(dataset,seed,'prefix')]
        need([[e['raw_runtime'],e['raw_size']] for e in events]==p['labels'],'Previously charged prefix only')
        old_case=next(c for c in old_manifest['cases'] if (c['dataset'],c['seed'])==(dataset,seed));need(case['pool']==old_case['pool'],'Same pool')
        for mode in MODES:
            arm=read(f'{OUT}/arms/{key}_{mode}.json');old=read(f'results/v34_constrained/arms/{key}_{mode}.json')
            need(arm['status']=='completed' and arm['logical_evaluations']==20 and arm['actual_new_accesses']==10 and arm['prefix_hash']==case['prefix_hash'],'Budget and prefix')
            ids=p['ids'][:];labels=[ys[i] for i in ids];order=p['order'] if mode=='joint_full' else [i for i in p['order'] if i in set(case['pool'])|set(ids)]
            need(len(arm['events'])==10,'Ten steps')
            for event in arm['events']:
                choice=integer_choice(xs,order,ids,labels,p['size_cap']);need(choice==event,'Independent scaled-integer decision replay')
                i=choice['row_id'];ids.append(i);labels.append(ys[i]);expected.append((dataset,seed,mode,i,source[i],*ys[i]))
            need(ids==arm['ids'] and labels==arm['labels'] and len(set(ids))==20,'Source-bound twenty-row state')
            best=min((i for i in ids if Decimal(ys[i][1])<=cap),key=lambda i:Decimal(ys[i][0]));runtime=Decimal(ys[best][0])
            need((best,ys[best][0],ys[best][1])==(arm['best_row'],arm['best_runtime'],arm['best_size']),'Exact feasible terminal')
            need(arm['infeasible_new_acquisitions']==sum(Decimal(ys[i][1])>cap for i in ids[10:]),'Infeasible charges')
            oldbest=min((i for i in old['ids'] if Decimal(ys[i][1])<=cap),key=lambda i:Decimal(ys[i][0]));oldrt=Decimal(ys[oldbest][0])
            need(oldbest==old['best_row'] and float(oldrt)==old['best_runtime'],'Old terminal source binding')
            changed=[j for j,(a,b) in enumerate(zip(old['ids'][10:],ids[10:])) if a!=b]
            record={'dataset':dataset,'seed':seed,'arm':mode,'trajectory_changed':bool(changed),'selection_set_changed':set(ids)!=set(old['ids']),
                'changed_positions':len(changed),'first_changed_step':changed[0] if changed else None,'old_best_row':oldbest,'exact_best_row':best,
                'old_runtime':str(oldrt),'exact_runtime':str(runtime),'terminal_runtime_changed':runtime!=oldrt,
                'exact_gain_over_old':float((oldrt-runtime)/oldrt)};records.append(record)
            for condition in ('assigned_ids','reverse_display','reassigned_ids'):
                llm=read(f'results/v34_constrained/arms/{key}_cached_llm_{condition}.json')
                job=next(j for j in jobs if (j['dataset'],j['seed'],j['condition'])==(dataset,seed,condition));req=next(r for r in requests if r['job_id']==job['job_id'])
                need(llm['ids'][10:]==[job['mapping'][s] for s in req['raw_output'].splitlines()] and llm['ids'][:10]==ids[:10],'Unchanged real response selection')
                lr=min((i for i in llm['ids'] if Decimal(ys[i][1])<=cap),key=lambda i:Decimal(ys[i][0]));lrt=Decimal(ys[lr][0])
                need(lr==llm['best_row'] and float(lrt)==llm['best_runtime'],'LLM source-bound feasible outcome')
                oldgain=(oldrt-lrt)/oldrt;newgain=(runtime-lrt)/runtime
                comparisons.append({'dataset':dataset,'seed':seed,'condition':condition,'baseline':mode,'llm_runtime':str(lrt),
                    'old_llm_gain':float(oldgain),'exact_llm_gain':float(newgain),'old_gain_decimal':str(oldgain),'exact_gain_decimal':str(newgain),
                    'comparison_sign_changed':(oldgain>0)-(oldgain<0)!=(newgain>0)-(newgain<0)})
    journal=lines(OUT+'/acquisitions.jsonl')
    need(len(journal)==200 and all(r['vector_charge']==1 for r in journal),'200 charged vectors')
    need([(r['dataset'],r['seed'],r['arm'],r['row_id'],r['source_line'],r['raw_runtime'],r['raw_size']) for r in journal]==expected,'Ordered source journal')
    progress=read(OUT+'/progress.json');need(progress['complete'] and len(progress['arms'])==20 and all(r['status']=='completed' for r in progress['arms']),'Full denominator')
    groups=[]
    for mode in MODES:
        for dataset in ('brotli','lrzip'):
            g=[r for r in records if r['dataset']==dataset and r['arm']==mode]
            groups.append({'dataset':dataset,'arm':mode,'cases':len(g),'changed_trajectories':sum(r['trajectory_changed'] for r in g),
                'changed_terminal_runtimes':sum(r['terminal_runtime_changed'] for r in g),'mean_exact_gain_over_old':mean(r['exact_gain_over_old'] for r in g)})
    llm_summaries=[]
    for condition in ('assigned_ids','reverse_display','reassigned_ids'):
        for mode in MODES:
            rr=[r for r in comparisons if r['condition']==condition and r['baseline']==mode]
            family=[{'dataset':d,'old_mean_gain':mean(r['old_llm_gain'] for r in rr if r['dataset']==d),
                'exact_mean_gain':mean(r['exact_llm_gain'] for r in rr if r['dataset']==d)} for d in ('brotli','lrzip')]
            llm_summaries.append({'condition':condition,'baseline':mode,'families':family,'old_equal_family_gain':mean(f['old_mean_gain'] for f in family),
                'exact_equal_family_gain':mean(f['exact_mean_gain'] for f in family),'wins':sum(r['exact_llm_gain']>0 for r in rr),
                'ties':sum(r['exact_llm_gain']==0 for r in rr),'harms':sum(r['exact_llm_gain']<0 for r in rr),
                'case_sign_changes':sum(r['comparison_sign_changed'] for r in rr)})
    return {'scope':'exploratory exact-arithmetic ablation on two exposed families; no new model inference','records':records,'groups':groups,
        'llm_comparisons':comparisons,'llm_summaries':llm_summaries,'changed_trajectories':sum(r['trajectory_changed'] for r in records),
        'changed_selection_sets':sum(r['selection_set_changed'] for r in records),'changed_terminal_runtimes':sum(r['terminal_runtime_changed'] for r in records),
        'verification':{'arms':20,'new_vectors':200,'independent_integer_decisions':200,'real_cached_llm_comparisons':60,'shared_prefix':10,'inclusive_budget':20}}

if __name__=='__main__':
    result=calculate();need(result==read(OUT+'/summary.json'),'Saved result mismatch')
    print(json.dumps({'verified':True,'runtime':sys.version,'isolated':sys.flags.isolated,'no_site':sys.flags.no_site,
        'scientific_summary_sha256':digest(result),'changed_trajectories':result['changed_trajectories'],
        'changed_terminal_runtimes':result['changed_terminal_runtimes'],**result['verification']},indent=2))
