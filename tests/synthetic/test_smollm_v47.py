import importlib.util
from pathlib import Path
import pytest

PATH=Path(__file__).resolve().parents[2]/'scripts/collect_smollm_v47.py'
spec=importlib.util.spec_from_file_location('v47',PATH)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

def test_used_choices_are_excluded_without_inventing_new_choices():
    text=module.grammar(['0','A','J'])
    assert '"0"' not in text and '"A"' not in text and '"J"' not in text
    assert text.count('|')==16
    assert '"1"' in text and '"I"' in text

@pytest.mark.parametrize('used',[['0','0'],['Z'],['00']])
def test_invalid_decoder_state_fails_closed(used):
    with pytest.raises(ValueError):module.grammar(used)
