"""Fixed acquired-label 3NN ranking; no source-table or model access."""
from decimal import Decimal, localcontext


def rank(candidates, state, pool):
    if len(pool) != 20 or len(set(pool)) != 20 or not set(pool) <= set(state.order):
        raise ValueError('Need twenty distinct known shortlist candidates')
    if len(state.ids) < 3 or len(state.ids) != len(state.labels) or len(set(state.ids)) != len(state.ids):
        raise ValueError('Invalid acquired state')
    with localcontext() as context:
        context.prec = 40
        labels = [Decimal(str(y[0])) for y in state.labels if len(y) == 1]
        if len(labels) != len(state.ids) or any(not y.is_finite() or y <= 0 for y in labels):
            raise ValueError('Positive scalar acquired labels required')
        scores = []
        for row in state.order:
            if row not in pool or row in state.ids: continue
            distances = [sum(a != b for a, b in zip(candidates.x[row], candidates.x[i])) for i in state.ids]
            near = sorted(range(len(state.ids)), key=lambda j: (distances[j], j))[:3]
            prediction = sum((labels[j] for j in near), Decimal(0))/3
            scores.append((prediction, {'row_id': row, 'neighbor_ids': [state.ids[j] for j in near],
                                       'predicted_target': str(prediction)}))
        return [details for score, details in sorted(scores, key=lambda pair: pair[0])]


def continue_branch(candidates, prefix, pool, mode, acquire, checkpoint=lambda state, trace: None):
    if mode not in ('batch_3nn', 'sequential_3nn') or len(prefix.ids) != 10 or set(pool) & set(prefix.ids):
        raise ValueError('Invalid mode, prefix or previously acquired shortlist row')
    state = prefix.clone(); batch = rank(candidates, prefix, pool)[:10]; trace = []
    if len(batch) != 10: raise ValueError('Incomplete candidate batch')
    for step in range(10):
        proposal = batch[step] if mode == 'batch_3nn' else rank(candidates, state, pool)[0]
        trace.append({'step': step, **proposal})
        state.observe(proposal['row_id'], acquire(proposal['row_id']), candidates.directions)
        checkpoint(state, trace)
    return state, trace
