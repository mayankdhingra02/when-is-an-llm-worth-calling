"""Synthetic regression for legacy held-out aliases; no measured outcomes."""
import pytest
from escalation.admission_v13_1 import exposed_groups


def test_legacy_heldout_smoke_is_exposed_and_unknown_split_fails_closed():
    assert exposed_groups({'datasets': [{'system_group': 'codec', 'split': 'heldout_smoke'}]}) == {'codec'}
    with pytest.raises(ValueError, match='Unknown historical split'):
        exposed_groups({'datasets': [{'system_group': 'codec', 'split': 'novel_spelling'}]})
