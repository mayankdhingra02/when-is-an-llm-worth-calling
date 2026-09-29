"""V173 interface: JSON-schema form of the V141-V172 grammar, parser, generic projection with collisions, and arm-B prompts.

Feature-only and acquired-label-only: no oracle, source table or hidden objective is read here.
"""
import json
from proposal_v127 import ALPHABET, encode
from spark_v144 import CAT as SPARK_CAT, distance as spark_distance
from hadoop_v148 import distance as hadoop_distance

def schema(ds, count):
    if not ds or any(not d or len(d) > len(ALPHABET) for d in ds): raise ValueError('Invalid feature domains')
    pattern = '^'+''.join('['+ALPHABET[:len(d)]+']' for d in ds)+'$'
    return {'type': 'object', 'properties': {'proposals': {'type': 'array', 'items': {'type': 'string', 'pattern': pattern}, 'minItems': count, 'maxItems': count}},
            'required': ['proposals'], 'additionalProperties': False}

def parse(content, ds, count):
    """Accept {"proposals": [...]} or a bare array of exactly `count` valid strings; map symbols to domain values."""
    try: obj = json.loads(content)
    except (ValueError, TypeError) as e: raise ValueError('Malformed JSON') from e
    rows = obj['proposals'] if isinstance(obj, dict) and set(obj) == {'proposals'} else obj
    if not isinstance(rows, list) or len(rows) != count: raise ValueError(f'Expected exactly {count} proposals')
    for r in rows:
        if not isinstance(r, str) or len(r) != len(ds) or any(ch not in ALPHABET[:len(d)] for ch, d in zip(r, ds)): raise ValueError('Bad proposal string')
    return [[d[ALPHABET.index(ch)] for ch, d in zip(r, ds)] for r in rows]

def distance_fn(origin, c):
    if origin == 'v141': return lambda p, i: sum(a != b for a, b in zip(p, c.x[i]))
    if origin == 'v144': return lambda p, i: spark_distance([v if j in SPARK_CAT else v/9 for j, v in enumerate(p)], c['x'][i])
    if origin == 'v148': return lambda p, i: hadoop_distance([p[0]/9, p[1]], c['x'][i])
    raise ValueError('Unknown origin')

def project_any(origin, c, order, measured, proposals):
    """Nearest unmeasured row per proposal (ties by candidate order, as in every origin projection); flags collisions."""
    d = distance_fn(origin, c); taken = set(measured); rows, diag = [], []
    for p in proposals:
        nearest = min(order, key=lambda i: d(p, i)); row = min((i for i in order if i not in taken), key=lambda i: d(p, i))
        diag.append({'proposal': list(p), 'row_id': row, 'distance': d(p, row), 'nearest_any_row': nearest, 'collision': nearest in taken})
        rows.append(row); taken.add(row)
    return rows, diag

B_SYSTEM = ('You are an optimizer for a software-configuration task with a fixed evaluation budget. Each round you propose exactly two new configurations; '
            'each is mapped to the nearest valid unmeasured configuration and then measured. Use the task description, the hard constraints and the measured trajectory. '
            'Respond only with a JSON object {"proposals": ["...", "..."]}.')

def example(origin, c, ds, i, y):
    perf = None if y is None else y
    if origin == 'v141': return {'settings': encode(c.x[i], ds), 'performance': None if perf is None else f'{perf:.6f}'}
    if origin == 'v144': return {'settings': [round(v, 5) for v in c['x'][i]], 'performance': perf}
    return {'settings': c['x'][i], 'performance': perf}

def trajectory(origin, c, ds, ids, labels, direction):
    rows = [(i, y[0]) for i, y in zip(ids, labels)]
    missing = [r for r in rows if r[1] is None]; present = [r for r in rows if r[1] is not None]
    present.sort(key=lambda r: -r[1] if direction == 'minimize' else r[1])  # worst first
    return [dict(example(origin, c, ds, i, None), note='missing source measurement (charged)') for i, _ in missing]+[example(origin, c, ds, i, y) for i, y in present]

def b_messages(original, origin, c, ds, ids, labels, direction, round_no, rounds, collisions, retry_reason):
    width = len(ds); remaining = 20-len(ids)-2
    block = {'round': f'{round_no} of {rounds}', 'remaining_evaluations_after_this_round': remaining,
             'hard_constraints': {'setting_length': width, 'allowed_symbols_by_position': [ALPHABET[:len(d)] for d in ds]},
             'objective': f'{direction} the performance value',
             'trajectory_worst_to_best': trajectory(origin, c, ds, ids, labels, direction),
             'diversification_collisions': collisions or 'none',
             'reminder': 'Propose exactly two distinct setting strings that differ from every measured setting, using only the allowed symbols at each position. No text outside the JSON object.',
             'output_format': {'proposals': ['<'+str(width)+' symbols>', '<'+str(width)+' symbols>']}}
    if retry_reason: block['retry'] = f'Your previous response in this round was not valid ({retry_reason}). Follow the output rules exactly.'
    return [{'role': 'system', 'content': B_SYSTEM},
            {'role': 'user', 'content': 'TASK DESCRIPTION (original instructions; the proposal count is overridden to exactly two per round).\n\nORIGINAL SYSTEM INSTRUCTIONS:\n'+original[0]['content']+'\n\nORIGINAL TASK DATA:\n'+original[1]['content']},
            {'role': 'user', 'content': json.dumps(block, separators=(',', ':'))}]
