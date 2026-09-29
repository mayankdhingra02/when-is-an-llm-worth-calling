"""Nine prospectively fixed native feasibility trials, no optimization or LLM."""
import hashlib,json,os,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.h2_v82 import expected,validate,PROFILES,ORDER
from escalation.bounded_process_v57 import run
from escalation.receipts_v70 import atomic_json
from run_planning_v55 import rss

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    for n,d in json.loads((ROOT/'reports/protocol_v82.freeze.json').read_text())['sha256'].items():assert sha(ROOT/n)==d,n
    rss(-1);out=ROOT/'results/v82_h2_feasibility';out.mkdir(exist_ok=False)
    lock=json.loads((ROOT/'configs/runtime_v82.lock.json').read_text());truth=expected();rows=[];start=time.monotonic();stop=None
    env={k:v for k,v in os.environ.items() if k not in ['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS','JDK_JAVA_OPTIONS','CLASSPATH']}
    try:
        for i,profile in enumerate(ORDER):
            if time.monotonic()-start>500:raise TimeoutError('stage reserve')
            p=out/f'trial_{i}';p.mkdir();c=PROFILES[profile]
            command=[str(ROOT/lock['java']),'-Xmx512m','-XX:ActiveProcessorCount=4','-cp',str(ROOT/lock['jar'])+os.pathsep+str(ROOT/lock['classes']),'H2Probe',str(c['mask']),str(c['recompile']).lower(),str(c['analyze_sample']),str(p)]
            row={'trial':i,'profile':profile,'config':c,'status':'charged','command':command,'path':str(p.relative_to(ROOT)),'charged_at_unix':time.time()};rows.append(row);atomic_json(p/'charge.json',row)
            atomic_json(out/'acquisitions.json',rows)
            def monitor(pid):
                memory=rss(pid);scratch=sum(f.stat().st_size for f in p.rglob('*') if f.is_file())
                return {'rss_bytes':memory,'scratch_bytes':scratch},('rss_cap' if memory>2*1024**3 else 'scratch_cap' if scratch>128*1024**2 else None)
            row['process']=run(command,cwd=ROOT,log_path=p/'process.log',wall_cap=60,monitor=monitor,env=env)
            atomic_json(p/'process_receipt.json',row['process'])
            assert row['process']['exit_code']==0 and row['process']['termination_reason'] is None
            row['metrics']=validate(p,c,truth);row['status']='valid';row['answers_sha256']=sha(p/'answers.csv')
            atomic_json(p/'result.json',row);atomic_json(out/'acquisitions.json',rows)
            print('validated',i,profile,flush=True)
    except Exception as e:
        stop=repr(e)
        if rows and rows[-1]['status']=='charged':rows[-1].update(status='failed',error=stop);atomic_json(ROOT/rows[-1]['path']/'failure.json',rows[-1])
        atomic_json(out/'failure.json',{'error':stop})
    finally:
        atomic_json(out/'acquisitions.json',rows)
        atomic_json(out/'summary.json',{'intended_trials':9,'charged_trials':len(rows),'valid_trials':sum(r['status']=='valid' for r in rows),'unattempted':9-len(rows),'complete':stop is None and len(rows)==9,'stop_reason':stop,'seconds':time.monotonic()-start,'new_model_requests':0})
    if stop:raise RuntimeError(stop)
if __name__=='__main__':main()
