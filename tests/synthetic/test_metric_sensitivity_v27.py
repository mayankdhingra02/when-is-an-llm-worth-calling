import pytest
from escalation.metric_sensitivity_v27 import relative_gain, summarize


def case(name, group, gains, seed=11):
    return {'dataset': name, 'system_group': group, 'seed': seed,
            'relative_gains': gains, 'mean_normalized_gain': 0.1}


def test_relative_gain_hand_arithmetic_and_unit_invariance():
    assert relative_gain(100, 80) == pytest.approx(.2)
    assert relative_gain(10, 12) == pytest.approx(-.2)
    assert relative_gain(1000, 800) == relative_gain(100, 80)
    assert relative_gain(200, 180) != relative_gain(100, 80)


@pytest.mark.parametrize('a,b', [(0, 1), (1, 0), (-1, 1), (1, float('nan')), (float('inf'), 1)])
def test_invalid_target_ratios_fail(a, b):
    with pytest.raises(ValueError):
        relative_gain(a, b)


def test_family_weights_not_seed_counts_and_no_ratio_of_means():
    out = summarize([case('a', 'a', [.1]*3), case('b', 'b', [.3]*3), case('b', 'b', [.3]*3, 23)])
    assert out['equal_family_mean_relative_gain'] == pytest.approx(.2)
    assert out['case_median_relative_gain'] == pytest.approx(.3)
    assert out['leave_one_family_out'][0]['mean_relative_gain'] == pytest.approx(.3)


def test_all_any_margins_include_harm_and_preserve_denominator():
    out = summarize([case('a', 'a', [.1, -.2, 0]), case('b', 'b', [.02]*3)])
    zero, one, five, ten = out['margins']
    assert zero['help_any_presentation'] == 2 and zero['help_all_presentations'] == 1
    assert zero['harm_any_presentation'] == 1 and zero['harm_all_presentations'] == 0
    assert five['help_any_presentation'] == 1 and ten['help_any_presentation'] == 0
    assert all(r['cases'] == 2 for r in out['margins'])


def test_duplicates_or_incomplete_presentations_fail():
    c = case('a', 'a', [0]*3)
    with pytest.raises(ValueError): summarize([c, c])
    with pytest.raises(ValueError): summarize([case('a', 'a', [0]*2)])
