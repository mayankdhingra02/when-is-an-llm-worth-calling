from types import SimpleNamespace
import pytest
from escalation.core import State
from escalation.transfer_v30 import validate_admission, branch, MODES


def specs():
    return [{'system_group': g, 'split': 'prospective_transfer', 'direction': '-', 'rows': 40,
             'evidence': {'synthetic': 'fixture'}, 'sha256': 'synthetic'} for g in ('opus', 'z3')]


def test_admission_rejects_exposure_and_nonmatching_direction():
    validate_admission(specs(), {'brotli', 'libvpx'})
    with pytest.raises(ValueError): validate_admission(specs(), {'opus'})
    altered = specs(); altered[0]['direction'] = '+'
    with pytest.raises(ValueError): validate_admission(altered, set())
    with pytest.raises(ValueError): validate_admission(specs()[:1], set())


@pytest.mark.parametrize('mode', MODES)
def test_all_fixed_modes_preserve_prefix_and_charge_ten(mode):
    c = SimpleNamespace(x=[(float(i%2), float(i//2)) for i in range(40)], names=('a','b'), directions=('-',))
    prefix = State(list(range(40)))
    for i in range(10): prefix.observe(i, [float(40-i)], c.directions)
    saved = prefix.record(); charged = []
    def acquire(i): charged.append(i); return [float(40-i)]
    final, trace = branch(c, prefix, list(range(10,30)), mode, acquire)
    assert prefix.record() == saved and len(charged) == len(set(charged)) == 10
    assert len(final.ids) == 20 and final.ids[:10] == prefix.ids
    if mode != 'full_classical': assert set(charged) <= set(range(10,30))
