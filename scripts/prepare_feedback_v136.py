"""Feature-only admission and fixed scheduling; no new outcome acquisitions."""
import random
from collect_smollm_v47 import ROOT,read,write,sha,now
from analyze_pointwise_v123 import candidates
from feedback_v136 import domains
def main():
 a=ROOT/'artifacts/study_v136';assert not (a/'jobs.json').exists()
 old=[j for j in read(ROOT/'artifacts/study_v127/jobs.json') if j['condition']=='normal']
 widths={j['system_group']:len(j['domains']) for j in old}
 groups=sorted(widths,key=lambda g:(widths[g],g));selected=[groups[0],groups[-1]]
 jobs=sorted([j for j in old if j['system_group'] in selected],key=lambda j:(j['system_group'],j['seed']))
 random.Random(136000).shuffle(jobs)
 for index,j in enumerate(jobs):
  spec,c=candidates(j['dataset']);assert domains(c.x)==j['domains'];assert sha(ROOT/j['prefix'])==j['prefix_sha256']
  write(a/'candidates'/f"{j['system_group']}.json",{'names':list(c.names),'x':c.x,'source_ids':c.source_ids,'directions':c.directions,'spec':spec})
  j['schedule']=[]
  for r in range(5):
   modes=['feedback','masked'];random.Random(136000+index*100+r).shuffle(modes)
   j['schedule'].append({'round':r,'sampling_seed':136000+index*100+r,'arm_order':modes})
  j['historical_batch']=f"results/v127_analysis/arms/{j['base_key']}_model.json" if j['system_group']=='llvm' else f"results/v135_analysis/arms/{j['base_key']}_normal.json"
  j['historical_sequential']=f"results/v41_transfer/arms/{j['base_key']}_full_sequential_3nn.json"
  for key in ['historical_batch','historical_sequential']:
   s=read(ROOT/j[key])['state'];p=read(ROOT/j['prefix'])['state'];assert s['ids'][:10]==p['ids'] and s['labels'][:10]==p['labels'] and len(set(s['ids']))==20
 assert len(jobs)==10
 write(a/'admission.json',{'rule':'Minimum and maximum feature counts among the six original V127 normal families; all five fixed seeds; no quality-based selection','widths':widths,'selected':selected,'at':now()})
 write(a/'jobs.json',jobs)
if __name__=='__main__':main()
