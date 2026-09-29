"""Prepare all prompts using only frozen prefixes and model-visible features."""
import random
from collect_smollm_v47 import ROOT,read,write,sha,now
from surrogate_v124 import IDS,SEEDS,messages

def main():
    out=ROOT/'artifacts/study_v124';assert not (out/'jobs.json').exists();cases=read(ROOT/'artifacts/study_v123/cases.json');specs={s['id']:s for s in read(ROOT/'data/manifest_v41.json')['datasets']};jobs=[]
    for j in cases:
        assert specs[j['dataset']]['direction']=='-';p=read(ROOT/j['prefix'])
        for i in IDS:
            path=out/'prompts'/f"{j['key']}_{i}.json";write(path,messages(p,i,specs[j['dataset']]['meaning']))
            for seed in SEEDS:jobs.append({**j,'base_key':j['key'],'key':f"{j['key']}_{i}_{seed}",'candidate_id':i,'sampling_seed':seed,'messages_path':str(path.relative_to(ROOT)),'prefix_sha256':sha(ROOT/j['prefix'])})
    random.Random(124000).shuffle(jobs);assert len(jobs)==180;write(out/'jobs.json',jobs);write(out/'cases.json',cases)
    write(out/'inputs.freeze.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in [out/'jobs.json',out/'cases.json']+sorted((out/'prompts').glob('*'))}})
    print('Prepared180requests from60candidate prompts; zero hidden target accesses')
if __name__=='__main__':main()
