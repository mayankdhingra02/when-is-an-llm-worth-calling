"""Synthetic interface tests; no compression measurement or model response."""
import sys,hashlib
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import xz_v140 as x
def test_domain_and_fixed_contract():
 assert len(x.XS)==216 and len(set(x.XS))==216
 for i,row in enumerate(x.XS):
  assert row[0]+row[1]<=4
  args=x.arguments(i);assert '--threads=1' in args and '--check=crc64' in args and '--no-adjust' in args and 'dict=8MiB' in args[-1]
 with pytest.raises(ValueError):x.arguments(-1)
def test_lossless_check_rejects_changed_bytes(tmp_path):
 p=tmp_path/'a';p.write_bytes(b'abc');w={'bytes':3,'sha256':hashlib.sha256(b'abc').hexdigest()};assert x.validated_bytes(p,w)['decoded_bytes']==3
 p.write_bytes(b'abd')
 with pytest.raises(ValueError):x.validated_bytes(p,w)
def test_context_sweep_uses_only_prefix_and_never_repeats():
 s=x.search.fresh('xz',11)
 for i in s['order'][:10]:x.search.observe('xz',s,i,100+i)
 a,_=x.selection(s,'context_sweep',11);assert len(a)==len(set(a))==10 and not set(a)&set(s['ids'])
 before=repr(s);x.selection(s,'context_sweep',11);assert repr(s)==before
def test_fallback_uses_separate_selection_identity(monkeypatch):
 s=x.search.fresh('xz',11)
 for i in s['order'][:10]:x.search.observe('xz',s,i,100+i)
 keys=[]
 def step(oracle,state,prefix,key,mode,k,row):keys.append(key);x.search.observe('xz',state,row,200+row)
 monkeypatch.setattr(x,'acquire_step',step);r=x.arm(None,s,'sequential_3nn',11,arm_name='llm')
 assert len(r['state']['ids'])==20 and all('_llm_' in k for k in keys) and len(s['ids'])==10
