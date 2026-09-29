"""Acquired-only optimizer over V15 recorded medians; physical costs remain separate."""
import csv,copy,math,random
from types import SimpleNamespace
from .quality_controls_v12 import choose

REFERENCES={
 'zstd':{'level':3,'window_log':19,'checksum':True},
 'lz4':{'level':1,'block_id':7,'dependent':False},
 'zlib':{'level':6,'memory_level':8,'filtered':False},
}
FEATURES={'zstd':('level','window_log','checksum'),'lz4':('level','block_id','dependent'),'zlib':('level','memory_level','filtered')}


def candidates(entry):
    family=entry['system_group'];rows=entry['configurations'];names=FEATURES[family]
    xs=tuple(tuple(float(r[n]) for n in names) for r in rows)
    if len(xs)!=32 or len(set(xs))!=32:raise ValueError('Frozen32-row feature space required')
    reference=next(i for i,r in enumerate(rows) if all(r[k]==v for k,v in REFERENCES[family].items()))
    return SimpleNamespace(x=xs),[r['config_id'] for r in rows],reference


class RecordedOracle:
    """Parse only the requested target vector; charge before parsing; clone prefix state."""
    def __init__(self,path,family,config_ids,journal,budget=20,prefix=None):
        self.path=path;self.family=family;self.config_ids=config_ids;self.journal=journal;self.budget=budget
        self.acquired=copy.deepcopy(prefix or {})
        if len(self.acquired)>budget:raise ValueError('Prefix exceeds budget')
    def acquire(self,index):
        if type(index) is not int or not 0<=index<len(self.config_ids) or index in self.acquired:raise ValueError('Invalid or duplicate acquisition')
        if len(self.acquired)>=self.budget:raise RuntimeError('Evaluation budget exhausted')
        self.acquired[index]=None
        self.journal({'row_id':index,'config_id':self.config_ids[index],'charged_recorded_vector':1})
        with open(self.path,newline='') as handle:
            for row in csv.DictReader(handle):
                if row['family']==self.family and row['config_id']==self.config_ids[index]:
                    if row['successful_trials']!='3':raise ValueError('Incomplete source observations')
                    label=[float(row['median_compression_ms']),float(row['compressed_bytes'])]
                    if not all(math.isfinite(v) and v>0 for v in label):raise ValueError('Invalid recorded target')
                    self.acquired[index]=label
                    return label.copy()
        raise ValueError('Missing source row')


def make_prefix(c,config_ids,reference,seed,oracle):
    order=list(range(len(config_ids)));random.Random(seed).shuffle(order)
    ids=[];labels=[];steps=[]
    initial=[reference]+[i for i in order if i!=reference][:3]
    for index in initial:
        labels.append(oracle.acquire(index));ids.append(index)
    cap=labels[0][1]
    while len(ids)<10:
        index,prediction=choose(c,order,ids,labels,cap,'joint_3nn')
        label=oracle.acquire(index);steps.append({'row_id':index,'prediction':prediction});ids.append(index);labels.append(label)
    return {'order':order,'ids':ids,'labels':labels,'size_cap':cap,'reference_row':reference,'prefix_steps':steps}


def continuation(c,prefix,oracle,method):
    ids=list(prefix['ids']);labels=copy.deepcopy(prefix['labels']);steps=[]
    while len(ids)<20:
        index,prediction=choose(c,prefix['order'],ids,labels,prefix['size_cap'],method)
        label=oracle.acquire(index);steps.append({'row_id':index,'prediction':prediction});ids.append(index);labels.append(label)
    feasible=[(label[0],i) for i,label in zip(ids,labels) if label[1]<=prefix['size_cap']]
    best_runtime,best_row=min(feasible)
    return {'ids':ids,'labels':labels,'steps':steps,'size_cap':prefix['size_cap'],'best_feasible_ms':best_runtime,'best_row':best_row,
            'infeasible_continuation_acquisitions':sum(y[1]>prefix['size_cap'] for y in labels[10:])}
