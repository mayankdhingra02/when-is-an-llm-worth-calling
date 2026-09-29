"""Explicit finite-domain acquisition boundary, prompts and predecision features."""
import csv, math, random, time
from collections import Counter
from pathlib import Path
import numpy as np
from .finite_domain import FiniteCandidates, modal_centroid, recommend, decode_indices, encode_indices
from .core import State, losses, distances
from .data import sha
from .io import digest

ALPHABET='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
VERSION='finite_symbols_10_v6'

def load_candidates(spec):
    """Read features only; save source row numbers for an independent lazy oracle."""
    if sha(spec['path'])!=spec['sha256']:raise ValueError('data hash mismatch')
    names=spec['feature_names'];objectives=spec['objective_columns'];meta=spec['metadata_columns']
    if set(names)&(set(objectives)|set(meta)) or spec['primary_objective'] not in objectives:raise ValueError('objective isolation')
    with Path(spec['path']).open(newline='') as f:
        reader=csv.DictReader(f,delimiter=spec['delimiter'])
        if len(reader.fieldnames)!=len(set(reader.fieldnames)) or set(reader.fieldnames)!=set(names)|set(objectives)|set(meta):raise ValueError('explicit schema mismatch')
        seen=set();xs=[];ids=[];duplicates=[]
        for line,row in enumerate(reader,2):
            if any(row[k]!=str(v) for k,v in spec['filters'].items()):continue
            x=tuple(float(row[k]) for k in names)
            if not all(math.isfinite(v) for v in x):raise ValueError('invalid feature')
            if x in seen:duplicates.append(line);continue
            seen.add(x);xs.append(x);ids.append(line)
    c=FiniteCandidates(tuple(names),tuple(xs),(spec['primary_objective'],),(spec['direction'],),tuple(ids))
    if len(xs)!=spec['rows'] or len(duplicates)!=spec['duplicates']:raise ValueError('candidate counts changed')
    return c

class LazyOracle:
    """Parse only the requested target cell, journal every actual acquisition."""
    def __init__(self,spec,c,budget=20,prefix=None,journal=None):
        self.spec=spec;self.c=c;self.budget=budget;self.journal=journal;self.acquired={};self.new_accesses=0
        if prefix:
            if len(prefix['ids'])!=len(prefix['labels']):raise ValueError('bad prefix')
            for i,y in zip(prefix['ids'],prefix['labels']):
                if type(i) is not int or not 0<=i<len(c.x) or i in self.acquired or len(y)!=1 or not math.isfinite(y[0]):raise ValueError('bad prefix')
                self.acquired[i]=list(y)
        if len(self.acquired)>budget:raise ValueError('prefix over budget')
    def acquire(self,i):
        if type(i) is not int or not 0<=i<len(self.c.x) or i in self.acquired:raise ValueError('invalid/duplicate acquisition')
        if len(self.acquired)>=self.budget:raise RuntimeError('evaluation budget exhausted')
        target=self.c.source_ids[i]
        with Path(self.spec['path']).open(newline='') as f:
            reader=csv.DictReader(f,delimiter=self.spec['delimiter'])
            for line,row in enumerate(reader,2):
                if line==target:
                    # Invalid objective attempts are charged and journaled, never dropped.
                    raw=row[self.spec['primary_objective']];self.new_accesses+=1
                    if self.journal:self.journal({'row_id':i,'source_line':line,'raw_target':raw})
                    self.acquired[i]=None
                    y=float(raw)
                    if not math.isfinite(y) or y<=0:raise ValueError('nonpositive/nonfinite runtime/throughput')
                    self.acquired[i]=[y];return [y]
        raise ValueError('source row missing')

def symbols(c,values):
    return ''.join(ALPHABET[i] for i in encode_indices(c,values))

def parse_symbols(raw,c,count=10):
    lines=raw.splitlines()
    if len(lines)!=count or any(len(r)!=len(c.names) for r in lines):raise ValueError('expected ten full symbol strings')
    result=[]
    for row in lines:
        try:indices=[ALPHABET.index(v) for v in row]
        except ValueError:raise ValueError('unknown symbol')
        result.append(decode_indices(c,indices))
    return result

def messages(c,state):
    scores=losses(state.labels,c.directions)
    history=[{'x':symbols(c,c.x[state.ids[j]]),'loss':round(float(scores[j]),6)} for j in range(len(state.ids))]
    mapping=[{ALPHABET[i]:v for i,v in enumerate(domain)} for domain in c.domains]
    if any(len(d)>len(ALPHABET) for d in c.domains):raise ValueError('too many domain levels')
    body={'feature_order':list(c.names),'symbol_to_value':mapping,'observations':history}
    return [{'role':'system','content':'Optimize configurations using only observed losses. Lower loss is better.'},
      {'role':'user','content':'Propose ten new configurations with low predicted loss. Each row must have one symbol per feature using symbol_to_value. Avoid observed configurations. Output exactly ten symbol strings separated by newlines, no other text.\n'+__import__('json').dumps(body,separators=(',',':'))}]

def features(c,s,seed):
    start=time.perf_counter();scores=losses(s.labels,c.directions);running=np.minimum.accumulate(scores)
    available=[i for i in s.order if i not in set(s.ids)];xs=[c.x[i] for i in available]
    rng=random.Random(seed+10000);choices=[]
    for _ in range(20):
        sample=rng.choices(range(len(s.ids)),k=len(s.ids));ranked=sorted(sample,key=lambda j:(scores[j],j));k=max(1,int(math.sqrt(len(sample))))
        b=modal_centroid(c,[s.ids[j] for j in ranked[:k]]);r=modal_centroid(c,[s.ids[j] for j in ranked[k:]])
        choices.append(available[int(np.argmin(distances(xs,b)-distances(xs,r)))])
    result={'log_candidates':math.log(len(c.x)),'variables':len(c.names),'objectives':1,'symbolic_fraction':1.,'remaining':10,
      'progress':float(min(scores[:4])-min(scores)),'plateau':len(scores)-1-int(np.where(running==running[-1])[0][0]),
      'separation':float(distances([modal_centroid(c,s.best)],modal_centroid(c,s.rest))[0]),'uncertainty':1-max(Counter(choices).values())/20}
    return result,time.perf_counter()-start
