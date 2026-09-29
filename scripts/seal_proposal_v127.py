"""Preserve V126 and earlier checkpoints, then seal the new proposal assay."""
import argparse,json
from collect_smollm_v47 import ROOT,read,write,sha,now
ART=ROOT/'artifacts/study_v127'
def history():
 old=ROOT/'artifacts/study_v126/evidence_manifest.json';assert sha(old)=='82dcce43d9f937d7eb0f5b65c789d6a73f0dad4855cc29de458a26a6883e54a7'
 stages=read(old)['historical']+[{'stage':'v124_v126_combined','manifest_sha256':sha(old),'redirects':{}}];manifests={sha(p):p for p in (ROOT/'artifacts').glob('*/evidence_manifest.json')};mapping=read(ART/'previous_snapshot/mapping.json');cache={};done=[]
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
 for n,h in read(ROOT/'reports/protocol_v127.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
 if args.verify_only:
  d=read(dest)
  for n,m in d['files'].items():assert sha(ROOT/n)==m['sha256'] and (ROOT/n).stat().st_size==m['bytes'],n
  print(json.dumps({'verified':True,'files':len(d['files']),'manifest_sha256':sha(dest),'historical_checkpoints':len(hist)}));return
 assert not dest.exists();names=['STATUS.md','README.md','THIRD_PARTY.md','reports/next_experiment.md','artifacts/study_v126/evidence_manifest.json','output/v127_replay.zip','output/v126_replay_corrected.zip'];paths={ROOT/n for n in names}
 for folder in ['scripts','reports','configs','tests/synthetic']:paths.update(p for p in (ROOT/folder).glob('*v127*') if p.is_file())
 for folder in [ART,ROOT/'results/v127_proposals',ROOT/'results/v127_analysis',ROOT/'output/v127_replay',ROOT/'output/v126_replay_corrected']:paths.update(p for p in folder.rglob('*') if p.is_file())
 paths={p for p in paths if p!=dest and p.name not in ['seal_creation.log','seal_verification.json'] and '__pycache__' not in p.parts}
 write(dest,{'at':now(),'scope':'V127 real full-domain feature proposals with matched projection and full-domain classical controls;exposed development;V126packaging wording correction;no held-out router or journal acceptance claim','historical':hist,'files':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)}});print(json.dumps({'files':len(paths),'manifest_sha256':sha(dest),'historical_checkpoints':len(hist)}))
if __name__=='__main__':main()
