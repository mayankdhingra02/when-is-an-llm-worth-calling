"""Acquisition boundary: hidden objectives never passed to search routines."""
import csv,hashlib,json,math
from pathlib import Path
from .core import Candidates

def read_table(path,ignored_columns=(),legacy_ignore_suffix_x=False):
    rows=list(csv.reader(Path(path).open())); names=[n.strip() for n in rows[0]]
    ys=[i for i,n in enumerate(names) if n.endswith(('+','-'))]
    xs=[i for i,n in enumerate(names) if not n.endswith(('+','-')) and n not in ignored_columns and not (legacy_ignore_suffix_x and n.endswith('X'))]
    if not ys: raise ValueError('no objective direction')
    seen=set();x=[];y=[];source=[];excluded=[]
    for idx,row in enumerate(rows[1:],start=2):
        if len(row)!=len(names): raise ValueError('ragged table')
        vals=[float(v) for v in row]
        if not all(math.isfinite(v) for v in vals): raise ValueError('missing/nonfinite')
        config=tuple(vals[j] for j in xs)
        if config in seen: excluded.append(idx);continue
        seen.add(config);x.append(config);y.append(tuple(vals[j] for j in ys));source.append(idx)
    c=Candidates(tuple(names[j] for j in xs),tuple(x),tuple(names[j] for j in ys),tuple(names[j][-1] for j in ys),tuple(source))
    return c,tuple(y),excluded

class Oracle:
    def __init__(self,labels,budget=20,prefix=None):
        self.__labels=labels;self.budget=budget;self.acquired={};self.new_accesses=0
        if prefix:
            if len(prefix['ids'])!=len(prefix['labels']): raise ValueError('bad prefix')
            for i,y in zip(prefix['ids'],prefix['labels']):
                if tuple(y)!=tuple(labels[i]) or i in self.acquired: raise ValueError('prefix mismatch')
                self.acquired[i]=tuple(y)
        if len(self.acquired)>budget: raise ValueError('prefix over budget')
    def acquire(self,i):
        if i in self.acquired: raise ValueError('duplicate acquisition')
        if len(self.acquired)>=self.budget: raise RuntimeError('evaluation budget exhausted')
        if not isinstance(i,int) or not 0<=i<len(self.__labels): raise ValueError('invalid index')
        y=tuple(self.__labels[i]);self.acquired[i]=y;self.new_accesses+=1
        return y

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def validate_manifest(m):
    bygroup={}
    for d in m['datasets']:
        g=d['system_group']; split=d['split']
        if g in bygroup and bygroup[g]!=split: raise ValueError('system group crosses splits')
        bygroup[g]=split
        if sha(d['path'])!=d['sha256']: raise ValueError('dataset hash mismatch')
    if len(bygroup)!=3: raise ValueError('smoke requires three distinct groups')
    if m.get('version',1)>=3:
        for d in m['datasets']:
            c,_,excluded=read_table(d['path'],ignored_columns=d['ignored_columns'])
            if list(c.names)!=d['feature_names'] or len(c.x)!=d['unique_configurations']:raise ValueError('explicit schema mismatch')
            if len(excluded)!=d['expected_duplicate_rows']:raise ValueError('duplicate count mismatch')
