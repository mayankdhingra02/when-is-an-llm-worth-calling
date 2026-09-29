"""Transform only saved prefix inputs into normal and intervention prompts."""
import json,random
from collect_smollm_v47 import ROOT,read,write,sha,now
from pointwise_v123 import messages,IDS

def main():
    out=ROOT/'artifacts/study_v123';assert not (out/'jobs.json').exists();specs={s['id']:s for s in read(ROOT/'data/manifest_v41.json')['datasets']};old=read(ROOT/'artifacts/study_v47/jobs.json');groups=sorted({j['system_group'] for j in old})[:3];assert groups==['berkeleydb','dune_hsmgp','hipacc']
    chosen=[j for g in groups for j in old if j['system_group']==g and j['seed']==11];assert len(chosen)==3;jobs=[]
    for base in chosen:
        p=read(ROOT/base['prefix']);assert len(p['state']['ids'])==10
        for condition,ids in [('normal',IDS),('loss_blind',IDS[:10]),('observations_reversed',IDS[:3])]:
            for candidate in ids:
                key=f"{base['key']}_{condition}_{candidate}";msgs=messages(p,candidate,condition,specs[base['dataset']]['meaning']);path=out/'prompts'/f'{key}.json';write(path,msgs);jobs.append({**base,'base_key':base['key'],'key':key,'candidate_id':candidate,'condition':condition,'messages_path':str(path.relative_to(ROOT)),'prefix_sha256':sha(ROOT/base['prefix'])})
    random.Random(123000).shuffle(jobs);assert len(jobs)==99;write(out/'jobs.json',jobs);write(out/'cases.json',chosen)
    write(out/'inputs.freeze.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in [out/'jobs.json',out/'cases.json']+sorted((out/'prompts').glob('*.json'))}})
    print('Prepared99prompts:60normal,30loss-blind,9observation-order; no target acquisitions')
if __name__=='__main__':main()
