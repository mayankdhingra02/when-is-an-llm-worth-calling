"""Synthetic checks for the V171 post-hoc audit; fixtures never enter research aggregates."""
import math, sys
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT/'scripts'))
from audit_v171 import relative_gain, log_gain, equal_group_mean, learnability, upper_bound, useful, robust, arm_summary

def test_relative_gain_respects_direction():
    assert relative_gain(10., 9., 'minimize') == pytest.approx(.1)
    assert relative_gain(10., 11., 'maximize') == pytest.approx(.1)
    assert relative_gain(10., 11., 'minimize') == pytest.approx(-.1)
    with pytest.raises(ValueError): relative_gain(10., 9., 'lower')
    with pytest.raises(ValueError): relative_gain(0., 1., 'minimize')

def test_log_gain_is_symmetric():
    assert log_gain(10., 5., 'minimize') == pytest.approx(-log_gain(5., 10., 'minimize'))
    assert log_gain(10., 20., 'maximize') == pytest.approx(math.log(2))

def test_equal_group_mean_weights_groups_not_cases():
    assert equal_group_mean([1., 1., 1., 0.], ['a', 'a', 'a', 'b']) == pytest.approx(.5)

def test_learnability_detects_single_group_positives():
    cases = [{'g': g, 'y': y} for g, y in [('a', 1), ('a', 1), ('b', 0), ('c', 0)]]
    out = learnability(cases, lambda c: c['y'] == 1, 'g')
    assert out['positives'] == 2 and out['groups_with_positives'] == 1 and out['informative_folds'] == 0
    held_a, = [f for f in out['folds'] if f['held_group'] == 'a']
    assert held_a['test_positives'] == 2 and held_a['training_positives'] == 0

def test_learnability_counts_informative_folds():
    cases = [{'g': g, 'y': y} for g, y in [('a', 1), ('b', 1), ('c', 0)]]
    assert learnability(cases, lambda c: c['y'] == 1, 'g')['informative_folds'] == 2

def test_upper_bound_matches_zero_success_formula_and_shrinks():
    assert upper_bound(0, 7) == pytest.approx(1-.05**(1/7))
    assert upper_bound(0, 20) < upper_bound(0, 7) and upper_bound(3, 3) == 1.
    with pytest.raises(ValueError): upper_bound(4, 3)

def cell(median, row, **flags):
    return {'median': median, 'row_id': row, 'quality_valid': True, 'stable': True, 'above_floor': True, **flags}

def test_native_useful_requires_distinct_setting_and_robust_requires_flags():
    same = {'direction': 'minimize', 'raw': {'sequential_3nn': cell(1., 5), 'llm': cell(.8, 5)}}
    assert not useful(same, 'llm') and not robust(same, 'llm')
    diff = {'direction': 'minimize', 'raw': {'sequential_3nn': cell(1., 5), 'llm': cell(.8, 6)}}
    assert useful(diff, 'llm') and robust(diff, 'llm')
    noisy = {'direction': 'minimize', 'raw': {'sequential_3nn': cell(1., 5), 'llm': cell(.8, 6, stable=False)}}
    assert useful(noisy, 'llm') and not robust(noisy, 'llm')
    short = {'direction': 'minimize', 'raw': {'sequential_3nn': cell(1., 5, above_floor=False), 'llm': cell(.8, 6)}}
    assert not robust(short, 'llm')

def test_arm_summary_skips_missing_arms_and_reports_headroom():
    cases = [{'g': 'a', 'direction': 'minimize', 'raw': {'sequential_3nn': 10., 'x': 9.}},
             {'g': 'b', 'direction': 'minimize', 'raw': {'sequential_3nn': 10., 'x': 11.}},
             {'g': 'b', 'direction': 'minimize', 'raw': {'sequential_3nn': 10., 'x': None}}]
    s = arm_summary(cases, 'x', 'g')
    assert s['cases'] == 2 and s['useful_over_sequential'] == 1 and s['groups_with_useful'] == ['a']
    assert s['equal_group_hindsight_headroom'] == pytest.approx(.05)
    assert arm_summary([{'g': 'a', 'raw': {'x': None}}], 'x', 'g') is None
