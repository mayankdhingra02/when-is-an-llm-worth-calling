"""Posthoc diagnostic design; never imported by an optimization policy."""
import random

def jobs():
    bases = [('superlu_11_prefix_00', [2, .1, 4]),
             ('superlu_23_prefix_00', [3, .01, 1])]
    rows = [dict(key=f'b{i}_p{panel}_r{repeat}', source=source,
                 configuration=base + [panel], repeat=repeat)
            for i, (source, base) in enumerate(bases)
            for panel in (16, 20, 21, 32) for repeat in range(5)]
    random.Random(96000).shuffle(rows)
    return rows

def classify(exit_code, guard, record):
    if guard:
        return guard
    if exit_code != 0:
        return 'worker_failure'
    if record is None:
        return 'missing_output'
    measurements = record.get('measurements', [])
    if len(measurements) != 3 or not all(m['certificate']['valid'] for m in measurements):
        return 'invalid_certificate'
    return 'valid'
