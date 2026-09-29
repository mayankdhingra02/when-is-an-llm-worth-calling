"""Fetch an explicit list of pinned owner documents, not measured CSVs."""
import json,time,urllib.request,hashlib
from collect_smollm_v47 import ROOT,read,write,append,sha,now
def main():
 base=ROOT/'artifacts/sources/v137';out=base/'input_sensitivity';identity=read(out/'identity.json');tree={x['path']:x for x in read(out/'tree.json')['tree']};plan=read(ROOT/'artifacts/study_v137/docs_plan.json');start=time.monotonic();total=read(base/'summary.json')['saved_bytes'];records=[];error=None
 try:
  for name in plan['paths']:
   assert name in tree and tree[name]['type']=='blob' and not name.endswith('.csv')
   dest=out/name;assert not dest.exists();url=f"https://raw.githubusercontent.com/{identity['repo']}/{identity['revision']}/{name}"
   if time.monotonic()-start>150:raise TimeoutError('Source reserve')
   append(base/'docs_attempts.jsonl',{'at':now(),'url':url})
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'bounded-research-source-audit'}),timeout=25) as r:b=r.read(min(3000000,20000000-total)+1)
   if len(b)>3000000 or total+len(b)>20000000:raise RuntimeError('Source size cap')
   total+=len(b);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b);assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==tree[name]['sha'];records.append({'path':str(dest.relative_to(ROOT)),'url':url,'bytes':len(b),'sha256':sha(dest),'git_sha':tree[name]['sha']})
 except Exception as e:error=repr(e)
 finally:write(base/'docs_summary.json',{'error':error,'files':records,'cumulative_stage_saved_bytes':total,'new_saved_bytes':sum(r['bytes'] for r in records),'seconds':time.monotonic()-start,'new_objective_values':0})
 if error:raise RuntimeError(error)
 print('Saved',len(records),'documents;',total,'total source bytes')
if __name__=='__main__':main()
