"""Independent reconstruction primitives checked only on synthetic examples."""
import importlib.util
from pathlib import Path
import pytest
SPEC=importlib.util.spec_from_file_location('portable_v26',Path(__file__).resolve().parents[2]/'scripts/verify_reproduction_v26.py')
portable=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(portable)

def test_independent_state_minimization_and_maximization():
    for direction,expected in [('-', [3,2]),('+',[0,1])]:
        state={'order':list(range(8)),'ids':[],'labels':[],'best':[],'rest':[]}
        for i,v in enumerate([4,3,2,1]):portable.observe(state,i,v,direction)
        assert state['best']==expected
        with pytest.raises(ValueError):portable.observe(state,0,999,direction)

def test_independent_ranking_does_not_read_targets():
    state={'order':[0,1,2,3,4,5],'ids':[0,1,2,3],'labels':[[1],[2],[9],[10]],'best':[0,1],'rest':[2,3]}
    features=[(0,),(0,),(1,),(1,),(0,),(1,)]
    assert portable.ranked(features,state)==[4,5]
    state['labels']=[[999],[998],[-999],[-998]]
    assert portable.ranked(features,state)==[4,5]

def test_byte_level_decode_excludes_special_tokens():
    tokenizer={'decoder':{'type':'ByteLevel'},'model':{'vocab':{'A':7,'Ċ':8}},'added_tokens':[{'id':9,'special':True}]}
    assert portable.decode_tokens([7,8,7,9],tokenizer)=='A\nA'

def test_decoder_rejects_unpinned_kind():
    with pytest.raises(ValueError):portable.decode_tokens([],{'decoder':{'type':'Other'}})
