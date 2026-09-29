"""Retrospective headroom mathematics; no selection or provider imports."""
import math


def bounds(scores, prefix_ids, shortlist_ids):
    values=[float(x) for x in scores]
    if not values or not all(math.isfinite(x) for x in values):raise ValueError('finite loss table required')
    if not prefix_ids or not shortlist_ids:raise ValueError('nonempty prefix and shortlist required')
    if set(prefix_ids)&set(shortlist_ids):raise ValueError('shortlist must be unacquired')
    if any(type(i) is not int or not 0<=i<len(values) for i in prefix_ids+shortlist_ids):raise ValueError('invalid row id')
    return {'shortlist':min(values[i] for i in prefix_ids+shortlist_ids),'full_table':min(values)}


def material(headroom, margin=.02):
    return headroom>margin


def relative_improvement(baseline, ideal, direction):
    if not math.isfinite(baseline) or not math.isfinite(ideal):raise ValueError('nonfinite target')
    if direction not in ('-','+'):raise ValueError('unknown direction')
    if baseline<=0:return None
    return (baseline-ideal)/baseline if direction=='-' else (ideal-baseline)/baseline
