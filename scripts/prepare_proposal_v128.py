"""Two additional exposed families; no new target acquisition in preparation."""
import random,functools,sys
from collect_smollm_v47 import ROOT,read,write,sha,now
sys.path.insert(0,str(ROOT/'src'))
from proposal_v128 import messages,domains

@functools.lru_cache(maxsize=2)
def candidates(dataset):
    if dataset=='wc_5d_c5':
        from table_check_v119 import candidates as load
    elif dataset=='mongodb_twins':
        from table_check_v121 import candidates as load
    else:raise ValueError('Dataset outside frozen cohort')
    spec,c,_=load();return spec,c

def main():
    out=ROOT/'artifacts/study_v128';assert not (out/'jobs.json').exists();cases=[];jobs=[]
    for group,version in [('storm',119),('mongodb',121)]:
        for old in read(ROOT/f'artifacts/study_v{version}/jobs.json'):
            j={k:old[k] for k in ['key','dataset','system_group','prefix']};j.update(seed=old['optimization_seed'],base_key=old['key'],classical_version=version)
            j['split']='exposed_development_extension';spec,c=candidates(j['dataset']);p=read(ROOT/j['prefix']);assert len(p['state']['ids'])==10
            j['prefix_sha256']=sha(ROOT/j['prefix']);cases.append(j)
            for condition in ['normal']+(['rotated_labels'] if j['seed']==11 else []):
                key=j['key']+'_'+condition;path=out/'prompts'/f'{key}.json'
                write(path,messages(c.names,c.x,p['state'],spec['meaning'],spec['direction'],condition))
                jobs.append({**j,'key':key,'condition':condition,'sampling_seed':128000+j['seed'],'random_proposal_seed':128900+len(cases)-1,'messages_path':str(path.relative_to(ROOT)),'domains':domains(c.x)})
    assert len(cases)==10 and len(jobs)==12
    random.Random(128000).shuffle(jobs);write(out/'jobs.json',jobs);write(out/'cases.json',cases)
    paths=[out/'jobs.json',out/'cases.json']+list((out/'prompts').glob('*.json'))
    write(out/'inputs.freeze.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted(paths)}})
    print('Prepared12requests,10normal and2rotation probes;zero new objectives')
if __name__=='__main__':main()
