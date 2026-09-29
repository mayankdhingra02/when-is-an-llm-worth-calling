"""Capped owner source/data retrieval, no benchmark executions."""
import time,urllib.request,tarfile
from pathlib import Path
from collect_smollm_v47 import ROOT,write,sha,now

def main():
 d=ROOT/'artifacts/sources/v133';d.mkdir(parents=True,exist_ok=False);a=ROOT/'artifacts/study_v133';t=time.monotonic();r={'at':now(),'bytes_received':0,'files':[],'cap_bytes':20000000,'complete':False}
 base='https://raw.githubusercontent.com/scikit-image/scikit-image/v0.20.0/skimage/data/'
 urls=[('libjpeg-turbo-3.1.2.tar.gz','https://codeload.github.com/libjpeg-turbo/libjpeg-turbo/tar.gz/refs/tags/3.1.2'),('skimage_fetchers.py',base+'_fetchers.py'),('skimage_registry.py',base+'_registry.py')]+[(n,base+n) for n in ['astronaut.png','coffee.png','rocket.jpg']]
 op=urllib.request.build_opener(urllib.request.ProxyHandler({}))
 try:
  for n,u in urls:
   p=d/n;f={'url':u,'path':str(p.relative_to(ROOT)),'bytes':0};r['files'].append(f)
   with op.open(u,timeout=30) as response,p.open('xb') as dest:
    assert response.url.startswith(('https://codeload.github.com/','https://raw.githubusercontent.com/'));f['final_url']=response.url
    while True:
     if time.monotonic()-t>180:raise TimeoutError('Download cap')
     b=response.read(min(1048576,r['cap_bytes']-r['bytes_received']+1))
     if not b:break
     dest.write(b);r['bytes_received']+=len(b);f['bytes']+=len(b)
     if r['bytes_received']>r['cap_bytes']:raise ValueError('Download bytes cap')
   f['sha256']=sha(p);write(a/'downloads.json',r)
  with tarfile.open(d/'libjpeg-turbo-3.1.2.tar.gz') as tar:
   ms=tar.getmembers();assert sum(m.size for m in ms)<100000000
   for m in ms:assert not Path(m.name).is_absolute() and '..' not in Path(m.name).parts and (m.isfile() or m.isdir()),m.name
   tar.extractall(d,filter='data')
  r['complete']=True
 except Exception as e:r['error']=repr(e);raise
 finally:r['seconds']=time.monotonic()-t;write(a/'downloads.json',r)
if __name__=='__main__':main()
