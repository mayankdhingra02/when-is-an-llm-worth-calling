"""Post-hoc synthetic-form tokenizer diagnostic using existing owner runtime."""
import ast,json,subprocess,time,os,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 out=ROOT/'artifacts/study_v128/synthetic_offline_tokenizer.json';assert not out.exists();binary=ROOT/'.local-runtime/llama-b11146/llama-tokenize';jobs=json.loads((ROOT/'artifacts/study_v128/jobs.json').read_text());rows=[];start=time.monotonic();env={k:v for k,v in os.environ.items() if not k.startswith(('LLAMA_','HF_','HUGGING_FACE_'))}
 for j in jobs:
  if j['condition']!='normal' or j['seed']!=11:continue
  content=json.dumps(['0'*len(j['domains'])]*10,separators=(',',':'));cmd=[str(binary),'-m',str(ROOT/'models/Qwen3-8B-Q4_K_M/Qwen3-8B-Q4_K_M.gguf'),'--offline','--stdin','--ids','--no-bos','--no-parse-special'];r={'dataset':j['dataset'],'synthetic_input':content,'command':cmd};t=time.monotonic()
  try:
   if t-start>=30:raise TimeoutError('Total30second diagnostic limit')
   p=subprocess.run(cmd,input=content,text=True,capture_output=True,cwd=ROOT,env=env,timeout=max(.1,30-(t-start)));r.update(returncode=p.returncode,stdout=p.stdout,stderr=p.stderr);assert p.returncode==0;r['tokens']=ast.literal_eval(p.stdout.strip());r['token_count']=len(r['tokens'])
  except Exception as e:r['error']=repr(e)
  r['seconds']=time.monotonic()-t;rows.append(r)
 out.write_text(json.dumps({'scope':'SYNTHETIC formatting/tokenizer fixture;not a generated model response or measured optimization result','generation_requests':0,'new_objective_acquisitions':0,'metadata_processes':len(rows),'seconds':time.monotonic()-start,'binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'rows':rows},indent=2)+'\n');print([(r['dataset'],r.get('token_count'),r.get('error')) for r in rows])
if __name__=='__main__':main()
