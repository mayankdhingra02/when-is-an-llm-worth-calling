"""Feature-only bounded transfer domain and direction-aware controls.

No target-file access is allowed in the ranking/prompt functions. The indexed
oracle is a separate acquisition boundary; unrequested objective cells remain
unparsed text. This is a nominal finite-domain adaptation, not SNAP2.
"""
import csv
import hashlib
import json
import math
import random
from decimal import Decimal
from pathlib import Path
import numpy as np
from .core import losses
from .finite_domain import FiniteCandidates, recommend
from .finite_v6 import ALPHABET
from .io import digest

SEEDS = (11, 23, 37, 53, 71)
MODES = ('full_classical', 'static_rank', 'batch_3nn', 'sequential_3nn',
         'full_sequential_3nn', 'random_shortlist', 'random_full')


def restrict(c, fixed, maximum=1024):
    """Fixed workload and hash-ranked subsample use features only, shared seeds."""
    positions = {c.names.index(k): v for k, v in fixed.items()}
    ids = [i for i, x in enumerate(c.x) if all(x[j] == v for j, v in positions.items())]
    eligible = len(ids)
    if len(ids) > maximum:
        ids = sorted(ids, key=lambda i: (digest({'salt': 'v41', 'x': c.x[i]}), i))[:maximum]
    ids.sort()
    if len(ids) < 30: raise ValueError('Fewer than thirty admissible candidates')
    result = FiniteCandidates(c.names, tuple(c.x[i] for i in ids), c.objective_names,
                              c.directions, tuple(c.source_ids[i] for i in ids))
    return result, {'eligible_before_subsample': eligible, 'selected': len(ids),
                    'source_lines': list(result.source_ids), 'feature_digest': digest(result.x)}


class IndexedOracle:
    """O(1) line lookup, same charged lazy parsing as V6; no optimizer reference."""
    def __init__(self, spec, candidates, prefix=None, journal=None):
        self.spec, self.c, self.journal = spec, candidates, journal
        self.acquired = {}
        self.new_accesses = 0
        # Existing registered CSVs have no quoted multiline records. Fail closed.
        self.lines = Path(spec['path']).read_text().splitlines()
        self.header = next(csv.reader([self.lines[0]], delimiter=spec['delimiter']))
        if len(self.lines) < max(candidates.source_ids): raise ValueError('Source line mismatch')
        if prefix:
            if len(prefix['ids']) != len(prefix['labels']): raise ValueError('Invalid prefix')
            for i, y in zip(prefix['ids'], prefix['labels']):
                if type(i) is not int or not 0 <= i < len(candidates.x) or i in self.acquired or len(y) != 1 or not math.isfinite(y[0]) or y[0] <= 0:
                    raise ValueError('Invalid acquired prefix')
                self.acquired[i] = list(y)
        if len(self.acquired) > 20: raise ValueError('Prefix over budget')

    def acquire(self, i):
        if type(i) is not int or not 0 <= i < len(self.c.x) or i in self.acquired: raise ValueError('Duplicate/invalid acquisition')
        if len(self.acquired) >= 20: raise RuntimeError('Twenty-evaluation budget exhausted')
        line = self.c.source_ids[i]
        row = dict(zip(self.header, next(csv.reader([self.lines[line-1]], delimiter=self.spec['delimiter']))))
        if tuple(float(row[k]) for k in self.c.names) != self.c.x[i]: raise ValueError('Source feature mismatch')
        self.new_accesses += 1
        self.acquired[i] = None
        raw = row[self.spec['primary_objective']]
        if self.journal: self.journal({'row_id': i, 'source_line': line, 'raw_target': raw})
        y = float(raw)
        if not math.isfinite(y) or y <= 0: raise ValueError('Invalid target; attempt charged')
        self.acquired[i] = [y]
        return [y]


def rank(c, state, pool):
    allowed, seen = set(pool), set(state.ids)
    available = [i for i in state.order if i in allowed and i not in seen]
    if len(state.ids) < 3: raise ValueError('Three acquired labels required')
    xs = np.asarray([c.x[i] for i in state.ids])
    scores = []
    for row in available:
        distances = (xs != np.asarray(c.x[row])).sum(axis=1)
        near = np.argsort(distances, kind='stable')[:3]
        prediction = sum(Decimal(str(state.labels[int(j)][0])) for j in near) / 3
        scores.append((prediction if c.directions[0] == '-' else -prediction, row))
    return [row for _, row in sorted(scores, key=lambda x: x[0])]


def branch(c, prefix, pool, seed, mode, acquire):
    if mode not in MODES or len(prefix.ids) != 10 or set(pool) & set(prefix.ids): raise ValueError('Bad paired branch')
    state = prefix.clone()
    available = [i for i in state.order if i not in set(state.ids)]
    if mode == 'static_rank': batch = pool[:10]
    elif mode == 'batch_3nn': batch = rank(c, state, pool)[:10]
    elif mode == 'random_shortlist': batch = random.Random(seed+40000).sample(pool, 10)
    elif mode == 'random_full': batch = random.Random(seed+41000).sample(available, 10)
    else: batch = None
    for step in range(10):
        if batch is not None: row = batch[step]
        elif mode == 'full_classical': row = recommend(c, state)
        else: row = rank(c, state, available if mode == 'full_sequential_3nn' else pool)[0]
        state.observe(row, acquire(row), c.directions)
    return state


def messages(c, state, pool):
    """Same V8 representation, cached domains to avoid repeated full-table scans."""
    if len(state.ids) != 10: raise ValueError('Predecision prefix required')
    domains = c.domains
    if max(map(len, domains)) > len(ALPHABET): raise ValueError('Too many domain levels')
    maps = [{value: ALPHABET[j] for j, value in enumerate(domain)} for domain in domains]
    def symbols(i): return ''.join(m[v] for m, v in zip(maps, c.x[i]))
    body = {'feature_order': c.names, 'symbol_to_value': domains,
            'observations': [{'x': symbols(i), 'loss': float(y)} for i, y in zip(state.ids, losses(state.labels, c.directions))],
            'candidates': [{'id': k, 'x': symbols(i)} for k, i in pool['mapping'].items()]}
    return [{'role': 'system', 'content': 'You optimize software configurations. Infer promising settings from acquired observations; smaller loss is better. Select ten distinct candidate IDs expected to achieve low loss. Output only ten IDs, one per line. Each ID must be selected from the supplied candidate list. No explanations.'},
            {'role': 'user', 'content': 'Observed losses are normalized using only acquired labels. Feature strings encode each setting by its index in symbol_to_value using 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz. Candidate order and IDs are randomly assigned. Select ten promising distinct candidate IDs.\n'+json.dumps(body, separators=(',', ':'))}]


def best(state, direction):
    return (min if direction == '-' else max)(y[0] for y in state.labels)


def relative_gain(reference, treatment, direction):
    if reference <= 0 or treatment <= 0: raise ValueError('Positive targets required')
    return (reference-treatment)/reference if direction == '-' else (treatment-reference)/reference


def current_config():
    """Carry only the already granted V38 allowance; cannot enable new inference."""
    from .config import load_config
    from .io import read
    from .size_prompt_v38 import authorization_config
    return authorization_config(load_config('configs/followup_v3.yaml'), read('configs/authorization_v22.json'),
        read('configs/authorization_v38.json'), hashlib.sha256(Path('reports/protocol_v38_size_prompt.freeze.json').read_bytes()).hexdigest())
