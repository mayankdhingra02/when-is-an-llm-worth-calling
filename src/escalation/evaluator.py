"""RETROSPECTIVE ONLY: full-table labels and normalization live here."""
import numpy as np
from .core import losses

def evaluate(all_labels,directions,ids):
    scores=losses(all_labels,directions)
    loss=float(min(scores[ids]));lo=float(min(scores));med=float(np.median(scores))
    return {'loss':loss,'quality':1-loss,'delta_percent':None if med==lo else 100*(1-(loss-lo)/(med-lo))}
