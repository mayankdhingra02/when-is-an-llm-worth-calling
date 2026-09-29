"""Owner-only, capped source acquisition; no configuration execution."""
import hashlib,tarfile,time,urllib.request
from pathlib import Path
from collect_smollm_v47 import ROOT,write,sha,now

def main():
 d=ROOT/'artifacts/sources/v131';d.mkdir(parents=True,exist_ok=False);a=ROOT/'artifacts/study_v131';start=time.monotonic();receipt={'at':now(),'bytes_received':0,'files':[],'complete':False}
 urls=['https://www.fftw.org/download.html','https://www.fftw.org/fftw-3.3.11.tar.gz.md5sum','https://www.fftw.org/fftw-3.3.11.tar.gz','https://www.wavpack.com/downloads.html','https://www.wavpack.com/wavpack-5.9.0.tar.xz']
 opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
 try:
  for url in urls:
   name=('fftw_download.html' if 'fftw.org/download.html' in url else 'wavpack_download.html' if 'downloads.html' in url else url.rsplit('/',1)[1]);item={'url':url,'path':str((d/name).relative_to(ROOT)),'bytes':0};receipt['files'].append(item)
   with opener.open(url,timeout=30) as response,(d/name).open('xb') as f:
    assert response.url.startswith(('https://www.fftw.org/','https://www.wavpack.com/'));item['final_url']=response.url
    while True:
     if time.monotonic()-start>180:raise TimeoutError('Download stage cap')
     b=response.read(min(1048576,20000000-receipt['bytes_received']+1))
     if not b:break
     f.write(b);receipt['bytes_received']+=len(b);item['bytes']+=len(b)
     if receipt['bytes_received']>20000000:raise ValueError('Download byte cap')
   item['sha256']=sha(d/name);write(a/'downloads.json',receipt)
  checksum=(d/'fftw-3.3.11.tar.gz.md5sum').read_text().split()[0];assert hashlib.md5((d/'fftw-3.3.11.tar.gz').read_bytes()).hexdigest()==checksum
  receipt['fftw_owner_md5']=checksum
  for name in ['fftw-3.3.11.tar.gz','wavpack-5.9.0.tar.xz']:
   with tarfile.open(d/name) as t:
    ms=t.getmembers();assert sum(m.size for m in ms)<80000000
    for m in ms:
     p=Path(m.name);assert not p.is_absolute() and '..' not in p.parts and (m.isfile() or m.isdir()),m.name
    t.extractall(d,filter='data')
  receipt['complete']=True
 except Exception as e:receipt['error']=repr(e);raise
 finally:receipt['seconds']=time.monotonic()-start;write(a/'downloads.json',receipt)
if __name__=='__main__':main()
