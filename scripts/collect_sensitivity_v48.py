"""V48 development-only choices; identical bounded V47 decoder, no target-table access."""
import hashlib, json, os, signal, subprocess, time, urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/v48_sensitivity'
ART=ROOT/'artifacts/study_v48'
IDS='0123456789ABCDEFGHIJ'
def read(p): return json.loads(Path(p).read_text())
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
def grammar(used):
    if len(used)!=len(set(used)) or any(c not in IDS for c in used):raise ValueError('Invalid used IDs')
    return 'root ::= '+ ' | '.join(json.dumps(c) for c in IDS if c not in used)
def main():
    cfg=read(ROOT/'configs/study_v48.json')
    if cfg['max_external_spend_usd']!=0 or cfg['host']!='127.0.0.1' or cfg['retries']!=0:raise ValueError('Unsafe config')
    if OUT.exists():raise ValueError('No implicit restart or duplicate collection')
    for path,h in read(ROOT/'reports/protocol_v48_sensitivity.freeze.json')['sha256'].items():
        if sha(ROOT/path)!=h:raise ValueError('Changed frozen input: '+path)
    model=ROOT/'models/SmolLM3-3B-Q4_K_M/SmolLM3-Q4_K_M.gguf'
    if sha(model)!='8334b850b7bd46238c16b0c550df2138f0889bf433809008cc17a8b05761863e':raise ValueError('Changed model')
    OUT.mkdir();ART.mkdir(exist_ok=True)
    command=[str(ROOT/'.local-runtime/llama-b11146/llama-server'),'-m',str(model),'--offline',
        '--host',cfg['host'],'--port',str(cfg['port']),'--no-webui','-ngl','99','-c','4096',
        '-np','1','-t','6','-b','512','-ub','128','--reasoning','off','--jinja','--no-warmup','--perf']
    ledger={'started_at':now(),'requests':0,'completed_cases':0,'external_spend_usd':0,'objective_accesses':0,'retries':0}
    write(OUT/'runtime.json',{'command':command,'config':cfg,'runtime_build':'b11146','model_sha256':sha(model)})
    started=time.monotonic();proc=None
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    def check():
        if time.monotonic()-started>cfg['max_stage_seconds']-5:raise TimeoutError('Stage exhausted')
    def api(route,payload=None):
        check()
        if route not in ('/health','/apply-template','/tokenize','/completion'):raise ValueError('Unapproved endpoint')
        req=urllib.request.Request(f"http://127.0.0.1:{cfg['port']}"+route,
            data=None if payload is None else json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
        with opener.open(req,timeout=min(cfg['request_timeout_seconds'],cfg['max_stage_seconds']-(time.monotonic()-started)-3)) as r:
            return json.load(r)
    try:
        import socket
        with socket.socket() as s:s.bind(('127.0.0.1',cfg['port']))
        with (ART/'server.log').open('w') as log:
            proc=subprocess.Popen(command,stdout=log,stderr=log,start_new_session=True,cwd=ROOT,
                env={k:v for k,v in os.environ.items() if not k.startswith(('LLAMA_','HF_','HUGGING_FACE_'))})
        for _ in range(100):
            if proc.poll() is not None:raise RuntimeError('Server startup failed')
            try:
                if api('/health').get('status')=='ok':break
            except (OSError,ValueError):time.sleep(.2)
        else:raise TimeoutError('Server health timeout')
        ledger['startup_seconds']=time.monotonic()-started
        tokens={c:api('/tokenize',{'content':c,'add_special':False})['tokens'] for c in IDS+'\n'}
        if any(len(t)!=1 for t in tokens.values()) or len({t[0] for t in tokens.values()})!=21:raise ValueError('Non-single-token ID/delimiter')
        write(OUT/'choice_tokenization.json',tokens)
        jobs=read(ROOT/'artifacts/study_v48/jobs.json')
        # All preflight checks precede first generation. No objective-table reads.
        prepared=[]
        for job in jobs:
            p=read(ROOT/job['prefix'])
            rendered=api('/apply-template',{'messages':p['messages'],'add_generation_prompt':True,
                'chat_template_kwargs':{'enable_thinking':False}})
            prompt=rendered['prompt']
            ids=api('/tokenize',{'content':prompt,'add_special':False,'parse_special':True})['tokens']
            if len(ids)+20>cfg['context_tokens']:raise ValueError('Context overflow')
            record={**job,'messages':p['messages'],'rendered':rendered,'prompt_tokens':ids,'prefix_hash':p['prefix_hash']}
            write(OUT/'preflight'/f"{job['key']}.json",record);prepared.append((job,p,prompt))
        write(OUT/'preflight_seal.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted((OUT/'preflight').glob('*.json'))}})
        for job,p,prompt in prepared:
            used=[];failure=None;case_start=time.monotonic();request_ids=[]
            for step in range(10):
                check()
                if ledger['requests']>=cfg['max_generation_requests']:raise RuntimeError('Request cap')
                payload={'prompt':prompt+''.join(c+'\n' for c in used),'n_predict':1,'temperature':0,
                    'seed':cfg['seed'],'grammar':grammar(used),'cache_prompt':bool(step),
                    'return_tokens':True,'stream':False,'repeat_penalty':1.0}
                identity=f"{job['key']}_{step}";request_ids.append(identity)
                request={'request_id':identity,'case':job['key'],'step':step,'at':now(),'payload':payload}
                ledger['requests']+=1;write(OUT/'ledger.json',ledger);append(OUT/'request_starts.jsonl',request)
                t=time.monotonic()
                try:
                    response=api('/completion',payload)
                    raw=response['content']
                    rec={**request,'status':'response','response':response,'wall_seconds':time.monotonic()-t}
                    append(OUT/'responses.jsonl',rec)
                    if raw not in IDS or len(raw)!=1 or raw in used:raise ValueError('Invalid/duplicate ID')
                    if response.get('tokens_predicted',1)>1:raise ValueError('Token cap exceeded')
                    used.append(raw)
                except Exception as e:
                    failure=f'{type(e).__name__}: {e}'
                    # Raw successful-but-malformed responses are already retained.
                    append(OUT/'errors.jsonl',{'request_id':identity,'error':failure,'at':now(),'wall_seconds':time.monotonic()-t})
                    if proc.poll() is not None or isinstance(e,(TimeoutError,OSError)):raise
                    break
            write(OUT/'choices'/f"{job['key']}.json",{**job,'selected_ids':used,'fallback_reason':failure,
                'request_ids':request_ids,'case_seconds':time.monotonic()-case_start,'prefix_hash':p['prefix_hash'],
                'status':'completed' if len(used)==10 else 'fallback'})
            ledger['completed_cases']+=1;write(OUT/'ledger.json',ledger)
            print(job['key'],len(used),'choices',flush=True)
    except Exception as e:
        ledger['stop_reason']=f'{type(e).__name__}: {e}'
        raise
    finally:
        if proc is not None and proc.poll() is None:
            os.killpg(proc.pid,signal.SIGTERM)
            try:proc.wait(timeout=3)
            except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
        ledger.update(finished_at=now(),stage_seconds=time.monotonic()-started,server_exit_code=None if proc is None else proc.returncode)
        write(OUT/'ledger.json',ledger)

if __name__=='__main__':main()
