"""Prospective real-model H2 continuation; explicit new allowance required."""
import argparse,hashlib,json,os,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.h2_v83 import expected,validate
from escalation.h2_v85 import CONFIGS,PRIOR,SEEDS,ARMS,choose,incumbent,guard,messages,vectors,authorize,check_cfg
from escalation.legal_proposals_v66 import LegalProposals
from escalation.receipts_v70 import atomic_json
from escalation.bounded_process_v57 import run
from runtime_h2_v85 import Runtime
from run_planning_v55 import rss
OUT=ROOT/'results/v85_h2_paired'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--approved-envelope-sha256',default='');args=parser.parse_args()
    freeze=ROOT/'reports/protocol_v85.freeze.json';digest=sha(freeze)
    approval=ROOT/'artifacts/study_v85_execution/user_approval.json'
    authorize(read(approval) if approval.exists() else None,digest,args.approved_envelope_sha256)
    cfg=read(ROOT/'configs/study_v85.json');check_cfg(cfg)
    for n,d in read(freeze)['sha256'].items():assert sha(ROOT/n)==d,n
    rss(-1);OUT.mkdir(exist_ok=False);atomic_json(OUT/'authorization.json',read(approval));atomic_json(OUT/'config.json',cfg)
    rt=Runtime(ROOT,OUT,cfg,generation_limit=35,seconds=1800);rows=[];cases=[];stop=None;truth=expected();lock=read(ROOT/'configs/runtime_v83.lock.json')
    env={k:v for k,v in os.environ.items() if k not in ['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS','JDK_JAVA_OPTIONS','CLASSPATH']}
    def acquire(cid,obs,seed,arm,purpose,decision_seconds=0.):
        rt.check();guard(cid,obs,purpose)
        if len(rows)>=115:raise ValueError('Physical trial cap')
        p=OUT/f'trial_{len(rows):03d}';p.mkdir();c=CONFIGS[cid]
        command=[str(ROOT/lock['java']),'-Xmx512m','-XX:ActiveProcessorCount=4','-cp',str(ROOT/lock['jar'])+os.pathsep+str(ROOT/lock['classes']),'H2Probe',str(c['mask']),str(c['recompile']).lower(),str(c['analyze_sample']),str(p)]
        row={'trial':len(rows),'seed':seed,'arm':arm,'purpose':purpose,'logical_evaluation':len(obs)+1,'config_id':cid,'config':c,'status':'charged','command':command,'path':str(p.relative_to(ROOT)),'charged_at_unix':time.time(),'decision_seconds':decision_seconds};rows.append(row);atomic_json(p/'charge.json',row);atomic_json(OUT/'acquisitions.json',rows)
        def monitor(pid):
            memory=rss(pid);scratch=sum(f.stat().st_size for f in p.rglob('*') if f.is_file())
            reason=rt.reason or ('server_exited' if rt.proc.poll() is not None else None) or ('rss_cap' if memory>2*1024**3 else 'scratch_cap' if scratch>128*1024**2 else None)
            return {'rss_bytes':memory,'scratch_bytes':scratch},reason
        row['process']=run(command,cwd=ROOT,log_path=p/'process.log',wall_cap=60,monitor=monitor,env=env);atomic_json(p/'process_receipt.json',row['process'])
        assert row['process']['exit_code']==0 and row['process']['termination_reason'] is None
        row['metrics']=validate(p,c,truth);row['status']='valid';row['answers_sha256']=sha(p/'answers.csv')
        atomic_json(p/'result.json',row);atomic_json(OUT/'acquisitions.json',rows)
        obs.append({'config_id':cid,'query_seconds':row['metrics']['query_seconds'],'physical_trial':row['trial'],'physical_source':'v85'})
        print('validated',row['trial'],'seed',seed,arm,purpose,flush=True)
    def model_choice(session,obs,seed):
        rt.check();folder=OUT/f'request_{seed}_{len(obs)-9}';folder.mkdir();msgs=messages(obs);atomic_json(folder/'messages.json',msgs)
        rendered=rt.api('/apply-template',{'messages':msgs,'add_generation_prompt':True,'chat_template_kwargs':{'enable_thinking':False}})
        tokens=rt.api('/tokenize',{'content':rendered['prompt'],'add_special':False,'parse_special':True})['tokens'];atomic_json(folder/'rendered.json',{'rendered':rendered,'tokens':tokens})
        if len(tokens)+64>4096:raise ValueError('Prompt exceeds context limit')
        legal=session.begin_request();payload={'prompt':rendered['prompt'],'grammar':legal['grammar'],'n_predict':64,'temperature':0,'seed':seed,'cache_prompt':False,'return_tokens':True,'stream':False,'repeat_penalty':1.0}
        atomic_json(folder/'request.json',{'request_id':folder.name,'prepared_at_unix':time.time(),'payload':payload,'eligible_ids':legal['eligible_ids'],'prompt_sha256':hashlib.sha256(rendered['prompt'].encode()).hexdigest()})
        t=time.monotonic()
        try:
            response=rt.generate(payload,folder);atomic_json(folder/'response.json',response)
        except Exception as e:
            decision=session.finish_request(transport_error=repr(e));atomic_json(folder/'decision.json',{**decision,'wall_seconds':time.monotonic()-t,'usage':None,'error':repr(e)});raise
        parsed=session.finish_request(response.get('content'),truncated=bool(response.get('truncated') or response.get('stopped_limit') or response.get('stop_type')=='limit'))
        atomic_json(folder/'decision.json',{**parsed,'wall_seconds':time.monotonic()-t,'usage':{'tokens_predicted':response.get('tokens_predicted'),'tokens_evaluated':response.get('tokens_evaluated')}})
        if not parsed['valid']:raise ValueError('Invalid real model response; no retry or fabricated fallback')
        if response.get('tokens_predicted') is not None and response['tokens_predicted']>64:raise ValueError('Output token cap violation')
        return parsed['selected_id']
    try:
        rt.start()
        for si,seed in enumerate(SEEDS):
            pp=ROOT/f'results/v84_h2_classical/prefix_{seed}.json';prefix=read(pp)['observations'];assert len(prefix)==10
            branches={a:[dict(o) for o in prefix] for a in ['rf_lcb','llm']};branches['prior']=[]
            case={'seed':seed,'prefix_sha256':sha(pp),'branches':branches,'selected':{},'complete':False};cases.append(case);session=LegalProposals(vectors(),[o['config_id'] for o in prefix],count=7)
            for j in range(7):
                for arm in (['rf_lcb','llm'] if (si+j)%2==0 else ['llm','rf_lcb']):
                    t=time.monotonic();cid=choose(branches[arm],'rf_lcb',seed) if arm=='rf_lcb' else model_choice(session,branches[arm],seed)
                    acquire(cid,branches[arm],seed,arm,'search',time.monotonic()-t);atomic_json(OUT/'cases.json',cases)
            selected={a:incumbent(branches[a]) for a in ['rf_lcb','llm']};selected['prior']=PRIOR;case['selected']=selected
            atomic_json(OUT/f'locked_{seed}.json',{'selected':selected,'physical_trials_at_lock':len(rows),'prefix_sha256':sha(pp)})
            for rep in range(3):
                offset=(si+rep)%3
                for arm in ARMS[offset:]+ARMS[:offset]:acquire(selected[arm],branches[arm],seed,arm,'fixed_prior' if arm=='prior' else 'confirmation');atomic_json(OUT/'cases.json',cases)
            assert sha(pp)==case['prefix_sha256'] and session.complete;assert [len(branches[a]) for a in ARMS]==[20,20,3];case['complete']=True;atomic_json(OUT/'cases.json',cases)
    except Exception as e:
        stop=repr(e)
        if rows and rows[-1]['status']=='charged':rows[-1].update(status='failed',error=stop);atomic_json(ROOT/rows[-1]['path']/'failure.json',rows[-1])
        atomic_json(OUT/'failure.json',{'error':stop})
    finally:
        rt.close();atomic_json(OUT/'acquisitions.json',rows);atomic_json(OUT/'cases.json',cases)
        atomic_json(OUT/'summary.json',{'intended_trials':115,'charged_trials':len(rows),'valid_trials':sum(r['status']=='valid' for r in rows),'unattempted_trials':115-len(rows),'completed_seeds':sum(c['complete'] for c in cases),'complete':stop is None and len(rows)==115 and rt.ledger['generation_requests']==35,'stop_reason':stop,'ledger':rt.ledger,'intended_generation_requests':35,'unattempted_generation_requests':35-rt.ledger['generation_requests'],'fallbacks':0,'historical_prefix_physical_trials':50,'planned_logical_rf_llm_evaluations':200,'planned_fixed_prior_evaluations':15})
    if stop:raise RuntimeError(stop)
if __name__=='__main__':main()
