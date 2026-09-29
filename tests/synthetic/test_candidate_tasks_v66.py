import hashlib
import pytest
from escalation.candidate_tasks_v66 import expected_query,read_pgm,sort_line,sorted_digest,grids
from escalation.legal_proposals_v66 import LegalProposals

def test_small_query_ground_truth_by_hand():
    assert expected_query(3)==[[0,0,1],[1,2,1],[2,6,1]]

def test_exact_sort_contract():
    assert sorted_digest(3)==hashlib.sha256(b'00000000\n00000001\n00000002\n').hexdigest()

def test_pgm_comments_and_binary_whitespace_are_distinct():
    assert read_pgm(b'P5\n# comment\n3 1\n255\n\n #')==(3,1,b'\n #')
    assert read_pgm(b'P5\r\n1 1\r\n255\r\n#')==(1,1,b'#')

@pytest.mark.parametrize('raw',[b'P5\n1 1\n255\n',b'P5\n0 1\n255\na',b'P2\n1 1\n255\na',b'P5\n1 1\n65535\nab',b'P5\n# no newline'])
def test_pgm_corruption_rejected(raw):
    with pytest.raises(ValueError):read_pgm(raw)

def test_each_predeclared_domain_has_48_distinct_admissible_vectors():
    for rows in grids().values():
        assert len(rows)==len(set(rows))==48
        assert len(LegalProposals(rows,list(range(10))).eligible_ids())==38
