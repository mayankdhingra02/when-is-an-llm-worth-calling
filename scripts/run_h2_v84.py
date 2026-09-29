"""Bounded native classical H2 collection; zero model access."""
import hashlib,json,os,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.h2_v83 import expected,validate
from escalation.h2_v84 import CONFIGS,PRIOR,SEEDS,ARMS,choose,prefix_choice,incumbent,guard
from escalation.bounded_process_v57 import run
from escalation.receipts_v70 import atomic_json
from run_planning_v55 import rss

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    for n,d in json.loads((ROOT/'reports/protocol_v84.freeze.json').read_text())['sha256'].items():assert sha(ROOT/n)==d,n
    rss(-1);out=ROOT/'results/v84_h2_classical';out.mkdir(exist_ok=False)
    lock=json.loads((ROOT/'configs/runtime_v83.lock.json').read_text());truth=expected();rows=[];cases=[];start=time.monotonic();stop=None
    env={k:v for k,v in os.environ.items() if k not in ['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS','JDK_JAVA_OPTIONS','CLASSPATH']}
    def acquire(cid,obs,seed,arm,purpose,decision_seconds=0.):
        guard(cid,obs,purpose)
        if len(rows)>=165 or time.monotonic()-start>1725:raise TimeoutError('Stage launch limit')
        p=out/f'trial_{len(rows):03d}';p.mkdir();c=CONFIGS[cid]
        command=[str(ROOT/lock['java']),'-Xmx512m','-XX:ActiveProcessorCount=4','-cp',str(ROOT/lock['jar'])+os.pathsep+str(ROOT/lock['classes']),'H2Probe',str(c['mask']),str(c['recompile']).lower(),str(c['analyze_sample']),str(p)]
        row={'trial':len(rows),'seed':seed,'arm':arm,'purpose':purpose,'logical_evaluation':len(obs)+1,'config_id':cid,'config':c,'status':'charged','command':command,'path':str(p.relative_to(ROOT)),'charged_at_unix':time.time(),'decision_seconds':decision_seconds};rows.append(row);atomic_json(p/'charge.json',row);atomic_json(out/'acquisitions.json',rows)
        def monitor(pid):
            memory=rss(pid);scratch=sum(f.stat().st_size for f in p.rglob('*') if f.is_file())
            return {'rss_bytes':memory,'scratch_bytes':scratch},('rss_cap' if memory>2*1024**3 else 'scratch_cap' if scratch>128*1024**2 else None)
        row['process']=run(command,cwd=ROOT,log_path=p/'process.log',wall_cap=60,monitor=monitor,env=env);atomic_json(p/'process_receipt.json',row['process'])
        assert row['process']['exit_code']==0 and row['process']['termination_reason'] is None
        row['metrics']=validate(p,c,truth);row['status']='valid';row['answers_sha256']=sha(p/'answers.csv')
        atomic_json(p/'result.json',row);atomic_json(out/'acquisitions.json',rows)
        observation={'config_id':cid,'query_seconds':row['metrics']['query_seconds'],'physical_trial':row['trial']};obs.append(observation)
        print('validated',row['trial'],'seed',seed,arm,purpose,'query',round(observation['query_seconds'],4),flush=True)
    try:
        for si,seed in enumerate(SEEDS):
            prefix=[];case={'seed':seed,'prefix':prefix,'branches':{},'selected':{},'complete':False};cases.append(case)
            for j in range(10):
                t=time.monotonic();cid=prefix_choice(prefix,seed);acquire(cid,prefix,seed,'prefix','search',time.monotonic()-t);atomic_json(out/'cases.json',cases)
            pp=out/f'prefix_{seed}.json';atomic_json(pp,{'seed':seed,'system_group':'h2','observations':prefix,'budget_used':10,'remaining_including_confirmations':10});case['prefix_sha256']=sha(pp)
            branches={arm:[dict(o) for o in prefix] for arm in ['rf_lcb','random']};branches['prior']=[];case['branches']=branches
            for j in range(7):
                for arm in (['rf_lcb','random'] if (si+j)%2==0 else ['random','rf_lcb']):
                    t=time.monotonic();cid=choose(branches[arm],arm,seed);acquire(cid,branches[arm],seed,arm,'search',time.monotonic()-t);atomic_json(out/'cases.json',cases)
            selected={arm:incumbent(branches[arm]) for arm in ['rf_lcb','random']};selected['prior']=PRIOR;case['selected']=selected;atomic_json(out/f'locked_{seed}.json',{'selected':selected,'physical_trials_at_lock':len(rows),'prefix_sha256':sha(pp)})
            for rep in range(3):
                offset=(si+rep)%3
                for arm in ARMS[offset:]+ARMS[:offset]:
                    acquire(selected[arm],branches[arm],seed,arm,'fixed_prior' if arm=='prior' else 'confirmation');atomic_json(out/'cases.json',cases)
            assert sha(pp)==case['prefix_sha256'];assert [len(branches[a]) for a in ARMS]==[20,20,3]
            case['complete']=True;atomic_json(out/'cases.json',cases)
    except Exception as e:
        stop=repr(e)
        if rows and rows[-1]['status']=='charged':rows[-1].update(status='failed',error=stop);atomic_json(ROOT/rows[-1]['path']/'failure.json',rows[-1])
        atomic_json(out/'failure.json',{'error':stop})
    finally:
        atomic_json(out/'acquisitions.json',rows);atomic_json(out/'cases.json',cases)
        atomic_json(out/'summary.json',{'intended_trials':165,'charged_trials':len(rows),'valid_trials':sum(r['status']=='valid' for r in rows),'unattempted':165-len(rows),'completed_seeds':sum(c['complete'] for c in cases),'complete':stop is None and len(rows)==165,'stop_reason':stop,'seconds':time.monotonic()-start,'new_model_requests':0})
    if stop:raise RuntimeError(stop)
if __name__=='__main__':main()
