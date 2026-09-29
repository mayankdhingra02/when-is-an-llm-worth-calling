"""Synthetic rule predictions are NOT LLM output or measured research results."""
import pytest
from escalation.rule_audit_v20 import IDS,predictions,compare,nonmonotone_assignment

@pytest.mark.parametrize('display',[list(IDS),list(IDS[::-1])])
def test_monotone_orders_cannot_distinguish_prefix_from_sequence_completion(display):
    p=predictions(display);assert p['display_prefix']==p['endpoint_sequence']

def test_nonmonotone_order_distinguishes_rules_without_claiming_model_behavior():
    display=nonmonotone_assignment();p=predictions(display)
    assert len(display)==len(set(display))==20
    assert p['display_prefix']!=p['endpoint_sequence']
    assert len(set(p['display_prefix'])&set(p['endpoint_sequence']))==5

def test_out_of_range_sequence_is_undefined_not_silently_wrapped():
    display=list(IDS);display[0],display[12]=display[12],display[0]
    # First C then1 => descending, remains valid; move D second for ascending overflow.
    display[1],display[13]=display[13],display[1]
    assert predictions(display)['endpoint_sequence'] is None

def test_invalid_evidence_rejected():
    with pytest.raises(ValueError):compare(list(IDS),['0']*10)
    with pytest.raises(ValueError):predictions(['0']*20)
