"""Post-hoc observed-presentation gain envelopes; no provider or objective access."""
import math
from statistics import mean

CONDITIONS = ('assigned_ids', 'reverse_display', 'reassigned_ids')
BASELINES = ('classical_loss', 'uniform_expected_loss', 'first_display_loss', 'lowest_ids_loss')
EPSILON = 1e-12
MATERIAL = .02

def analyze(records, expected):
    unique = [r for r in records if r['condition'] != 'assigned_ids_repeat']
    indexed = {(r['dataset'], r['seed'], r['condition']): r for r in unique}
    if len(indexed) != len(unique) or set(indexed) != set(expected):
        raise ValueError('Missing, extra or duplicate case/presentation')
    cases = []
    for dataset, seed in sorted({(k[0], k[1]) for k in expected}):
        rows = [indexed[(dataset, seed, c)] for c in CONDITIONS]
        if len({r['system_group'] for r in rows}) != 1:
            raise ValueError('Inconsistent system group')
        if any(r['status'] != 'completed' or not all(math.isfinite(r[f]) for f in (*BASELINES, 'llm_loss')) for r in rows):
            raise ValueError('Incomplete or nonfinite outcome')
        for field in ('classical_loss', 'uniform_expected_loss'):
            if max(r[field] for r in rows) - min(r[field] for r in rows) > EPSILON:
                raise ValueError('Presentation-invariant baseline changed')
        case = {'dataset': dataset, 'seed': seed, 'system_group': rows[0]['system_group'],
                'llm_loss_range': max(r['llm_loss'] for r in rows) - min(r['llm_loss'] for r in rows)}
        for baseline in BASELINES:
            gains = [r[baseline] - r['llm_loss'] for r in rows]
            case[baseline] = {'gains': dict(zip(CONDITIONS, gains)), 'minimum': min(gains),
                'mean': mean(gains), 'maximum': max(gains),
                'positive_all': min(gains) > EPSILON, 'positive_any': max(gains) > EPSILON,
                'sign_flip': min(gains) < -EPSILON and max(gains) > EPSILON,
                'material_all': min(gains) > MATERIAL, 'material_any': max(gains) > MATERIAL}
        cases.append(case)
    groups = []
    for group in sorted({c['system_group'] for c in cases}):
        rows = [c for c in cases if c['system_group'] == group]
        groups.append({'system_group': group, 'cases': len(rows),
                       'mean_loss_range': mean(c['llm_loss_range'] for c in rows),
                       **{b: {f: mean(c[b][f] for c in rows) for f in ('minimum','mean','maximum')} for b in BASELINES}})
    return {'scope': 'Post-hoc development-only observed-presentation envelopes; not generalization or a deployable policy',
            'conditions': list(CONDITIONS), 'epsilon': EPSILON, 'material_margin': MATERIAL,
            'case_count': len(cases), 'presentation_count': len(unique), 'families': groups, 'cases': cases,
            'aggregate': {b: {**{f: mean(g[b][f] for g in groups) for f in ('minimum','mean','maximum')},
                **{f: sum(c[b][f] for c in cases) for f in ('positive_all','positive_any','sign_flip','material_all','material_any')}} for b in BASELINES},
            'leave_one_family_out': {g['system_group']: {b: mean(h[b]['mean'] for h in groups if h is not g)
                 for b in BASELINES} for g in groups} if len(groups)>1 else {}}
