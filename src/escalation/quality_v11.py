"""Retrospective only: output-size-constrained runtime summaries."""
import math


def fastest(ids, runtime, size=None, cap=None):
    if not ids:raise ValueError('nonempty acquired/candidate set required')
    if size is not None and cap is None:raise ValueError('explicit size cap required')
    feasible=[]
    for i in ids:
        if type(i) is not int or not 0<=i<len(runtime):raise ValueError('invalid row id')
        if not math.isfinite(runtime[i]) or runtime[i]<=0:raise ValueError('positive finite runtime required')
        if size is not None:
            if not math.isfinite(size[i]) or size[i]<=0:raise ValueError('positive finite size required')
            if size[i]>cap:continue
        feasible.append(i)
    if not feasible:raise ValueError('no feasible incumbent')
    chosen=min(feasible,key=lambda i:runtime[i])
    return chosen,len(feasible)


def constrained_case(prefix, candidates, arms, runtime, size):
    anchor,_=fastest(prefix,runtime);cap=size[anchor]
    prefix_set=set(prefix)
    if prefix_set&set(candidates):raise ValueError('shortlist overlaps acquired prefix')
    result={'anchor':anchor,'size_cap':cap,'anchor_runtime':runtime[anchor],'arms':{},'bounds':{}}
    for name,ids in arms.items():
        if not prefix_set<=set(ids):raise ValueError('arm missing shared prefix')
        i,n=fastest(ids,runtime,size,cap)
        result['arms'][name]={'row_id':i,'runtime':runtime[i],'size':size[i],'feasible_rows':n}
    for name,ids in [('shortlist',prefix+candidates),('full_table',list(range(len(runtime))))]:
        i,n=fastest(ids,runtime,size,cap)
        result['bounds'][name]={'row_id':i,'runtime':runtime[i],'size':size[i],'feasible_rows':n}
    return result
