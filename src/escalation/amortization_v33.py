"""Explicit reuse-scenario arithmetic; never a predictor or provider adapter."""
import math
from statistics import mean

WORK_SECONDS = (0., 1., 10., 100., 1000., 10000., 100000.)

def validate(gain, request_seconds):
    if not math.isfinite(gain) or not math.isfinite(request_seconds) or request_seconds < 0:
        raise ValueError('Finite gain and observed nonnegative request time required')

def recovery_threshold(gain, request_seconds):
    """Baseline future work seconds at equality S*g=C, None if no gain."""
    validate(gain, request_seconds)
    return request_seconds/gain if gain > 0 else None

def net_saved(gain, request_seconds, baseline_work_seconds):
    validate(gain, request_seconds)
    if not math.isfinite(baseline_work_seconds) or baseline_work_seconds < 0:
        raise ValueError('Nonnegative finite baseline work required')
    return baseline_work_seconds*gain-request_seconds

def presentation_scenarios(rows):
    if len(rows)!=3 or {r['condition'] for r in rows}!={'assigned_ids','reverse_display','reassigned_ids'}:
        raise ValueError('Exactly three unique observed presentations required')
    assigned=next(r for r in rows if r['condition']=='assigned_ids')
    thresholds=[recovery_threshold(r['gain'],r['request_seconds']) for r in rows]
    g=mean(r['gain'] for r in rows);c=mean(r['request_seconds'] for r in rows)
    return {'assigned_gain':assigned['gain'],'assigned_request_seconds':assigned['request_seconds'],
        'assigned_recovery_seconds':recovery_threshold(assigned['gain'],assigned['request_seconds']),
        'uniform_presentation_mean_gain':g,'uniform_presentation_mean_request_seconds':c,
        'uniform_presentation_recovery_seconds':recovery_threshold(g,c),
        'all_three_positive':all(r['gain']>0 for r in rows),
        'all_three_recovery_seconds':max(thresholds) if all(t is not None for t in thresholds) else None,
        'any_gain':any(r['gain']>0 for r in rows),'any_harm':any(r['gain']<0 for r in rows)}
