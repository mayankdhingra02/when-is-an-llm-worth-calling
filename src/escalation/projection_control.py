"""Model-free control: independent uniform coordinates + the v3 projection rule.

Only Candidates and State enter proposal generation; no oracle, hidden labels,
model responses or objective statistics are accepted. This is not an LLM adapter.
"""
import hashlib
import random
from .core import project

VERSION = 'uniform_domains_projection_v1'

def proposal_seed(data_hash, seed):
    key = f'{VERSION}:{data_hash}:{seed}'.encode()
    return int.from_bytes(hashlib.sha256(key).digest()[:8], 'big')

class UniformProjection:
    def __init__(self, candidates, seed):
        self.candidates = candidates
        self.rng = random.Random(seed)
        self.domains = candidates.domains

    def propose_batch(self, count=5):
        if count <= 0:
            raise ValueError('positive batch size required')
        return [[self.rng.choice(domain) for domain in self.domains]
                for _ in range(count)]

    def select(self, state, proposal):
        return project(self.candidates, state, proposal)


def continue_projection(c, state, oracle, seed, checkpoint=None, resource=None):
    """Acquire 10 labels from a saved 10-label prefix, in two batches of five."""
    if len(state.ids) != 10 or list(oracle.acquired) != state.ids:
        raise ValueError('matching ten-label prefix required')
    control = UniformProjection(c, seed)
    events = []
    for batch in range(1, 3):
        proposals = control.propose_batch(5)
        for proposal in proposals:
            if resource is not None:
                resource.check()
            index, event = control.select(state, proposal)
            value = oracle.acquire(index)
            state.observe(index, value, c.directions)
            events.append({**event, 'proposal': proposal, 'row_id': index,
                           'batch': batch, 'fallback': False,
                           'proposal_source': VERSION})
            if checkpoint is not None:
                checkpoint(state, events)
    return events
