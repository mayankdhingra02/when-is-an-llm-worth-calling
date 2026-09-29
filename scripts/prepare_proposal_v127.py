"""Prepare all thirty prefixes without parsing unacquired objective values."""
import random
from collect_smollm_v47 import ROOT,read,write,sha,now
from analyze_pointwise_v123 import candidates
from proposal_v127 import messages,domains,grammar

def main():
 out=ROOT/'artifacts/study_v127';assert not (out/'jobs.json').exists();cases=read(ROOT/'artifacts/study_v47/jobs.json');assert len(cases)==30;jobs=[]
 for k,j in enumerate(cases):
  spec,c=candidates(j['dataset']);p=read(ROOT/j['prefix'])
  for condition in ['normal']+(['rotated_labels'] if j['seed']==11 else []):
   key=j['key']+'_'+condition;path=out/'prompts'/f'{key}.json';write(path,messages(c.names,c.x,p['state'],spec['meaning'],spec['direction'],condition));jobs.append({**j,'base_key':j['key'],'key':key,'condition':condition,'sampling_seed':127000+j['seed'],'random_proposal_seed':127900+k,'messages_path':str(path.relative_to(ROOT)),'prefix_sha256':sha(ROOT/j['prefix']),'domains':domains(c.x)})
 random.Random(127000).shuffle(jobs);write(out/'jobs.json',jobs);write(out/'cases.json',cases)
 write(out/'inputs.freeze.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in [out/'jobs.json',out/'cases.json']+sorted((out/'prompts').glob('*.json'))}})
 print('Prepared36real requests,30normal and6matched label-rotation probes;zero hidden labels')
if __name__=='__main__':main()
