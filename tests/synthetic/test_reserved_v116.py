"""Synthetic only: reserved-family feature isolation and retrieval boundaries."""
import sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from audit_reserved_v116 import partition
from fetch_admission_v116 import check_url


def test_targets_are_never_parsed_or_used(tmp_path):
    a=tmp_path/'a.csv';b=tmp_path/'b.csv'
    a.write_text('fixed,tune,loss-\n1,2,POISON\n1,3,not-a-number\n2,3,hidden\n')
    b.write_text('fixed,tune,loss-\n1,2,-99999\n1,3,99999\n2,3,0\n')
    x=partition(a,['fixed','tune'],['loss-'],['fixed'])
    assert x==partition(b,['fixed','tune'],['loss-'],['fixed'])
    assert x['largest_contract_configurations']==2 and x['utility_contracts']==2
    assert not x['certifies_utility_equivalence']


def test_no_target_column_in_features(tmp_path):
    p=tmp_path/'a.csv';p.write_text('f,loss-\n1,1\n')
    with pytest.raises(ValueError,match='objective'):partition(p,['loss-'],['loss-'],[])


def test_nonfinite_features_rejected(tmp_path):
    p=tmp_path/'a.csv';p.write_text('f,loss-\nNaN,POISON\n')
    with pytest.raises(ValueError,match='Nonfinite'):partition(p,['f'],['loss-'],[])


def test_duplicate_rows_do_not_inflate_domain(tmp_path):
    p=tmp_path/'a.csv';p.write_text('f,loss-\n1,POISON\n1,POISON2\n')
    assert partition(p,['f'],['loss-'],[])['unique_configurations']==1


@pytest.mark.parametrize('url',[
 'http://raw.githubusercontent.com/dice-project/DICE-Configuration-BO4CO/abc/README.md',
 'https://example.org/dice-project/DICE-Configuration-BO4CO/abc/README.md',
 'https://raw.githubusercontent.com/unknown/project/abc/README.md',
 'https://raw.githubusercontent.com/dice-project/DICE-Configuration-BO4CO/abc/data.csv',
 'https://raw.githubusercontent.com/dice-project/DICE-Configuration-BO4CO/abc/data.mat',
 'https://user:pass@raw.githubusercontent.com/dice-project/DICE-Configuration-BO4CO/abc/README.md'])
def test_fetch_rejects_unselected_or_outcome_urls(url):
    with pytest.raises(ValueError):check_url(url)
