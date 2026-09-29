"""V22 larger pinned model; reuse unchanged V19 CPU worker and cleanup."""
import hashlib,multiprocessing as mp,time
from pathlib import Path
from .provider import LocalProvider,WorkerUnavailable
from .provider_v19 import worker,OrderProbeProvider
from .resources import LimitReached
from .io import read,write,append,now,digest
from .larger_v22 import MODEL_ID,REVISION,require

def file_sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

class LargerProvider(LocalProvider):
    close=OrderProbeProvider.close

    def __enter__(self):
        manifest=read('artifacts/model_manifest_v22.json')
        require(manifest['complete'] and manifest['model_id']==MODEL_ID and manifest['revision']==REVISION,'Model provenance')
        plan=read('artifacts/study_v22/model_download_plan.json')
        require(len(manifest['files'])==len(plan['files'])==len({r['file'] for r in manifest['files']}),'Model file denominator')
        base=Path('models/Qwen2.5-1.5B-Instruct').resolve()
        expected={r['rfilename']:r for r in plan['files']}
        for row in manifest['files']:
            name=row['file']; require(name in expected,'Unexpected model file')
            require(row['bytes']==expected[name]['size'] and file_sha(base/name)==row['sha256'],'Model file changed')
            if 'lfs' in expected[name]:require(row['sha256']==expected[name]['lfs']['sha256'],'Owner weight hash mismatch')
            else:
                data=(base/name).read_bytes()
                require(hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()==expected[name]['blobId'],'Owner Git blob mismatch')
        self.resources.check();ctx=mp.get_context('spawn');self.pipe,child=ctx.Pipe()
        self.process=ctx.Process(target=worker,args=(child,str(base)),daemon=True)
        started=time.perf_counter();self.process.start();child.close()
        if not self.pipe.poll(min(90,self.resources.remaining())):
            self.close();raise LimitReached('Model load timeout')
        self.identity=self.pipe.recv()
        if not self.identity.get('ready'):
            self.close();raise RuntimeError(self.identity)
        self.identity.update(model_id=MODEL_ID,revision=REVISION,provider='local_transformers',
            seed_support='greedy; no sampling seed; numerical nondeterminism possible',adapter='larger_v22',
            startup_wall_seconds=time.perf_counter()-started)
        write(self.log.parent/'model_runtime.json',self.identity)
        return self

    def request(self,messages,context):
        if self.process is None or not self.process.is_alive():
            raise WorkerUnavailable('worker unavailable; stopped before reserving a request')
        request_id=self.resources.request();t=time.perf_counter()
        record={**context,**self.identity,'request_id':request_id,'started':now(),'messages':messages,'parameters':{'do_sample':False,'max_new_tokens':self.cfg['inference']['max_output_tokens_per_request']},'input_tokens':None,'output_tokens':None,'raw_output':None,'status':'started'}
        record['cache_key']=digest({'messages':messages,'model':self.identity['model_id'],'revision':self.identity['revision'],'parameters':record['parameters'],'context':context,'parser_projection':context.get('prompt_version','v1'),'grammar_domains':context.get('grammar_domains'),'grammar_mode':context.get('grammar_mode')})
        append(self.log.with_name('request_starts.jsonl'),record)
        try:
            if self.process is None or not self.process.is_alive():raise RuntimeError('local model worker unavailable')
            self.pipe.send({'messages':messages,'max_tokens':self.cfg['inference']['max_output_tokens_per_request'],'grammar_domains':context.get('grammar_domains'),'grammar_mode':context.get('grammar_mode')})
            timeout=min(self.cfg['inference']['request_timeout_seconds'],max(0,self.resources.remaining()))
            if not self.pipe.poll(timeout):
                self.close();raise TimeoutError('local request timed out; worker terminated')
            answer=self.pipe.recv()
            if 'worker_error' in answer:raise RuntimeError(answer['worker_error'])
            record.update(answer);record['status']='response'
        except Exception as e:record.update({'status':'error','error':f'{type(e).__name__}: {e}'})
        finally:
            record['finished']=now();record['wall_seconds']=time.perf_counter()-t;append(self.log,record);self.resources.checkpoint()
        return record
