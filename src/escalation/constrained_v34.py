"""Charged joint-label boundary and fixed size-aware continuation controls."""
import csv,math
from pathlib import Path
from .quality_controls_v12 import choose

MODES=('joint_shortlist','joint_full','static_rank','runtime_3nn',
       'cached_llm_assigned_ids','cached_llm_reverse_display','cached_llm_reassigned_ids')

class JointOracle:
    def __init__(self,spec,candidates,journal,prefix=None):
        self.spec=spec;self.c=candidates;self.journal=journal
        self.used=set() if prefix is None else set(prefix['ids']);self.new_accesses=0
    def acquire(self,row_id):
        if type(row_id) is not int or not 0<=row_id<len(self.c.source_ids) or row_id in self.used or len(self.used)>=20:
            raise ValueError('Invalid, duplicate or over-budget joint acquisition')
        with Path(self.spec['path']).open(newline='') as f:
            for number,row in enumerate(csv.DictReader(f,delimiter=self.spec['delimiter']),2):
                if number!=self.c.source_ids[row_id]:continue
                self.used.add(row_id);self.new_accesses+=1
                self.journal({'row_id':row_id,'source_line':number,'raw_runtime':row['performance'],'raw_size':row['size'],'vector_charge':1})
                pair=[float(row['performance']),float(row['size'])]
                if not all(math.isfinite(v) and v>0 for v in pair):raise ValueError('Invalid charged joint outcome')
                return pair
        raise ValueError('Source row missing')

def terminal(ids,labels,cap):
    eligible=[j for j,y in enumerate(labels) if y[1]<=cap]
    if not eligible:raise ValueError('Feasible incumbent required')
    best=min(eligible,key=lambda j:labels[j][0]);raw=min(range(len(ids)),key=lambda j:labels[j][0])
    return {'best_row':ids[best],'best_runtime':labels[best][0],'best_size':labels[best][1],
        'runtime_only_best_row':ids[raw],'runtime_only_best_runtime':labels[raw][0],
        'runtime_only_best_size':labels[raw][1],'runtime_only_best_violates_cap':labels[raw][1]>cap,
        'infeasible_new_acquisitions':sum(y[1]>cap for y in labels[10:])}

def continuation(c,prefix,pool,mode,selected,acquire,checkpoint=lambda state:None):
    if mode not in MODES or len(prefix['ids'])!=10 or len(set(pool))!=20:
        raise ValueError('Fixed mode, ten-prefix and twenty-row pool required')
    if len(pool)!=20 or set(pool)&set(prefix['ids']) or not set(pool)<=set(prefix['order']):raise ValueError('Invalid pool')
    if mode not in ('joint_shortlist','joint_full'):
        if len(selected)!=10 or len(set(selected))!=10 or set(selected)&set(prefix['ids']) or not set(selected)<=set(pool):
            raise ValueError('Invalid frozen selection')
    ids=list(prefix['ids']);labels=[list(y) for y in prefix['labels']];events=[]
    order=prefix['order'] if mode=='joint_full' else [i for i in prefix['order'] if i in set(pool)|set(ids)]
    for step in range(10):
        if mode.startswith('joint_'):row,trace=choose(c,order,ids,labels,prefix['size_cap'],'joint_3nn')
        else:row,trace=selected[step],{'frozen_action':True}
        labels.append(acquire(row));ids.append(row);events.append({'row_id':row,**trace})
        checkpoint({'ids':ids,'labels':labels,'events':events})
    return {'ids':ids,'labels':labels,'events':events,'size_cap':prefix['size_cap'],**terminal(ids,labels,prefix['size_cap'])}
