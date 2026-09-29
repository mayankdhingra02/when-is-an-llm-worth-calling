"""Seal the V171 independent post-hoc audit and the frozen, unauthorized V172 proposal."""
import argparse,json
from collect_smollm_v47 import ROOT,read,write,sha,now
ART=ROOT/'artifacts/study_v171'
SNAP=ART/'previous_snapshot'
V170='artifacts/study_v170/evidence_manifest.json';V170_SHA='2eb6a885f3cf0af98c0149230c7619b6a795e1f0f6e63810c69b528617d32517'
def history():
 old=ROOT/V170;assert sha(old)==V170_SHA
 stages=read(old)['historical']+[{'stage':'v170_ezr_sources','manifest_sha256':V170_SHA,'redirects':{}}]
 manifests={sha(p):p for p in (ROOT/'artifacts').glob('*/evidence_manifest.json')};mapping=read(SNAP/'mapping.json');cache={};done=[]
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
 for n,h in read(ART/'freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
 for n,m in read(SNAP/'mapping.json').items():assert sha(ROOT/m['snapshot_path'])==m['sha256'],n
 if args.verify_only:
  d=read(dest)
  for n,m in d['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
  print(json.dumps({'verified':True,'files':len(d['files']),'manifest_sha256':sha(dest),'historical_checkpoints':len(hist)}));return
 assert not dest.exists();names=['.gitignore','STATUS.md','README.md','THIRD_PARTY.md','CLAUDE_HANDOFF.md','reports/next_experiment.md',V170];paths={ROOT/n for n in names}
 for folder in ['scripts','reports','configs','tests/synthetic']:
  for tag in ['v171','v172']:paths.update(p for p in (ROOT/folder).glob(f'*{tag}*') if p.is_file())
 for folder in ['artifacts/study_v171','results/v171_audit']:paths.update(p for p in (ROOT/folder).rglob('*') if p.is_file())
 paths={p for p in paths if p!=dest and p.name not in ['seal_creation.log','seal_verification.json'] and '__pycache__' not in p.parts}
 write(dest,{'at':now(),'scope':'V171: independent post-hoc exploratory audit of sealed exposed records (zero acquisitions, model requests, downloads or native executions) plus a hash-frozen V172 model-scale proposal that is not authorized for collection.','historical':hist,'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}})
 print(json.dumps({'files':len(paths),'manifest_sha256':sha(dest),'historical_checkpoints':len(hist)}))
if __name__=='__main__':main()
