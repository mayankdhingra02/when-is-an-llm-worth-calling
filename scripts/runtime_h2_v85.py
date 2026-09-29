"""Offline loopback model lifecycle; counting and resource limits before I/O."""
import json,os,signal,socket,subprocess,threading,time,urllib.request
from pathlib import Path
from run_planning_v55 import rss
from escalation.receipts_v70 import atomic_json
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):raise ValueError('Redirects forbidden')
class Runtime:
    def __init__(self,root,out,cfg,*,generation_limit=0,seconds=180):
        self.root=root;self.out=out;self.cfg=cfg;self.limit=generation_limit;self.seconds=seconds;self.proc=None;self.thread=None;self.done=threading.Event();self.reason=None;self.started=time.monotonic()
        self.ledger={'generation_requests':0,'http_requests':0,'retries':0,'external_spend_usd':0,'peak_server_rss_bytes':0}
        self.opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
    def check(self):
        if self.reason:raise RuntimeError(self.reason)
        if time.monotonic()-self.started>self.seconds-160 if self.seconds>300 else time.monotonic()-self.started>self.seconds-10:raise TimeoutError('Stage reserve reached')
        if self.proc is not None and self.proc.poll() is not None:raise RuntimeError('Model server exited')
    def watch(self):
        while not self.done.wait(.5):
            try:
                if self.proc is not None and self.proc.poll() is None:self.ledger['peak_server_rss_bytes']=max(self.ledger['peak_server_rss_bytes'],rss(self.proc.pid))
                if self.ledger['peak_server_rss_bytes']>8*1024**3:self.reason='server_rss_cap'
                if time.monotonic()-self.started>=self.seconds-10:self.reason='stage_timeout'
            except Exception as e:self.reason='watchdog_error:'+repr(e)
            if self.reason:
                if self.proc is not None and self.proc.poll() is None:
                    try:os.killpg(self.proc.pid,signal.SIGKILL)
                    except ProcessLookupError:pass
                return
    def start(self):
        rss(-1)
        with socket.socket() as sock:sock.bind(('127.0.0.1',18492))
        command=json.loads((self.root/'artifacts/study_v78/runtime_plan.json').read_text())['command']
        assert command[command.index('--host')+1]=='127.0.0.1' and command[command.index('--port')+1]=='18492' and '--offline' in command
        atomic_json(self.out/'runtime.json',{'command':command,'generation_limit':self.limit,'seconds_cap':self.seconds,'requested_seed_support':'fixed per-seed request; no cross-device determinism guarantee'})
        with (self.out/'server.log').open('xb') as f:self.proc=subprocess.Popen(command,cwd=self.root,stdout=f,stderr=f,start_new_session=True,env={k:v for k,v in os.environ.items() if not k.startswith(('LLAMA_','HF_','HUGGING_FACE_'))})
        self.thread=threading.Thread(target=self.watch,daemon=True);self.thread.start();t=time.monotonic()
        while True:
            if time.monotonic()-t>120:raise TimeoutError('Model startup timeout')
            try:
                if self.api('/health').get('status')=='ok':break
            except OSError:time.sleep(.25)
        self.ledger['startup_seconds']=time.monotonic()-self.started
    def _send(self,route,payload=None):
        self.check();self.ledger['http_requests']+=1
        req=urllib.request.Request('http://127.0.0.1:18492'+route,data=None if payload is None else json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
        with self.opener.open(req,timeout=120) as response:return json.load(response)
    def api(self,route,payload=None):
        if route not in ['/health','/apply-template','/tokenize']:raise ValueError('Disallowed non-generation route')
        return self._send(route,payload)
    def generate(self,payload,folder):
        self.check()
        if self.ledger['generation_requests']>=self.limit:raise PermissionError('Generation allowance exhausted or zero')
        if payload['n_predict']!=64 or payload['temperature']!=0 or payload['stream'] is not False:raise ValueError('Changed generation contract')
        self.ledger['generation_requests']+=1
        atomic_json(folder/'attempt_started.json',{'generation_number':self.ledger['generation_requests'],'started_at_unix':time.time()});atomic_json(self.out/'ledger.json',self.ledger)
        return self._send('/completion',payload)
    def close(self):
        self.done.set()
        if self.thread is not None:self.thread.join(timeout=3)
        if self.proc is not None and self.proc.poll() is None:
            os.killpg(self.proc.pid,signal.SIGTERM)
            try:self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:os.killpg(self.proc.pid,signal.SIGKILL);self.proc.wait(timeout=3)
        self.ledger.update(seconds=time.monotonic()-self.started,resource_stop_reason=self.reason,server_exit_code=None if self.proc is None else self.proc.returncode)
        atomic_json(self.out/'ledger.json',self.ledger)
