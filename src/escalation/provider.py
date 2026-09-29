"""Local-only inference. No HTTP client, credentials or paid backend path."""
import multiprocessing as mp,os,time,hashlib
from pathlib import Path
from .io import read,write,append,now,digest
from .data import sha
from .resources import LimitReached

class WorkerUnavailable(RuntimeError): pass

MODEL_ID='Qwen/Qwen2.5-0.5B-Instruct'
REVISION='7ae557604adf67be50417f59c2c2f167def9a775'

def worker(pipe,model_path):
    os.environ.update({'HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1','HF_HUB_DISABLE_TELEMETRY':'1','TOKENIZERS_PARALLELISM':'false','HF_HOME':str(Path('.cache/huggingface').resolve())})
    try:
        import torch
        from transformers import AutoModelForCausalLM,AutoTokenizer
        torch.set_num_threads(4);device='mps' if torch.backends.mps.is_available() else 'cpu'
        t=time.perf_counter()
        tokenizer=AutoTokenizer.from_pretrained(model_path,local_files_only=True,trust_remote_code=False)
        model=AutoModelForCausalLM.from_pretrained(model_path,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float16 if device=='mps' else torch.float32).to(device).eval()
        pipe.send({'ready':True,'device':device,'dtype':str(model.dtype),'model_load_seconds':time.perf_counter()-t,'torch':torch.__version__})
        while True:
            job=pipe.recv()
            if job is None:break
            t=time.perf_counter()
            text=tokenizer.apply_chat_template(job['messages'],tokenize=False,add_generation_prompt=True)
            inputs=tokenizer(text,return_tensors='pt').to(device)
            if inputs['input_ids'].shape[1]+job['max_tokens']>32768:raise ValueError('context overflow')
            generation_kwargs={}
            grammar_info={}
            if job.get('grammar_domains') is not None:
                from .grammar import BinaryJSONGrammar,BinaryLinesGrammar
                grammar=BinaryLinesGrammar(tokenizer,job['grammar_domains']) if job.get('grammar_mode')=='binary_lines_v3' else BinaryJSONGrammar(tokenizer,job['grammar_domains'])
                generation_kwargs['prefix_allowed_tokens_fn']=grammar.constraint(inputs['input_ids'].shape[1])
                job['max_tokens']=len(grammar.schedule)
                grammar_info={'grammar_sha256':grammar.sha256,'grammar_schedule':grammar.schedule,'model_choice_positions':grammar.choice_positions}
            with torch.inference_mode():
                ids=model.generate(**inputs,do_sample=False,max_new_tokens=job['max_tokens'],pad_token_id=tokenizer.eos_token_id,**generation_kwargs)
            generated=ids[0,inputs['input_ids'].shape[1]:].tolist()
            pipe.send({**grammar_info,'generated_token_ids':generated,'raw_output':tokenizer.decode(generated,skip_special_tokens=True),'input_tokens':int(inputs['input_ids'].shape[1]),'output_tokens':len(generated),'rendered_prompt_sha256':hashlib.sha256(text.encode()).hexdigest(),'generation_seconds':time.perf_counter()-t,'finish_reason':'length' if len(generated)==job['max_tokens'] else 'eos'})
    except Exception as e:
        try:pipe.send({'worker_error':f'{type(e).__name__}: {e}'})
        except Exception:pass
    finally:pipe.close()

class LocalProvider:
    def __init__(self,cfg,resources,log):
        i=cfg['inference']
        if i['allow_paid_api'] or i['max_external_spend_usd']!=0 or not i['local_endpoint_only'] or i['backend'] not in ('local_or_verified_cache','local_transformers'):raise ValueError('only unpaid local inference is implemented')
        self.cfg=cfg;self.resources=resources;self.log=Path(log);self.process=None
    def __enter__(self):
        m=read('artifacts/model_manifest.json')
        if not m['complete'] or m['model_id']!=MODEL_ID or m['revision']!=REVISION:raise ValueError('model provenance')
        base=Path('models/Qwen2.5-0.5B-Instruct').resolve()
        if sum(f['bytes'] for f in m['files'])>self.cfg['resources']['max_model_download_gib']*1024**3:raise LimitReached('model size cap')
        for f in m['files']:
            if sha(base/f['file'])!=f['sha256']:raise ValueError('model file hash mismatch')
        self.resources.check();ctx=mp.get_context('spawn');self.pipe,child=ctx.Pipe()
        self.process=ctx.Process(target=worker,args=(child,str(base)),daemon=True);t=time.perf_counter();self.process.start();child.close()
        if not self.pipe.poll(min(180,self.resources.remaining())):
            self.close();raise LimitReached('model load timeout')
        self.identity=self.pipe.recv()
        if not self.identity.get('ready'):
            self.close();raise RuntimeError(self.identity)
        self.identity.update({'startup_wall_seconds':time.perf_counter()-t,'model_id':MODEL_ID,'revision':REVISION,'provider':'local_transformers','seed_support':'greedy; no sampling seed; device numerical nondeterminism possible'})
        write(self.log.parent/'model_runtime.json',self.identity);return self
    def request(self,messages,context):
        if self.process is None or not self.process.is_alive():
            raise WorkerUnavailable('worker unavailable; stopped before reserving a request')
        request_id=self.resources.request();t=time.perf_counter()
        record={**context,**self.identity,'request_id':request_id,'started':now(),'messages':messages,'parameters':{'do_sample':False,'max_new_tokens':self.cfg['inference']['max_output_tokens_per_request']},'input_tokens':None,'output_tokens':None,'raw_output':None,'status':'started'}
        record['cache_key']=digest({'messages':messages,'model':MODEL_ID,'revision':REVISION,'parameters':record['parameters'],'context':context,'parser_projection':context.get('prompt_version','v1'),'grammar_domains':context.get('grammar_domains'),'grammar_mode':context.get('grammar_mode')})
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
    def close(self):
        if self.process:
            if self.process.is_alive():self.process.terminate()
            self.process.join(timeout=5)
            if self.process.is_alive():self.process.kill();self.process.join(timeout=5)
            self.process=None
        if hasattr(self,'pipe'):
            self.pipe.close()
    def __exit__(self,*args):self.close()
