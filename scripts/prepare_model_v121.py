"""Freeze normal and paired loss-blind messages before any model call."""
import copy,json
from table_check_v121 import ROOT,read,write,sha,now,frozen
from verify_table_classical_v121 import verify

def blinded(messages):
    msgs=copy.deepcopy(messages);lead,body=msgs[1]['content'].split('\n',1);d=json.loads(body)
    for row in d['observations']:row['loss']=.5
    msgs[1]['content']=lead+'\n'+json.dumps(d,separators=(',',':'));return msgs

def main():
    frozen();assert verify()['verified'];jobs=[]
    for j in read(ROOT/'artifacts/study_v121/jobs.json'):
        for condition in ['normal','loss_blind']:
            key=j['key']+'_'+condition;p=read(ROOT/j['prefix']);p['messages']=p['messages'] if condition=='normal' else blinded(p['messages'])
            pp=ROOT/f'artifacts/study_v121/model_prefixes/{key}.json';write(pp,p)
            jobs.append({**j,'key':key,'base_key':j['key'],'condition':condition,'prefix':str(pp.relative_to(ROOT)),'original_prefix':j['prefix']})
    assert len(jobs)==10;write(ROOT/'artifacts/study_v121/model_jobs.json',jobs)
    paths=[ROOT/'results/v121_classical/policy_precommit.json',ROOT/'artifacts/study_v121/model_jobs.json']+[ROOT/j['prefix'] for j in jobs]
    write(ROOT/'artifacts/study_v121/model_inputs.freeze.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths}})
if __name__=='__main__':main()
