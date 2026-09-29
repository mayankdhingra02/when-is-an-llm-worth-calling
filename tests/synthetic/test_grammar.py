import json
from types import SimpleNamespace
import pytest
from escalation.grammar import BinaryJSONGrammar
from escalation.provider import LocalProvider,WorkerUnavailable
from escalation.config import load_config

class CharacterTokenizer:
    eos_token_id=999
    def encode(self,s,**kwargs):return list(map(ord,s))
    def decode(self,ids):return ''.join(map(chr,[i for i in ids if i!=999]))

def test_constraints_leave_every_binary_coordinate_to_model():
    t=CharacterTokenizer();g=BinaryJSONGrammar(t,[[0,1]]*39)
    assert len(g.choice_positions)==78
    for bit in [0,1]:
        ids=[tokens[bit] if len(tokens)==2 else tokens[0] for tokens in g.schedule]
        assert json.loads(t.decode(ids))=={'candidates':[[bit]*39]*2}

def test_fixed_domains_and_boundaries():
    t=CharacterTokenizer();g=BinaryJSONGrammar(t,[[1],[0,1]])
    assert g.allowed(g.choice_positions[0])==[ord('1')]
    with pytest.raises(ValueError):g.allowed(len(g.schedule))
    with pytest.raises(ValueError):BinaryJSONGrammar(t,[[2]])

def test_dead_worker_does_not_consume_request_cap(tmp_path):
    provider=LocalProvider(load_config(),SimpleNamespace(request=lambda:pytest.fail('must not reserve')),tmp_path/'requests.jsonl')
    with pytest.raises(WorkerUnavailable):provider.request([], {})

def test_five_binary_lines_preserve_every_model_choice():
    from escalation.grammar import BinaryLinesGrammar
    from escalation.followup_v3 import parse_bits,compact_messages,synthetic_fixture
    t=CharacterTokenizer();g=BinaryLinesGrammar(t,[[0,1]]*39);c,s=synthetic_fixture(39)
    raw=t.decode([tokens[-1] for tokens in g.schedule])
    assert parse_bits(raw,c)==[[1]*39]*5
    assert len(g.choice_positions)==195
    assert 'Choose five' in compact_messages(c,s,[])[1]['content']
    with pytest.raises(ValueError):parse_bits('0'*39,c)
