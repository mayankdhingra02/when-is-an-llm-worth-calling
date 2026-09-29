"""Ensure a bound cannot assume all vocabulary tokens are single digits."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from audit_output_capacity_v127 import capacity_bound
DS=[[0,1]]*52+[[0,1,2]]*7

def test_single_digit_vocab_proves_cap_failure_but_special_tokens_do_not_help():
 b=capacity_bound(['0','1','2','[','"','Ġ','<|special_0000000|>'],DS)
 assert b['conservative_token_lower_bound']==520 and b['provably_exceeds_cap']

def test_multidigit_compatible_token_removes_proof():
 b=capacity_bound(['0','1','2','Ġ01'],DS)
 assert b['max_binary_digits_in_any_charset_compatible_vocabulary_token']==2
 assert b['conservative_token_lower_bound']==260 and not b['provably_exceeds_cap']
