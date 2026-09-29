"""Synthetic correctness/budget fixtures; excluded from measured aggregates."""
import copy,hashlib,sys
from pathlib import Path
import pytest
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import jpeg_v133 as j

def prefix():
 s=j.search.fresh(j.TASK,11)
 for i in s['order'][:10]:j.search.observe(j.TASK,s,i,1000+i)
 return s

def test_domain_and_search_namespace():
 import native_v131
 assert j.TASK not in native_v131.TASKS
 assert len(j.XS)==len(set(j.XS))==70
 assert {x[0] for x in j.XS}==set(range(1,8))

@pytest.mark.parametrize('mode',j.MODES+['llm'])
def test_isolated_budget_and_portfolio(mode):
 p=prefix();saved=copy.deepcopy(p);calls=[]
 class Fake:
  def acquire(self,key,row):calls.append(row);return 2000+row
 proposals=[j.XS[p['ids'][0]]]*10 if mode=='llm' else None
 a=j.arm(Fake(),p,mode,11,proposals)
 assert p==saved and len(calls)==len(set(calls))==10
 assert len(a['state']['ids'])==20 and not set(calls)&set(p['ids'])
 if mode=='predictor_sweep':
  target=[j.XS.index((v,0,l)) for l in [0,1] for v in range(1,8) if j.XS.index((v,0,l)) not in p['ids']]
  assert calls[:min(10,len(target))]==target[:10]
 with pytest.raises(ValueError):j.search.observe(j.TASK,a['state'],next(x for x in p['order'] if x not in a['state']['ids']),1)

def test_pixel_validator_rejects_one_byte_change_and_shape(tmp_path):
 im=Image.new('RGB',(3,2),(17,22,39));p=tmp_path/'fixture.ppm';im.save(p);w={'width':3,'height':2,'pixel_bytes':18,'pixel_sha256':hashlib.sha256(im.tobytes()).hexdigest()};j.validated_pixels(p,w)
 im.putpixel((0,0),(18,22,39));im.save(p)
 with pytest.raises(ValueError):j.validated_pixels(p,w)
 Image.new('RGB',(2,3),(17,22,39)).save(p)
 with pytest.raises(ValueError):j.validated_pixels(p,w)

def test_lossless_scan_scripts():
 for p in range(1,8):
  for layout in [0,1]:
   lines=(j.ROOT/f'data/native_v133/scans_{p}_{layout}.txt').read_text().strip().splitlines()
   assert len(lines)==(1 if layout==0 else 3)
   assert all(x.split(':')[1].strip()==f'{p} 0 0 0;' for x in lines)
