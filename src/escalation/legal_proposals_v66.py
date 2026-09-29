"""Finite-domain constrained proposal state; receives no hidden objective table.

Grammar narrows each individual completion to one remaining configuration. The
server must still enforce it; independent acceptance checks fail closed. This is
an interface, not measured model output or an optimization policy.
"""
import json
import math


def canonical(row):
    if not isinstance(row, (list, tuple)) or not row:
        raise ValueError('Configuration must be a nonempty vector')
    for value in row:
        if type(value) not in (str, bool, int, float) or (type(value) is float and not math.isfinite(value)):
            raise ValueError('Only finite JSON scalar features are supported')
    normalized = [int(v) if type(v) is float and v.is_integer() else v for v in row]
    return json.dumps(normalized, ensure_ascii=True, allow_nan=False, separators=(',', ':'))


class LegalProposals:
    def __init__(self, configurations, acquired_ids, count=10):
        self._vectors = tuple(canonical(row) for row in configurations)
        if len(set(self._vectors)) != len(self._vectors):
            raise ValueError('Duplicate configurations must be resolved before admission')
        if type(count) is not int or count < 1: raise ValueError('Invalid remaining budget')
        ids = list(acquired_ids)
        if len(ids) != len(set(ids)) or any(type(i) is not int or i < 0 or i >= len(self._vectors) for i in ids):
            raise ValueError('Invalid acquired IDs')
        if len(self._vectors) - len(ids) < count: raise ValueError('Insufficient unobserved candidates')
        self._excluded = set(ids)
        self.count = count
        self.selected = []
        self.requests = 0
        self.pending = None
        self.failure = None

    def eligible_ids(self):
        return tuple(i for i in range(len(self._vectors)) if i not in self._excluded)

    def begin_request(self):
        if self.failure is not None: raise RuntimeError('Session failed; no retries')
        if self.pending is not None: raise RuntimeError('Request already pending')
        if self.requests >= self.count: raise RuntimeError('Request cap reached')
        eligible = self.eligible_ids()
        # GBNF alternation of escaped literal complete JSON vectors, no recursion.
        grammar = 'root ::= ' + ' | '.join(json.dumps(self._vectors[i], ensure_ascii=True) for i in eligible)
        self.requests += 1  # charge before any transport
        self.pending = eligible
        return {'request_number': self.requests, 'grammar': grammar,
                'eligible_ids': list(eligible),
                'eligible_configurations': [json.loads(self._vectors[i]) for i in eligible]}

    def finish_request(self, raw=None, truncated=False, transport_error=None):
        if self.pending is None: raise RuntimeError('No charged pending request')
        allowed = self.pending
        self.pending = None
        reason = None
        selected = None
        if transport_error is not None: reason = 'transport_error'
        elif truncated: reason = 'truncated'
        else:
            try:
                # Exact canonical bytes avoid Python bool/int equality and decoder coercion.
                if not isinstance(raw, str) or raw not in {self._vectors[i] for i in allowed}:
                    raise ValueError('Completion did not obey finite grammar')
                selected = self._vectors.index(raw)
            except (ValueError, TypeError): reason = 'invalid_or_excluded_configuration'
        if reason is not None:
            self.failure = reason
            return {'valid': False, 'reason': reason, 'selected_id': None}
        self._excluded.add(selected)
        self.selected.append(selected)
        return {'valid': True, 'reason': None, 'selected_id': selected}

    @property
    def complete(self):
        return len(self.selected) == self.count and self.pending is None and self.failure is None
