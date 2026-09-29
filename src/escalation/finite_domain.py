"""Unexecuted-study finite-domain nominal adaptation, separate from v3/v4.

All numeric-looking levels are treated as categorical values. This deliberately
ignores ordinal distances. No model adapter or measured LLM output is provided.
"""
from dataclasses import dataclass
from collections import Counter
import math,random
import numpy as np
from .core import State,distances

@dataclass(frozen=True)
class FiniteCandidates:
    names: tuple
    x: tuple
    objective_names: tuple
    directions: tuple
    source_ids: tuple
    def __post_init__(self):
        if not 1<=len(self.names)<=64:raise ValueError('need 1-64 explicit features')
        if not 20<=len(self.x)<=200000 or len(set(self.x))!=len(self.x):raise ValueError('unique candidate pool size')
        if len(self.source_ids)!=len(self.x):raise ValueError('source IDs mismatch')
        if any(len(r)!=len(self.names) or any(not math.isfinite(v) for v in r) for r in self.x):raise ValueError('invalid feature vector')
        if len(self.objective_names)!=1 or len(self.directions)!=1 or self.directions[0] not in ('+','-'):raise ValueError('one explicit objective required')
    @property
    def domains(self):return [sorted({r[j] for r in self.x}) for j in range(len(self.names))]


def modal_centroid(c,ids):
    if not ids:raise ValueError('nonempty acquired group required')
    return tuple(min(Counter(c.x[i][j] for i in ids).items(),key=lambda p:(-p[1],p[0]))[0] for j in range(len(c.names)))


def recommend(c,state,method='centroid_nominal'):
    available=[i for i in state.order if i not in set(state.ids)]
    if not available:raise ValueError('no unevaluated candidates')
    if len(state.ids)<4 or method=='random':return available[0]
    if method!='centroid_nominal':raise ValueError('unknown method')
    best=modal_centroid(c,state.best);rest=modal_centroid(c,state.rest)
    score=distances([c.x[i] for i in available],best)-distances([c.x[i] for i in available],rest)
    return available[int(np.argmin(score))]


def encode_indices(c,proposal):
    if len(proposal)!=len(c.names):raise ValueError('proposal shape')
    return [domain.index(value) for domain,value in zip(c.domains,proposal)]


def decode_indices(c,indices):
    if len(indices)!=len(c.names):raise ValueError('proposal shape')
    result=[]
    for domain,index in zip(c.domains,indices):
        if type(index) is not int or not 0<=index<len(domain):raise ValueError('invalid domain index')
        result.append(domain[index])
    return result


def uniform_proposals(c,seed,count=10):
    if count<=0:raise ValueError('positive count required')
    rng=random.Random(seed)
    return [[rng.choice(domain) for domain in c.domains] for _ in range(count)]
