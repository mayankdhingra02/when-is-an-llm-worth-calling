"""Evaluator-only exhaustive admitted-domain coverage, never optimizer input."""
import json,time,sys,statistics
from fractions import Fraction
from collect_smollm_v47 import ROOT,read,write,append,sha,now
sys.path.insert(0,str(ROOT/'src'))
from analyze_pointwise_v123 import candidates
from escalation.core import State
from escalation.transfer_v41 import IndexedOracle,best
OUT=ROOT/'results/v126_domain_audit'

def optimum(values,direction):
    if direction not in ['-','+']:raise ValueError('Unknown objective direction')
    return (min if direction=='-' else max)(values)

def exact_gain(reference,target,direction):
    if direction not in ['-','+'] or reference<=0 or target<=0:raise ValueError('Invalid objective contract')
    a,b=Fraction(str(reference)),Fraction(str(target))
    return (a-b)/a if direction=='-' else (b-a)/a

def plan(prefix):
    ids=prefix['ids'];order=prefix['order']
    if len(ids)!=10 or len(set(ids))!=10 or len(set(order))!=len(order) or not set(ids)<=set(order):raise ValueError('Bad prefix/order')
    available=[i for i in order if i not in set(ids)]
    return [available[i:i+10] for i in range(0,len(available),10)]

def frozen():
    for n,h in read(ROOT/'reports/protocol_v126.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n

def prepare():
    out=ROOT/'artifacts/study_v126';out.mkdir(exist_ok=False);jobs=read(ROOT/'artifacts/study_v47/jobs.json');chosen=[j for j in jobs if j['seed']==11];assert len(chosen)==6;plans=[]
    for j in chosen:
        p=read(ROOT/j['prefix']);spec,c=candidates(j['dataset']);assert len(c.x)==len(p['state']['order'])
        for b,ids in enumerate(plan(p['state'])):plans.append({**j,'base_key':j['key'],'key':j['key']+f'_coverage_{b:03d}','selected_rows':ids,'prefix_sha256':sha(ROOT/j['prefix'])})
    assert sum(len(j['selected_rows']) for j in plans)==4932;write(out/'plans.json',plans);write(out/'cases.json',jobs);write(out/'coverage_prefixes.json',chosen);print('Planned',len(plans),'coverage branches,4932acquisitions,zero LLM calls')

def collect():
    frozen();OUT.mkdir(exist_ok=False);start=time.monotonic();count=0;completed=0;error=None
    try:
        for j in read(ROOT/'artifacts/study_v126/plans.json'):
            p=read(ROOT/j['prefix']);spec,c=candidates(j['dataset']);state=State(**p['state']).clone();oracle=IndexedOracle(spec,c,p['state'],lambda e:append(OUT/'acquisitions.jsonl',{'key':j['key'],'dataset':j['dataset'],**e}))
            for i in j['selected_rows']:
                if count>=4932 or time.monotonic()-start>180:raise RuntimeError('Coverage stage limit')
                count+=1;state.observe(i,oracle.acquire(i),c.directions)
            assert len(state.ids)<=20;write(OUT/'branches'/f"{j['key']}.json",{**j,'state':state.record(),'logical_evaluations':len(state.ids),'new_acquisitions':len(j['selected_rows'])});completed+=1
    except Exception as e:error=repr(e)
    finally:write(OUT/'collection.json',{'complete':error is None and count==4932,'error':error,'new_recorded_acquisitions':count,'completed_branches':completed,'intended_branches':len(read(ROOT/'artifacts/study_v126/plans.json')),'seconds':time.monotonic()-start,'new_model_requests':0,'scope':'Coverage-only diagnostic branches, not competitive optimization policies'})
    if error:raise RuntimeError(error)
    print('Collected',count,'recorded values across',completed,'bounded coverage branches')

def evaluate():
    frozen();receipt=read(OUT/'collection.json');assert receipt['complete'];targets={};events=[json.loads(x) for x in (OUT/'acquisitions.jsonl').read_text().splitlines()]
    for j in read(ROOT/'artifacts/study_v126/coverage_prefixes.json'):
        p=read(ROOT/j['prefix']);targets[j['dataset']]={i:y[0] for i,y in zip(p['state']['ids'],p['state']['labels'])}
    for e in events:
        t=targets[e['dataset']];assert e['row_id'] not in t;t[e['row_id']]=float(e['raw_target'])
    rows=[]
    for j in read(ROOT/'artifacts/study_v126/cases.json'):
        spec,c=candidates(j['dataset']);t=targets[j['dataset']];assert set(t)==set(range(len(c.x)));p=read(ROOT/j['prefix'])
        for i,y in zip(p['state']['ids'],p['state']['labels']):assert y[0]==t[i]
        direction=spec['direction'];global_best=optimum(t.values(),direction);pool_best=optimum([y[0] for y in p['state']['labels']]+[t[i] for i in p['pool']['mapping'].values()],direction);refs={}
        for mode in ['batch_3nn','full_sequential_3nn','random_full']:
            s=read(ROOT/f"results/v41_transfer/arms/{j['key']}_{mode}.json")['state'];assert s['ids'][:10]==p['state']['ids'] and s['labels'][:10]==p['state']['labels'] and len(set(s['ids']))==20
            for i,y in zip(s['ids'],s['labels']):assert t[i]==y[0]
            refs[mode]=optimum([y[0] for y in s['labels']],direction)
        portfolio=ROOT/f"results/v115_portfolio/arms/{j['key']}.json"
        if portfolio.exists():
            s=read(portfolio)['state'];assert s['ids'][:10]==p['state']['ids']
            for i,y in zip(s['ids'],s['labels']):assert t[i]==y[0]
            refs['single_portfolio']=optimum([y[0] for y in s['labels']],direction)
        def relative(v):return float(exact_gain(v,global_best,direction))
        gains={m:relative(v) for m,v in refs.items()};assert all(v>=0 for v in gains.values())
        rows.append({**j,'direction':direction,'domain_size':len(t),'domain_best':global_best,'shortlist_best':pool_best,'references':refs,'hindsight_global_gains':gains,'joint_batch_sequential_5pct_possible':all(exact_gain(refs[m],global_best,direction)>=Fraction('0.05') for m in ['batch_3nn','full_sequential_3nn']),'sequential_5pct_possible':exact_gain(refs['full_sequential_3nn'],global_best,direction)>=Fraction('0.05')})
    groups=sorted({r['system_group'] for r in rows});families=[]
    for g in groups:
        rs=[r for r in rows if r['system_group']==g];families.append({'system_group':g,'cases':len(rs),'domain_size':rs[0]['domain_size'],'domain_best':rs[0]['domain_best'],'mean_global_gain_vs_sequential':statistics.mean(r['hindsight_global_gains']['full_sequential_3nn'] for r in rs),'joint_5pct_possible':sum(r['joint_batch_sequential_5pct_possible'] for r in rs),'sequential_5pct_possible':sum(r['sequential_5pct_possible'] for r in rs),'sequential_attains_global_best':sum(r['references']['full_sequential_3nn']==r['domain_best'] for r in rs)})
    result={'scope':'Post-exposure evaluator-only admitted-domain ceilings; not LLM outcomes, not deployable routing or held-out validation','cases':rows,'families':families,'collection':receipt,'joint_5pct_possible_cases':sum(r['joint_batch_sequential_5pct_possible'] for r in rows),'sequential_5pct_possible_cases':sum(r['sequential_5pct_possible'] for r in rows),'equal_family_mean_global_gain_vs_sequential':statistics.mean(r['mean_global_gain_vs_sequential'] for r in families)};write(OUT/'comparison.json',result)
    lines=['# V126: exhaustive admitted-domain feasibility audit','','This coverage audit follows rediscovery of the prior V42fixed-shortlist bound. It asks whether moving outside that shortlist could make a5%gain possible. All six existing development families and five prefixes each are retained; none is a new holdout. The direction-aware optimum is over the admitted, feature-restricted/subsampled domain, not every possible configuration of the real software. All values come from original recorded benchmark tables, not fresh native execution.','','| Family | Domain rows | Mean maximum gain vs sequential3NN | Joint5%possible /5 | Sequential already global-best /5 |','|---|---:|---:|---:|---:|']
    for r in families:lines.append(f"| {r['system_group']} | {r['domain_size']} | {100*r['mean_global_gain_vs_sequential']:.3f}% | {r['joint_5pct_possible']} | {r['sequential_attains_global_best']} |")
    lines+=['',f"Across30exposed prefixes, {result['joint_5pct_possible_cases']}could in principle gain≥5%against both batch and full sequential3NN if the unrestricted admitted-domain optimum were found; {result['sequential_5pct_possible_cases']}could beat sequential alone by≥5%. Equal-family mean ceiling versus sequential: {100*result['equal_family_mean_global_gain_vs_sequential']:.3f}%. This is hindsight opportunity, not an achieved LLM gain or a learned controller result.",'',f"Actual audit collection: {receipt['new_recorded_acquisitions']}new recorded outcome accesses in {receipt['completed_branches']}coverage branches, {receipt['seconds']:.3f}s, zero model calls. Each branch reuses an existing seed11prefix10 and acquires at most10new outcomes, so no branch exceedsB20. Short final chunks use fewer evaluations and are coverage diagnostics, not competitive policies. Original60prefix outcomes retain their historical cost; the4932remaining outcomes complete the4992-row admitted domains and are covered by the charged journal. Historical control states for all30prefixes are matched to this domain and their labels replayed.",'','The coverage plan was frozen using only existing feature order and prefix IDs before these new accesses. The merged outcome map is evaluator-only. Never provide it, its extrema/ranks, or the hindsight opportunity label to optimizer/LLM/controller inputs. Development feasibility can motivate a new intervention; filtering fresh test cases by their revealed optimum would leak outcomes. Known portfolio references are included when available (not fabricated for missing seeds); primary feasibility covers all30against fixed batch/sequential controls.','','This audit does not establish that an LLM can identify the good configurations, that stochastic proposals beat a cheap optimizer, or that the original benchmark rows have verified equal functional utility. Prior V43/V44uniform/diverse-pool results remain relevant. It does not justify selecting favorable families/seeds for a confirmatory evaluation. No threshold was changed to call an old failure positive; the fixed-pool5%screen remains unattainable.']
    (ROOT/'reports/domain_audit_v126.md').write_text('\n'.join(lines)+'\n');print(json.dumps({'families':families,'joint_5pct_possible_cases':result['joint_5pct_possible_cases'],'sequential_5pct_possible_cases':result['sequential_5pct_possible_cases']},indent=2))
if __name__=='__main__':
    prepare() if '--prepare' in sys.argv else evaluate() if '--evaluate' in sys.argv else collect()
