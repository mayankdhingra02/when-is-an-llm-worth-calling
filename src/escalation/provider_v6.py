"""Versioned local finite-domain worker; frozen v1-v5 providers are unchanged."""
import multiprocessing as mp,os,time,hashlib
from pathlib import Path
from .provider import LocalProvider,MODEL_ID,REVISION
from .io import read,write
from .data import sha
from .resources import LimitReached

def worker(pipe,model_path):
    os.environ.update({'HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1','HF_HUB_DISABLE_TELEMETRY':'1','TOKENIZERS_PARALLELISM':'false','HF_HOME':str(Path('.cache/huggingface').resolve())})
    try:
        import torch
        from transformers import AutoModelForCausalLM,AutoTokenizer
        from .grammar_v6 import FiniteSymbolsGrammar
        torch.set_num_threads(4);device='mps' if torch.backends.mps.is_available() else 'cpu';t=time.perf_counter()
        tokenizer=AutoTokenizer.from_pretrained(model_path,local_files_only=True,trust_remote_code=False)
        model=AutoModelForCausalLM.from_pretrained(model_path,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float16 if device=='mps' else torch.float32).to(device).eval()
        pipe.send({'ready':True,'device':device,'dtype':str(model.dtype),'model_load_seconds':time.perf_counter()-t,'torch':torch.__version__})
        while True:
            job=pipe.recv()
            if job is None:break
            t=time.perf_counter()
            if job.get('grammar_mode')!='finite_symbols_10_v6':raise ValueError('unknown finite grammar version')
            grammar=FiniteSymbolsGrammar(tokenizer,job['grammar_domains'])
            if len(grammar.schedule)>job['max_tokens']:raise ValueError('configured token cap too small')
            text=tokenizer.apply_chat_template(job['messages'],tokenize=False,add_generation_prompt=True)
            inputs=tokenizer(text,return_tensors='pt').to(device)
            if inputs['input_ids'].shape[1]+len(grammar.schedule)>32768:raise ValueError('context overflow')
            with torch.inference_mode():
                ids=model.generate(**inputs,do_sample=False,max_new_tokens=len(grammar.schedule),pad_token_id=tokenizer.eos_token_id,prefix_allowed_tokens_fn=grammar.constraint(inputs['input_ids'].shape[1]))
            generated=ids[0,inputs['input_ids'].shape[1]:].tolist()
            pipe.send({'grammar_sha256':grammar.sha256,'grammar_schedule':grammar.schedule,'model_choice_positions':grammar.choice_positions,
              'generated_token_ids':generated,'raw_output':tokenizer.decode(generated,skip_special_tokens=True),'input_tokens':int(inputs['input_ids'].shape[1]),'output_tokens':len(generated),
              'rendered_prompt_sha256':hashlib.sha256(text.encode()).hexdigest(),'generation_seconds':time.perf_counter()-t,
              'finish_reason':'eos' if generated and generated[-1]==tokenizer.eos_token_id else 'length'})
    except Exception as e:
        try:pipe.send({'worker_error':f'{type(e).__name__}: {e}'})
        except Exception:pass
    finally:pipe.close()

class FiniteProvider(LocalProvider):
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
        self.identity.update({'startup_wall_seconds':time.perf_counter()-t,'model_id':MODEL_ID,'revision':REVISION,'provider':'local_transformers',
          'seed_support':'greedy; no sampling seed; device numerical nondeterminism possible','adapter':'finite_symbols_10_v6'})
        write(self.log.parent/'model_runtime.json',self.identity);return self
