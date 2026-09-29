"""Decode licensed photographs once; no configuration performance observations."""
import ast,hashlib
from PIL import Image
from collect_smollm_v47 import ROOT,read,write,sha,now

def main():
 a=ROOT/'artifacts/study_v133';d=ROOT/'data/native_v133';d.mkdir(exist_ok=False);src=ROOT/'artifacts/sources/v133';assert read(a/'build.json')['status']=='complete'
 tree=ast.parse((src/'skimage_registry.py').read_text());registry=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='registry' for t in n.targets));rows=[]
 for name in ['astronaut.png','coffee.png','rocket.jpg']:
  f=src/name;assert sha(f)==registry['data/'+name];im=Image.open(f);im.load();assert im.mode=='RGB';raw=im.tobytes();ppm=d/(f.stem+'.ppm');im.save(ppm)
  rows.append({'name':f.stem,'source':str(f.relative_to(ROOT)),'source_sha256':sha(f),'ppm':str(ppm.relative_to(ROOT)),'ppm_sha256':sha(ppm),'width':im.width,'height':im.height,'mode':im.mode,'pixel_bytes':len(raw),'pixel_sha256':hashlib.sha256(raw).hexdigest()})
 # Both legal lossless scan layouts, same predictor across all RGB channels.
 for p in range(1,8):
  for layout in [0,1]:
   parts=['0 1 2'] if layout==0 else ['0','1','2'];(d/f'scans_{p}_{layout}.txt').write_text('\n'.join(f'{part}: {p} 0 0 0;' for part in parts)+'\n')
 write(a/'workloads.json',{'at':now(),'workloads':rows,'preparation_decoder':'Pillow '+Image.__version__,'criterion':'Exact RGB pixel bytes and dimensions after external djpeg; no resize/crop/color conversion; rocket source already JPEG, target is its decoded pixels','configuration_executions':0})
if __name__=='__main__':main()
