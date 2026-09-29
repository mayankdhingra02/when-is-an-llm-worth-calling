"""Frozen paired EI/mean evaluation; no new hidden labels until choice seal."""
import json,time,statistics,csv,sys
from collect_smollm_v47 import ROOT,read,write,append,sha,now
sys.path.insert(0,str(ROOT/'src'))
from analyze_pointwise_v123 import candidates,references,CONTROLS,PRIMARY
from surrogate_v124 import IDS,SEEDS,parse,predictions,choose
from escalation.core import State
from escalation.transfer_v41 import rank,IndexedOracle,best,relative_gain
OUT=ROOT/'results/v124_analysis'
def frozen():
    for name in ['reports/protocol_v124.freeze.json','artifacts/study_v124/inputs.freeze.json']:
        for n,h in read(ROOT/name)['sha256'].items():assert sha(ROOT/n)==h,n

def make_choices():
    jobs=read(ROOT/'artifacts/study_v124/jobs.json');jm={j['key']:j for j in jobs};responses=[json.loads(x) for x in (ROOT/'results/v124_surrogate/responses.jsonl').read_text().splitlines()];assert len({r['key'] for r in responses})==len(responses);scores={};invalid=[]
    for r in responses:
        assert r['key'] in jm
        try:scores[r['key']]=parse(r['response'])
        except ValueError:invalid.append(r['key'])
    choices=[]
    for j in read(ROOT/'artifacts/study_v124/cases.json'):
        p=read(ROOT/j['prefix']);values={i:[scores[f"{j['key']}_{i}_{seed}"] for seed in SEEDS if f"{j['key']}_{i}_{seed}" in scores] for i in IDS};valid=sum(len(v) for v in values.values());stats=predictions(values,p) if all(len(v)>=2 for v in values.values()) else None
        for mode in ['ei','mean']:
            if stats is not None:ids,rows=choose(stats,p,mode)
            else:
                _,c=candidates(j['dataset']);rows=rank(c,State(**p['state']),p['pool']['ranked'])[:10];inverse={v:k for k,v in p['pool']['mapping'].items()};ids=[inverse[i] for i in rows]
            choices.append({**j,'base_key':j['key'],'key':j['key']+'_'+mode,'mode':mode,'valid_predictions':valid,'invalid_or_missing_predictions':60-valid,'fallback':stats is None,'statistics':stats,'selected_ids':ids,'selected_rows':rows,'prefix_sha256':sha(ROOT/j['prefix']),'matches_first10_set':set(ids)==set(IDS[:10])})
    return choices,{'intended_requests':180,'returned':len(responses),'valid_scores':len(scores),'invalid_returned':invalid,'unreturned_requests':180-len(responses),'negative_predictions':sum(v<0 for v in scores.values())}

def evaluate():
    frozen();OUT.mkdir(exist_ok=False);choices,diagnostics=make_choices();write(OUT/'diagnostics.json',diagnostics)
    for c in choices:write(OUT/'choices'/f"{c['key']}.json",c)
    write(OUT/'selection_seal.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'results/v124_surrogate/responses.jsonl',OUT/'diagnostics.json']+sorted((OUT/'choices').glob('*.json'))}})
    count=0;start=time.monotonic();arms=[];error=None
    try:
        for choice in choices:
            spec,c=candidates(choice['dataset']);p=read(ROOT/choice['prefix']);state=State(**p['state']).clone();oracle=IndexedOracle(spec,c,p['state'],lambda e:append(OUT/'acquisitions.jsonl',{'key':choice['key'],**e}))
            for i in choice['selected_rows']:
                if count>=60 or time.monotonic()-start>180:raise RuntimeError('Acquisition stage cap')
                count+=1;state.observe(i,oracle.acquire(i),c.directions)
            refs=references({**choice,'key':choice['base_key']},p,spec['direction']);target=best(state,spec['direction']);r={**choice,'target':target,'references':refs,'gains':{m:relative_gain(v,target,spec['direction']) for m,v in refs.items()},'state':state.record(),'direction':spec['direction']};arms.append(r);write(OUT/'arms'/f"{r['key']}.json",r)
    except Exception as e:error=repr(e)
    finally:write(OUT/'summary.json',{'complete':error is None and len(arms)==6,'error':error,'intended_arms':6,'independent_families':3,'cases':arms,'actual_new_acquisitions':count,'evaluation_seconds':time.monotonic()-start})
    if error:raise RuntimeError(error)
    print('Acquired',count,'recorded outcomes; six paired B20 branches')

def report():
    frozen();s=read(OUT/'summary.json');assert s['complete'];d=read(OUT/'diagnostics.json');ledger=read(ROOT/'results/v124_surrogate/ledger.json');raw=[json.loads(x) for x in (ROOT/'results/v124_surrogate/responses.jsonl').read_text().splitlines()];comparisons={}
    for mode in ['ei','mean']:
        rows=[r for r in s['cases'] if r['mode']==mode];contrasts={m:{'mean':statistics.mean(r['gains'][m] for r in rows),'wins':sum(r['gains'][m]>1e-12 for r in rows),'ties':sum(abs(r['gains'][m])<=1e-12 for r in rows),'losses':sum(r['gains'][m]<-1e-12 for r in rows)} for m in CONTROLS};joint=sum(not r['fallback'] and all(r['gains'][m]>=.05 for m in PRIMARY) for r in rows);passed=all(not r['fallback'] for r in rows) and joint>0 and all(contrasts[m]['mean']>0 for m in PRIMARY)
        comparisons[mode]={'contrasts':contrasts,'joint_5pct_wins':joint,'screen_passed':passed,'fallbacks':sum(r['fallback'] for r in rows)}
    effect=[]
    for j in read(ROOT/'artifacts/study_v124/cases.json'):
        a=next(r for r in s['cases'] if r['base_key']==j['key'] and r['mode']=='ei');b=next(r for r in s['cases'] if r['base_key']==j['key'] and r['mode']=='mean');effect.append({'key':j['key'],'same_selected_set':set(a['selected_rows'])==set(b['selected_rows']),'ei_gain_over_mean':relative_gain(b['target'],a['target'],a['direction'])})
    usage={f:{'observed_sum':sum(r['response'][f] for r in raw if type(r['response'].get(f)) is int),'missing_receipts':180-sum(type(r['response'].get(f)) is int for r in raw)} for f in ['tokens_predicted','tokens_evaluated']}
    result={'comparisons':comparisons,'primary_screen_passed':comparisons['ei']['screen_passed'],'diagnostics':d,'ei_vs_mean':effect,'cost':{'ledger':ledger,'usage':usage,'new_recorded_acquisitions':s['actual_new_acquisitions'],'deployment_requests_per_escalation':60,'deployment_allocated_output_tokens':1920,'deployment_evaluations':20,'same_responses_reused_by_mean_ablation':True,'normal_request_seconds_by_family':{j['key']:sum(r['wall_seconds'] for r in raw if r['key'].startswith(j['key']+'_')) for j in read(ROOT/'artifacts/study_v124/cases.json')}}};write(OUT/'comparison.json',result)
    lines=['# V124: source-grounded local stochastic surrogate adaptation','','Three exposed development systems, one saved seed11 prefix each. Qwen3-8B Q4_K_M predicts raw performance three times per candidate, temperature0.7/top_p0.95, no numeric clipping or grammar. Population mean/standard deviation feed expected improvement (EI); ranking by mean is a predeclared ablation using the same real responses. Each selects10of20saved candidates from prefix10. This is a compact software-context, local-model, batch adaptation, not a full LLAMBO replication.','','| Mode | Control | Mean gain | Wins/ties/losses |','|---|---|---:|---|']
    for mode,x in comparisons.items():
        for m,v in x['contrasts'].items():lines.append(f"| {mode} | {m} | {100*v['mean']:.3f}% | {v['wins']}/{v['ties']}/{v['losses']} |")
    lines+=['',f"Primary EI screening criterion: {'MET' if result['primary_screen_passed'] else 'NOT MET'}; joint≥5%wins {comparisons['ei']['joint_5pct_wins']}/3. Mean ablation screen: {comparisons['mean']['screen_passed']}. This is descriptive development screening, not significance or held-out generalization.",'','| Family | Mode | Valid predictions /60 | Selected IDs (not prompt input) | Target |','|---|---|---:|---|---:|']
    for r in s['cases']:lines.append(f"| {r['system_group']} | {r['mode']} | {r['valid_predictions']} | {''.join(r['selected_ids'])} | {r['target']:.8g} |")
    lines+=['',f"Actual collection: {ledger['generation_requests']}charged local requests, {d['returned']}returned, {d['valid_scores']}valid scalar predictions, {len(d['invalid_returned'])}invalid returned responses, {d['unreturned_requests']}unreturned. Negative predictions: {d['negative_predictions']}; these are preserved, not clipped. At least2of3valid samples per candidate are required; otherwise both arms use recorded batch3NN fallback. Valid samples are aggregated without imputing malformed samples; every failed sample stays in the denominator. No retries or outcome-based response selection.",'',f"Generated tokens observed: {usage['tokens_predicted']['observed_sum']}; missing receipts: {usage['tokens_predicted']['missing_receipts']}; allocated: {ledger['allocated_output_tokens']}. Lifecycle {ledger['stage_seconds']:.3f}s, peak sampled serverRSS {ledger['peak_server_rss_bytes']:,}bytes. New recorded acquisitions: {s['actual_new_acquisitions']}. Both branches were charged separately even if their selected sets coincide. Deployment would need60requests and10newobjective evaluations per escalation; mean/EI reuse here is research analysis, not free model deployment. Startup and metadata are extra. No native-time/dollar benefit claim.",'','The model, JSON serialization, raw target contract, stochastic decoding and batch acquisition differ from V123; this is not a one-factor causal ablation. Three stochastic samples are a noisy uncertainty estimate. Prediction-derived dispersion is unavailable before calling the model, so it cannot be a cheap router feature. The same development families have extensive previous exposure; no new holdout, controller training or novelty claim. Original source correctness/noise/licensing limitations remain. The mean ablation cannot replace EI as the primary result after inspecting outcomes.','','Owner code/license hashes: artifacts/sources/v124/manifest.json. Protocol and mapping: reports/protocol_v124.md and freeze. Real templates/requests/responses: results/v124_surrogate. Choices and source journals: results/v124_analysis. Prior positive and negative outcomes remain immutable.']
    (ROOT/'reports/surrogate_v124.md').write_text('\n'.join(lines)+'\n')
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
    for ax,mode in zip(axes,['ei','mean']):
        rows=[r for r in s['cases'] if r['mode']==mode];w=.19
        for k,m in enumerate(PRIMARY+['single_portfolio']):ax.bar([i+(k-1.5)*w for i in range(3)],[100*r['gains'][m] for r in rows],w,label=m)
        ax.set_xticks(range(3),[r['system_group'] for r in rows],rotation=15);ax.axhline(0,color='black',linewidth=.7);ax.set_ylabel('Relative gain (%)');ax.set_title(mode.upper());ax.legend(fontsize=7)
    fig.suptitle('V124: three exposed development families, one prefix each');fig.savefig(OUT/'surrogate.png',dpi=160);plt.close(fig);print(json.dumps({'comparisons':comparisons,'ei_vs_mean':effect},indent=2))
if __name__=='__main__':report() if '--report' in sys.argv else evaluate()
