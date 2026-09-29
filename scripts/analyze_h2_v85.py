"""Validate actual V85 model/native traces and replay acquired-only policies."""
import hashlib,json,math,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.h2_v83 import expected,validate
from escalation.h2_v85 import CONFIGS,PRIOR,SEEDS,ARMS,choose,incumbent,messages,vectors,authorize,check_cfg
from escalation.legal_proposals_v66 import LegalProposals

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def analyze():
    raw=ROOT/'results/v85_h2_paired';s=read(raw/'summary.json');rows=read(raw/'acquisitions.json');cases=read(raw/'cases.json');truth=expected();lock=read(ROOT/'configs/runtime_v83.lock.json');cfg=read(raw/'config.json');check_cfg(cfg)
    freeze=ROOT/'reports/protocol_v85.freeze.json'
    for n,d in read(freeze)['sha256'].items():assert sha(ROOT/n)==d,n
    authorize(read(raw/'authorization.json'),sha(freeze),sha(freeze))
    assert s['complete'] and s['stop_reason'] is None and s['charged_trials']==s['valid_trials']==s['intended_trials']==len(rows)==115 and s['unattempted_trials']==0
    assert s['completed_seeds']==len(cases)==5 and s['intended_generation_requests']==s['ledger']['generation_requests']==35 and s['unattempted_generation_requests']==s['fallbacks']==0
    ledger=s['ledger'];assert read(raw/'ledger.json')==ledger and ledger['retries']==ledger['external_spend_usd']==0 and ledger['seconds']<1800 and ledger['resource_stop_reason'] is None and ledger['server_exit_code']==0 and ledger['peak_server_rss_bytes']<=8*1024**3
    assert read(raw/'runtime.json')['command']==read(ROOT/'artifacts/study_v78/runtime_plan.json')['command']
    for i,r in enumerate(rows):
        p=raw/f'trial_{i:03d}';c=CONFIGS[r['config_id']];assert r['trial']==i and r['config']==c and r['status']=='valid' and r['path']==str(p.relative_to(ROOT))
        cmd=[str(ROOT/lock['java']),'-Xmx512m','-XX:ActiveProcessorCount=4','-cp',str(ROOT/lock['jar'])+':'+str(ROOT/lock['classes']),'H2Probe',str(c['mask']),str(c['recompile']).lower(),str(c['analyze_sample']),str(p)]
        assert r['command']==cmd
        charge=read(p/'charge.json');assert charge['status']=='charged'
        for k in charge:
            if k!='status':assert charge[k]==r[k],(i,k)
        receipt=read(p/'process_receipt.json');assert receipt==r['process'] and receipt['exit_code']==0 and receipt['termination_reason'] is None and receipt['wall_seconds']<60
        assert receipt['sampled_maxima']['rss_bytes']<2*1024**3 and receipt['sampled_maxima']['scratch_bytes']<128*1024**2
        assert validate(p,c,truth)==r['metrics'] and sha(p/'answers.csv')==r['answers_sha256'] and read(p/'result.json')==r
        assert math.isfinite(r['metrics']['query_seconds']) and r['metrics']['query_seconds']>0
    cursor=0;request_counter=0;usage=[];results=[];historical_rows=read(ROOT/'results/v84_h2_classical/acquisitions.json')
    def consume(seed,arm,purpose,cid,obs):
        nonlocal cursor
        r=rows[cursor];assert (r['seed'],r['arm'],r['purpose'],r['config_id'],r['logical_evaluation'])==(seed,arm,purpose,cid,len(obs)+1)
        obs.append({'config_id':cid,'query_seconds':r['metrics']['query_seconds'],'physical_trial':cursor,'physical_source':'v85'});cursor+=1
    def reconstruct_model(session,obs,seed):
        nonlocal request_counter
        p=raw/f'request_{seed}_{len(obs)-9}';request=read(p/'request.json');rendered=read(p/'rendered.json');response=read(p/'response.json');decision=read(p/'decision.json');msgs=messages(obs)
        assert read(p/'messages.json')==msgs and all(m['content'] in rendered['rendered']['prompt'] for m in msgs)
        assert len(rendered['tokens'])+64<=4096 and request['prompt_sha256']==hashlib.sha256(rendered['rendered']['prompt'].encode()).hexdigest()
        legal=session.begin_request();assert request['eligible_ids']==legal['eligible_ids']
        expected_payload={'prompt':rendered['rendered']['prompt'],'grammar':legal['grammar'],'n_predict':64,'temperature':0,'seed':seed,'cache_prompt':False,'return_tokens':True,'stream':False,'repeat_penalty':1.0}
        assert request['payload']==expected_payload and request['request_id']==p.name
        request_counter+=1;attempt=read(p/'attempt_started.json');assert attempt['generation_number']==request_counter and attempt['started_at_unix']>=request['prepared_at_unix']
        parsed=session.finish_request(response.get('content'),truncated=bool(response.get('truncated') or response.get('stopped_limit') or response.get('stop_type')=='limit'))
        assert parsed['valid'] and all(decision[k]==v for k,v in parsed.items()) and decision['wall_seconds']>0
        u={'tokens_predicted':response.get('tokens_predicted'),'tokens_evaluated':response.get('tokens_evaluated')};assert decision['usage']==u
        assert u['tokens_predicted'] is None or 0<=u['tokens_predicted']<=64
        usage.append(u);return parsed['selected_id']
    for si,seed in enumerate(SEEDS):
        case=cases[si];assert case['seed']==seed and case['complete'];pp=ROOT/f'results/v84_h2_classical/prefix_{seed}.json';prefix=read(pp)['observations'];assert sha(pp)==case['prefix_sha256'] and len(prefix)==10
        prefix_cost=0.
        for o in prefix:
            r=historical_rows[o['physical_trial']];assert r['seed']==seed and r['arm']=='prefix' and r['config_id']==o['config_id'] and r['metrics']['query_seconds']==o['query_seconds']
            prefix_cost+=r['process']['wall_seconds']+r['decision_seconds']
        branches={a:[dict(o) for o in prefix] for a in ['rf_lcb','llm']};branches['prior']=[];session=LegalProposals(vectors(),[o['config_id'] for o in prefix],count=7)
        for j in range(7):
            for arm in (['rf_lcb','llm'] if (si+j)%2==0 else ['llm','rf_lcb']):
                cid=choose(branches[arm],'rf_lcb',seed) if arm=='rf_lcb' else reconstruct_model(session,branches[arm],seed)
                consume(seed,arm,'search',cid,branches[arm])
        selected={a:incumbent(branches[a]) for a in ['rf_lcb','llm']};selected['prior']=PRIOR
        assert case['selected']==selected and read(raw/f'locked_{seed}.json')=={'selected':selected,'physical_trials_at_lock':cursor,'prefix_sha256':sha(pp)}
        for rep in range(3):
            offset=(si+rep)%3
            for arm in ARMS[offset:]+ARMS[:offset]:consume(seed,arm,'fixed_prior' if arm=='prior' else 'confirmation',selected[arm],branches[arm])
        assert session.complete and branches==case['branches'] and [len(branches[a]) for a in ARMS]==[20,20,3]
        arms={}
        for arm in ARMS:
            new=[rows[o['physical_trial']] for o in branches[arm] if o.get('physical_source')=='v85'];conf=new[-3:];t=[r['metrics']['query_seconds'] for r in conf];med=statistics.median(t);index=statistics.median(r['metrics']['index_and_analyze_seconds'] for r in conf);spread=(max(t)-min(t))/med
            newcost=sum(r['process']['wall_seconds']+r['decision_seconds'] for r in new);tuning=newcost+(prefix_cost if arm!='prior' else 0)+(ledger['startup_seconds'] if arm=='llm' else 0)
            arms[arm]={'config_id':selected[arm],'config':CONFIGS[selected[arm]],'confirmation_seconds':t,'median_seconds':med,'range_over_median':spread,'precision_pass':med>=.1 and spread<=.2,'logical_evaluations':len(branches[arm]),'new_physical_evaluations':len(new),'selection_seconds':sum(r['decision_seconds'] for r in new),'median_index_analyze_seconds':index,'actual_new_branch_collection_seconds':newcost,'modeled_branch_tuning_seconds_including_historical_prefix':tuning,'index_plus_query_seconds':{str(k):index+k*med for k in [1,10,100,1000]},'modeled_tune_then_serve_seconds':{str(k):tuning+index+k*med for k in [1,10,100,1000]}}
        llm=arms['llm']
        for control in ['rf_lcb','prior']:
            llm['gain_vs_'+control]=1-llm['median_seconds']/arms[control]['median_seconds'];llm['material_gain_vs_'+control]=llm['gain_vs_'+control]>=.1;llm['comparison_precision_vs_'+control]=llm['precision_pass'] and arms[control]['precision_pass']
        results.append({'seed':seed,'arms':arms,'historical_prefix_collection_seconds':prefix_cost,'hindsight_best_rf_llm_median_seconds':min(arms[a]['median_seconds'] for a in ['rf_lcb','llm']),'hindsight_is_deployable':False})
    assert cursor==115 and request_counter==35 and len(list(raw.glob('request_*')))==35 and ledger['http_requests']>=3*35+1
    return {'complete':True,'independent_system_groups':1,'cases':results,'new_physical_trials':115,'historical_prefix_physical_trials':50,'logical_rf_llm_evaluations':200,'logical_prior_evaluations':15,'checked_scored_answers':115*6144,'generation_requests':35,'http_requests':ledger['http_requests'],'usage':{k:{'known_sum':sum(u[k] for u in usage if u[k] is not None),'unknown_requests':sum(u[k] is None for u in usage)} for k in ['tokens_evaluated','tokens_predicted']},'actual_native_seconds':sum(r['process']['wall_seconds'] for r in rows),'actual_selection_seconds':sum(r['decision_seconds'] for r in rows),'actual_stage_seconds':ledger['seconds'],'model_startup_seconds':ledger['startup_seconds'],'scope':'exposed one-family development adaptation; no generalization or learned-router claim'}
def main():
    data=analyze();out=ROOT/'results/v85_h2_analysis';out.mkdir(exist_ok=False);(out/'summary.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps({k:v for k,v in data.items() if k!='cases'},indent=2))
if __name__=='__main__':main()
