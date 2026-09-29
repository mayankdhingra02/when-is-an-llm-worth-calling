"""Frozen development analysis. Selection is sealed before target access."""
import json,time,statistics,csv
from functools import lru_cache
from collect_smollm_v47 import ROOT,read,write,append,sha,now
import sys
sys.path.insert(0,str(ROOT/'src'))
from pointwise_v123 import IDS,parse,choose,messages
from escalation.core import State
from escalation.finite_v6 import load_candidates
from escalation.transfer_v41 import restrict,rank,IndexedOracle,best,relative_gain
OUT=ROOT/'results/v123_analysis'
CONTROLS=['batch_3nn','full_sequential_3nn','random_full','presentation_first10','single_portfolio']
PRIMARY=['batch_3nn','full_sequential_3nn','presentation_first10']
def frozen():
    for f in ['reports/protocol_v123.freeze.json','artifacts/study_v123/inputs.freeze.json']:
        for n,h in read(ROOT/f)['sha256'].items():assert sha(ROOT/n)==h,n

@lru_cache(maxsize=3)
def candidates(dataset):
    spec=next(s for s in read(ROOT/'data/manifest_v41.json')['datasets'] if s['id']==dataset)
    c,subset=restrict(load_candidates(spec),spec['fixed_features']);assert subset==spec['subset']
    return spec,c

def refpaths(key):
    return {**{m:f'results/v41_transfer/arms/{key}_{m}.json' for m in CONTROLS[:3]},'presentation_first10':f'results/v41_models/0.5/arms/{key}.json','single_portfolio':f'results/v115_portfolio/arms/{key}.json'}

def references(job,p,direction):
    refs={}
    for mode,path in refpaths(job['key']).items():
        state=read(ROOT/path)['state'];assert state['ids'][:10]==p['state']['ids'] and state['labels'][:10]==p['state']['labels'] and len(set(state['ids']))==20
        if mode=='presentation_first10':assert state['ids'][10:]==[p['pool']['mapping'][i] for i in IDS[:10]]
        refs[mode]=best(State(**state),direction)
    return refs

def scores_and_diagnostics():
    raw=[json.loads(x) for x in (ROOT/'results/v123_pointwise/responses.jsonl').read_text().splitlines()];assert len({r['key'] for r in raw})==len(raw)
    scores={}
    for r in raw:
        try:scores[r['key']]=parse(r['response'])
        except ValueError:pass
    cfg=read(ROOT/'configs/study_v123.json');rows=[]
    for job in read(ROOT/'artifacts/study_v123/cases.json'):
        key=job['key'];changes=[];stability=[]
        for condition,ids,margin in [('loss_blind',IDS[:10],cfg['loss_change_margin']),('observations_reversed',IDS[:3],cfg['order_stability_margin'])]:
            for i in ids:
                a=scores.get(f'{key}_normal_{i}');b=scores.get(f'{key}_{condition}_{i}');delta=None if a is None or b is None else abs(a-b)
                record={'candidate_id':i,'normal':a,'intervention':b,'absolute_change':delta}
                if condition=='loss_blind':record['changed']=delta is not None and delta+1e-12>=margin;changes.append(record)
                else:record['stable']=delta is not None and delta<=margin+1e-12;stability.append(record)
        rows.append({'key':key,'system_group':job['system_group'],'loss_probes':changes,'order_probes':stability,'responsive':sum(x['changed'] for x in changes)>=cfg['minimum_loss_changes_per_family']})
    responsive=sum(r['responsive'] for r in rows);stable=sum(p['stable'] for r in rows for p in r['order_probes'])
    return scores,{'families':rows,'responsive_families':responsive,'stable_order_probes':stable,'loss_criterion_met':responsive>=cfg['minimum_responsive_families'],'order_criterion_met':stable>=cfg['minimum_stable_order_probes'],'intended_requests':99,'returned_responses':len(raw),'valid_scores':len(scores),'unknown_or_invalid_scores':99-len(scores)}

def selection(job,scores):
    p=read(ROOT/job['prefix']);normal={i:scores[f"{job['key']}_normal_{i}"] for i in IDS if f"{job['key']}_normal_{i}" in scores}
    if len(normal)==20:ids,rows=choose(normal,p);fallback=False
    else:
        _,c=candidates(job['dataset']);rows=rank(c,State(**p['state']),p['pool']['ranked'])[:10];inverse={v:k for k,v in p['pool']['mapping'].items()};ids=[inverse[r] for r in rows];fallback=True
    assert len(set(rows))==10 and not set(rows)&set(p['state']['ids'])
    return {**job,'selected_ids':ids,'selected_rows':rows,'scores':normal,'fallback':fallback,'unique_scores':len(set(normal.values())),'matches_first10_set':set(ids)==set(IDS[:10]),'prefix_sha256':sha(ROOT/job['prefix'])}

def evaluate():
    frozen();OUT.mkdir(exist_ok=False);scores,diagnostics=scores_and_diagnostics();write(OUT/'diagnostics.json',diagnostics)
    choices=[selection(j,scores) for j in read(ROOT/'artifacts/study_v123/cases.json')]
    for r in choices:write(OUT/'choices'/f"{r['key']}.json",r)
    write(OUT/'selection_seal.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'results/v123_pointwise/responses.jsonl',OUT/'diagnostics.json']+sorted((OUT/'choices').glob('*.json'))}})
    start=time.monotonic();count=0;arms=[];error=None
    try:
        for choice in choices:
            spec,c=candidates(choice['dataset']);p=read(ROOT/choice['prefix']);state=State(**p['state']).clone();oracle=IndexedOracle(spec,c,p['state'],lambda e:append(OUT/'acquisitions.jsonl',{'key':choice['key'],**e}));t=time.monotonic()
            for i in choice['selected_rows']:
                if count>=30 or time.monotonic()-start>180:raise RuntimeError('Evaluation stage cap')
                count+=1;state.observe(i,oracle.acquire(i),c.directions)
            refs=references(choice,p,spec['direction']);target=best(state,spec['direction']);r={**choice,'state':state.record(),'direction':spec['direction'],'target':target,'references':refs,'gains':{m:relative_gain(v,target,spec['direction']) for m,v in refs.items()},'continuation_seconds':time.monotonic()-t};write(OUT/'arms'/f"{r['key']}.json",r);arms.append(r)
    except Exception as e:error=repr(e)
    finally:write(OUT/'summary.json',{'complete':error is None and len(arms)==3,'error':error,'intended_cases':3,'cases':arms,'actual_new_acquisitions':count,'stage_seconds':time.monotonic()-start})
    if error:raise RuntimeError(error)
    print('Acquired',count,'recorded outcomes from3frozen prefixes')

def report():
    frozen();s=read(OUT/'summary.json');assert s['complete'];rows=s['cases'];d=read(OUT/'diagnostics.json');ledger=read(ROOT/'results/v123_pointwise/ledger.json');raw=[json.loads(x) for x in (ROOT/'results/v123_pointwise/responses.jsonl').read_text().splitlines()]
    contrasts={m:{'mean':statistics.mean(r['gains'][m] for r in rows),'wins':sum(r['gains'][m]>1e-12 for r in rows),'ties':sum(abs(r['gains'][m])<=1e-12 for r in rows),'losses':sum(r['gains'][m]<-1e-12 for r in rows)} for m in CONTROLS}
    joint=sum(not r['fallback'] and all(r['gains'][m]>=.05 for m in PRIMARY) for r in rows)
    quality=joint>0 and all(contrasts[m]['mean']>0 for m in PRIMARY);normalvalid=sum(not r['fallback'] for r in rows)
    usage={}
    for field in ['tokens_predicted','tokens_evaluated']:
        vals=[r['response'].get(field) for r in raw];usage[field]={'observed_sum':sum(v for v in vals if type(v) is int),'missing_responses':99-sum(type(v) is int for v in vals)}
    normal=[r for r in raw if '_normal_' in r['key']];blind=[r for r in raw if '_loss_blind_' in r['key']];reverse=[r for r in raw if '_observations_reversed_' in r['key']]
    cost={'actual':{**ledger,'usage':usage,'new_recorded_acquisitions':s['actual_new_acquisitions'],'historical_prefix_labels':30,'historical_comparator_arms':15},'estimated_deployment':{'requests_per_escalation':20,'allocated_output_tokens_per_escalation':320,'objective_budget':20,'checkpoint':10,'measured_normal_request_seconds_total':sum(r['wall_seconds'] for r in normal),'normal_request_seconds_by_family':{j['key']:sum(r['wall_seconds'] for r in normal if r['key'].startswith(j['key']+'_normal_')) for j in rows},'note':'Request timing excludes cold-start/setup; normal calls interleaved with probes. No dollar or native objective-time conversion.'},'diagnostic_request_counts':{'loss_blind':len(blind),'observation_order':len(reverse)}}
    result={'contrasts':contrasts,'normal_valid_cases':normalvalid,'fallbacks':3-normalvalid,'joint_5pct_wins':joint,'quality_criterion_met':quality,'screen_passed':normalvalid==3 and quality and d['loss_criterion_met'] and d['order_criterion_met'],'diagnostics':d,'cost':cost};write(OUT/'comparison.json',result)
    lines=['# V123: pointwise numeric surrogate development screen','','A materially different interface asks Qwen3-8B Q4_K_M for one scalar prediction per configuration, without candidate IDs or a list to choose from. Twenty predictions select ten configurations from the same saved shortlist. Three previously exposed families, seed11 each, were chosen alphabetically before inference. This is development screening, not held-out validation or a full LLAMBO replication. No controller was refitted.','','| Control | Mean relative gain | Wins/ties/losses |','|---|---:|---:|---:|']
    for m,v in contrasts.items():lines.append(f"| {m} | {100*v['mean']:.3f}% | {v['wins']}/{v['ties']}/{v['losses']} |")
    lines+=['',f"Normal valid branches: {normalvalid}/3. Joint≥5% wins versus batch3NN, sequential3NN and first-ten: {joint}/3. Loss responsiveness: {d['responsive_families']}/3 families meet≥3 of10 changed predictions by≥0.02 (requires2). Observation-order stability: {d['stable_order_probes']}/9 paired probes differ by≤0.05 (requires7). Frozen combined screening criterion: {'MET' if result['screen_passed'] else 'NOT MET'}.",'','| Family | Distinct predictions | Selected IDs (provenance only) | Batch gain | Sequential gain | First-ten gain | Portfolio gain |','|---|---:|---|---:|---:|---:|---:|']
    for r in rows:lines.append(f"| {r['system_group']} | {r['unique_scores']} | {''.join(r['selected_ids'])} | {100*r['gains']['batch_3nn']:.3f}% | {100*r['gains']['full_sequential_3nn']:.3f}% | {100*r['gains']['presentation_first10']:.3f}% | {100*r['gains']['single_portfolio']:.3f}% |")
    lines+=['',f"Actual collection: {ledger['generation_requests']} charged real local requests, {usage['tokens_predicted']['observed_sum']} observed generated tokens, {usage['tokens_predicted']['missing_responses']} missing generated-token receipts, {ledger['allocated_output_tokens']} allocated tokens, {s['actual_new_acquisitions']} new recorded acquisitions; {ledger['stage_seconds']:.3f}s lifecycle and {ledger['peak_server_rss_bytes']:,}bytes peak sampled serverRSS. No retries, downloads or external spending. Each logical arm isB20 from the identical acquired prefix10; old prefixes and15 comparator branches were reused, with their historical collection costs retained. Diagnostic interventions add39requests; deployment would need20normal requests per escalation plus setup, not99.",'','All99 intended requests and all three intended branches remain in the denominator. Missing/invalid scores require batch3NN fallback; no partial-score cherry-picking. Raw outputs, rendered templates, tokenization, generation settings, timestamps, model revision/blob hash, precollection and pre-acquisition seals remain saved. Fixed ID-order tie breaking is an explicit free rule, not evidence of model reasoning. Scores are clipped to[0,1] and quantized to0.01; this may discard useful ranking information. The order probes cover only3candidates per family. Loss removal is a responsiveness diagnostic, not a demand that every individual prediction must change. Both conditions share greedy sampling, with no cross-hardware determinism claim.','','Interpretation is conditional on these recorded datasets, fixed shortlist, prefix, model and adapter. Three exposed families and one seed each cannot support a generalizable router or a Q2-readiness claim. Original source correctness/noise and redistribution limitations remain unchanged. Do not tune this prompt on the measured outcomes and relabel it confirmatory. Prior broad model/decoder experiments, including V92/V93 and V103, remain relevant negative evidence.','','Evidence: reports/protocol_v123.md and its freeze; artifacts/study_v123/jobs.json; results/v123_pointwise/responses.jsonl and generation_starts.jsonl; results/v123_analysis/diagnostics.json, selection_seal.json, acquisitions.jsonl, arms and comparison.json. Safe replay: scripts/verify_pointwise_v123.py, then scripts/analyze_pointwise_v123.py --report.']
    (ROOT/'reports/pointwise_v123.md').write_text('\n'.join(lines)+'\n')
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained');xs=list(range(3));width=.19
    for k,m in enumerate(PRIMARY+['single_portfolio']):axes[0].bar([x+(k-1.5)*width for x in xs],[100*r['gains'][m] for r in rows],width,label=m)
    axes[0].axhline(0,color='black',linewidth=.7);axes[0].set_xticks(xs,[r['system_group'] for r in rows],rotation=15);axes[0].set_ylabel('Relative gain (%)');axes[0].legend(fontsize=7);axes[0].set_title('Recorded optimization outcome')
    for k,r in enumerate(d['families']):
        changes=[p['absolute_change'] for p in r['loss_probes']];st=[p['absolute_change'] for p in r['order_probes']];axes[1].scatter([k-.12]*len(changes),changes,marker='o',color='tab:blue',alpha=.6,label='Loss removal' if k==0 else None);axes[1].scatter([k+.12]*len(st),st,marker='x',color='tab:orange',label='Reverse observations' if k==0 else None)
    axes[1].set_xticks(xs,[r['system_group'] for r in rows],rotation=15);axes[1].set_ylabel('Absolute change in predicted loss');axes[1].legend(fontsize=8);axes[1].set_title('Input intervention probes');fig.suptitle('V123: three exposed development families, one prefix each')
    fig.savefig(OUT/'pointwise.png',dpi=160);plt.close(fig);print(json.dumps({k:result[k] for k in ['contrasts','screen_passed','normal_valid_cases','joint_5pct_wins']},indent=2))
if __name__=='__main__':
    import sys
    report() if '--report' in sys.argv else evaluate()
