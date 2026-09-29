"""Exact acquired-label 3NN adaptation; no unacquired objective access in chooser."""
import csv
from fractions import Fraction
from pathlib import Path

def choose(c,order,ids,labels,cap):
    if len(ids)!=len(labels) or len(ids)<3 or len(ids)!=len(set(ids)):raise ValueError('Invalid acquired state')
    acquired=[[Fraction(v) for v in pair] for pair in labels];limit=Fraction(cap)
    if any(len(p)!=2 or any(v<=0 for v in p) for p in acquired) or limit<=0:raise ValueError('Positive joint labels/cap required')
    available=[i for i in order if i not in ids];scores=[]
    for position,row in enumerate(available):
        near=sorted(range(len(ids)),key=lambda j:(sum(a!=b for a,b in zip(c.x[row],c.x[ids[j]])),j))[:3]
        runtime=sum((acquired[j][0] for j in near),Fraction(0));size=sum((acquired[j][1] for j in near),Fraction(0))
        scores.append((row,position,runtime,size,[ids[j] for j in near]))
    feasible=[v for v in scores if v[3]<=3*limit]
    if not scores:raise ValueError('No candidates')
    best=min(feasible,key=lambda v:(v[2],v[1])) if feasible else min(scores,key=lambda v:(v[3],v[2],v[1]))
    return best[0],{'neighbor_ids':best[4],'runtime_sum_fraction':str(best[2]),'size_sum_fraction':str(best[3]),'predicted_feasible':best[3]<=3*limit}

class Oracle:
    def __init__(self,spec,c,prefix,journal):self.spec=spec;self.c=c;self.used=set(prefix['ids']);self.journal=journal;self.new_accesses=0
    def acquire(self,row_id):
        if type(row_id) is not int or not 0<=row_id<len(self.c.source_ids) or row_id in self.used or len(self.used)>=20:raise ValueError('Invalid/duplicate/over-budget row')
        with Path(self.spec['path']).open(newline='') as f:
            for line,row in enumerate(csv.DictReader(f,delimiter=self.spec['delimiter']),2):
                if line!=self.c.source_ids[row_id]:continue
                self.used.add(row_id);self.new_accesses+=1
                raw=[row['performance'],row['size']]
                self.journal({'row_id':row_id,'source_line':line,'raw_runtime':raw[0],'raw_size':raw[1],'vector_charge':1})
                if any(Fraction(v)<=0 for v in raw):raise ValueError('Invalid acquired outcome')
                return raw
        raise ValueError('Missing source row')

def continuation(c,prefix,pool,mode,acquire,checkpoint=lambda x:None):
    if mode not in ('joint_shortlist','joint_full') or len(prefix['ids'])!=10 or len(set(prefix['ids']))!=10:raise ValueError('Fixed mode and ten-prefix required')
    if len(pool)!=len(set(pool)) or len(pool)!=20 or set(pool)&set(prefix['ids']):raise ValueError('Twenty unseen pool members')
    ids=prefix['ids'][:];labels=[p[:] for p in prefix['labels']];events=[]
    order=prefix['order'] if mode=='joint_full' else [i for i in prefix['order'] if i in set(pool)|set(ids)]
    for _ in range(10):
        row,details=choose(c,order,ids,labels,prefix['size_cap']);labels.append(acquire(row));ids.append(row)
        events.append({'row_id':row,**details});checkpoint({'ids':ids,'labels':labels,'events':events})
    eligible=[j for j,y in enumerate(labels) if Fraction(y[1])<=Fraction(prefix['size_cap'])]
    best=min(eligible,key=lambda j:Fraction(labels[j][0]))
    return {'ids':ids,'labels':labels,'events':events,'best_row':ids[best],'best_runtime':labels[best][0],'best_size':labels[best][1],
        'infeasible_new_acquisitions':sum(Fraction(y[1])>Fraction(prefix['size_cap']) for y in labels[10:])}
