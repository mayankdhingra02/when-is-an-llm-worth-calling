import json
import pytest
from escalation.kanzi_policy_v78 import messages,vectors,validate_acquisition
from escalation.kanzi_v75 import grid
from escalation.legal_proposals_v66 import LegalProposals

def test_prompt_allowlist_and_meaningful_vector_domain():
    g=grid();assert len(set(map(tuple,vectors(g))))==448
    clean=[{'config_id':0,'compressed_bytes':123}]
    dirty=[dict(clean[0],hidden_label='forbidden',other_arm_outcome='forbidden',physical_receipt='forbidden')]
    assert messages(g,clean)==messages(g,dirty)
    text=json.dumps(messages(g,clean));assert 'forbidden' not in text and 'HUFFMAN' in text and 'BWT' in text

def test_legal_session_excludes_acquired_and_bounds_calls():
    g=grid();s=LegalProposals(vectors(g),list(range(10)),count=7)
    p=s.begin_request();assert not set(p['eligible_ids'])&set(range(10))
    cid=p['eligible_ids'][0];decision=s.finish_request(json.dumps(vectors(g)[cid],separators=(',',':')));assert decision['selected_id']==cid
    p=s.begin_request();assert cid not in p['eligible_ids']

@pytest.mark.parametrize('count',[150,151])
def test_paired_physical_cap(count):
    with pytest.raises(ValueError):validate_acquisition(0,[],'search',count)
