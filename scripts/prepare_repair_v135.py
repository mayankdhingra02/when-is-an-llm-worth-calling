"""Prepare same-prompt SAC capacity repair; zero hidden-target parsing."""
import copy
from collect_smollm_v47 import ROOT,read,write,sha,now
from analyze_pointwise_v123 import candidates
from proposal_v128 import domains

def main():
 a=ROOT/'artifacts/study_v135';a.mkdir(exist_ok=False);jobs=[]
 for j in sorted(read(ROOT/'artifacts/study_v127/jobs.json'),key=lambda j:j['seed']):
  if j['system_group']!='sac' or j['condition']!='normal':continue
  spec,c=candidates(j['dataset']);assert domains(c.x)==j['domains'];p=read(ROOT/j['prefix']);assert sha(ROOT/j['prefix'])==j['prefix_sha256'];path=a/'prompts'/f"{j['key']}.json";write(path,read(ROOT/j['messages_path']));job={**j,'old_messages_path':j['messages_path'],'messages_path':str(path.relative_to(ROOT))};assert sha(path)==sha(ROOT/j['messages_path']);jobs.append(job)
  write(a/'candidates.json',{'names':list(c.names),'x':[list(x) for x in c.x],'source_ids':list(c.source_ids),'directions':list(c.directions),'source_spec':spec})
 assert len(jobs)==5 and all(len(j['domains'])==59 for j in jobs);write(a/'jobs.json',jobs)
 paths=[a/'jobs.json',a/'candidates.json']+list((a/'prompts').glob('*.json'))+[ROOT/j['prefix'] for j in jobs]
 write(a/'inputs.freeze.json',{'at':now(),'scope':'Original prompts/prefixes and feature-only candidates; zero new objective accesses','sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths}})
if __name__=='__main__':main()
