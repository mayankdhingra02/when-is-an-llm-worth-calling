"""Preserve V140 and earlier checkpoints, then seal V141 matched-model replication and V142 startup repair."""
import argparse,json
from collect_smollm_v47 import ROOT,read,write,sha,now
ART=ROOT/'artifacts/study_v141'
SNAP=ROOT/'artifacts/study_v141/previous_snapshot'
def history():
 old=ROOT/'artifacts/study_v140/evidence_manifest.json';assert sha(old)=='9bcffcf529696ae825c3fc4826f123fec5d35da0677796eac6884eb27b1557a2'
 stages=read(old)['historical']+[{'stage':'v139_sources_v140_native_xz','manifest_sha256':sha(old),'redirects':{}}];manifests={sha(p):p for p in (ROOT/'artifacts').glob('*/evidence_manifest.json')};mapping=read(SNAP/'mapping.json');cache={};done=[]
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
 for version in [141,142]:
  for n,h in read(ROOT/f'reports/protocol_v{version}.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
 if args.verify_only:
  d=read(dest)
  for n,m in d['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
  print(json.dumps({'verified':True,'files':len(d['files']),'manifest_sha256':sha(dest),'historical_checkpoints':len(hist)}));return
 assert not dest.exists();names=['STATUS.md','README.md','THIRD_PARTY.md','reports/next_experiment.md','artifacts/study_v140/evidence_manifest.json','output/v141_replay.zip'];paths={ROOT/n for n in names}
 for folder in ['scripts','reports','configs','tests/synthetic']:
  for version in [141,142]:paths.update(p for p in (ROOT/folder).glob(f'*v{version}*') if p.is_file())
 for folder in ['artifacts/study_v141','artifacts/study_v142','results/v141_models','results/v142_smollm','results/v141_analysis','output/v141_replay']:
  paths.update(p for p in (ROOT/folder).rglob('*') if p.is_file())
 paths={p for p in paths if p!=dest and p.name not in ['seal_creation.log','seal_verification.json'] and '__pycache__' not in p.parts}
 write(dest,{'at':now(),'scope':'V141 prospective matched-model replication with V142 pre-outcome startup repair on six exposed families; 60 intended real local requests, 600 recorded acquisitions; no new holdout or journal readiness claim','historical':hist,'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}})
 print(json.dumps({'files':len(paths),'manifest_sha256':sha(dest),'historical_checkpoints':len(hist)}))
if __name__=='__main__':main()
