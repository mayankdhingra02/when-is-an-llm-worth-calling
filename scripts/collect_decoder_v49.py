"""Bounded local decoder comparison; no target table access or paid client."""
import hashlib,json,os,signal,socket,subprocess,time,urllib.request
from pathlib import Path
from datetime import datetime,timezone
from decoder_v49_common import parse_native,IDS
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results/v49_decoder';ART=ROOT/'artifacts/study_v49'
def read(p):return json.loads(Path(p).read_text())
def write(p,v):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def append(p,v):
    with Path(p).open('a') as f:f.write(json.dumps(v)+'\n')
def now():return datetime.now(timezone.utc).isoformat()
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def grammar(used):return 'root ::= '+' | '.join(json.dumps(c) for c in IDS if c not in used)
def main():
    cfg=read(ROOT/'configs/study_v49.json')
    assert cfg['max_generation_requests']==144 and cfg['max_stage_seconds']==900
    assert cfg['max_native_output_tokens']==128 and cfg['context_tokens']==4096
    assert cfg['host']=='127.0.0.1' and cfg['port']==18475 and cfg['retries']==0
    assert all(cfg[k]==0 for k in ('max_external_spend_usd','max_new_download_bytes','max_new_objective_accesses'))
    if OUT.exists():raise ValueError('No implicit restart')
    for path,h in read(ROOT/'reports/protocol_v49_decoder.freeze.json')['sha256'].items():
        if sha(ROOT/path)!=h:raise ValueError('Frozen input changed: '+path)
    model=ROOT/'models/SmolLM3-3B-Q4_K_M/SmolLM3-Q4_K_M.gguf'
    assert sha(model)=='8334b850b7bd46238c16b0c550df2138f0889bf433809008cc17a8b05761863e'
    oldruntime=read(ROOT/'results/v48_sensitivity/runtime.json')
    command=list(oldruntime['command']);command[command.index('--port')+1]=str(cfg['port'])
    OUT.mkdir();ledger={'started_at':now(),'requests':0,'completed_cases':0,'valid_cases':0,'retries':0,'objective_accesses':0,'external_spend_usd':0}
    write(OUT/'runtime.json',{'command':command,'config':cfg,'model_sha256':sha(model),'runtime_build':'b11146'})
    started=time.monotonic();proc=None;opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    def api(route,payload=None):
        left=cfg['max_stage_seconds']-(time.monotonic()-started)-5
        if left<=0:raise TimeoutError('Stage cap')
        assert route in ('/health','/apply-template','/tokenize','/completion')
        req=urllib.request.Request(f"http://127.0.0.1:{cfg['port']}"+route,data=None if payload is None else json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
        with opener.open(req,timeout=min(cfg['request_timeout_seconds'],left)) as r:return json.load(r)
    try:
        with socket.socket() as s:s.bind((cfg['host'],cfg['port']))
        with (ART/'server.log').open('w') as log:
            proc=subprocess.Popen(command,stdout=log,stderr=log,start_new_session=True,cwd=ROOT,
                env={k:v for k,v in os.environ.items() if not k.startswith(('LLAMA_','HF_','HUGGING_FACE_'))})
        for _ in range(100):
            if proc.poll() is not None:raise RuntimeError('Server startup failed')
            try:
                if api('/health').get('status')=='ok':break
            except (OSError,ValueError):time.sleep(.2)
        else:raise TimeoutError('Health timeout')
        ledger['startup_seconds']=time.monotonic()-started
        prepared=[]
        for job in read(ART/'jobs.json'):
            p=read(ROOT/job['prefix'])
            rendered=api('/apply-template',{'messages':p['messages'],'add_generation_prompt':True,'chat_template_kwargs':{'enable_thinking':False}})
            ids=api('/tokenize',{'content':rendered['prompt'],'add_special':False,'parse_special':True})['tokens']
            old=read(ROOT/'results/v48_sensitivity/preflight'/f"{job['source_key']}.json")
            assert rendered['prompt']==old['rendered']['prompt'] and ids==old['prompt_tokens']
            assert len(ids)+(128 if job['decoder']=='native' else 20)<=4096
            write(OUT/'preflight'/f"{job['key']}.json",{**job,'messages':p['messages'],'rendered':rendered,'prompt_tokens':ids,'prefix_hash':p['prefix_hash']})
            prepared.append((job,p,rendered['prompt']))
        write(OUT/'preflight_seal.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted((OUT/'preflight').glob('*.json'))}})
        for job,p,prompt in prepared:
            used=[];request_ids=[];case_start=time.monotonic();parsed=None
            for step in range(1 if job['decoder']=='native' else 10):
                assert ledger['requests']<cfg['max_generation_requests']
                payload={'prompt':prompt+''.join(c+'\n' for c in used),'n_predict':128 if job['decoder']=='native' else 1,
                    'temperature':0,'seed':11,'cache_prompt':bool(step),'return_tokens':True,'stream':False,'repeat_penalty':1.0}
                if job['decoder']=='forced':payload['grammar']=grammar(used)
                identity=f"{job['key']}_{step}";request_ids.append(identity)
                request={'request_id':identity,'case':job['key'],'step':step,'at':now(),'payload':payload}
                ledger['requests']+=1;write(OUT/'ledger.json',ledger);append(OUT/'request_starts.jsonl',request)
                t=time.monotonic()
                try:response=api('/completion',payload)
                except Exception as e:
                    append(OUT/'errors.jsonl',{'request_id':identity,'error':f'{type(e).__name__}: {e}','at':now(),'wall_seconds':time.monotonic()-t});raise
                append(OUT/'responses.jsonl',{**request,'response':response,'wall_seconds':time.monotonic()-t})
                assert response['tokens_predicted']<=payload['n_predict']
                if job['decoder']=='native':
                    parsed=parse_native(response['content'],response.get('truncated',False) or response.get('stopped_limit',False) or response.get('stop_type')=='limit');used=parsed['selected_ids']
                else:
                    raw=response['content']
                    if len(raw)!=1 or raw not in IDS or raw in used:
                        parsed={'valid':False,'selected_ids':[],'reasons':['invalid_forced_id']};break
                    used.append(raw)
            if parsed is None:parsed={'valid':len(used)==10,'selected_ids':used,'reasons':[]}
            write(OUT/'choices'/f"{job['key']}.json",{**job,**parsed,'request_ids':request_ids,'case_seconds':time.monotonic()-case_start,'prefix_hash':p['prefix_hash'],'status':'valid' if parsed['valid'] else 'invalid'})
            ledger['completed_cases']+=1;ledger['valid_cases']+=parsed['valid'];write(OUT/'ledger.json',ledger)
            print(job['key'], 'valid' if parsed['valid'] else parsed['reasons'],flush=True)
    except Exception as e:
        ledger['stop_reason']=f'{type(e).__name__}: {e}';raise
    finally:
        if proc is not None and proc.poll() is None:
            os.killpg(proc.pid,signal.SIGTERM)
            try:proc.wait(timeout=3)
            except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
        ledger.update(finished_at=now(),stage_seconds=time.monotonic()-started,server_exit_code=None if proc is None else proc.returncode)
        write(OUT/'ledger.json',ledger)
if __name__=='__main__':main()
