"""Feature-only search and acquired-label state. No dataset loading here."""
from dataclasses import dataclass, field
import copy, math, random, time
import numpy as np


def losses(y, directions):
    a=np.asarray(y,dtype=float)
    span=np.ptp(a,axis=0)
    z=np.divide(a-a.min(axis=0),span,out=np.zeros_like(a),where=span!=0)
    z=np.where(np.asarray(directions)=='+',1-z,z)
    z[:,span==0]=0
    return np.sqrt(np.mean(z*z,axis=1))

@dataclass(frozen=True)
class Candidates:
    names: tuple
    x: tuple
    objective_names: tuple
    directions: tuple
    source_ids: tuple
    def __post_init__(self):
        if len(self.x)<20 or len(self.x)!=len(set(self.x)): raise ValueError('need >=20 unique configurations')
        if not self.names or any(len(r)!=len(self.names) for r in self.x): raise ValueError('feature shape')
        if any(v not in (0,1) for r in self.x for v in r): raise ValueError('pilot requires binary symbolic schema')
    @property
    def domains(self): return [sorted(set(r[j] for r in self.x)) for j in range(len(self.names))]

@dataclass
class State:
    order: list
    ids: list=field(default_factory=list)
    labels: list=field(default_factory=list)
    best: list=field(default_factory=list)
    rest: list=field(default_factory=list)
    def clone(self): return copy.deepcopy(self)
    def observe(self,i,y,directions):
        if i in self.ids: raise ValueError('duplicate observation')
        self.ids.append(i); self.labels.append(list(y))
        if len(self.ids)==4:
            ranked=sorted(range(4),key=lambda j:(losses(self.labels,directions)[j],j))
            self.best=[self.ids[j] for j in ranked[:2]];self.rest=[self.ids[j] for j in ranked[2:]]
        elif len(self.ids)>4:
            self.best.append(i)
            scores=dict(zip(self.ids,losses(self.labels,directions)))
            if len(self.best)>int(math.sqrt(len(self.ids))):
                worst=max(self.best,key=lambda j:(scores[j],self.ids.index(j)))
                self.best.remove(worst);self.rest.append(worst)
    def record(self): return copy.deepcopy(self.__dict__)


def initial_state(c,seed):
    order=list(range(len(c.x)));random.Random(seed).shuffle(order)
    return State(order)

def centroid(c,ids):
    # Binary symbolic modes; ties select zero. No objective summaries.
    return (np.asarray([c.x[i] for i in ids]).mean(axis=0)>0.5).astype(int)

def distances(x,point): return np.sqrt(np.mean(np.asarray(x)!=np.asarray(point),axis=1))

def recommend(c,s,method='ezr_centroid_adapted'):
    available=[i for i in s.order if i not in set(s.ids)]
    if not available: raise ValueError('empty pool')
    if len(s.ids)<4 or method=='random': return available[0]
    b=centroid(c,s.best);r=centroid(c,s.rest)
    scores=distances([c.x[i] for i in available],b)-distances([c.x[i] for i in available],r)
    return available[int(np.argmin(scores))]

def project(c,s,proposal):
    used=set(s.ids);available=[i for i in s.order if i not in used]
    d=distances([c.x[i] for i in available],proposal);i=available[int(np.argmin(d))]
    seen=distances([c.x[j] for j in s.ids],proposal)
    return i,{'distance':float(min(d)),'projected':bool(min(d)>0),'duplicate':bool(min(seen)==0),'collision':bool(min(seen)<min(d)), 'nearest_seen':s.ids[int(np.argmin(seen))]}

def features(c,s,seed,remaining=10):
    started=time.perf_counter();l=losses(s.labels,c.directions)
    running=np.minimum.accumulate(l)
    plateau=len(l)-1-int(np.where(running==running[-1])[0][0])
    rng=random.Random(seed+10000);recommendations=[]
    for _ in range(20):
        sample=rng.choices(range(len(s.ids)),k=len(s.ids))
        ranked=sorted(sample,key=lambda j:(l[j],j));m=max(1,int(math.sqrt(len(sample))))
        b=centroid(c,[s.ids[j] for j in ranked[:m]]);r=centroid(c,[s.ids[j] for j in ranked[m:]])
        available=[i for i in s.order if i not in set(s.ids)]
        scores=distances([c.x[i] for i in available],b)-distances([c.x[i] for i in available],r)
        recommendations.append(available[int(np.argmin(scores))])
    from collections import Counter
    z={'log_candidates':math.log(len(c.x)),'variables':len(c.names),'objectives':len(c.directions),'symbolic_fraction':1.,'remaining':remaining,'progress':float(min(l[:4])-min(l)),'plateau':plateau,'separation':float(distances([centroid(c,s.best)],centroid(c,s.rest))[0]),'uncertainty':1-max(Counter(recommendations).values())/20}
    return z,time.perf_counter()-started
