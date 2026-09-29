import importlib.util,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/f'{name}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
parser=load('decoder_v49_common');analysis=load('analyze_decoder_v49')
def test_native_valid_and_whitespace():
    r=parser.parse_native('\n'+'\n'.join(' '+str(i)+' ' for i in range(10))+'\n')
    assert r['valid'] and r['selected_ids']==list('0123456789')
def test_rejects_duplicates_explanations_and_unknowns_without_repair():
    for text in ['\n'.join('0123456788'),'Here are the IDs:\n'+'\n'.join('0123456789'),'\n'.join('012345678Z'),'0,1,2,3,4,5,6,7,8,9']:
        r=parser.parse_native(text);assert not r['valid'] and not r['selected_ids']
def test_truncated_and_short_outputs_fail():
    assert not parser.parse_native('\n'.join('0123456789'),True)['valid']
    assert not parser.parse_native('\n'.join('0123'))['valid']
def test_missing_pair_retains_denominator_and_bounds():
    s=analysis.summarize_pairs([{'system_group':'a','overlap':1},{'system_group':'a','overlap':None}])
    assert s['intended']==2 and s['valid']==1
    assert s['family_mean_overlap_lower']==.5 and s['family_mean_overlap_upper']==1
    assert s['set_changes']==0

def test_overlap_uses_sets_not_sequence():
    assert analysis.overlap(range(10),reversed(range(10)))==1
    assert analysis.overlap(range(10),range(10,20))==0
