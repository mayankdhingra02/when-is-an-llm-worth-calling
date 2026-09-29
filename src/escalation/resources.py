"""Persistent, fail-closed single experiment and request ledger."""
import fcntl,time,os
from pathlib import Path
from .io import read,write,now

class LimitReached(RuntimeError): pass

class Resources:
    def __init__(self,config,path='artifacts/resource_ledger.json'):
        self.c=config;self.path=Path(path);self.lock=None;self.last=None
    def __enter__(self):
        self.path.parent.mkdir(parents=True,exist_ok=True)
        self.lock=self.path.with_suffix('.lock').open('a')
        try: fcntl.flock(self.lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError: self.lock.close();raise LimitReached('another experiment is running')
        self.d=read(self.path) if self.path.exists() else {'requests':0,'experiment_seconds':0.,'external_spend_usd':0,'sessions':[]}
        if self.d.get('active_since'):
            # Crash downtime is conservatively counted until explicitly audited.
            self.d['experiment_seconds']+=max(0,time.time()-self.d['active_since'])
        self.d['active_since']=time.time();self.last=time.monotonic()
        self.d['sessions'].append({'started':now(),'pid':os.getpid()});self.checkpoint();return self
    def checkpoint(self):
        t=time.monotonic()
        if self.last is not None:self.d['experiment_seconds']+=t-self.last
        self.last=t;self.d['active_since']=time.time();write(self.path,self.d)
    def remaining(self):
        self.checkpoint();return self.c['resources']['max_experiment_runtime_minutes']*60-self.d['experiment_seconds']
    def check(self):
        if self.remaining()<=0:raise LimitReached('cumulative experiment runtime exhausted')
    def request(self):
        self.check()
        if self.d['requests']>=self.c['inference']['max_new_model_requests']:raise LimitReached('model request cap exhausted')
        self.d['requests']+=1;self.checkpoint();return self.d['requests']
    def __exit__(self,*args):
        self.checkpoint();self.d['active_since']=None;self.d['sessions'][-1]['finished']=now();write(self.path,self.d)
        fcntl.flock(self.lock,fcntl.LOCK_UN);self.lock.close()
