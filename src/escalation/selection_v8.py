"""Acquired-label-only shortlist and exact candidate selection; no oracle access."""
import json, random
from .core import distances, losses
from .finite_domain import modal_centroid
from .finite_v6 import ALPHABET, symbols

VERSION = 'candidate_ids_v8'

def shortlist(c, state, seed):
    if len(state.ids) != 10 or len(set(state.ids)) != 10:
        raise ValueError('exact ten-label checkpoint required')
    available = [i for i in state.order if i not in set(state.ids)]
    if len(available) < 20:
        raise ValueError('need twenty unobserved candidates')
    score = distances([c.x[i] for i in available], modal_centroid(c, state.best)) - distances([c.x[i] for i in available], modal_centroid(c, state.rest))
    ranked = [i for _, i in sorted(zip(score, available), key=lambda pair: pair[0])][:20]
    presented = list(ranked)
    random.Random(seed + 70000).shuffle(presented)
    return {'ranked': ranked, 'mapping': dict(zip(ALPHABET[:20], presented))}

def messages(c, state, pool):
    observed = losses(state.labels, c.directions)
    body = {'feature_order': c.names, 'symbol_to_value': c.domains,
            'observations': [{'x': symbols(c, c.x[i]), 'loss': float(y)} for i, y in zip(state.ids, observed)],
            'candidates': [{'id': k, 'x': symbols(c, c.x[i])} for k, i in pool['mapping'].items()]}
    return [{'role': 'system', 'content': 'You optimize software configurations. Infer promising settings from acquired observations; smaller loss is better. Select ten distinct candidate IDs expected to achieve low loss. Output only ten IDs, one per line. Each ID must be selected from the supplied candidate list. No explanations.'},
            {'role': 'user', 'content': 'Observed losses are normalized using only acquired labels. Feature strings encode each setting by its index in symbol_to_value using 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz. Candidate order and IDs are randomly assigned. Select ten promising distinct candidate IDs.\n' + json.dumps(body, separators=(',', ':'))}]

def parse_ids(raw, pool):
    ids = raw.strip().splitlines()
    if len(ids) != 10 or len(set(ids)) != 10 or any(k not in pool['mapping'] for k in ids):
        raise ValueError('require ten distinct exact candidate IDs')
    return [pool['mapping'][k] for k in ids]

def control_rows(pool, seed, arm):
    if arm == 'static_rank':
        return pool['ranked'][:10]
    if arm == 'uniform_selection':
        return random.Random(seed + 40000).sample(list(pool['mapping'].values()), 10)
    raise ValueError('unknown control')
