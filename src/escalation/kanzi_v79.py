"""V79 classical comparator; exposed V78-informed preset strategy, no LLM."""
from .kanzi_v75 import grid,choose as classical_choose
METHODS=['rf_lcb','preset']
# Owner level 7 transform/entropy, descending candidate block sizes.
# Explicitly V78-informed: not an a-priori universal default claim.
PRESET_IDS=tuple(sorted((i for i,c in enumerate(grid()) if c['transform']=='LZP+TEXT+BWT+LZP' and c['entropy']=='CM'), key=lambda i:-grid()[i]['block_bytes']))

def choose(x,observations,method,seed,rng=None):
    if method=='preset':
        observed={o['config_id'] for o in observations}
        for cid in PRESET_IDS:
            if cid not in observed:return cid
        return classical_choose(x,observations,'rf_lcb',seed)
    return classical_choose(x,observations,method,seed,rng)

def guard(cid,observations,purpose,count):
    if type(cid) is not int or not 0<=cid<448:raise ValueError('Invalid configuration')
    if len(observations)>=20 or count>=450:raise ValueError('Budget exhausted')
    if purpose not in ['search','confirmation']:raise ValueError('Invalid purpose')
    if purpose=='search' and cid in {o['config_id'] for o in observations}:raise ValueError('Duplicate search')
