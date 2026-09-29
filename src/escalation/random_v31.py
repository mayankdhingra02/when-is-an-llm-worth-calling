"""Fixed random controls; inputs contain candidate IDs and acquired state only."""
import hashlib
import random
from .consensus_v28 import continue_branch

MODES = ('random_full', 'random_shortlist')

def select(prefix, shortlist, dataset, seed, mode):
    if mode not in MODES or len(prefix.ids) != 10:
        raise ValueError('Fixed random mode and ten-label prefix required')
    if len(shortlist) != 20 or len(set(shortlist)) != 20 or set(shortlist) & set(prefix.ids):
        raise ValueError('Twenty unique unacquired shortlist rows required')
    if not set(shortlist) <= set(prefix.order):
        raise ValueError('Shortlist outside candidate domain')
    available = sorted(set(prefix.order)-set(prefix.ids)) if mode == 'random_full' else sorted(shortlist)
    if len(available) < 10: raise ValueError('Insufficient candidates')
    material = f'v31|{dataset}|{seed}|{mode}'
    entropy = hashlib.sha256(material.encode('utf-8')).hexdigest()
    selected = random.Random(int(entropy, 16)).sample(available, 10)
    return {'selected': selected, 'seed_material': material, 'seed_sha256': entropy, 'pool_size': len(available)}

def branch(prefix, shortlist, dataset, seed, mode, directions, acquire, checkpoint=lambda state: None):
    selection = select(prefix, shortlist, dataset, seed, mode)
    return continue_branch(prefix, selection['selected'], directions, acquire, checkpoint), selection
