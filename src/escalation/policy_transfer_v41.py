"""Frozen-controller transfer and family-level analysis; no fitting or inference.

Predecision masks accept only case identity and the nine saved prefix features.
Outcome-dependent hindsight masks live in a separate evaluator and are labelled.
"""
import itertools
import math
import random
import numpy as np

PENALTIES = (0., .01, .05)


def predecision_masks(rows, seal):
    if not rows: raise ValueError('Nonempty predecision cohort required')
    keys = seal['benefit']['features']
    identities = [(r['dataset'], r['seed']) for r in rows]
    if len(set(identities)) != len(rows): raise ValueError('Duplicate case')
    for row in rows:
        if set(row) != {'dataset', 'seed', 'system_group', 'features'} or set(row['features']) != set(keys):
            raise ValueError('Only explicit predecision features and identity allowed')
    r = seal['benefit']
    x = np.asarray([[row['features'][k] for k in keys] for row in rows], dtype=float)
    mean, scale, coefficient = (np.asarray(r[k], dtype=float) for k in ('mean', 'scale', 'coefficient'))
    if any(a.shape != (len(keys),) for a in (mean, scale, coefficient)) or np.any(scale <= 0):
        raise ValueError('Malformed sealed coefficients')
    if not all(np.isfinite(a).all() for a in (x, mean, scale, coefficient)) or not math.isfinite(r['intercept']):
        raise ValueError('Nonfinite feature/model value')
    scores = ((x-mean)/scale) @ coefficient + r['intercept']
    threshold = math.inf if r['threshold'] is None else r['threshold']
    uth = math.inf if seal['uncertainty']['threshold'] is None else seal['uncertainty']['threshold']
    masks = {'never': [False]*len(rows), 'always': [True]*len(rows),
             'benefit': (scores > threshold).tolist(),
             'uncertainty': [row['features']['uncertainty'] > uth for row in rows]}
    # Match realized counts without observing outcomes. These require a cohort;
    # they are diagnostics, not claims of an online deployment policy.
    for index, name in enumerate(('benefit', 'uncertainty')):
        order = sorted(range(len(rows)), key=lambda i: identities[i])
        selected = set(random.Random(41001+index).sample(order, sum(masks[name])))
        masks['random_matched_'+name+'_diagnostic'] = [i in selected for i in range(len(rows))]
        rate = r['development_oof_rate'] if name == 'benefit' else seal['uncertainty']['rate']
        if not 0 <= rate <= 1: raise ValueError('Invalid development rate')
        rng = random.Random(41011+index)
        chosen = {i: rng.random() < rate for i in order}
        masks['random_development_'+name] = [chosen[i] for i in range(len(rows))]
    return masks, scores.tolist()


def family_contrast(gains, groups):
    if len(gains) != len(groups) or not gains: raise ValueError('Nonempty paired values required')
    values = np.asarray(gains, dtype=float)
    if not np.isfinite(values).all(): raise ValueError('Incomplete/nonfinite outcomes cannot be dropped')
    names = sorted(set(groups))
    means = np.asarray([np.mean([v for v,g in zip(values,groups) if g == name]) for name in names])
    if len(names) > 16: raise ValueError('Exact sign flips bounded to sixteen families')
    rng = np.random.default_rng(41000)
    samples = means[rng.integers(0,len(names),size=(10000,len(names)))].mean(axis=1)
    null = [abs(np.mean(means*np.asarray(signs))) for signs in itertools.product((-1,1),repeat=len(names))]
    return {'family_mean_gain': float(means.mean()), 'family_means': dict(zip(names,means.tolist())),
            'families': len(names), 'cases': len(values), 'bootstrap95': np.quantile(samples,[.025,.975]).tolist(),
            'exact_family_sign_flip_p': float(np.mean(np.asarray(null) >= abs(means.mean())-1e-14)),
            'wins': int(sum(values > 1e-12)), 'ties': int(sum(abs(values) <= 1e-12)), 'harms': int(sum(values < -1e-12))}


def observed_usage(records, field):
    """An unobserved token/runtime value is unknown, never silently zero."""
    values = [r.get(field) for r in records]
    if any(v is None for v in values): return None
    if any(not isinstance(v,(int,float)) or not math.isfinite(v) or v < 0 for v in values):
        raise ValueError('Invalid observed usage')
    return sum(values)


def evaluate_policies(gains, groups, masks, request_records, prefix_seconds, classical_seconds):
    n = len(gains)
    if any(len(x) != n for x in (groups,request_records,prefix_seconds,classical_seconds)) or any(len(mask) != n for mask in masks.values()):
        raise ValueError('Intended denominator mismatch')
    family_contrast(gains,groups)  # Reject missing values before selecting any mask.
    rows = []
    for penalty in PENALTIES:
        local = {**masks, 'hindsight_oracle_diagnostic': [g > penalty for g in gains]}
        for name, mask in local.items():
            if any(type(v) is not bool for v in mask): raise ValueError('Boolean decisions required')
            selected = [r for r,m in zip(request_records,mask) if m]
            net = [(gain-penalty) if call else 0. for gain,call in zip(gains,mask)]
            quality = [gain if call else 0. for gain,call in zip(gains,mask)]
            selected_seconds = observed_usage(selected,'wall_seconds')
            known = sum(prefix_seconds)+sum(t for t,m in zip(classical_seconds,mask) if not m)
            rows.append({'policy':name,'hypothetical_relative_penalty_per_call':penalty,
                'nondeployable_diagnostic':name.endswith('_diagnostic'),
                'quality':family_contrast(quality,groups),'net_utility':family_contrast(net,groups),
                'calls':sum(mask),'intended_cases':n,'retrospective_deployment_objective_accesses':20*n,
                'observed_selected_input_tokens':observed_usage(selected,'input_tokens'),
                'observed_selected_output_tokens':observed_usage(selected,'output_tokens'),
                'selected_model_failures':sum(r.get('status')!='response' for r in selected),
                'estimated_observed_components_seconds':None if selected_seconds is None else known+selected_seconds,
                'runtime_exclusions':'model startup, policy scoring, model-branch objective access and unmeasured deployment overhead; not end-to-end latency',
                'cost_scope':'retrospective selected branch; all-arm research collection is reported separately; penalty is not USD'})
    return rows
