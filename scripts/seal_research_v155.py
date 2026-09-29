"""Preserve earlier checkpoints and seal V154 checkpoint adaptations plus V155 charged GP continuations."""
import argparse,json
from collect_smollm_v47 import ROOT,read,write,sha,now
ART=ROOT/'artifacts/study_v155'
SNAP=ROOT/'artifacts/study_v154/previous_snapshot'
def history():
 old=ROOT/'artifacts/study_v153/evidence_manifest.json';assert sha(old)=='ebc368c28eb72d3a65cf0457c2831f0658315ea7a50d9091c7b7dfbd8b032f76'
 stages=read(old)['historical']+[{'stage':'v149_v153_corrected_router_native_memcached','manifest_sha256':sha(old),'redirects':{}}];manifests={sha(p):p for p in (ROOT/'artifacts').glob('*/evidence_manifest.json')};mapping=read(SNAP/'mapping.json');cache={};done=[]
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
 for frozen in ['artifacts/study_v154/freeze.json','artifacts/study_v155/freeze.json']:
  for n,h in read(ROOT/frozen)['sha256'].items():assert sha(ROOT/n)==h,n
 if args.verify_only:
  d=read(dest)
  for n,m in d['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
  print(json.dumps({'verified':True,'files':len(d['files']),'manifest_sha256':sha(dest),'historical_checkpoints':len(hist)}));return
 assert not dest.exists();names=['.gitignore','STATUS.md','README.md','THIRD_PARTY.md','reports/next_experiment.md','artifacts/study_v153/evidence_manifest.json'];paths={ROOT/n for n in names}
 for folder in ['scripts','reports','configs','tests/synthetic']:
  for version in [154,155]:paths.update(p for p in (ROOT/folder).glob(f'*v{version}*') if p.is_file())
 for folder in ['artifacts/study_v154','artifacts/study_v155','results/v154_controllers','results/v155_gp']:
  paths.update(p for p in (ROOT/folder).rglob('*') if p.is_file())
 paths={p for p in paths if p!=dest and p.name not in ['seal_creation.log','seal_verification.json'] and '__pycache__' not in p.parts}
 write(dest,{'at':now(),'scope':'V154 paper-inspired checkpoint adaptations on genuine historical outcomes; V155 1393 charged GP acquisitions,139complete arms and one unscorable sensitivity arm; no new model/native calls or journal certification','historical':hist,'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}})
 print(json.dumps({'files':len(paths),'manifest_sha256':sha(dest),'historical_checkpoints':len(hist)}))
if __name__=='__main__':main()
