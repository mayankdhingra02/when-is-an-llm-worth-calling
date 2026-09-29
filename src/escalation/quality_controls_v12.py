"""Feature/acquired-label-only constrained three-nearest-neighbor acquisition."""
import numpy as np


def choose(c,order,ids,joint_labels,size_cap,method):
    available=[i for i in order if i not in set(ids)]
    if not available:raise ValueError('no available candidate')
    if method=='random':return available[0],{'predicted_runtime':None,'predicted_size':None}
    if method!='joint_3nn' or len(ids)!=len(joint_labels) or len(ids)<3:raise ValueError('invalid acquired-state method')
    labels=np.asarray(joint_labels,dtype=float)
    if labels.shape!=(len(ids),2) or not np.isfinite(labels).all() or (labels<=0).any():raise ValueError('positive acquired runtime/size required')
    observed=np.asarray([c.x[i] for i in ids]);xs=np.asarray([c.x[i] for i in available])
    distances=(xs[:,None,:]!=observed[None,:,:]).mean(axis=2)
    near=np.argsort(distances,axis=1,kind='stable')[:,:3]
    predicted=labels[near].mean(axis=1)
    feasible=np.flatnonzero(predicted[:,1]<=size_cap)
    if len(feasible):position=min(feasible,key=lambda j:(predicted[j,0],int(j)))
    else:position=min(range(len(available)),key=lambda j:(predicted[j,1],predicted[j,0],j))
    return available[position],{'predicted_runtime':float(predicted[position,0]),'predicted_size':float(predicted[position,1]),'predicted_feasible':bool(predicted[position,1]<=size_cap)}
