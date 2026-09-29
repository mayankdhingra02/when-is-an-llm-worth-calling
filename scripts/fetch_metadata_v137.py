"""Bounded unauthenticated owner metadata retrieval; never execute upstream code."""
import json,time,urllib.request,urllib.parse,hashlib,sys
from collect_smollm_v47 import ROOT,read,write,append,sha,now
OUT=ROOT/'artifacts/sources/v137'
def main():
 OUT.mkdir(exist_ok=False);start=time.monotonic();total=0;records=[];error=None
 def get(url,path,cap=4000000):
  nonlocal total
  assert urllib.parse.urlparse(url).hostname in ['api.github.com','raw.githubusercontent.com']
  if time.monotonic()-start>150:raise TimeoutError('Source stage reserve')
  req=urllib.request.Request(url,headers={'User-Agent':'bounded-research-source-audit','Accept':'application/vnd.github+json'})
  append(OUT/'attempts.jsonl',{'at':now(),'url':url,'path':path})
  with urllib.request.urlopen(req,timeout=25) as r:body=r.read(min(cap,20000000-total)+1)
  if len(body)>cap or total+len(body)>20000000:raise RuntimeError('Source byte limit')
  total+=len(body);p=OUT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(body);records.append({'url':url,'path':str(p.relative_to(ROOT)),'bytes':len(body),'sha256':sha(p)});write(OUT/'ledger.json',{'saved_bytes':total,'files':records});return body
 try:
  for repo,branch in [('llesoil/input_sensitivity','master'),('ideas-labo/SeMPL','main')]:
   tag=repo.split('/')[-1];commit=json.loads(get(f'https://api.github.com/repos/{repo}/commits/{branch}',f'{tag}/commit.json'))['sha']
   tree=json.loads(get(f'https://api.github.com/repos/{repo}/git/trees/{commit}?recursive=1',f'{tag}/tree.json'));assert tree.get('truncated') is False
   for name in ['README.md','LICENSE']:
    item=next((x for x in tree['tree'] if x['path']==name and x['type']=='blob'),None)
    if item:
     b=get(f'https://raw.githubusercontent.com/{repo}/{commit}/{name}',f'{tag}/{name}');assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==item['sha']
   write(OUT/tag/'identity.json',{'repo':repo,'revision':commit})
 except Exception as e:error=repr(e)
 finally:write(OUT/'summary.json',{'at':now(),'saved_bytes':total,'seconds':time.monotonic()-start,'error':error,'files':records,'new_objective_acquisitions':0,'model_requests':0})
 if error:raise RuntimeError(error)
 print('Saved',total,'metadata bytes')
if __name__=='__main__':main()
