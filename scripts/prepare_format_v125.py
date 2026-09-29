import random
from collect_smollm_v47 import ROOT,read,write,sha,now
from format_probe_v125 import messages
from surrogate_v124 import SEEDS

def main():
 out=ROOT/'artifacts/study_v125';out.mkdir(exist_ok=False);j=next(j for j in read(ROOT/'artifacts/study_v124/cases.json') if j['system_group']=='hipacc');p=read(ROOT/j['prefix']);spec=next(s for s in read(ROOT/'data/manifest_v41.json')['datasets'] if s['id']==j['dataset']);jobs=[]
 for condition in ['marked_json','reference_text']:
  for i in '012':
   path=out/'prompts'/f'{condition}_{i}.json';write(path,messages(p,i,spec['meaning'],condition))
   for seed in SEEDS:jobs.append({**j,'base_key':j['key'],'key':f"{j['key']}_{condition}_{i}_{seed}",'condition':condition,'candidate_id':i,'sampling_seed':seed,'messages_path':str(path.relative_to(ROOT)),'prefix_sha256':sha(ROOT/j['prefix']),'original_request_key':f"{j['key']}_{i}_{seed}"})
 random.Random(125000).shuffle(jobs);write(out/'jobs.json',jobs);write(out/'cases.json',[j]);write(out/'inputs.freeze.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in [out/'jobs.json',out/'cases.json']+sorted((out/'prompts').glob('*'))}});print('Prepared18format probes; no targets acquired')
if __name__=='__main__':main()
