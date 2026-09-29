"""Approved local lifecycle, hard wall watchdog and charged generation limits."""
import json,os,signal,socket,subprocess,threading,time,urllib.request,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from decoder_v93_common import check_payload
from escalation.receipts_v70 import atomic_json
from run_planning_v55 import rss
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):raise ValueError('Loopback redirects forbidden')
class Runtime:
    def __init__(self,out,cfg):
        self.out=out;self.cfg=cfg;self.started=time.monotonic();self.proc=None;self.thread=None;self.done=threading.Event();self.reason=None
        self.ledger={'generation_requests':0,'compatibility_requests':0,'scientific_requests':0,'http_requests':0,'peak_server_rss_bytes':0,'retries':0,'external_spend_usd':0}
        self.opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
    def check(self):
        if self.reason:raise RuntimeError(self.reason)
        if time.monotonic()-self.started>self.cfg['max_generation_stage_seconds']-125:raise TimeoutError('Reserve reached')
        if self.proc is not None and self.proc.poll() is not None:raise RuntimeError('Server exited')
    def watch(self):
        while not self.done.wait(.5):
            try:
                self.ledger['peak_server_rss_bytes']=max(self.ledger['peak_server_rss_bytes'],rss(self.proc.pid))
                if self.ledger['peak_server_rss_bytes']>self.cfg['max_server_rss_bytes']:self.reason='server_rss_cap'
                if time.monotonic()-self.started>=self.cfg['max_generation_stage_seconds']-5:self.reason='wall_cap'
            except Exception as e:self.reason='watchdog_error:'+repr(e)
            if self.reason:
                try:os.killpg(self.proc.pid,signal.SIGKILL)
                except ProcessLookupError:pass
                return
    def start(self):
        rss(-1)
        with socket.socket() as sock:sock.bind(('127.0.0.1',18591))
        command=[str(ROOT/'.local-runtime/llama-b11146/llama-server'),'-m',str(ROOT/'models/Qwen3-8B-Q4_K_M/Qwen3-8B-Q4_K_M.gguf'),'--offline','--host','127.0.0.1','--port','18591','--no-webui','-ngl','99','-c','8192','-np','1','-t','6','-b','512','-ub','128','--reasoning','off','--jinja','--no-warmup','--perf']
        atomic_json(self.out/'runtime.json',{'command':command,'config':self.cfg,'seed_support':'Request seed11,greedy decoding; no cross-device determinism guarantee'})
        with (self.out/'server.log').open('xb') as f:self.proc=subprocess.Popen(command,cwd=ROOT,stdout=f,stderr=f,start_new_session=True,env={k:v for k,v in os.environ.items() if not k.startswith(('LLAMA_','HF_','HUGGING_FACE_'))})
        self.thread=threading.Thread(target=self.watch,daemon=True);self.thread.start();t=time.monotonic()
        while True:
            if time.monotonic()-t>120:raise TimeoutError('Startup timeout')
            try:
                if self.api('/health').get('status')=='ok':break
            except OSError:time.sleep(.25)
        self.ledger['startup_seconds']=time.monotonic()-self.started
    def _send(self,route,payload=None):
        self.check();self.ledger['http_requests']+=1
        req=urllib.request.Request('http://127.0.0.1:18591'+route,data=None if payload is None else json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
        with self.opener.open(req,timeout=120) as r:return json.load(r)
    def api(self,route,payload=None):
        if route not in ['/health','/apply-template','/tokenize']:raise ValueError('Disallowed metadata route')
        return self._send(route,payload)
    def generate(self,payload,kind,identity):
        check_payload(payload);self.check()
        if kind not in ['compatibility','scientific']:raise ValueError('Unknown generation namespace')
        k=kind+'_requests';limit=self.cfg[k.replace('requests','request_cap')]
        if self.ledger[k]>=limit or self.ledger['generation_requests']>=self.cfg['new_generation_request_cap']:raise PermissionError('Generation cap')
        self.ledger[k]+=1;self.ledger['generation_requests']+=1
        atomic_json(self.out/'ledger.json',self.ledger)
        with (self.out/'generation_starts.jsonl').open('a') as f:f.write(json.dumps({'identity':identity,'kind':kind,'at_unix':time.time(),'generation':self.ledger['generation_requests'],'payload':payload})+'\n')
        return self._send('/completion',payload)
    def close(self):
        self.done.set()
        if self.thread is not None:self.thread.join(timeout=2)
        if self.proc is not None and self.proc.poll() is None:
            os.killpg(self.proc.pid,signal.SIGTERM)
            try:self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:os.killpg(self.proc.pid,signal.SIGKILL);self.proc.wait(timeout=3)
        self.ledger.update(stage_seconds=time.monotonic()-self.started,resource_stop_reason=self.reason,server_exit_code=None if self.proc is None else self.proc.returncode)
        atomic_json(self.out/'ledger.json',self.ledger)
