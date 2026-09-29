"""V65 native configuration proposals; no hidden outcomes accepted as inputs."""
import json
import math
from .sat_v64 import grid


def messages(prefix):
    configurations = grid()
    if len(prefix) != 10 or len({o['config_id'] for o in prefix}) != 10:
        raise ValueError('Expected ten unique acquired outcomes')
    observed = [{'configuration': configurations[o['config_id']], 'penalized_ms': o['value_ms']} for o in prefix]
    if any(not math.isfinite(o['penalized_ms']) or o['penalized_ms'] <= 0 for o in observed):
        raise ValueError('Invalid acquired score')
    return [
        {'role': 'system', 'content': 'You select software configurations using only observed measurements. Return exactly the requested JSON, without explanations or code fences.'},
        {'role': 'user', 'content': 'Optimize MiniSat core on one fixed generated planted 3-CNF task with 512 variables and 2201 clauses. Minimize median penalized whole-process milliseconds over three repetitions. A CPU-limit or other resource noncompletion scores 40000 ms per repetition; CPU limit 18 seconds, wall limit 20 seconds. All valid solutions are independently checked. The optimizer has evaluated the following ten configurations. You may choose ten more.\n\nEach configuration is an array [var-decay, cla-decay, rfirst, rinc, phase-saving]. Allowed values respectively: [0.8,0.95], [0.9,0.999], [25,100,400], [1.2,2], [0,2]. Luby restarts are enabled, random decision frequency is zero, and all other options are fixed.\n\nObserved configurations in acquisition order:\n' + json.dumps(observed, separators=(',', ':')) + '\n\nReturn one JSON array containing exactly ten distinct allowed configuration arrays that do not duplicate any observed configuration. Choose the set to give the best chance of finding a low score. No further measurements will be supplied during this request.'}
    ]


def parse_response(content, prefix, truncated=False):
    if truncated:
        return {'valid': False, 'selected_ids': [], 'reason': 'truncated'}
    try:
        result = json.loads(content)
    except (ValueError, TypeError):
        return {'valid': False, 'selected_ids': [], 'reason': 'invalid_json'}
    allowed = [list(row) for row in grid()]
    if not isinstance(result, list) or len(result) != 10:
        return {'valid': False, 'selected_ids': [], 'reason': 'count_or_shape'}
    ids = []
    for row in result:
        if (not isinstance(row, list) or len(row) != 5 or
            any(type(x) not in (int, float) or not math.isfinite(x) for x in row) or row not in allowed):
            return {'valid': False, 'selected_ids': [], 'reason': 'outside_domain'}
        ids.append(allowed.index(row))
    if len(set(ids)) != 10:
        return {'valid': False, 'selected_ids': [], 'reason': 'duplicate_proposal'}
    if set(ids) & {o['config_id'] for o in prefix}:
        return {'valid': False, 'selected_ids': [], 'reason': 'observed_proposal'}
    return {'valid': True, 'selected_ids': ids, 'reason': None}
