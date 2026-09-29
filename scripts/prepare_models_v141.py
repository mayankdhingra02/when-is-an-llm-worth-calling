"""Prepare feature-only matched model jobs; no new target acquisition."""
import random
from collect_smollm_v47 import ROOT,read,write,sha,now
def main():
 a=ROOT/'artifacts/study_v141';assert not (a/'jobs.json').exists()
 jobs=read(ROOT/'artifacts/study_v138/jobs.json');assert len(jobs)==30
 for j in jobs:
  assert sha(ROOT/j['prefix'])==j['prefix_sha256'];old=j['messages_path'];p=a/'prompts'/f"{j['key']}.json";write(p,read(ROOT/old));assert sha(p)==sha(ROOT/old)
  j.update(old_messages_path=old,messages_path=str(p.relative_to(ROOT)),sampling_seed=141000+j['seed'])
  c=ROOT/f"artifacts/study_v138/candidates/{j['system_group']}.json";write(a/'candidates'/c.name,read(c))
 random.Random(141100).shuffle(jobs);write(a/'jobs.json',jobs)
 paths=list((a/'prompts').glob('*.json'))+list((a/'candidates').glob('*.json'))+[a/'jobs.json',a/'models.json']+[ROOT/j['prefix'] for j in jobs]
 write(a/'inputs.freeze.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths}})
if __name__=='__main__':main()
