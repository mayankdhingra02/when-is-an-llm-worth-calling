"""Preserve earlier checkpoints, then seal V149 rejected analysis, corrected V151, V150/V152 native feasibility and V153 paired native study."""
import argparse,json
from collect_smollm_v47 import ROOT,read,write,sha,now
ART=ROOT/'artifacts/study_v153'
SNAP=ROOT/'artifacts/study_v149/previous_snapshot'
def history():
 old=ROOT/'artifacts/study_v148/evidence_manifest.json';assert sha(old)=='6f944e3680f1e0442331b4dd9b968acc35ef5ac4e98006147135d72e16032bd4'
 stages=read(old)['historical']+[{'stage':'v146_v148_hadoop','manifest_sha256':sha(old),'redirects':{}}];manifests={sha(p):p for p in (ROOT/'artifacts').glob('*/evidence_manifest.json')};mapping=read(SNAP/'mapping.json');cache={};done=[]
 def matches(p,m):
  if not p.exists() or p.stat().st_size!=m['bytes']:return False
  if p not in cache:cache[p]=sha(p)
  return cache[p]==m['sha256']
 for s in stages:
  if 'manifest_sha256' not in s:
   assert s=={'stage':'v78_blocked_checkpoint','audit_status_verified':True};a=read(ROOT/'artifacts/study_v78_blocked/audit.json');assert sha(ROOT/'artifacts/study_v78_execution/previous_snapshot/STATUS.md')==a['status_sha256'];assert sha(ROOT/'artifacts/study_v78_blocked/previous_snapshot/STATUS.md')==a['previous_status_sha256'];done.append(s);continue
  f=manifests[s['manifest_sha256']];files=read(f)['files'];redirects={}
  for n,m in files.items():
   ps=[ROOT/n]
   if n in s['redirects']:ps.append(ROOT/s['redirects'][n])
   if n in mapping:ps.append(ROOT/mapping[n]['snapshot_path'])
   match=next((p for p in ps if matches(p,m)),None);assert match is not None,(s['stage'],n)
   if match!=ROOT/n:redirects[n]=str(match.relative_to(ROOT))
  done.append({'stage':s['stage'],'manifest_sha256':sha(f),'verified_files':len(files),'redirects':redirects})
 return done

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--verify-only',action='store_true');args=ap.parse_args();hist=history();dest=ART/'evidence_manifest.json'
 for frozen in ['artifacts/study_v149/freeze.json','artifacts/study_v151/freeze.json','artifacts/study_v150/preprobe.freeze.json','artifacts/study_v152/preprobe.freeze.json','reports/protocol_v153.freeze.json','artifacts/study_v153/inputs.freeze.json']:
  for n,h in read(ROOT/frozen)['sha256'].items():assert sha(ROOT/n)==h,n
 if args.verify_only:
  d=read(dest)
  for n,m in d['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
  print(json.dumps({'verified':True,'files':len(d['files']),'manifest_sha256':sha(dest),'historical_checkpoints':len(hist)}));return
 assert not dest.exists();names=['.gitignore','STATUS.md','README.md','THIRD_PARTY.md','reports/next_experiment.md','artifacts/study_v148/evidence_manifest.json'];paths={ROOT/n for n in names}
 for folder in ['scripts','reports','configs','tests/synthetic']:
  for version in [149,150,151,152,153]:paths.update(p for p in (ROOT/folder).glob(f'*v{version}*') if p.is_file())
 for folder in ['artifacts/study_v149','artifacts/study_v150','artifacts/study_v151','artifacts/study_v152','artifacts/study_v153','artifacts/sources/v150','results/v149_router','results/v151_router','results/v150_native','results/v152_native','results/v153_native','results/v153_models']:
  paths.update(p for p in (ROOT/folder).rglob('*') if p.is_file())
 paths.update(ROOT/n for n in ['.native-v150/memcached-1.6.45/memcached','.native-v150/memcached-1.6.45/COPYING','.native-v150/libevent-2.1.13-stable/LICENSE','.native-v150/prefix/lib/libevent.a','.native-v150/memcached_client','.native-v150/memcached_client_v152'])
 paths={p for p in paths if p!=dest and p.name not in ['seal_creation.log','seal_verification.json'] and '__pycache__' not in p.parts}
 write(dest,{'at':now(),'scope':'V149 rejected key-collision analysis retained; V151 corrected exploratory routing; V150/V152 forty native feasibility probes; V153 ten real local model requests and four hundred native evaluations including charged validation; no journal-readiness certification','historical':hist,'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}})
 print(json.dumps({'files':len(paths),'manifest_sha256':sha(dest),'historical_checkpoints':len(hist)}))
if __name__=='__main__':main()
