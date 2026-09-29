"""Verify bounded owner-download receipts offline, without parsing target cells."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 base=ROOT/'artifacts/sources/v137';names=['summary','docs_summary','code_summary','feature_summary','node_contract_summary','cleaning_summary'];total=0;seen=set();git=0
 for name in names:
  d=json.loads((base/f'{name}.json').read_text());assert d.get('error') is None;stage=0
  for f in d['files']:
   p=ROOT/f['path'];assert p not in seen;seen.add(p);b=p.read_bytes();assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'];assert f['url'].startswith(('https://api.github.com/','https://raw.githubusercontent.com/'));stage+=len(b)
   if 'git_sha' in f:assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==f['git_sha'];git+=1
  total+=stage;assert total==d.get('cumulative_stage_saved_bytes',d.get('saved_bytes'))
  if 'new_saved_bytes' in d:assert stage==d['new_saved_bytes']
 assert total==7059029<=20000000
 r={'verified':True,'files':len(seen),'git_blob_hashes_verified':git,'stage_saved_bytes':total,'cumulative_saved_bytes':10238031060+total,'cumulative_cap_bytes':10737418240,'remaining_bytes':10737418240-10238031060-total,'objective_values_parsed':0}
 (ROOT/'artifacts/study_v137/source_verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
