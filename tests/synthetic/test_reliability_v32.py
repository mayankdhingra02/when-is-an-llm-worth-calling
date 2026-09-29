import pytest
from escalation.reliability_v32 import schedule, compare

def test_shuffled_schedule_reuses_no_measurements_across_rounds():
    settings=[{'config_id':str(i)} for i in range(7)]
    rows=schedule(settings)
    assert rows==schedule(settings[::-1]) and len(rows)==140
    assert [r['trial_id'] for r in rows]==list(range(140))
    for repetition in range(20):
        assert {r['setting']['config_id'] for r in rows if r['repetition']==repetition}=={str(i) for i in range(7)}
    assert settings==[{'config_id':str(i)} for i in range(7)]
    with pytest.raises(ValueError):schedule(settings+settings)

def test_timing_summary_identity_and_known_gain():
    assert compare([10]*20,[10]*20)['rounds_equal']==20
    result=compare([9]*20,[10]*20)
    assert result['relative_gain_of_medians']==pytest.approx(.1)
    assert result['paired_p10']==result['paired_p90']==.1 and result['rounds_faster']==20
    with pytest.raises(ValueError):compare([0]*20,[10]*20)

def test_median_of_pairs_not_conflated_with_ratio_of_medians():
    cheap=[1]*10+[10]*10; reference=[2]*10+[10]*10
    result=compare(cheap,reference)
    assert result['median_paired_relative_gain']==.25
    assert result['relative_gain_of_medians']==pytest.approx(1/12)
