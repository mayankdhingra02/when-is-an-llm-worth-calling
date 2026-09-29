"""Descriptive relative-target sensitivity; no optimizer or provider access."""
import math
from statistics import mean, median

MARGINS = (0.0, 0.01, 0.05, 0.10)
TOLERANCE = 1e-12


def relative_gain(baseline, candidate):
    if not all(math.isfinite(x) and x > 0 for x in (baseline, candidate)):
        raise ValueError('Relative objective comparison requires positive finite targets')
    return (baseline - candidate) / baseline


def summarize(cases):
    if not cases or len({(c['dataset'], c['seed']) for c in cases}) != len(cases):
        raise ValueError('Missing or duplicate cases')
    groups = sorted({c['system_group'] for c in cases})
    rows = []
    for c in cases:
        gains = c['relative_gains']
        if len(gains) != 3 or not all(math.isfinite(x) for x in gains):
            raise ValueError('Exactly three finite presentation gains required')
        rows.append({**c, 'mean_relative_gain': mean(gains),
                     'minimum_relative_gain': min(gains), 'maximum_relative_gain': max(gains)})
    families = [{'system_group': g, 'cases': sum(c['system_group'] == g for c in rows),
                 'mean_relative_gain': mean(c['mean_relative_gain'] for c in rows if c['system_group'] == g),
                 'mean_normalized_gain': mean(c['mean_normalized_gain'] for c in rows if c['system_group'] == g)}
                for g in groups]
    margins = [{'margin_fraction': m, 'cases': len(rows),
                'help_any_presentation': sum(c['maximum_relative_gain'] > m + TOLERANCE for c in rows),
                'help_all_presentations': sum(c['minimum_relative_gain'] > m + TOLERANCE for c in rows),
                'harm_any_presentation': sum(c['minimum_relative_gain'] < -m - TOLERANCE for c in rows),
                'harm_all_presentations': sum(c['maximum_relative_gain'] < -m - TOLERANCE for c in rows)} for m in MARGINS]
    return {'cases': rows, 'families': families, 'margins': margins,
            'equal_family_mean_relative_gain': mean(g['mean_relative_gain'] for g in families),
            'equal_family_mean_normalized_gain': mean(g['mean_normalized_gain'] for g in families),
            'case_median_relative_gain': median(c['mean_relative_gain'] for c in rows),
            'leave_one_family_out': [{'excluded_family': g,
              'mean_relative_gain': mean(f['mean_relative_gain'] for f in families if f['system_group'] != g),
              'mean_normalized_gain': mean(f['mean_normalized_gain'] for f in families if f['system_group'] != g)}
              for g in groups] if len(groups) > 1 else []}
