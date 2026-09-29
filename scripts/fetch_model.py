"""Download official Qwen files without authentication or remote code."""
import hashlib,json,pathlib,time
from download_guard import fetch
root=pathlib.Path(__file__).resolve().parents[1]
meta={'id':'Qwen/Qwen2.5-0.5B-Instruct','sha':'7ae557604adf67be50417f59c2c2f167def9a775'}
(root/'artifacts').mkdir(exist_ok=True)
sha=meta['sha']; out=root/'models/Qwen2.5-0.5B-Instruct';out.mkdir(parents=True,exist_ok=True)
files=['LICENSE','README.md','config.json','generation_config.json','merges.txt','model.safetensors','tokenizer.json','tokenizer_config.json','vocab.json']
ledger=[]; total=0; started=time.time()
known_path=root/'artifacts/model_manifest.json'
known=json.loads(known_path.read_text())['files'] if known_path.exists() else []
for name in files:
 url=f'https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/resolve/{sha}/{name}'
 target=out/name
 expected=next((f['sha256'] for f in known if f['file']==name),None)
 data=fetch(url,target,model=True,expected=expected);total+=len(data)
 ledger.append({'file':name,'url':url,'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
 print(name,ledger[-1]['bytes'],flush=True)
 (root/'artifacts/model_manifest.json').write_text(json.dumps({'model_id':meta['id'],'revision':sha,'license':'Apache-2.0','files':ledger,'complete':len(ledger)==len(files),'download_bytes':total},indent=2))
