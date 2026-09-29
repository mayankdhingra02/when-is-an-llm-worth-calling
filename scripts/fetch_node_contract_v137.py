"""Bounded owner-only follow-up: input mapping and benchmark flag propagation."""
import hashlib,time,urllib.request
from collect_smollm_v47 import ROOT,read,write,sha,now,append
def main():
 base=ROOT/'artifacts/sources/v137';owner=base/'input_sensitivity';identity=read(owner/'identity.json');tree={x['path']:x for x in read(owner/'tree.json')['tree']}
 names=['replication/containers/nodejs/listInputs.csv','replication/containers/nodejs/listInputs.txt']
 requests=[{'url':f"https://raw.githubusercontent.com/{identity['repo']}/{identity['revision']}/{n}",'path':str((owner/n).relative_to(ROOT)),'git_sha':tree[n]['sha']} for n in names]
 requests += [{'url':f'https://raw.githubusercontent.com/nodejs/node/v15.14.0/benchmark/{n}','path':f'artifacts/sources/v137/node-v15.14.0/benchmark/{n}'} for n in ['run.js','common.js']]
 plan=ROOT/'artifacts/study_v137/node_contract_plan.json';assert not plan.exists();write(plan,{'at':now(),'scope':'Owner source/mapping only, no targets or execution','requests':requests,'max_new_bytes':1000000,'max_seconds':120})
 start=time.monotonic();total=read(base/'feature_summary.json')['cumulative_stage_saved_bytes'];original=total;files=[];error=None
 try:
  for req in requests:
   p=ROOT/req['path'];assert not p.exists()
   if time.monotonic()-start>90:raise TimeoutError('Stage reserve')
   append(base/'node_contract_attempts.jsonl',{'at':now(),'url':req['url']})
   with urllib.request.urlopen(urllib.request.Request(req['url'],headers={'User-Agent':'bounded-research-audit'}),timeout=25) as r:b=r.read(1000001-(total-original))
   if total-original+len(b)>1000000 or total+len(b)>20000000:raise RuntimeError('Source cap')
   p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);total+=len(b)
   if 'git_sha' in req:assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==req['git_sha']
   files.append({**req,'bytes':len(b),'sha256':sha(p)})
 except Exception as e:error=repr(e)
 finally:write(base/'node_contract_summary.json',{'error':error,'files':files,'new_saved_bytes':total-original,'cumulative_stage_saved_bytes':total,'seconds':time.monotonic()-start,'new_objective_values':0})
 if error:raise RuntimeError(error)
 print('Saved',len(files),'owner mapping/source files;',total,'cumulative source bytes')
if __name__=='__main__':main()
